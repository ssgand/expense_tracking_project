# Expense Tracker Application

## Project Overview

The Expense Tracker Application is a backend-focused Django project designed to help users record, categorize, and analyze their personal expenses. The application provides a structured data model that supports expense entry, categorization, budgeting, and future reporting features such as weekly, monthly, and yearly summaries.

At this stage, the project focuses on **database design and domain modeling**, establishing a solid foundation for future API development, authentication, and frontend integration.

---

## Project Objectives

* Allow users to record and manage personal expenses
* Classify expenses using predefined and user-defined categories
* Support budget tracking and financial summaries over time
* Provide a scalable backend suitable for REST API exposure

---

## Technology Stack

* **Backend Framework:** Django
* **Language:** Python
* **Database:** Django ORM
* **Project Type:** Backend / API-first architecture

---

## Project Structure (Current)

```
expense_tracking_project/
│
├── expense_tracking_app/
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   └── __init__.py
│
├── expense_tracking_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
└── README.md
```

---

## Data Models Implemented

The project currently includes a comprehensive and well-normalized domain model that covers users, categories, expenses, recurring expenses, and budgets. Abstract base models are used to reduce duplication and enforce consistency.

### Abstract Base Models

#### TimestampedModel (Abstract)

* Provides `created_at` and `updated_at` fields
* Automatically tracks record creation and modification times
* Inherited by all core domain models to ensure auditability

#### UserCategoryRelationship (Abstract)

* Defines a reusable relationship between a user and a category
* Enforces ownership and categorization across multiple models
* Used by expenses, recurring expenses, and budgets

### CustomUser Model

* Custom authentication model extending `AbstractBaseUser` and `PermissionsMixin`
* Uses **email as the primary login identifier** (`USERNAME_FIELD = 'email'`)
* Fields:

  * `username`
  * `email` (unique)
  * `preferred_currency` (ISO 4217, 3 characters)
  * `is_staff`, `is_active`
* Includes a custom user manager for controlled user and superuser creation
* Designed to support multi-currency expense tracking

### Category Model

* Stores expense categories (e.g., Food, Transport, Rent)
* Fields:

  * `name`
  * `description`
* Timestamped for auditing and reporting purposes

### Expense Model

* Represents one-time expense entries
* Inherits user–category ownership via `UserCategoryRelationship`
* Fields:

  * `amount`
  * `currency`
  * `description`
  * `expense_date`
* Supports precise financial values using `DecimalField`

### RecurringExpense Model

* Represents repeating expenses such as rent or subscriptions
* Inherits user–category ownership
* Fields:

  * `amount`
  * `currency`
  * `description`
  * `next_pay_date`
  * `frequency` (Daily, Weekly, Monthly, Yearly)
* Designed to support automated expense generation in future phases

### Budget Model

* Represents spending limits over a defined time period
* Inherits user–category ownership
* Fields:

  * `amount`
  * `currency`
  * `start_date`
  * `end_date`
* Enables budget tracking and overspending detection

---

## Key Design Decisions

* **Model-first approach:** Ensures data integrity and scalability before building APIs or UI
* **Normalized schema:** Reduces redundancy and improves reporting accuracy
* **Extensibility:** Models are designed to support future features without major refactoring

---

## Current Progress Summary

**Completed:**

* Django project initialization
* Creation of dedicated `expense_tracking_app`
* Full implementation of core data models
* Initial migrations generated
* Models structured for future REST API integration

**Not Yet Started:**

* User authentication endpoints
* CRUD APIs for expenses and categories
* Budget logic and validations
* Reporting and summaries
* Frontend or mobile integration

---

## How to Run the Project (Current State)

```bash
# Install dependencies
pip install django

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver
```

---

## Project Status

**Status:** In Progress

**Current Phase:** Backend modeling and database design

---

## Author

**Name:** Steve Gandhi Sekamondo

**Project:** Expense Tracker App
