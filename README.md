# Expense Tracker API

A RESTful, API-first backend built with **Django** and **Django REST Framework**, designed for expense tracking, recurring expenses, budgets, and categories using a **custom user model**.

---

## Table of Contents

- Overview
- Tech Stack
- Design Principles
- Authentication
- User Model
- API Endpoints
  - Authentication
  - Profile
  - Categories
  - Budgets
  - Recurring Expenses
- Validation Rules
- Security & Ownership Rules
- Planned Features
- Project Status

---

## Overview

This API allows users to:

- Sign up and authenticate using email
- Manage their profile
- Create and manage budgets
- Track recurring expenses
- Organize expenses using categories

The application is **API-only** and intended to be consumed by mobile or web clients.

---

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL (recommended)
- JWT or Token Authentication

---

## Design Principles

- API-only (no server-rendered pages)
- Custom user model (email-based authentication)
- Explicit ownership enforcement
- No hard deletion of user data
- Secure password handling via Django
- Clear separation of concerns (models, serializers, views)

---

## Authentication

### Authentication Method

- Email + Password
- JWT-based authentication (recommended)

```
USERNAME_FIELD = email
```

---

## User Model

### Fields

| Field | Type |
|-----|-----|
| username | string |
| email | string (unique) |
| preferred_currency | string (ISO 4217) |
| is_active | boolean |
| is_staff | boolean |
| created_at | datetime |
| updated_at | datetime |

Passwords are **never stored in plain text** and are hashed using Django’s built-in password hashing framework.

---

## API Endpoints

All endpoints require authentication unless stated otherwise.

---

## Authentication Endpoints

### Signup

**POST** `/api/signup/`

#### Request
```json
{
  "username": "steve",
  "email": "steve@example.com",
  "preferred_currency": "USD",
  "password": "StrongPassword123"
}
```

#### Response
```json
{
  "id": 1,
  "email": "steve@example.com",
  "preferred_currency": "USD"
}
```

---

### Login

**POST** `/api/login/`

#### Request
```json
{
  "email": "steve@example.com",
  "password": "StrongPassword123"
}
```

#### Response
```json
{
  "access": "jwt-access-token",
  "refresh": "jwt-refresh-token"
}
```

---

### Logout

**POST** `/api/logout/`

Invalidates the refresh token.

---

## Profile

### Get Profile

**GET** `/api/profile/`

#### Response
```json
{
  "username": "steve",
  "email": "steve@example.com",
  "preferred_currency": "USD",
  "created_at": "2026-01-01T10:00:00Z"
}
```

---

### Update Profile

**PATCH** `/api/profile/`

#### Request
```json
{
  "username": "steve_g",
  "preferred_currency": "EUR"
}
```

#### Response
```json
{
  "username": "steve_g",
  "preferred_currency": "EUR"
}
```

---

## Password Management

### Change Password

**POST** `/api/change-password/`

#### Request
```json
{
  "current_password": "StrongPassword123",
  "new_password": "NewStrongerPassword456"
}
```

#### Response
```json
{
  "detail": "Password updated successfully"
}
```

---

## Categories

Categories are **global reference data** and are not user-owned.

---

### Create Category

**POST** `/api/categories/`

#### Request
```json
{
  "name": "Food",
  "description": "Food and groceries"
}
```

#### Response
```json
{
  "id": 1,
  "name": "Food",
  "description": "Food and groceries"
}
```

---

### List Categories

**GET** `/api/categories/`

#### Response
```json
[
  {
    "id": 1,
    "name": "Food",
    "description": "Food and groceries"
  }
]
```

---

## Budgets

Budgets are **user-owned** and linked to categories.

---

### Create Budget

**POST** `/api/budgets/`

#### Request
```json
{
  "category": 1,
  "amount": 500.00,
  "currency": "USD",
  "start_date": "2026-01-01",
  "end_date": "2026-01-31"
}
```

#### Response
```json
{
  "id": 1,
  "category": 1,
  "amount": "500.000",
  "currency": "USD",
  "start_date": "2026-01-01",
  "end_date": "2026-01-31"
}
```

---

## Recurring Expenses

Recurring expenses are **user-owned**, category-based, and scheduled.

---

### Frequency Enum

```
DAILY
WEEKLY
MONTHLY
YEARLY
```

---

### Create Recurring Expense

**POST** `/api/recurring-expenses/`

#### Request
```json
{
  "category": 1,
  "amount": 50.00,
  "currency": "USD",
  "description": "Internet subscription",
  "next_pay_date": "2026-02-01",
  "frequency": "MONTHLY"
}
```

#### Response
```json
{
  "id": 1,
  "category": 1,
  "amount": "50.000",
  "currency": "USD",
  "description": "Internet subscription",
  "next_pay_date": "2026-02-01",
  "frequency": "MONTHLY"
}
```

---

## Validation Rules

- `amount` must be greater than 0
- `start_date` must be before `end_date`
- `next_pay_date` cannot be in the past
- `frequency` must be a valid enum value

---

## Security & Ownership Rules

- Users can only access their own budgets and recurring expenses
- `user` field is never writable via the API
- All endpoints require authentication
- Passwords are hashed and never returned in responses

---

## Planned Features (Not Implemented Yet)

### Email Change with Verification
- Two-step email update
- Token-based verification
- Expiration handling

### Soft Delete (Account Deactivation)
- Users can deactivate accounts
- No physical deletion of user data
- Records remain for audit and recovery

---

## Project Status

**Current version:** Core API complete  
**Next version:** Account lifecycle management

---

## Notes

This project is structured for long-term maintainability, security correctness, and future expansion.
