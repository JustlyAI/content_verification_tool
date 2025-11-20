"""
FastAPI Backend for Content Verification Tool
"""

import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from pathlib import Path
import logging
import tempfile
import shutil
from termcolor import cprint

from app.models import (
    UploadResponse,
    ChunkingRequest,
    ChunkingResponse,
    ExportRequest,
    ExportResponse,
    ErrorResponse,
    ChunkingMode,
    OutputFormat,
    UploadReferencesResponse,
    VerificationRequest,
    VerificationResponse,
)
from app.processing import (
    document_processor,
    document_chunker,
    output_generator,
    document_cache,
)
from app.corpus import corpus_manager
from app.verification import gemini_verifier


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Content Verification Tool API",
    description="Backend API for document verification checklist generation",
    version="1.0.0",
)

# Add CORS middleware to allow frontend communication
# Get allowed origins from environment variable (comma-separated list)
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

# Support regex patterns for Cloud Run dynamic URLs
allowed_origin_regex = os.getenv("ALLOWED_ORIGIN_REGEX", None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if not allowed_origin_regex else ["*"],  # Use * if regex is set
    allow_origin_regex=allowed_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for processed documents
# In production, use Redis or a database
DOCUMENT_STORE: Dict[str, dict] = {}


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    cprint("=" * 80, "cyan")
    cprint("🚀 Content Verification Tool API Starting...", "green", attrs=["bold"])
    cprint("=" * 80, "cyan")
    cprint("[API] Initializing document processor...", "cyan")
    cprint("[API] Initializing chunker...", "cyan")
    cprint("[API] Initializing output generator...", "cyan")
    cprint("[API] All services initialized successfully ✓", "green")
    cprint(f"[API] CORS allowed origins: {', '.join(allowed_origins)}", "cyan")
    if allowed_origin_regex:
        cprint(f"[API] CORS origin regex: {allowed_origin_regex}", "cyan")
    cprint("=" * 80, "cyan")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Content Verification Tool API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload",
            "chunk": "/chunk",
            "export": "/export",
            "download": "/download/{document_id}",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "cache_dir": str(document_cache.cache_dir),
        "output_dir": str(output_generator.output_dir),
        "documents_in_store": len(DOCUMENT_STORE),
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and convert document using Docling

    Args:
        file: Uploaded PDF or DOCX file

    Returns:
        UploadResponse with document metadata
    """
    cprint(f"\n[API] Received upload request: {file.filename}", "cyan", attrs=["bold"])

    try:
        # Read file content
        file_content = await file.read()
        cprint(f"[API] Read {len(file_content)} bytes from {file.filename}", "cyan")

        # Process document with Docling
        result = document_processor.convert_document(
            file_content=file_content, filename=file.filename, use_cache=True
        )

        # Generate document ID (use hash of file content)
        import hashlib

        document_id = hashlib.md5(file_content).hexdigest()

        # Store document data
        DOCUMENT_STORE[document_id] = {
            "docling_document": result["docling_document"],
            "filename": result["filename"],
            "page_count": result["page_count"],
            "file_size": result["file_size"],
            "chunks_cache": {},  # Cache chunks by mode
        }

        cprint(f"[API] Document stored with ID: {document_id}", "green")

        return UploadResponse(
            document_id=document_id,
            filename=result["filename"],
            page_count=result["page_count"],
            file_size=result["file_size"],
            message=f"Document uploaded and converted successfully ({result['page_count']} pages)",
        )

    except ValueError as e:
        cprint(f"[API] Validation error: {e}", "red")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        cprint(f"[API] Error processing upload: {e}", "red")
        raise HTTPException(
            status_code=500, detail=f"Error processing document: {str(e)}"
        )


@app.post("/api/verify/upload-references", response_model=UploadReferencesResponse)
async def upload_references(
    case_context: str = Form(None), files: List[UploadFile] = File(...)
):
    """
    Upload reference documents and create File Search store

    Args:
        case_context: Context about the verification case (optional)
        files: List of reference documents (PDF/DOCX)

    Returns:
        UploadReferencesResponse with store information and metadata
    """
    cprint(
        f"\n[API] Received reference upload request: {len(files)} files",
        "cyan",
        attrs=["bold"],
    )
    if case_context:
        cprint(f"[API] Case context: {case_context[:100]}...", "cyan")
    else:
        cprint("[API] No case context provided", "cyan")

    try:
        # Generate a case ID
        import hashlib
        import time

        case_id = hashlib.md5(f"{case_context or 'default'}{time.time()}".encode()).hexdigest()[:8]

        # Create File Search store
        store_name, display_name = corpus_manager.create_store(case_id)
        cprint(f"[API] Created store: {store_name}", "green")

        # Process each file
        metadata_list = []
        temp_files = []

        for idx, file in enumerate(files):
            cprint(
                f"[API] Processing file {idx + 1}/{len(files)}: {file.filename}", "cyan"
            )

            # Save file temporarily
            file_content = await file.read()
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, suffix=Path(file.filename).suffix
            )
            temp_file.write(file_content)
            temp_file.close()
            temp_files.append(temp_file.name)

            try:
                # Use optimized upload method (single upload for both metadata and store)
                metadata, _ = corpus_manager.upload_reference_with_metadata(
                    file_path=temp_file.name,
                    filename=file.filename,
                    store_name=store_name,
                    case_context=case_context,
                )
                metadata_list.append(metadata)
                cprint(
                    f"[API] ✓ Uploaded {file.filename} to store (optimized)", "green"
                )

            except Exception as e:
                cprint(f"[API] ✗ Error processing {file.filename}: {e}", "red")
                # Continue with other files

        # Clean up temp files
        for temp_file in temp_files:
            try:
                Path(temp_file).unlink()
            except:
                pass

        cprint(
            f"[API] Reference upload complete: {len(metadata_list)} documents", "green"
        )

        return UploadReferencesResponse(
            store_id=store_name,
            store_name=display_name,
            documents_uploaded=len(metadata_list),
            metadata=metadata_list,
        )

    except ValueError as e:
        cprint(f"[API] Validation error: {e}", "red")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        cprint(f"[API] Error uploading references: {e}", "red")
        raise HTTPException(
            status_code=500, detail=f"Error uploading references: {str(e)}"
        )


@app.post("/api/verify/execute", response_model=VerificationResponse)
async def execute_verification(request: VerificationRequest):
    """
    Execute AI verification on chunked document

    Args:
        request: VerificationRequest with document_id, store_id, case_context, splitting_mode

    Returns:
        VerificationResponse with verified chunks and statistics
    """
    cprint(
        f"\n[API] Received verification request: {request.document_id}",
        "cyan",
        attrs=["bold"],
    )
    cprint(f"[API] Store ID: {request.store_id}", "cyan")
    cprint(f"[API] Splitting mode: {request.splitting_mode.value}", "cyan")

    import time

    start_time = time.time()

    try:
        # Get document from store
        if request.document_id not in DOCUMENT_STORE:
            raise HTTPException(status_code=404, detail="Document not found")

        doc_data = DOCUMENT_STORE[request.document_id]

        # Get or generate chunks
        if request.splitting_mode.value in doc_data["chunks_cache"]:
            chunks = doc_data["chunks_cache"][request.splitting_mode.value]
            cprint(f"[API] Using cached chunks: {len(chunks)} chunks", "green")
        else:
            # Chunk document
            chunks = document_chunker.chunk_document(
                docling_document=doc_data["docling_document"],
                mode=request.splitting_mode,
            )
            doc_data["chunks_cache"][request.splitting_mode.value] = chunks
            cprint(f"[API] Generated chunks: {len(chunks)} chunks", "green")

        # Verify chunks using Gemini
        cprint(f"[API] Starting AI verification for {len(chunks)} chunks...", "cyan")
        verified_chunks = await gemini_verifier.verify_batch(
            chunks=chunks,
            store_name=request.store_id,
            case_context=request.case_context,
        )

        # Update cached chunks with verification results
        doc_data["chunks_cache"][request.splitting_mode.value] = verified_chunks

        # Calculate statistics
        total_verified = sum(1 for c in verified_chunks if c.verified)
        processing_time = time.time() - start_time

        cprint(
            f"[API] ✓ Verification complete: {total_verified}/{len(verified_chunks)} verified in {processing_time:.2f}s",
            "green",
        )

        return VerificationResponse(
            document_id=request.document_id,
            verified_chunks=verified_chunks,
            total_verified=total_verified,
            total_chunks=len(verified_chunks),
            processing_time_seconds=processing_time,
            store_id=request.store_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        cprint(f"[API] Error executing verification: {e}", "red")
        raise HTTPException(
            status_code=500, detail=f"Error executing verification: {str(e)}"
        )


@app.post("/chunk", response_model=ChunkingResponse)
async def chunk_document(request: ChunkingRequest):
    """
    Chunk document according to specified mode

    Args:
        request: ChunkingRequest with document_id and splitting_mode

    Returns:
        ChunkingResponse with chunks and metadata
    """
    cprint(
        f"\n[API] Received chunking request: {request.document_id} ({request.splitting_mode.value})",
        "cyan",
        attrs=["bold"],
    )

    try:
        # Get document from store
        if request.document_id not in DOCUMENT_STORE:
            raise HTTPException(status_code=404, detail="Document not found")

        doc_data = DOCUMENT_STORE[request.document_id]

        # Check if chunks are already cached for this mode
        if request.splitting_mode.value in doc_data["chunks_cache"]:
            cprint(
                f"[API] Using cached chunks for {request.splitting_mode.value} mode",
                "green",
            )
            chunks = doc_data["chunks_cache"][request.splitting_mode.value]
        else:
            # Chunk document
            chunks = document_chunker.chunk_document(
                docling_document=doc_data["docling_document"],
                mode=request.splitting_mode,
            )

            # Cache chunks
            doc_data["chunks_cache"][request.splitting_mode.value] = chunks
            cprint(
                f"[API] Cached chunks for {request.splitting_mode.value} mode", "green"
            )

        return ChunkingResponse(
            document_id=request.document_id,
            splitting_mode=request.splitting_mode,
            chunks=chunks,
            total_chunks=len(chunks),
            message=f"Document chunked successfully ({len(chunks)} chunks in {request.splitting_mode.value} mode)",
        )

    except HTTPException:
        raise
    except Exception as e:
        cprint(f"[API] Error chunking document: {e}", "red")
        raise HTTPException(
            status_code=500, detail=f"Error chunking document: {str(e)}"
        )


@app.post("/export", response_model=ExportResponse)
async def export_document(request: ExportRequest):
    """
    Export verification document in specified format

    Args:
        request: ExportRequest with document_id, splitting_mode, and output_format

    Returns:
        ExportResponse with export metadata
    """
    cprint(
        f"\n[API] Received export request: {request.document_id} ({request.splitting_mode.value} -> {request.output_format.value})",
        "cyan",
        attrs=["bold"],
    )

    try:
        # Get document from store
        if request.document_id not in DOCUMENT_STORE:
            raise HTTPException(status_code=404, detail="Document not found")

        doc_data = DOCUMENT_STORE[request.document_id]

        # Get or generate chunks
        if request.splitting_mode.value in doc_data["chunks_cache"]:
            chunks = doc_data["chunks_cache"][request.splitting_mode.value]
        else:
            # Chunk document
            chunks = document_chunker.chunk_document(
                docling_document=doc_data["docling_document"],
                mode=request.splitting_mode,
            )
            doc_data["chunks_cache"][request.splitting_mode.value] = chunks

        # Generate output
        output_path = output_generator.generate_output(
            chunks=chunks,
            original_filename=doc_data["filename"],
            output_format=request.output_format,
        )

        # Store output path in document data
        doc_data["last_export"] = {
            "path": output_path,
            "format": request.output_format.value,
            "filename": output_path.name,
        }

        cprint(f"[API] Export complete: {output_path.name}", "green")

        return ExportResponse(
            document_id=request.document_id,
            output_format=request.output_format,
            filename=output_path.name,
            message=f"Document exported successfully as {request.output_format.value}",
        )

    except HTTPException:
        raise
    except Exception as e:
        cprint(f"[API] Error exporting document: {e}", "red")
        raise HTTPException(
            status_code=500, detail=f"Error exporting document: {str(e)}"
        )


@app.get("/download/{document_id}")
async def download_file(document_id: str):
    """
    Download the last exported file for a document

    Args:
        document_id: Document identifier

    Returns:
        FileResponse with the exported file
    """
    cprint(f"\n[API] Received download request: {document_id}", "cyan", attrs=["bold"])

    try:
        # Get document from store
        if document_id not in DOCUMENT_STORE:
            raise HTTPException(status_code=404, detail="Document not found")

        doc_data = DOCUMENT_STORE[document_id]

        # Check if export exists
        if "last_export" not in doc_data:
            raise HTTPException(
                status_code=404, detail="No export found for this document"
            )

        export_data = doc_data["last_export"]
        file_path = export_data["path"]

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Export file not found")

        cprint(f"[API] Sending file: {file_path.name}", "green")

        # Determine media type
        if export_data["format"] in ["word_landscape", "word_portrait"]:
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif export_data["format"] == "excel":
            media_type = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif export_data["format"] == "json":
            media_type = "application/json"
        else:  # CSV
            media_type = "text/csv"

        return FileResponse(
            path=file_path, filename=export_data["filename"], media_type=media_type
        )

    except HTTPException:
        raise
    except Exception as e:
        cprint(f"[API] Error downloading file: {e}", "red")
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")


@app.delete("/api/verify/reset/{document_id}")
async def reset_verification(document_id: str):
    """
    Clear AI verification results for a document

    Args:
        document_id: Document identifier

    Returns:
        Success message
    """
    cprint(
        f"\n[API] Received reset verification request: {document_id}",
        "cyan",
        attrs=["bold"],
    )

    try:
        # Get document from store
        if document_id not in DOCUMENT_STORE:
            raise HTTPException(status_code=404, detail="Document not found")

        doc_data = DOCUMENT_STORE[document_id]

        # Clear verification results from all cached chunks
        chunks_reset = 0
        for mode in doc_data["chunks_cache"]:
            for chunk in doc_data["chunks_cache"][mode]:
                # Reset all verification fields to None
                chunk.verified = None
                chunk.verification_score = None
                chunk.verification_source = None
                chunk.verification_note = None
                chunk.citations = None
                chunks_reset += 1

        cprint(f"[API] ✓ Cleared verification from {chunks_reset} chunks", "green")

        return {
            "message": "Verification results cleared successfully",
            "chunks_reset": chunks_reset,
        }

    except HTTPException:
        raise
    except Exception as e:
        cprint(f"[API] Error resetting verification: {e}", "red")
        raise HTTPException(
            status_code=500, detail=f"Error resetting verification: {str(e)}"
        )


@app.delete("/api/corpus/{store_id}")
async def delete_corpus(store_id: str):
    """
    Delete a File Search corpus/store

    Args:
        store_id: File Search store ID to delete

    Returns:
        Success message
    """
    cprint(
        f"\n[API] Received delete corpus request: {store_id}", "cyan", attrs=["bold"]
    )

    try:
        # Delete the store using corpus_manager
        success = corpus_manager.delete_store(store_id)

        if success:
            cprint(f"[API] ✓ Corpus deleted successfully: {store_id}", "green")
            return {"message": "Corpus deleted successfully", "store_id": store_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete corpus")

    except HTTPException:
        raise
    except Exception as e:
        cprint(f"[API] Error deleting corpus: {e}", "red")
        raise HTTPException(status_code=500, detail=f"Error deleting corpus: {str(e)}")


@app.delete("/cache/clear")
async def clear_cache():
    """Clear document cache"""
    cprint("\n[API] Clearing cache...", "cyan", attrs=["bold"])

    try:
        document_cache.clear_all()
        DOCUMENT_STORE.clear()

        return {"message": "Cache cleared successfully", "documents_cleared": 0}

    except Exception as e:
        cprint(f"[API] Error clearing cache: {e}", "red")
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    cprint("\n" + "=" * 80, "cyan")
    cprint("🚀 Starting Content Verification Tool API Server", "green", attrs=["bold"])
    cprint("=" * 80, "cyan")
    cprint("📝 API Documentation: http://localhost:8000/docs", "yellow")
    cprint("🏥 Health Check: http://localhost:8000/health", "yellow")
    cprint("=" * 80 + "\n", "cyan")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
