# Error Tracking - Processing Demo Session

This document tracks errors encountered and resolved during the processing demo notebook development.

---

## Error #1: KeyError accessing docling_doc.pages[0]

**Date**: 2025-11-16
**File**: `processing_demo.ipynb` - Cell 4 (PDF Processing)
**Status**: ✅ Resolved

### Error Message
```python
KeyError: 0
```

### Stack Trace
```
Cell In[2], line 36
     34 if hasattr(docling_doc, 'pages'):
     35     print(f"   Total pages: {len(docling_doc.pages)}")
---> 36     print(f"   First page: {docling_doc.pages[0] if docling_doc.pages else 'N/A'}")

KeyError: 0
```

### Issue Description
When attempting to access the first page of a DoclingDocument object using `docling_doc.pages[0]`, a KeyError is raised. This suggests that `pages` is not a list but rather a dictionary or another data structure that doesn't support integer indexing.

### Analysis
- The `hasattr(docling_doc, 'pages')` check passes
- The `len(docling_doc.pages)` works (indicating pages exists and has length)
- Direct integer indexing `pages[0]` fails with KeyError

### Hypothesis
The `pages` attribute is likely:
- A dictionary with page keys (possibly page numbers as keys)
- A custom collection object that requires different access patterns
- Needs to be accessed via iteration or `.items()` method

### Root Cause
The `DoclingDocument.pages` attribute is a **dictionary** (likely with page IDs or 1-based page numbers as keys), not a list. Attempting to access with integer index `[0]` fails because there's no key `0`.

### Solution
Access pages by iterating or using proper keys instead of integer indices:

```python
# ❌ WRONG - Treats pages as list
print(f"   First page: {docling_doc.pages[0]}")

# ✅ CORRECT - Iterate over pages
if hasattr(docling_doc, 'pages') and docling_doc.pages:
    first_page_key = next(iter(docling_doc.pages.keys()))
    print(f"   First page key: {first_page_key}")
    print(f"   Page keys: {list(docling_doc.pages.keys())}")
```

### Fix Applied
Updated `processing_demo.ipynb` Cell 4 to properly access pages dictionary instead of treating it as a list.

### Related Code
```python
# Fixed code in notebook
if hasattr(docling_doc, 'pages'):
    print(f"   Total pages: {len(docling_doc.pages)}")
    if docling_doc.pages:
        page_keys = list(docling_doc.pages.keys())
        print(f"   Page keys: {page_keys[:5]}")  # Show first 5 keys
```

---

## Error #2: FileNotFoundError - LibreOffice executable not found

**Date**: 2025-11-16
**File**: `backend/app/processing/document_processor.py:83` (DOCX → PDF conversion)
**Status**: 🔍 Investigating

### Error Message
```python
FileNotFoundError: [Errno 2] No such file or directory: 'libreoffice'
```

### Stack Trace
```
File ~/Dev/ai-law/content_verification_tool/backend/app/processing/document_processor.py:210
    pdf_path = self._convert_docx_to_pdf(tmp_path)

File ~/Dev/ai-law/content_verification_tool/backend/app/processing/document_processor.py:83
    result = subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(docx_path)
    ], ...)
```

### Issue Description
When attempting to convert a DOCX file to PDF, the code calls the `libreoffice` command via subprocess. This command is not found on the system, causing the conversion to fail.

### Analysis
**Root Cause**: LibreOffice is either:
1. Not installed on the system
2. Installed but the executable path is different (e.g., on macOS: `/Applications/LibreOffice.app/Contents/MacOS/soffice`)
3. Not in the system PATH

### Hypothesis
The code assumes LibreOffice is installed and accessible via the `libreoffice` command. On different platforms, the executable name/path varies:
- **Linux**: Usually `libreoffice` in PATH
- **macOS**: `/Applications/LibreOffice.app/Contents/MacOS/soffice` or `soffice`
- **Windows**: `soffice.exe` or full path to executable

### Solution Options

#### Option 1: Install LibreOffice (Quick Fix)
```bash
# macOS
brew install --cask libreoffice

# Linux (Ubuntu/Debian)
sudo apt-get install libreoffice

# Verify installation
libreoffice --version
# OR on macOS
/Applications/LibreOffice.app/Contents/MacOS/soffice --version
```

#### Option 2: Update Code to Find LibreOffice Dynamically
Modify `document_processor.py` to:
1. Check multiple possible paths for LibreOffice
2. Use `shutil.which()` to find the executable
3. Support both `libreoffice` and `soffice` commands
4. Provide helpful error message if not found

#### Option 3: Skip DOCX Conversion for Demo
For notebook demonstration purposes, comment out or skip Cell 6 (DOCX processing) and focus on PDF processing only.

### Docker vs Local Development

**Important Discovery**:
- ✅ LibreOffice **IS installed** in the Docker container (backend/Dockerfile:14-15)
- ✅ Docker sets environment variable: `DOCLING_LIBREOFFICE_CMD=/usr/bin/libreoffice` (Dockerfile:43)
- ❌ The code does NOT use this environment variable - it's hardcoded to "libreoffice" (document_processor.py:85)
- ❌ LibreOffice is NOT installed on local macOS for development/testing

**Why This Matters**:
- Production (Docker): DOCX processing works fine ✅
- Local Development (macOS): DOCX processing fails ❌
- Jupyter Notebooks: Running locally, so fails ❌

### Recommended Fix

**Option A: Quick Local Fix (For Notebook/Development)**
Install LibreOffice locally:
```bash
brew install --cask libreoffice
```

**Option B: Code Improvement (Best Practice)**
Update `document_processor.py` to use the environment variable and fall back to dynamic detection:
```python
# At top of file
import shutil

# In _convert_docx_to_pdf method
libreoffice_cmd = os.getenv('DOCLING_LIBREOFFICE_CMD')
if not libreoffice_cmd:
    # Try to find it dynamically
    for cmd in ['libreoffice', 'soffice']:
        if shutil.which(cmd):
            libreoffice_cmd = cmd
            break

    # Try macOS path
    if not libreoffice_cmd:
        macos_path = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
        if Path(macos_path).exists():
            libreoffice_cmd = macos_path

if not libreoffice_cmd:
    raise Exception("LibreOffice not found. Please install it or set DOCLING_LIBREOFFICE_CMD env variable.")

result = subprocess.run([
    libreoffice_cmd,  # Use dynamic command
    "--headless",
    ...
])
```

**Option C: Skip for Notebook Demo**
For notebook demonstration purposes only, skip Cell 6 (DOCX processing)

### Related Code
```python
# Current code in document_processor.py:83
result = subprocess.run([
    "libreoffice",  # ❌ Hardcoded command
    "--headless",
    "--convert-to", "pdf",
    ...
], ...)

# Proposed fix - dynamic executable finding
def _find_libreoffice_executable():
    """Find LibreOffice executable on the system"""
    possible_commands = ["libreoffice", "soffice"]
    possible_paths = [
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",  # macOS
        "C:\\Program Files\\LibreOffice\\program\\soffice.exe",  # Windows
    ]

    # Try common commands
    for cmd in possible_commands:
        if shutil.which(cmd):
            return cmd

    # Try known paths
    for path in possible_paths:
        if Path(path).exists():
            return path

    return None
```

### Impact
- **Blocking**: DOCX processing in the notebook
- **Workaround**: Use PDF files only for demonstration
- **Production Impact**: DOCX upload feature will fail until LibreOffice is properly configured

---

**Legend:**
- 🔍 Investigating
- 🛠️ In Progress
- ✅ Resolved
- ❌ Blocked
