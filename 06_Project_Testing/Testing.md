# Project Testing Report - NetConnect

This document details the test strategy, execution plan, unit test results, and bug tracking formats.

---

## 1. Test Cases Specification

### Backend API Tests
| Test Case ID | Feature | Description | Inputs | Expected Output | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-BE-01** | Health Check | Validate API root status. | GET `/` | Status 200, status="healthy" | Passed |
| **TC-BE-02** | Generation Empty | Validate empty field validations. | POST `/api/starters/generate` with `""` | Status 422, Validation Error | Passed |
| **TC-BE-03** | Generation Fallback | Validate offline generation templates. | POST `/api/starters/generate` with valid data, `api_key=None` | Status 201, 3 generated starters | Passed |
| **TC-BE-04** | History Log | Check database session log persistence. | GET `/api/history` | List of past sessions | Passed |
| **TC-BE-05** | Update Feedback | Rate a conversation starter session. | PUT `/api/history/{id}/feedback` with `"thumbs_up"` | Status 200, feedback="thumbs_up" | Passed |
| **TC-BE-06** | Update Feedback Invalid | Validate feedback validation rules. | PUT `/api/history/{id}/feedback` with `"invalid_str"` | Status 400, Bad Request | Passed |
| **TC-BE-07** | Fact Verification | Validate Wikipedia API search parser. | POST `/api/facts/verify` with `"zero knowledge proof"` | Status 200, summary matches Wikipedia | Passed |

---

## 2. Test Execution Command

Both local and CI testing runs are executed via Python's built-in `unittest` module. In our reorganized structure, the test suite is located inside `05_Project_Development/backend/tests/`.

Run commands inside `05_Project_Development/`:
```bash
cd 05_Project_Development
python -m unittest discover -s backend/tests
```

### Unit Test Execution Log
```text
Ran 12 tests in 0.109s

OK
```

---

## 3. Bug Report Format

If you identify a bug during manual testing, please submit it using this format:

- **Bug Title**: `[BUG] Brief summary of the issue`
- **Preconditions**: Environment details (e.g. OS version, Python version, Gemini API key status)
- **Steps to Reproduce**:
  1. Navigate to the generator tab.
  2. Input event details with special characters...
  3. Click "Generate Starters".
- **Expected Behavior**: What should have happened.
- **Actual Behavior**: Error stacktrace or unexpected rendering.
- **Severity**: Low / Medium / High / Critical.
