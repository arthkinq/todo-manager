# TODO Manager API Documentation

This document describes all available endpoints, required authentication methods, request payloads, and responses for the TODO Manager API.

## Base URL
All API endpoints are prefixed with the base URL of the server (e.g., `http://127.0.0.1:8000`).

## Authentication
Most endpoints require an `Authorization` header using the Bearer scheme with a valid JWT access token.
**Format:** `Authorization: Bearer <your_access_token>`

---

## 1. Authentication Endpoints (`/auth`)

### 1.1. Register User
Creates a new user account.

- **URL:** `/auth/register`
- **Method:** `POST`
- **Auth Required:** No
- **Request Body (JSON):**
  ```json
  {
    "email": "user@example.com",
    "password": "your_secure_password"
  }
  ```
- **Success Response:**
  - **Code:** `201 Created`
  - **Content:**
    ```json
    {
      "email": "user@example.com",
      "id": 1,
      "is_active": true
    }
    ```

### 1.2. Login
Authenticates a user and returns JWT tokens (Access and Refresh).
*Note: This endpoint expects form data, not JSON, as required by the OAuth2 specification.*

- **URL:** `/auth/login`
- **Method:** `POST`
- **Auth Required:** No
- **Content-Type:** `application/x-www-form-urlencoded`
- **Request Body (Form Data):**
  - `username`: "user@example.com"
  - `password`: "your_secure_password"
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1...",
      "refresh_token": "a1b2c3d4e5f6...",
      "token_type": "bearer"
    }
    ```

### 1.3. Refresh Token
Exchanges a valid Refresh token for a new Access and Refresh token pair (Token Rotation).

- **URL:** `/auth/refresh`
- **Method:** `POST`
- **Auth Required:** No
- **Request Body (JSON):**
  ```json
  {
    "refresh_token": "a1b2c3d4e5f6..."
  }
  ```
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1...",
      "refresh_token": "new_random_token...",
      "token_type": "bearer"
    }
    ```

### 1.4. Logout
Revokes the user's current Refresh token, preventing further token renewals.

- **URL:** `/auth/logout`
- **Method:** `POST`
- **Auth Required:** Yes
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**
    ```json
    {
      "detail": "Успешный выход из системы"
    }
    ```

---

## 2. Tasks Endpoints (`/tasks`)
*All task endpoints enforce data isolation. Users can only interact with tasks they own.*

### 2.1. Create Task
Creates a new task for the authenticated user.

- **URL:** `/tasks`
- **Method:** `POST`
- **Auth Required:** Yes
- **Request Body (JSON):**
  ```json
  {
    "title": "Buy groceries",
    "description": "Milk, Eggs, Bread",
    "completed": false
  }
  ```
  *(Note: `description` and `completed` are optional)*
- **Success Response:**
  - **Code:** `201 Created`
  - **Content:**
    ```json
    {
      "title": "Buy groceries",
      "description": "Milk, Eggs, Bread",
      "completed": false,
      "id": 1,
      "owner_id": 1
    }
    ```

### 2.2. Get All Tasks
Retrieves a list of tasks belonging to the authenticated user.

- **URL:** `/tasks`
- **Method:** `GET`
- **Auth Required:** Yes
- **URL Parameters (Optional):**
  - `skip` (integer): Number of records to skip (default: 0)
  - `limit` (integer): Maximum number of records to return (default: 100)
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**
    ```json
    [
      {
        "title": "Buy groceries",
        "description": "Milk, Eggs, Bread",
        "completed": false,
        "id": 1,
        "owner_id": 1
      }
    ]
    ```

### 2.3. Get Task by ID
Retrieves a specific task by its ID.

- **URL:** `/tasks/{task_id}`
- **Method:** `GET`
- **Auth Required:** Yes
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**
    ```json
    {
      "title": "Buy groceries",
      "description": "Milk, Eggs, Bread",
      "completed": false,
      "id": 1,
      "owner_id": 1
    }
    ```
- **Error Response:** `404 Not Found` or `403 Forbidden`

### 2.4. Update Task
Updates specific fields of an existing task.

- **URL:** `/tasks/{task_id}`
- **Method:** `PUT`
- **Auth Required:** Yes
- **Request Body (JSON):**
  ```json
  {
    "completed": true
  }
  ```
  *(Note: Send only the fields you wish to update. All fields are optional.)*
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**
    ```json
    {
      "title": "Buy groceries",
      "description": "Milk, Eggs, Bread",
      "completed": true,
      "id": 1,
      "owner_id": 1
    }
    ```

### 2.5. Delete Task
Deletes a specific task.

- **URL:** `/tasks/{task_id}`
- **Method:** `DELETE`
- **Auth Required:** Yes
- **Success Response:**
  - **Code:** `204 No Content` (Returns nothing)
