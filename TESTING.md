# Testing Guide

Comprehensive guide for testing the FastAPI Employee Management System.

## Table of Contents
- [Manual Testing with cURL](#manual-testing-with-curl)
- [Testing with Postman](#testing-with-postman)
- [Automated Testing with pytest](#automated-testing-with-pytest)
- [API Testing Scenarios](#api-testing-scenarios)

---

## Manual Testing with cURL

### 1. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

Expected Response:
```json
{
  "success": true,
  "message": "Application is up and running at 8000"
}
```

### 2. Get All Employees
```bash
curl -X GET "http://localhost:8000/"
```

### 3. Create Employee
```bash
curl -X POST "http://localhost:8000/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "john_doe",
    "age": 28,
    "department": "backend",
    "salary": 95000.0,
    "position": "sde2"
  }'
```

### 4. Update Employee
```bash
curl -X PUT "http://localhost:8000/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "john_doe",
    "newName": "john_smith"
  }'
```

### 5. Search Employees
```bash
# Basic search with pagination
curl "http://localhost:8000/search?skip=0&limit=5"

# Search by name
curl "http://localhost:8000/search?name=john_doe&skip=0&limit=10"
```

### 6. Get Employee by Name
```bash
curl "http://localhost:8000/home/john_doe"
```

---

## Testing with Postman

### Import Collection
1. Open Postman
2. Create new Collection: "Employee Management API"
3. Add requests as shown below

### Request Templates

#### GET /health
- **Method**: GET
- **URL**: http://localhost:8000/health
- **Tests**:
```javascript
pm.test("Status code is 200", () => {
    pm.response.to.have.status(200);
});

pm.test("Response has success field", () => {
    pm.expect(pm.response.json()).to.have.property('success');
    pm.expect(pm.response.json().success).to.equal(true);
});
```

#### POST / (Create Employee)
- **Method**: POST
- **URL**: http://localhost:8000/
- **Headers**: 
  - Content-Type: application/json
- **Body** (raw JSON):
```json
{
  "name": "alice_smith",
  "age": 32,
  "department": "frontend",
  "salary": 105000.0,
  "position": "sde3"
}
```
- **Tests**:
```javascript
pm.test("Employee created successfully", () => {
    pm.expect(pm.response.code).to.be.oneOf([200, 201]);
    pm.expect(pm.response.json().success).to.equal(true);
    pm.expect(pm.response.json().message).to.include("created");
});

pm.test("Response contains employee data", () => {
    const responseBody = pm.response.json();
    pm.expect(responseBody.data).to.have.property('name');
    pm.expect(responseBody.data).to.have.property('salary');
});
```

#### PUT / (Update Employee)
- **Method**: PUT
- **URL**: http://localhost:8000/
- **Headers**:
  - Content-Type: application/json
- **Body**:
```json
{
  "name": "alice_smith",
  "newName": "alice_johnson"
}
```

#### GET /search (Pagination)
- **Method**: GET
- **URL**: http://localhost:8000/search?skip=0&limit=5
- **Query Parameters**:
  - skip: 0
  - limit: 5
  - name (optional): employee name

#### GET /home/{name} (Get by Name)
- **Method**: GET
- **URL**: http://localhost:8000/home/alice_smith

---

## Automated Testing with pytest

### Test File: `test_main.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestHealth:
    def test_health_check_status(self):
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_content(self):
        response = client.get("/health")
        json_data = response.json()
        assert json_data["success"] is True
        assert "Application is up and running" in json_data["message"]

class TestGetAllEmployees:
    def test_get_all_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200
    
    def test_get_all_returns_data(self):
        response = client.get("/")
        json_data = response.json()
        assert "success" in json_data
        assert "data" in json_data

class TestCreateEmployee:
    def test_create_employee_success(self):
        employee_data = {
            "name": "test_employee",
            "age": 30,
            "department": "testing",
            "salary": 80000.0,
            "position": "qa_engineer"
        }
        response = client.post("/", json=employee_data)
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is True
        assert "created successfully" in json_data["message"]
    
    def test_create_employee_missing_field(self):
        incomplete_data = {
            "name": "test_employee",
            "age": 30
            # Missing department, salary, position
        }
        response = client.post("/", json=incomplete_data)
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_create_employee_invalid_type(self):
        invalid_data = {
            "name": "test_employee",
            "age": "thirty",  # Should be integer
            "department": "testing",
            "salary": 80000.0,
            "position": "qa_engineer"
        }
        response = client.post("/", json=invalid_data)
        assert response.status_code == 422

class TestUpdateEmployee:
    def test_update_existing_employee(self):
        # First create an employee
        client.post("/", json={
            "name": "update_test",
            "age": 28,
            "department": "backend",
            "salary": 90000.0,
            "position": "developer"
        })
        
        # Then update
        update_data = {
            "name": "update_test",
            "newName": "update_test_new"
        }
        response = client.put("/", json=update_data)
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is True
    
    def test_update_nonexistent_employee(self):
        update_data = {
            "name": "nonexistent_employee",
            "newName": "new_name"
        }
        response = client.put("/", json=update_data)
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is False
        assert "not found" in json_data["message"]

class TestSearch:
    def test_search_basic(self):
        response = client.get("/search?skip=0&limit=10")
        assert response.status_code == 200
    
    def test_search_with_name_filter(self):
        response = client.get("/search?name=utsav&skip=0&limit=10")
        assert response.status_code == 200
    
    def test_search_pagination(self):
        response1 = client.get("/search?skip=0&limit=5")
        response2 = client.get("/search?skip=5&limit=5")
        assert response1.status_code == 200
        assert response2.status_code == 200

class TestGetByName:
    def test_get_existing_employee(self):
        response = client.get("/home/utsav")
        assert response.status_code == 200
    
    def test_get_nonexistent_employee(self):
        response = client.get("/home/nonexistent_xyz_123")
        assert response.status_code == 200
        json_data = response.json()
        # Implementation may vary - check actual behavior

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Run Tests
```bash
# Run all tests
pytest test_main.py -v

# Run specific test class
pytest test_main.py::TestHealth -v

# Run specific test function
pytest test_main.py::TestCreateEmployee::test_create_employee_success -v

# Run with coverage report
pytest test_main.py --cov=. --cov-report=html
```

---

## API Testing Scenarios

### Scenario 1: Complete CRUD Cycle

1. **Create Employee**
   ```bash
   curl -X POST "http://localhost:8000/" \
     -H "Content-Type: application/json" \
     -d '{"name":"scenario1","age":30,"department":"it","salary":100000.0,"position":"developer"}'
   ```

2. **Read Employee**
   ```bash
   curl "http://localhost:8000/home/scenario1"
   ```

3. **Update Employee**
   ```bash
   curl -X PUT "http://localhost:8000/" \
     -H "Content-Type: application/json" \
     -d '{"name":"scenario1","newName":"scenario1_updated"}'
   ```

4. **Verify Update**
   ```bash
   curl "http://localhost:8000/home/scenario1_updated"
   ```

### Scenario 2: Error Handling

1. **Invalid Data Type**
   ```bash
   curl -X POST "http://localhost:8000/" \
     -H "Content-Type: application/json" \
     -d '{"name":"test","age":"not_a_number","department":"it","salary":100000.0,"position":"dev"}'
   # Expected: 422 Unprocessable Entity
   ```

2. **Missing Required Field**
   ```bash
   curl -X POST "http://localhost:8000/" \
     -H "Content-Type: application/json" \
     -d '{"name":"test","age":30}'
   # Expected: 422 Unprocessable Entity
   ```

3. **Search Non-existent Employee**
   ```bash
   curl "http://localhost:8000/home/employee_does_not_exist_xyz"
   # Expected: 200 with error message
   ```

### Scenario 3: Load Testing

```bash
# Install Apache Bench
# Ubuntu/Debian
sudo apt-get install apache2-utils

# macOS
brew install httpd

# Run 100 requests with 10 concurrent connections
ab -n 100 -c 10 http://localhost:8000/health

# Run load test on employee creation
ab -n 50 -c 5 -p employee.json -T application/json http://localhost:8000/
```

With `employee.json`:
```json
{
  "name": "load_test",
  "age": 25,
  "department": "testing",
  "salary": 75000.0,
  "position": "qa"
}
```

### Scenario 4: Performance Testing with Python

```python
import time
import requests
import statistics

BASE_URL = "http://localhost:8000"
NUM_REQUESTS = 100

def test_endpoint_performance(endpoint, method="GET"):
    times = []
    for i in range(NUM_REQUESTS):
        start = time.time()
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        end = time.time()
        times.append((end - start) * 1000)  # Convert to ms
    
    print(f"\n{method} {endpoint}")
    print(f"Requests: {NUM_REQUESTS}")
    print(f"Min: {min(times):.2f}ms")
    print(f"Max: {max(times):.2f}ms")
    print(f"Avg: {statistics.mean(times):.2f}ms")
    print(f"Median: {statistics.median(times):.2f}ms")
    print(f"Std Dev: {statistics.stdev(times):.2f}ms")

# Run performance tests
test_endpoint_performance("/health")
test_endpoint_performance("/")
test_endpoint_performance("/search?skip=0&limit=10")
```

---

## Browser-Based Testing

### Using Swagger UI
1. Navigate to: http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in required parameters
4. Click "Execute"
5. View response, headers, and curl command

### Using ReDoc
1. Navigate to: http://localhost:8000/redoc
2. View detailed API documentation
3. Explore request/response schemas

---

## Continuous Integration Testing

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest test_main.py -v --tb=short
```

---

## Testing Checklist

- [ ] Health check endpoint returns 200
- [ ] Can create employee with valid data
- [ ] Cannot create employee with missing required fields
- [ ] Cannot create employee with invalid data types
- [ ] Can retrieve all employees
- [ ] Can search employees by name
- [ ] Can update employee name
- [ ] Cannot update non-existent employee
- [ ] Can retrieve employee by path parameter
- [ ] Pagination works correctly
- [ ] Error responses have appropriate status codes
- [ ] API documentation is accessible (Swagger/ReDoc)
- [ ] Response format is consistent
- [ ] Concurrent requests handled properly
- [ ] Performance meets requirements

---

## Debugging Tips

### View Application Logs
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/")
async def get_all():
    logger.debug("Fetching all employees")
    return data
```

### Check JSON File
```bash
cat asset/data.json | python -m json.tool  # Pretty print JSON
```

### Use FastAPI Debugger
```python
import pdb

@app.get("/")
async def get_all():
    pdb.set_trace()  # Breakpoint
    return data
```

---

**Last Updated**: 2024
**Version**: 1.0.0
