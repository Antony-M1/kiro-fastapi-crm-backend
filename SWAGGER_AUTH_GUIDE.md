# How to Use Authentication in Swagger UI

## Step-by-Step Guide

### 1. Create a User
First, create a user account:
- Go to `POST /admin/init-admin` (for first admin user)
- Or use `POST /users/` (for regular signup)
- Example request body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123",
  "role": "Administrator"
}
```

### 2. Login
- Go to `POST /auth/login`
- Click "Try it out"
- Enter your credentials:
```json
{
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```
- Click "Execute"
- Copy the `access_token` from the response (the long string)

### 3. Authorize in Swagger
- Look for the **Authorize** button (🔓 lock icon) at the top right of the Swagger page
- Click it
- In the "Value" field, enter: `Bearer <paste_your_access_token_here>`
- **Important**: Include the word "Bearer" followed by a space, then your token
- Example:
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzAxNTI4MDAwLCJ0eXBlIjoiYWNjZXNzIiwic2Vzc2lvbl9pZCI6MX0.abc123xyz
```
- Click **Authorize**
- Click **Close**

### 4. Use Protected Endpoints
Now you can use any protected endpoint:
- `GET /users/` - List all users
- `POST /leads/` - Create a lead
- `GET /customers/` - List customers
- etc.

The authorization header will be automatically included in all requests.

### 5. Logout
When you're done:
- Go to `POST /auth/logout`
- Click "Try it out" and "Execute"
- This will invalidate your tokens
- Click the **Authorize** button again and click **Logout** to clear it from Swagger

## Token Format

### Correct Format:
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Wrong Formats (Don't use these):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...           ❌ Missing "Bearer"
bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...     ❌ Lowercase "bearer"
Bearer: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...    ❌ Colon after Bearer
"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."   ❌ Quotes around it
```

## Token Expiry

- **Access Token**: Expires in 24 hours
- **Refresh Token**: Expires in 60 days

When your access token expires:
1. Use `POST /auth/refresh` with your refresh_token
2. Get a new access_token
3. Update the authorization in Swagger with the new token

## Troubleshooting

### "Not authenticated" error
- Make sure you clicked the Authorize button
- Check that you included "Bearer " before the token
- Verify your token hasn't expired

### "Session has been revoked" error
- You logged out or the session was invalidated
- Login again to get new tokens

### "Invalid authentication credentials" error
- Your token is malformed or expired
- Login again to get a fresh token
