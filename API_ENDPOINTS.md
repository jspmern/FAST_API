# API Endpoints Reference Guide

Quick reference for all available endpoints in the Employee Management System API.

---

## Base URL
```
http://localhost:8000
```

## Standard Response Format
All responses follow this structure:

**Success Response:**
```json
{
  "success": true,
  "message": "Operation description",
  "data": {}
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error description"
}
```

---

## Endpoints Summary

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| GET | `/health` | Health check | ✅ |
| GET | `/` | Get all employees | ✅ |
| POST | `/` | Create employee | ✅ |
| PUT | `/` | Update employee | ✅ |
| GET | `/search` | Search employees | ✅ |
| GET | `/home/{name}` | Get by name | ✅ |

---

## Detailed Endpoint Documentation

### 1. Health Check
Check if API is running

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:8000
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Application is up and running at 8000"
}
```

**Use Cases:**
- Service health monitoring
- Load balancer health probes
- Uptime monitoring

---

### 2. Get All Employees
Retrieve all employees in the system

**Request:**
```http
GET / HTTP/1.1
Host: localhost:8000
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "name": "utsav",
      "age": 30,
      "department": "computer science",
      "salary": 10000000.0,
      "position": "sde1"
    },
    {
      "name": "utsav1",
      "age": 30,
      "department": "computer science",
      "salary": 10000000.0,
      "position": "sde1"
    }
  ]
}
```

**Error Response (500):**
```json
{
  "success": false,
  "message": "Error reading employee data"
}
```

**Query Parameters:** None

**Path Parameters:** None

**Request Headers:**
- None required

**Response Headers:**
- Content-Type: application/json

**Performance:**
- O(n) where n is number of employees
- All employees loaded into memory

---

### 3. Create Employee
Add new employee to the system

**Request:**
```http
POST / HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "name": "john_doe",
  "age": 28,
  "department": "backend",
  "salary": 95000.0,
  "position": "sde2"
}
```

**cURL:**
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

**Python Requests:**
```python
import requests

employee_data = {
    "name": "john_doe",
    "age": 28,
    "department": "backend",
    "salary": 95000.0,
    "position": "sde2"
}

response = requests.post("http://localhost:8000/", json=employee_data)
print(response.json())
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Employee created successfully",
  "data": {
    "name": "john_doe",
    "age": 28,
    "department": "backend",
    "salary": 95000.0,
    "position": "sde2"
  }
}
```

**Error Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "department"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

**Request Body Schema:**
```
{
  "name": string (required)         // Employee name
  "age": integer (required)         // Age value
  "department": string (required)   // Department name
  "salary": float (required)        // Salary amount
  "position": string (required)     // Job position
}
```

**Validation Rules:**
- All fields required (no defaults)
- name: Non-empty string
- age: Valid integer
- department: Non-empty string
- salary: Valid float
- position: Non-empty string

**Status Codes:**
- 200: Employee created successfully
- 400: Bad request
- 422: Validation error
- 500: Server error

---

### 4. Update Employee
Modify employee information (currently name only)

**Request:**
```http
PUT / HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "name": "old_name",
  "newName": "new_name"
}
```

**cURL:**
```bash
curl -X PUT "http://localhost:8000/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "john_doe",
    "newName": "john_smith"
  }'
```

**Python Requests:**
```python
import requests

update_data = {
    "name": "john_doe",
    "newName": "john_smith"
}

response = requests.put("http://localhost:8000/", json=update_data)
print(response.json())
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Employee updated successfully"
}
```

**Error Response - Not Found (200):**
```json
{
  "success": false,
  "message": "Employee not found"
}
```

**Request Body Schema:**
```
{
  "name": string (required)      // Current employee name
  "newName": string (required)   // New employee name
}
```

**Limitation:**
- Currently only supports name updates
- To update other fields, delete and recreate or modify the function

**Status Codes:**
- 200: Success (even if employee not found)
- 400: Bad request
- 422: Validation error
- 500: Server error

---

### 5. Search Employees
Search and filter employees with pagination

**Request:**
```http
GET /search?skip=0&limit=10&name=utsav HTTP/1.1
Host: localhost:8000
```

**cURL Examples:**
```bash
# Get first 10 employees
curl "http://localhost:8000/search?skip=0&limit=10"

# Get next 10 employees
curl "http://localhost:8000/search?skip=10&limit=10"

# Filter by name
curl "http://localhost:8000/search?name=utsav"

# Combined: filter by name and paginate
curl "http://localhost:8000/search?skip=0&limit=20&name=john"
```

**Python Requests:**
```python
import requests

params = {
    "skip": 0,
    "limit": 10,
    "name": "utsav"
}

response = requests.get("http://localhost:8000/search", params=params)
print(response.json())
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "0 10 utsav"
}
```

**Query Parameters:**

| Parameter | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| skip | integer | No | 0 | ≥ 0 | Records to skip (offset) |
| limit | integer | No | 10 | 1-100 | Max records to return |
| name | string | No | null | Any string | Filter by employee name |

**Limitations:**
- Filtering logic not fully implemented
- Returns message, not actual filtered data
- Consider this endpoint for enhancement

**Status Codes:**
- 200: Success
- 400: Bad request
- 500: Server error

---

### 6. Get Employee by Name
Retrieve specific employee by name

**Request:**
```http
GET /home/{name} HTTP/1.1
Host: localhost:8000
```

**cURL Examples:**
```bash
# Get specific employee
curl "http://localhost:8000/home/utsav"

# URL encoding for names with spaces
curl "http://localhost:8000/home/john%20doe"
```

**Python Requests:**
```python
import requests

response = requests.get("http://localhost:8000/home/utsav")
print(response.json())
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "name": "utsav",
    "age": 30,
    "department": "computer science",
    "salary": 10000000.0,
    "position": "sde1"
  }
}
```

**Error Response (200 OK):**
```json
{
  "success": false,
  "message": "Employee not found"
}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Employee name to search |

**Performance:**
- O(n) linear search through all employees
- No indexing on employee names

**Status Codes:**
- 200: Success or not found (always returns 200)
- 500: Server error

---

## Advanced Usage Examples

### Example 1: Bulk Create Employees
```python
import requests

employees = [
    {"name": "alice", "age": 32, "department": "frontend", "salary": 105000.0, "position": "sde3"},
    {"name": "bob", "age": 28, "department": "backend", "salary": 95000.0, "position": "sde2"},
    {"name": "charlie", "age": 25, "department": "devops", "salary": 85000.0, "position": "sde1"},
]

for employee in employees:
    response = requests.post("http://localhost:8000/", json=employee)
    print(f"Created {employee['name']}: {response.json()['success']}")
```

### Example 2: Pagination Loop
```python
import requests

BASE_URL = "http://localhost:8000"
skip = 0
limit = 5
all_employees = []

while True:
    response = requests.get(f"{BASE_URL}/search", params={"skip": skip, "limit": limit})
    data = response.json()
    
    if not data.get('data'):
        break
    
    all_employees.extend(data['data'])
    skip += limit

print(f"Total employees: {len(all_employees)}")
```

### Example 3: Error Handling
```python
import requests
from requests.exceptions import RequestException

def safe_create_employee(employee_data):
    try:
        response = requests.post("http://localhost:8000/", json=employee_data)
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return {"status": "success", "data": result['data']}
            else:
                return {"status": "failed", "message": result['message']}
        elif response.status_code == 422:
            return {"status": "validation_error", "details": response.json()}
        else:
            return {"status": "error", "code": response.status_code}
    
    except RequestException as e:
        return {"status": "connection_error", "message": str(e)}

# Usage
result = safe_create_employee({
    "name": "test",
    "age": 30,
    "department": "it",
    "salary": 100000.0,
    "position": "dev"
})
print(result)
```

---

## HTTP Status Codes

| Code | Name | Meaning |
|------|------|---------|
| 200 | OK | Request successful |
| 201 | Created | Resource created (not currently used) |
| 204 | No Content | Successful but no content to return |
| 400 | Bad Request | Malformed request syntax |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Authentication successful but access denied |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Server temporarily unavailable |

---

## Common Error Scenarios

### Missing Required Field
**Problem:** Missing `department` field in POST request
```json
{
  "name": "john",
  "age": 30,
  "salary": 100000.0,
  "position": "dev"
}
```

**Response (422):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "department"],
      "msg": "Field required"
    }
  ]
}
```

**Solution:** Include all required fields

### Invalid Data Type
**Problem:** Age as string instead of integer
```json
{
  "name": "john",
  "age": "thirty",
  "department": "it",
  "salary": 100000.0,
  "position": "dev"
}
```

**Response (422):**
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["body", "age"],
      "msg": "Input should be a valid integer"
    }
  ]
}
```

**Solution:** Use correct data types

### Employee Not Found
**Problem:** Searching for non-existent employee
```
GET /home/nonexistent_employee
```

**Response (200):**
```json
{
  "success": false,
  "message": "Employee not found"
}
```

**Solution:** Verify employee name exists

---

## Performance Tips

1. **Use Pagination:** Always use `skip` and `limit` for large datasets
2. **Cache Responses:** Implement client-side caching for frequently accessed data
3. **Batch Operations:** Group multiple creates into a single loop
4. **Connection Pooling:** Use connection pools in production clients

---

## Rate Limiting (Future)
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1609459200
```

---

## Authentication (Future)
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/"
```

---

## CORS Headers (If Enabled)
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type
```

---

## Testing This API

### With Postman
1. Import endpoints into Postman collection
2. Set up environment variables
3. Create test scripts for validation
4. Run collection tests

### With cURL
```bash
# Save as test.sh
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "Testing Health Check..."
curl -X GET "$BASE_URL/health"

echo -e "\n\nTesting Get All..."
curl -X GET "$BASE_URL/"

echo -e "\n\nCreating Employee..."
curl -X POST "$BASE_URL/" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","age":30,"department":"it","salary":100000.0,"position":"dev"}'
```

Run with:
```bash
chmod +x test.sh
./test.sh
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024 | Initial release |

---

## Support & Issues

- Check [README.md](README.md) for detailed documentation
- Review [TESTING.md](TESTING.md) for testing guide
- Check Swagger UI at `/docs` for interactive documentation

---

**Last Updated:** 2024
**API Version:** 1.0.0
