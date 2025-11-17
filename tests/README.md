# Content Verification Tool - Test Suite

Comprehensive test suite for the Document Verification Assistant, covering file upload, document processing, Gemini AI metadata extraction (Flash-lite), AI-powered verification loop (Flash), and output generation.

## Test Overview

### Test Categories

1. **Unit Tests** (`@pytest.mark.unit`)

   - Document processor and file upload
   - Document chunker (paragraph/sentence modes)
   - Output generator (Word/Excel/CSV/JSON)
   - Fast tests with no external dependencies

2. **Gemini AI Tests** (`@pytest.mark.gemini`)

   - Flash-lite metadata extraction
   - Flash verification loop
   - File Search store management
   - Requires `GEMINI_API_KEY`

3. **Integration Tests** (`@pytest.mark.integration`)

   - FastAPI endpoint testing
   - API request/response validation
   - End-to-end workflows

4. **Slow Tests** (`@pytest.mark.slow`)
   - Full AI verification workflows
   - Batch processing tests
   - Multi-document scenarios

## Setup

### 1. Install Dependencies

```bash
pip install pytest pytest-asyncio pandas openpyxl python-docx
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note:** Gemini tests will be skipped if `GEMINI_API_KEY` is not set.

### 3. Verify Setup

```bash
pytest --version
```

## Running Tests

### Run All Tests

```bash
# From project root
pytest tests/

# With verbose output
pytest tests/ -v
```

### Run Specific Test Categories

```bash
# Unit tests only (fast)
pytest tests/ -m unit

# Integration tests
pytest tests/ -m integration

# Gemini AI tests (requires API key)
pytest tests/ -m gemini

# Exclude slow tests
pytest tests/ -m "not slow"
```

### Run Specific Test Files

```bash
# Document processor tests
pytest tests/test_document_processor.py

# Chunker tests
pytest tests/test_chunker.py

# Gemini metadata extraction
pytest tests/test_gemini_metadata_extraction.py

# Gemini verification loop
pytest tests/test_gemini_verification_loop.py

# Output generator tests
pytest tests/test_output_generator.py

# API endpoint tests
pytest tests/test_api_endpoints.py

# End-to-end workflows
pytest tests/test_e2e_workflows.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_gemini_metadata_extraction.py::TestGeminiMetadataExtraction

# Run a specific test function
pytest tests/test_document_processor.py::TestDocumentProcessor::test_convert_document_pdf

# Run tests matching a pattern
pytest tests/ -k "metadata"
```

## Test Structure

```
tests/
├── conftest.py                             # Pytest fixtures and configuration
├── pytest.ini                              # Pytest settings
├── README.md                               # This file
├── test_document_processor.py              # Document upload and processing
├── test_chunker.py                         # Chunking strategies
├── test_gemini_metadata_extraction.py      # Gemini Flash-lite metadata extraction
├── test_gemini_verification_loop.py        # Gemini Flash verification loop
├── test_output_generator.py                # Output format generation
├── test_api_endpoints.py                   # FastAPI endpoint testing
└── test_e2e_workflows.py                   # End-to-end workflows
```

## Key Test Scenarios

### 1. File Upload and Management

```python
# Tests document validation, caching, PDF/DOCX conversion
pytest tests/test_document_processor.py -v
```

**Covers:**

- File size validation (< 100MB)
- Supported formats (PDF, DOCX)
- Docling conversion
- Document caching

### 2. Flash-lite Metadata Extraction

```python
# Tests Gemini Flash model for metadata generation
pytest tests/test_gemini_metadata_extraction.py -v -m gemini
```

**Covers:**

- AI-powered metadata generation
- Document type classification
- Keyword extraction
- Case context incorporation
- JSON structured output

### 3. Flash-driven Verification Loop

```python
# Tests Gemini Flash model for chunk verification
pytest tests/test_gemini_verification_loop.py -v -m gemini
```

**Covers:**

- File Search store creation
- Reference document upload and indexing
- Single chunk verification
- Batch verification with rate limiting
- Citation extraction
- Verification score validation (1-10)
- Retry mechanism for rate limits

### 4. End-to-End AI Verification

```python
# Tests complete workflow with AI verification
pytest tests/test_e2e_workflows.py::TestAIVerificationWorkflow -v -m gemini
```

**Workflow Steps:**

1. Upload target document
2. Create File Search store
3. Generate metadata (Flash-lite)
4. Upload reference documents
5. Chunk target document
6. Verify chunks (Flash verification loop)
7. Export verified results
8. Download final document

## Test Fixtures

### Document Fixtures

- `sample_document_content`: Minimal PDF for testing
- `sample_docx_content`: DOCX with test paragraphs
- `sample_chunks_data`: Pre-chunked document data
- `sample_verified_chunks_data`: Chunks with verification results

### Gemini Fixtures

- `gemini_api_key`: Loads API key from environment
- `gemini_client`: Initialized Gemini client
- `mock_file_search_store`: Temporary File Search store
- `sample_case_context`: Test case context string
- `sample_metadata`: Sample DocumentMetadata object

### Utility Fixtures

- `temp_dir`: Temporary directory for test outputs
- `test_client`: FastAPI TestClient for API testing

## Test Output

### Success Output

```
============================== test session starts ===============================
platform darwin -- Python 3.11.x, pytest-8.x.x
collected 87 items

tests/test_document_processor.py ✓✓✓✓✓✓✓✓✓                              [ 10%]
tests/test_chunker.py ✓✓✓✓✓✓✓✓✓✓✓✓                                      [ 24%]
tests/test_gemini_metadata_extraction.py ✓✓✓✓✓✓✓✓✓                      [ 34%]
tests/test_gemini_verification_loop.py ✓✓✓✓✓✓✓✓✓✓✓                      [ 47%]
tests/test_output_generator.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓                          [ 63%]
tests/test_api_endpoints.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓                           [ 81%]
tests/test_e2e_workflows.py ✓✓✓✓✓✓                                       [100%]

============================== 87 passed in 45.23s ===============================
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run unit tests (no API key required)
        run: pytest tests/ -m "unit and not gemini"

      - name: Run Gemini tests (with API key)
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: pytest tests/ -m gemini
        if: env.GEMINI_API_KEY != ''
```

## Troubleshooting

### Common Issues

1. **Missing GEMINI_API_KEY**

   ```
   SKIPPED [1] conftest.py:48: GEMINI_API_KEY not found
   ```

   **Solution:** Set `GEMINI_API_KEY` in `.env` file

2. **LibreOffice not found (for DOCX conversion)**

   ```
   FileNotFoundError: libreoffice command not found
   ```

   **Solution:** Install LibreOffice

   ```bash
   # macOS
   brew install libreoffice

   # Ubuntu/Debian
   apt-get install libreoffice
   ```

3. **SpaCy model not found**

   ```
   OSError: Can't find model 'en_core_web_sm'
   ```

   **Solution:** Install SpaCy model

   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Rate limit errors from Gemini**
   ```
   Error: Rate limit exceeded
   ```
   **Solution:** Tests include retry logic and delays. If persistent, run with smaller batch sizes:
   ```bash
   pytest tests/ -m gemini --timeout=300
   ```

## Coverage Report

Generate test coverage report:

```bash
pip install pytest-cov
pytest tests/ --cov=backend --cov-report=html --cov-report=term
```

View HTML report:

```bash
open htmlcov/index.html
```

## Test Development Guidelines

### Adding New Tests

1. **Choose the right marker:**

   - `@pytest.mark.unit` - Fast, isolated tests
   - `@pytest.mark.integration` - API/workflow tests
   - `@pytest.mark.gemini` - Requires Gemini API
   - `@pytest.mark.slow` - Long-running tests

2. **Use fixtures from conftest.py**

   ```python
   def test_my_feature(self, sample_docx_content, gemini_client):
       # Test implementation
       pass
   ```

3. **Add cleanup logic for Gemini resources**

   ```python
   def teardown_method(self):
       for store_name in self.stores_to_cleanup:
           self.service.client.file_search_stores.delete(name=store_name)
   ```

4. **Use cprint for clear test output**

   ```python
   from termcolor import cprint

   cprint("[TEST] Testing feature...", "cyan")
   cprint("[TEST] ✓ Feature works!", "green")
   ```

## Performance Benchmarks

### Expected Test Times

- **Unit tests** (no Gemini): ~10-20 seconds
- **Integration tests**: ~15-30 seconds
- **Gemini metadata extraction**: ~3-5 seconds per document
- **Gemini verification**: ~0.5-1 second per chunk
- **Full E2E workflow**: ~30-60 seconds

### Optimization Tips

1. Run fast tests first:

   ```bash
   pytest tests/ -m "unit and not slow"
   ```

2. Parallel execution:

   ```bash
   pip install pytest-xdist
   pytest tests/ -n auto
   ```

3. Skip slow tests during development:
   ```bash
   pytest tests/ -m "not slow"
   ```

## Contact

For questions or issues with the test suite, please check:

- Project documentation in `/docs`
- GitHub issues
- Implementation reports in project root

---

**Happy Testing! 🧪**
