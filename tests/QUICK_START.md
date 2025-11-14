# Test Suite Quick Start Guide

## 🚀 Quick Start (30 seconds)

```bash
# 1. Install test dependencies
pip install -r tests/requirements-test.txt

# 2. Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"

# 3. Run all tests
pytest tests/ -v

# 4. Run only fast unit tests (no API needed)
pytest tests/ -m "unit and not gemini" -v
```

## 📊 Test Coverage Summary

| Test Suite | Tests | Focus Area | Marker |
|------------|-------|------------|--------|
| `test_document_processor.py` | 9 | File upload, validation, caching | `unit` |
| `test_chunker.py` | 14 | Paragraph/sentence chunking | `unit` |
| `test_gemini_metadata_extraction.py` | 10 | Flash-lite metadata generation | `gemini` |
| `test_gemini_verification_loop.py` | 11 | Flash verification loop | `gemini` |
| `test_output_generator.py` | 16 | Word/Excel/CSV/JSON output | `unit` |
| `test_api_endpoints.py` | 17 | FastAPI endpoints | `integration` |
| `test_e2e_workflows.py` | 10 | Complete workflows | `integration` |

**Total: 87 comprehensive tests**

## 🎯 Common Test Scenarios

### Test File Upload
```bash
pytest tests/test_document_processor.py::TestDocumentProcessor::test_upload_pdf -v
```

### Test Chunking (No API Key Needed)
```bash
pytest tests/test_chunker.py -v
```

### Test Gemini Metadata Extraction (Requires API Key)
```bash
pytest tests/test_gemini_metadata_extraction.py::TestGeminiMetadataExtraction::test_generate_metadata_from_docx -v
```

### Test Gemini Verification Loop (Requires API Key)
```bash
pytest tests/test_gemini_verification_loop.py::TestGeminiChunkVerification::test_verify_single_chunk -v
```

### Test Output Generation
```bash
pytest tests/test_output_generator.py::TestOutputGenerator::test_generate_excel -v
```

### Test API Endpoints
```bash
pytest tests/test_api_endpoints.py::TestUploadEndpoint -v
```

### Test Full E2E Workflow (Requires API Key, ~60s)
```bash
pytest tests/test_e2e_workflows.py::TestAIVerificationWorkflow::test_full_ai_verification_workflow -v
```

## 🔍 Test by Category

### Unit Tests Only (Fast, No External Dependencies)
```bash
pytest tests/ -m unit -v
# ~10-20 seconds
```

### Integration Tests (API + Workflows)
```bash
pytest tests/ -m integration -v
# ~15-30 seconds
```

### Gemini AI Tests (Requires GEMINI_API_KEY)
```bash
pytest tests/ -m gemini -v
# ~30-45 seconds
```

### Skip Slow Tests
```bash
pytest tests/ -m "not slow" -v
# Skips long-running E2E tests
```

## 🧪 Test What You're Working On

### Working on Document Processing?
```bash
pytest tests/test_document_processor.py tests/test_chunker.py -v
```

### Working on Gemini Integration?
```bash
pytest tests/test_gemini_metadata_extraction.py tests/test_gemini_verification_loop.py -v
```

### Working on Output Generation?
```bash
pytest tests/test_output_generator.py -v
```

### Working on API Endpoints?
```bash
pytest tests/test_api_endpoints.py -v
```

## 📈 Performance Expectations

- **Unit tests**: 10-20 seconds
- **Integration tests**: 15-30 seconds
- **Gemini tests**: 30-45 seconds
- **Full E2E workflow**: 30-60 seconds
- **All tests**: ~2-3 minutes

## ⚠️ Before Committing

Run this before committing your code:

```bash
# Run fast tests first
pytest tests/ -m "unit and not slow" -v

# If those pass, run integration tests
pytest tests/ -m "integration and not slow" -v

# Finally, run Gemini tests if you have API access
pytest tests/ -m gemini -v
```

## 🐛 Debugging Failed Tests

### Verbose output
```bash
pytest tests/test_name.py -vv
```

### Show print statements
```bash
pytest tests/test_name.py -s
```

### Stop on first failure
```bash
pytest tests/ -x
```

### Run only failed tests from last run
```bash
pytest --lf
```

### Show full test output
```bash
pytest tests/ -vv -s --tb=long
```

## 📝 Writing New Tests

1. **Add to appropriate test file** based on functionality
2. **Use existing fixtures** from `conftest.py`
3. **Add appropriate markers**: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.gemini`, `@pytest.mark.slow`
4. **Use cprint for visibility**:
   ```python
   from termcolor import cprint
   cprint("[TEST] Testing feature...", "cyan")
   cprint("[TEST] ✓ Success!", "green")
   ```

## 🔧 Troubleshooting

### No tests collected
```bash
# Make sure you're in the project root
cd /path/to/content_verification_tool
pytest tests/ -v
```

### Import errors
```bash
# Install test dependencies
pip install -r tests/requirements-test.txt
```

### Gemini tests skipped
```bash
# Set API key
export GEMINI_API_KEY="your_key_here"

# Or add to .env file
echo "GEMINI_API_KEY=your_key_here" >> .env
```

### LibreOffice not found
```bash
# macOS
brew install libreoffice

# Ubuntu/Debian
apt-get install libreoffice
```

## 💡 Tips

- **Run tests in watch mode** (requires pytest-watch):
  ```bash
  pip install pytest-watch
  ptw tests/
  ```

- **Generate coverage report**:
  ```bash
  pytest tests/ --cov=backend --cov-report=html
  open htmlcov/index.html
  ```

- **Run tests in parallel** (faster):
  ```bash
  pip install pytest-xdist
  pytest tests/ -n auto
  ```

---

**Need Help?** Check `tests/README.md` for detailed documentation.
