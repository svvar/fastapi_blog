# FastAPI Application

## Overview

This project is a FastAPI application with features for managing users, posts, and comments. It includes authentication, CRUD operations, AI moderation, auto-replies and tests for endpoints.

## **Important Note**

<h2 style="color:red;"><b>Gemini AI which is used in project doesn't work in Ukraine. Use VPN if you're in Ukraine</h2>

## Features

- User Registration and Login
- Create, Read, Update, Delete (CRUD) for Posts and Comments
- JWT-based Authentication
- AI Moderation for Posts and Comments
- Auto-Reply for Comments
- Automated Tests for Endpoints

---

## Installation and run

### Prerequisites

- Python 3.10 (developed with this)
- Virtual Environment

---

### Step 1: Clone the Repository

```sh
git clone https://github.com/svvar/fastapi_blog.git
cd fastapi_blog
```

### Step 2: Set Up the Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Requirements

```sh
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory and add the following environment variables
```md
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key_here
```

### Step 5: Run the Application

```sh
fastapi run app/main.py
```
---

### The application will be available at http://127.0.0.1:8000
### Try the API using the Swagger UI at http://127.0.0.1:8000/docs

---

## Running Tests

```sh
pytest
```
Test will run and show the results in the terminal.

