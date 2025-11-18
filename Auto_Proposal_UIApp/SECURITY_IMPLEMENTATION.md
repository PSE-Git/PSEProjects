# Security Implementation - Auto Proposal UI App

## Overview
This document describes the authentication and authorization security features implemented in the Auto Proposal UI application.

## Authentication System

### Flask-Login Integration
- **Package**: Flask-Login 0.6.3
- **Purpose**: Session-based authentication and user management
- **Login View**: `/login` route
- **Session Management**: Secure server-side sessions with secret key

### User Class
```python
class User(UserMixin):
    - Implements Flask-Login UserMixin interface
    - Stores user data from backend API authentication
    - Fields: email, full_name, designation, phone, role, company_id, token, etc.
```

### User Loader
```python
@login_manager.user_loader
def load_user(user_id):
    - Loads user from session data
    - Returns User object if valid session exists
    - Returns None if session is invalid/expired
```

## Protected Routes

### All routes requiring authentication (14 routes):
1. **`/proposals`** - List/create proposals (index)
2. **`/proposals/view/<id>`** - View specific proposal
3. **`/proposals/edit/<id>`** - Edit proposal
4. **`/proposals/<id>/check-pdf`** - Check PDF existence
5. **`/proposals/<id>/generate-pdf`** - Generate PDF
6. **`/proposals/<id>/send-email`** - Send proposal via email
7. **`/proposals/new`** - Create new proposal
8. **`/users`** - Users/proposals list
9. **`/profile`** - User profile management
10. **`/logout`** - Logout (requires authentication to logout)
11. **`/boq`** - BOQ items management
12. **`/boq/edit/<id>`** - Edit BOQ item
13. **`/boq/delete/<id>`** - Delete BOQ item
14. **`/boq/bulk-delete`** - Bulk delete BOQ items

### Public Routes (no authentication required):
1. **`/`** - Root redirect (redirects to login if not authenticated, profile if authenticated)
2. **`/login`** - Login page (redirects to profile if already authenticated)
3. **`/uploads/<filename>`** - Serve uploaded files (PDFs, etc.)
4. **`/image/<filename>`** - Serve image files (logos, etc.)

## Authentication Flow

### Login Process
1. User submits email and password via `/login` POST
2. Credentials sent to backend API: `POST /api/auth/login`
3. Backend validates credentials and returns user data + token
4. User data stored in session
5. Flask-Login `login_user()` called with User object
6. User redirected to profile page or original requested page

### Session Management
- Session data stored server-side with secure cookie
- User object loaded on each request via `@login_manager.user_loader`
- Current user accessible via `current_user` in templates and routes

### Logout Process
1. User clicks logout
2. `logout_user()` clears Flask-Login session
3. `session.pop('user')` removes user data from session
4. User redirected to login page

## Security Features

### Route Protection
- **@login_required decorator**: All protected routes use this decorator
- **Automatic redirect**: Unauthenticated users redirected to `/login`
- **Flash messages**: User-friendly messages shown: "Please log in to access this page."
- **Next parameter**: After login, users redirected to originally requested page

### URL Access Prevention
Even with direct URL access attempts:
- `/proposals/new` → Redirects to login if not authenticated
- `/proposals/view/123` → Redirects to login if not authenticated
- `/proposals/edit/123` → Redirects to login if not authenticated
- `/boq` → Redirects to login if not authenticated
- `/profile` → Redirects to login if not authenticated
- `/users` → Redirects to login if not authenticated

### Session Security
- Secret key used for session encryption
- Session data stored server-side only
- No sensitive data in cookies
- Session expires on browser close (can be configured)

## Backend API Integration

### Authentication Endpoint
```
POST http://localhost:8000/api/auth/login
Body: {
  "company_name": "string",
  "email": "string",
  "password": "string"
}
Response: {
  "user": { ...user_data... },
  "token": "jwt_token"
}
```

### API Error Handling
- Connection errors: User-friendly error message shown
- Invalid credentials: Error message from API displayed
- Session preserved across requests for API calls

## Configuration

### Environment Variables
- `FLASK_SECRET`: Secret key for session encryption (default: 'dev-secret' for development)
- `BACKEND_API_BASE`: Backend API URL (default: 'http://localhost:8000')

### Login Manager Settings
```python
login_manager.login_view = 'login'  # Route name for login page
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'  # Flash message category
```

## Testing Authentication

### Test Unauthenticated Access
1. Clear browser cookies/session
2. Try to access: `http://127.0.0.1:5000/proposals/new`
3. Expected: Redirect to `/login` with message "Please log in to access this page."

### Test Valid Login
1. Navigate to `http://127.0.0.1:5000/login`
2. Enter valid credentials from backend database
3. Expected: Redirect to `/profile` with welcome message

### Test Invalid Login
1. Navigate to `http://127.0.0.1:5000/login`
2. Enter invalid credentials
3. Expected: Stay on login page with error message

### Test Protected Routes
1. Login with valid credentials
2. Access any protected route (e.g., `/proposals/new`)
3. Expected: Page loads successfully

### Test Logout
1. While logged in, access `/logout`
2. Expected: Redirect to `/login` with "Logged out successfully" message
3. Try accessing protected route
4. Expected: Redirect to `/login`

## Security Best Practices Implemented

✅ All sensitive routes protected with `@login_required`
✅ Session-based authentication with secure cookies
✅ Backend API integration for credential validation
✅ No password storage in frontend application
✅ Automatic redirect for unauthenticated access attempts
✅ User-friendly error messages (no sensitive info leaked)
✅ Logout functionality to clear sessions
✅ Session data validated on each request
✅ Prevention of direct URL access without authentication

## Future Enhancements (Optional)

- [ ] Remember Me functionality
- [ ] Session timeout configuration
- [ ] Password reset flow
- [ ] Two-factor authentication
- [ ] Role-based access control (RBAC) for different user types
- [ ] Audit logging for authentication events
- [ ] Rate limiting for login attempts
- [ ] CSRF protection for forms
- [ ] HTTPS enforcement in production
