# CRM Application with FastAPI

A complete CRM application built with FastAPI, featuring JWT authentication, user management, and comprehensive CRM modules including Leads, Customers, Contacts, and Opportunities.

## Features

- **JWT Authentication**: Access tokens (24 hours) and refresh tokens (60 days)
- **User Management**: Full CRUD operations with role-based access
- **Lead Management**: Track and manage sales leads
- **Customer Management**: Maintain customer records
- **Contact Management**: Store contact information
- **Opportunity Management**: Track sales opportunities
- **Secure**: All APIs protected with JWT authentication

## Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

3. **Run the application**:
```bash
uvicorn app.main:app --reload
```

4. **Access the API documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/login` - Login and get tokens
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout

### Users
- `POST /users/` - Create user
- `GET /users/` - List users
- `GET /users/{user_id}` - Get user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Leads
- `POST /leads/` - Create lead
- `GET /leads/` - List leads
- `GET /leads/{lead_id}` - Get lead
- `PUT /leads/{lead_id}` - Update lead
- `DELETE /leads/{lead_id}` - Delete lead

### Customers
- `POST /customers/` - Create customer
- `GET /customers/` - List customers
- `GET /customers/{customer_id}` - Get customer
- `PUT /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer

### Contacts
- `POST /contacts/` - Create contact
- `GET /contacts/` - List contacts
- `GET /contacts/{contact_id}` - Get contact
- `PUT /contacts/{contact_id}` - Update contact
- `DELETE /contacts/{contact_id}` - Delete contact

### Opportunities
- `POST /opportunities/` - Create opportunity
- `GET /opportunities/` - List opportunities
- `GET /opportunities/{opportunity_id}` - Get opportunity
- `PUT /opportunities/{opportunity_id}` - Update opportunity
- `DELETE /opportunities/{opportunity_id}` - Delete opportunity

## Database Models

- **User**: User accounts with roles (Administrator, Sales User, Sales Manager)
- **JWT Session**: Token management and tracking
- **Lead**: Sales leads with status tracking
- **Customer**: Customer records with type and territory
- **Contact**: Contact information linked to customers
- **Opportunity**: Sales opportunities with probability tracking
- **Communication**: Activity logs for interactions
- **Task**: Follow-up tasks and reminders
- **Campaign**: Marketing campaigns

## Authentication Flow

1. Login with email/password to receive access and refresh tokens
2. Include access token in Authorization header: `Bearer <token>`
3. When access token expires, use refresh token to get new tokens
4. All API endpoints (except auth) require valid access token

## Token Configuration

- Access Token: 24 hours expiry
- Refresh Token: 60 days expiry
- Algorithm: HS256

# Debugger
`.vscode` file is update to show the how the krio is working in debugging mode