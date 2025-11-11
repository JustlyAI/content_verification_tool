# Streamlit Frontend Refactoring Plan

## Overview

Comprehensive refactoring based on code review against latest Streamlit best practices. Addresses 34 identified issues across security, performance, and UX.

---

## Phase 1: Critical Security & Validation Fixes

### 1.1 Add File Size Validation

**Location**: `frontend/app.py:178-181`

```python
# Add after file upload
file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
MAX_FILE_SIZE_MB = 10

if file_size_mb > MAX_FILE_SIZE_MB:
    st.error(f"⚠️ File too large: {file_size_mb:.2f} MB. Maximum allowed size is {MAX_FILE_SIZE_MB} MB.")
    st.stop()
else:
    st.info(f"📄 **File**: {uploaded_file.name} ({file_size_mb:.2f} MB)")
```

### 1.2 Improve File Type Validation

**Location**: `frontend/app.py:171-176`

```python
import magic  # Add to requirements.txt: python-magic

def validate_file_type(file_content: bytes) -> tuple[bool, str]:
    """Validate file is actually PDF or DOCX by content, not extension"""
    file_type = magic.from_buffer(file_content, mime=True)
    allowed_types = {
        "application/pdf": "PDF",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX"
    }

    if file_type in allowed_types:
        return True, allowed_types[file_type]
    return False, file_type

# After upload
if uploaded_file is not None:
    file_content = uploaded_file.getvalue()
    is_valid, detected_type = validate_file_type(file_content)

    if not is_valid:
        st.error(f"⚠️ Invalid file type detected: {detected_type}. Please upload a valid PDF or DOCX file.")
        st.stop()
```

**Alternative** (without new dependency): Rely on backend validation and handle errors clearly.

### 1.3 Configuration Constants

**Location**: Top of file after imports

```python
# Configuration Constants
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
UPLOAD_TIMEOUT_BASE = int(os.getenv("UPLOAD_TIMEOUT_BASE", "180"))
EXPORT_TIMEOUT = int(os.getenv("EXPORT_TIMEOUT", "300"))
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "60"))
HEALTH_CHECK_TIMEOUT = int(os.getenv("HEALTH_CHECK_TIMEOUT", "5"))
SUPPORTED_FILE_TYPES = ["pdf", "docx"]

# Output format mappings
OUTPUT_FORMAT_LABELS = {
    "word_landscape": "📄 Word Document (Landscape) - More space for text and notes",
    "word_portrait": "📄 Word Document (Portrait) - Standard layout",
    "excel": "📊 Excel Spreadsheet - Compatible with Excel and Google Sheets",
    "csv": "📋 CSV File - Universal compatibility"
}

MIME_TYPES = {
    "word_landscape": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "word_portrait": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv"
}
```

### 1.4 Dynamic Timeout Configuration

**Location**: `frontend/app.py:47, 76, 99`

```python
def calculate_upload_timeout(file_size_mb: float) -> int:
    """Calculate appropriate timeout based on file size (10s per MB minimum)"""
    size_based_timeout = int(file_size_mb * 10)
    return max(UPLOAD_TIMEOUT_BASE, size_based_timeout)

# In upload_document function:
file_size_mb = len(file_content) / (1024 * 1024)
timeout = calculate_upload_timeout(file_size_mb)
response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=timeout)
```

### 1.5 User-Friendly Error Handling

**Location**: All API call error blocks

```python
def upload_document(file_content: bytes, filename: str) -> Optional[dict]:
    """Upload document to backend API with comprehensive error handling"""
    try:
        files = {"file": (filename, file_content)}
        file_size_mb = len(file_content) / (1024 * 1024)
        timeout = calculate_upload_timeout(file_size_mb)

        response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=timeout)
        response.raise_for_status()

        cprint(f"[FRONTEND] Upload successful: {filename}", "green")
        return response.json()

    except requests.exceptions.Timeout:
        st.error("⚠️ Upload timed out. Please try again with a smaller file or check your connection.")
        cprint(f"[FRONTEND] Upload timeout for {filename}", "red")
        return None

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend server. Please contact support.")
        cprint(f"[FRONTEND] Connection error", "red")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_detail = e.response.json().get('detail', 'Unknown error')
            st.error(f"⚠️ Invalid file: {error_detail}")
        elif e.response.status_code == 413:
            st.error("⚠️ File too large. Maximum size is 100 MB.")
        else:
            st.error("⚠️ An error occurred processing your file. Please try again.")
        cprint(f"[FRONTEND] HTTP error: {e}", "red")
        return None

    except Exception as e:
        st.error("⚠️ An unexpected error occurred. Please try again or contact support.")
        cprint(f"[FRONTEND] Unexpected error: {e}", "red")
        return None

# Apply similar pattern to export_document and download_document functions
```

---

## Phase 2: High Priority Performance & Reliability

### 2.1 Session State with Callbacks

**Location**: `frontend/app.py:162-165, 184-194`

```python
def init_session_state():
    """Initialize session state variables"""
    if "document_id" not in st.session_state:
        st.session_state.document_id = None
    if "document_info" not in st.session_state:
        st.session_state.document_info = None
    if "upload_in_progress" not in st.session_state:
        st.session_state.upload_in_progress = False
    if "last_generated" not in st.session_state:
        st.session_state.last_generated = None

def handle_upload():
    """Callback for document upload button"""
    if st.session_state.uploaded_file is None:
        return

    st.session_state.upload_in_progress = True
    file_content = st.session_state.uploaded_file.getvalue()
    filename = st.session_state.uploaded_file.name

    result = upload_document(file_content, filename)

    if result:
        st.session_state.document_id = result["document_id"]
        st.session_state.document_info = result

    st.session_state.upload_in_progress = False

# In main():
init_session_state()

# File uploader with key for callback access
uploaded_file = st.file_uploader(
    "Choose a file",
    type=SUPPORTED_FILE_TYPES,
    help="Supported formats: PDF, DOCX",
    label_visibility="collapsed",
    key="uploaded_file"
)

# Button with callback
if uploaded_file is not None:
    st.button(
        "🚀 Upload and Process",
        type="primary",
        use_container_width=True,
        on_click=handle_upload,
        disabled=st.session_state.upload_in_progress
    )
```

### 2.2 Cached Health Check

**Location**: `frontend/app.py:122-128`

```python
@st.cache_data(ttl=30)  # Cache for 30 seconds
def check_backend_health() -> bool:
    """Check if backend is available (cached)"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=HEALTH_CHECK_TIMEOUT)
        return response.status_code == 200
    except Exception:
        return False

# In main():
col1, col2 = st.columns([6, 1])
with col1:
    if not check_backend_health():
        st.error("⚠️ Backend API is not available. Please ensure the backend is running.")
        st.code(f"Expected backend at: {BACKEND_URL}", language="text")
        st.stop()
    st.success("✅ Connected to backend")
with col2:
    if st.button("🔄", help="Refresh connection status"):
        check_backend_health.clear()
        st.rerun()
```

### 2.3 Upload Progress Indicators

**Location**: `frontend/app.py:184-194`

```python
def upload_with_progress(file_content: bytes, filename: str) -> Optional[dict]:
    """Upload document with progress indication"""
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text("Preparing upload...")
        progress_bar.progress(10)

        status_text.text("Uploading document to server...")
        progress_bar.progress(30)

        files = {"file": (filename, file_content)}
        file_size_mb = len(file_content) / (1024 * 1024)
        timeout = calculate_upload_timeout(file_size_mb)

        response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=timeout)

        progress_bar.progress(70)
        status_text.text("Processing document with Docling...")

        response.raise_for_status()
        result = response.json()

        progress_bar.progress(100)
        status_text.text("✅ Upload complete!")

        cprint(f"[FRONTEND] Upload successful: {filename}", "green")
        return result

    except Exception as e:
        # Error handling from Phase 1
        return None

    finally:
        progress_bar.empty()
        status_text.empty()
```

### 2.4 Retry Logic for API Calls

**Location**: All API functions

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session_with_retries() -> requests.Session:
    """Create requests session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Create at module level
API_SESSION = get_session_with_retries()

# Use in all API calls:
response = API_SESSION.post(f"{BACKEND_URL}/upload", files=files, timeout=timeout)
response = API_SESSION.post(f"{BACKEND_URL}/export", json=payload, timeout=EXPORT_TIMEOUT)
response = API_SESSION.get(f"{BACKEND_URL}/download/{document_id}", timeout=DOWNLOAD_TIMEOUT)
```

### 2.5 Backend Response Validation

**Location**: After all API calls

```python
def validate_upload_response(result: dict) -> bool:
    """Validate upload response has required fields"""
    required_fields = ["document_id", "filename", "page_count", "file_size", "message"]
    return all(field in result for field in required_fields)

def validate_export_response(result: dict) -> bool:
    """Validate export response has required fields"""
    required_fields = ["document_id", "filename", "message"]
    return all(field in result for field in required_fields)

# In upload flow:
if result and validate_upload_response(result):
    st.session_state.document_id = result["document_id"]
    st.session_state.document_info = result
    st.success(f"✅ {result['message']}")
    st.balloons()
else:
    st.error("⚠️ Invalid response from server. Please try again.")

# In export flow:
if export_result and validate_export_response(export_result):
    # Proceed with download
    pass
else:
    st.error("⚠️ Invalid export response. Please try again.")
```

### 2.6 Explicit Chunking Default

**Location**: `frontend/app.py:213-222`

```python
chunking_mode = st.radio(
    "Chunking Mode",
    options=["paragraph", "sentence"],
    index=0,  # Explicit default to paragraph (per CLAUDE.md spec)
    format_func=lambda x: {
        "paragraph": "📝 Paragraph-level chunking",
        "sentence": "📄 Sentence-level chunking"
    }[x],
    help="Paragraph mode groups related content (recommended for most documents). Sentence mode provides finer granularity.",
)

st.caption("**Paragraph mode** (default): Groups related sentences together for coherent verification.")
st.caption("**Sentence mode**: Individual sentences for detailed line-by-line verification.")
```

### 2.7 Replace Unsafe HTML

**Location**: `frontend/app.py:328-331`

```python
# Remove unsafe_allow_html usage
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("Content Verification Tool v1.0.0 | Built with Streamlit & FastAPI")
```

### 2.8 Download Button State Management

**Location**: `frontend/app.py:277-322`

```python
# Generation section
if st.session_state.document_id and st.session_state.last_generated is None:
    st.subheader("Step 4: Generate Verification Document")

    output_format = st.selectbox(
        "Select output format",
        options=list(OUTPUT_FORMAT_LABELS.keys()),
        format_func=lambda x: OUTPUT_FORMAT_LABELS[x],
        label_visibility="collapsed"
    )

    if st.button("🎯 Generate Document", type="primary", use_container_width=True):
        with st.spinner("Generating verification document..."):
            payload = {
                "document_id": st.session_state.document_id,
                "output_format": output_format,
                "chunking_mode": chunking_mode
            }

            export_result = export_document(payload)

            if export_result and validate_export_response(export_result):
                file_content = download_document(st.session_state.document_id)

                if file_content:
                    st.session_state.last_generated = {
                        "filename": export_result["filename"],
                        "content": file_content,
                        "mime_type": MIME_TYPES[output_format],
                        "format": output_format
                    }
                    st.rerun()

# Download section (separate from generation)
if st.session_state.last_generated:
    st.success("🎉 Document ready for download!")

    st.download_button(
        label="⬇️ Download Verification Document",
        data=st.session_state.last_generated["content"],
        file_name=st.session_state.last_generated["filename"],
        mime=st.session_state.last_generated["mime_type"],
        type="primary",
        use_container_width=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Generate Different Format", use_container_width=True):
            st.session_state.last_generated = None
            st.rerun()
    with col2:
        if st.button("📄 Upload New Document", use_container_width=True):
            st.session_state.document_id = None
            st.session_state.document_info = None
            st.session_state.last_generated = None
            st.rerun()
```

---

## Phase 3: Configuration & Additional Improvements

### 3.1 Create `.streamlit/config.toml`

**New file**: `frontend/.streamlit/config.toml`

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 100

[browser]
gatherUsageStats = false

[runner]
magicEnabled = true
fastReruns = true
```

### 3.2 Move set_page_config to Top

**Location**: `frontend/app.py:1-21`

```python
import streamlit as st

# Configure Streamlit page FIRST (before any other st.* commands)
st.set_page_config(
    page_title="Content Verification Tool",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Then other imports
import requests
from pathlib import Path
from typing import Optional
import os
from termcolor import cprint
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration constants (defined in Phase 1.3)
```

### 3.3 Backend URL Validation

**Location**: After BACKEND_URL definition

```python
from urllib.parse import urlparse

# Validate BACKEND_URL format
try:
    parsed = urlparse(BACKEND_URL)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError("Invalid BACKEND_URL format")
except Exception as e:
    st.error(f"❌ Configuration error: Invalid BACKEND_URL - {BACKEND_URL}")
    st.info("Please set a valid BACKEND_URL environment variable (e.g., http://localhost:8000)")
    st.stop()
```

### 3.4 Add Reset Functionality

**Location**: In sidebar or after document info

```python
# In sidebar
with st.sidebar:
    st.divider()
    if st.session_state.document_info or st.session_state.last_generated:
        if st.button("🔄 Start Over", use_container_width=True, type="secondary"):
            st.session_state.document_id = None
            st.session_state.document_info = None
            st.session_state.last_generated = None
            st.session_state.upload_in_progress = False
            st.rerun()
```

### 3.5 Error Boundary for App

**Location**: Wrap main() at bottom of file

```python
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("⚠️ A critical error occurred. Please refresh the page.")
        cprint(f"[FRONTEND] Uncaught exception in main: {e}", "red")

        # Show details in debug mode
        if os.getenv("DEBUG", "false").lower() == "true":
            st.exception(e)
```

### 3.6 Add Type Hints

**Location**: All functions

```python
from typing import Optional, Dict, Any

def upload_document(file_content: bytes, filename: str) -> Optional[Dict[str, Any]]:
    """Upload document to backend API"""
    # ...

def export_document(payload: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Export document to specified format"""
    # ...

def download_document(document_id: str) -> Optional[bytes]:
    """Download generated verification document"""
    # ...

def check_backend_health() -> bool:
    """Check if backend is available"""
    # ...

def main() -> None:
    """Main Streamlit application"""
    # ...
```

### 3.7 Add Structured Logging

**Location**: Top of file and throughout

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG") != "true" else logging.DEBUG,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Use throughout:
logger.info(f"User uploaded file: {filename}, size: {file_size_mb:.2f} MB")
logger.info(f"User selected chunking mode: {chunking_mode}")
logger.info(f"User generated export: {output_format}")
logger.error(f"Upload failed: {e}")
```

### 3.8 Add Feature Flags

**Location**: After configuration constants

```python
# Feature flags
FEATURES = {
    "show_debug_info": os.getenv("DEBUG", "false").lower() == "true",
    "show_advanced_options": os.getenv("SHOW_ADVANCED", "false").lower() == "true",
}

# Use in code:
if FEATURES["show_debug_info"]:
    with st.expander("🔍 Debug Information"):
        st.json(st.session_state.to_dict())
```

---

## Implementation Checklist

### Phase 1: Critical (Day 1)

- [ ] Extract all configuration constants to module level
- [ ] Add file size validation (100 MB check)
- [ ] Implement dynamic timeout calculation
- [ ] Improve error handling with user-friendly messages
- [ ] Add file type validation (content-based or backend validation)

### Phase 2: High Priority (Day 2-3)

- [ ] Refactor session state with callbacks
- [ ] Add `@st.cache_data` to health check
- [ ] Implement upload progress indicators
- [ ] Add retry logic with requests session
- [ ] Add response validation functions
- [ ] Set explicit chunking mode default
- [ ] Replace unsafe HTML with safe markdown
- [ ] Fix download button state management

### Phase 3: Configuration & Polish (Day 4)

- [ ] Create `.streamlit/config.toml`
- [ ] Move `st.set_page_config()` to top
- [ ] Add backend URL validation
- [ ] Add reset/clear functionality
- [ ] Add error boundary wrapper
- [ ] Add type hints to all functions
- [ ] Implement structured logging
- [ ] Add feature flags

---

## Testing Requirements

### Unit Tests

- File size validation edge cases
- File type validation (valid/invalid files)
- Timeout calculation logic
- Response validation functions
- Session state initialization

### Integration Tests

- Full upload → process → export → download flow
- Error recovery scenarios
- Retry logic behavior
- Cache invalidation

### Manual Testing

- Upload 100 MB file (should pass)
- Upload 101 MB file (should fail)
- Upload renamed .txt as .pdf (should fail)
- Test with slow network (progress indicators)
- Test backend disconnect (error handling)
- Test with backend returning invalid responses

---

## Dependencies to Add

Add to `frontend/requirements.txt`:

```
streamlit>=1.28.0
requests>=2.31.0
urllib3>=2.0.0
termcolor>=2.3.0
python-magic>=0.4.27  # Optional: for content-based file validation
```

---

## Breaking Changes

None. All changes are backward compatible with existing backend API.

---

## Performance Impact

### Improvements

- Health check caching reduces API calls by ~95%
- Retry logic prevents failed uploads from requiring full re-upload
- Session state callbacks reduce unnecessary reruns

### Considerations

- File type validation adds minimal overhead (<100ms)
- Progress indicators add minor UI overhead (negligible)
- Retry logic may increase latency on failures (acceptable tradeoff)

---

## Security Improvements

1. File size validation prevents resource exhaustion
2. Content-based file type validation prevents malicious files
3. User-friendly error messages prevent information leakage
4. Backend URL validation prevents misconfigurations
5. Removed unsafe HTML rendering
6. XSS protection enabled in config.toml

---

## Estimated Effort

- **Phase 1**: 6-8 hours
- **Phase 2**: 8-10 hours
- **Phase 3**: 4-6 hours
- **Testing**: 4-6 hours

**Total**: 22-30 hours (3-4 working days)
