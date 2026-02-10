"""
DEPRECATED: This file contains old custom JWT/bcrypt authentication code.

Task T-221/T-222: Authentication is now handled by Better Auth service.
The frontend uses Better Auth JavaScript client for signup/signin/logout.
The backend validates Better Auth JWTs via get_current_user dependency in deps.py.

This file is kept for reference only. Do NOT use these endpoints.

For authentication, users should:
1. Use Better Auth frontend (signup/signin/logout)
2. Get JWT token from Better Auth
3. Send JWT in Authorization header to all protected endpoints
4. Backend validates token via Depends(get_current_user) which calls verify_better_auth_token()

To remove this file entirely:
- Delete backend/app/api/auth.py
- Remove the auth router registration from backend/app/main.py
- All auth is now frontend-handled via Better Auth client
"""

# This file is intentionally empty/deprecated to mark the migration away from custom auth
