"""
Authentication dependency for FastAPI endpoints.
"""
import os
from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.api.auth.jwt_utils import decode_token

# OAuth2 scheme for extracting Bearer tokens
security = HTTPBearer()

# Toggle for calling Django profile endpoint (OFF by default for baby-step)
FETCH_DJANGO_PROFILE = os.getenv('FETCH_DJANGO_PROFILE', 'false').lower() == 'true'


class User:
    """Simple user dataclass for authenticated user info."""
    
    def __init__(self, user_id: int, username: str, email: str = None):
        self.user_id = user_id
        self.username = username
        self.email = email
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email
        }


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Extract and validate JWT token, return current user info.
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        
    Returns:
        User object with basic user information
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        # Extract token from Bearer scheme
        token = credentials.credentials
        
        # Decode and validate token
        payload = decode_token(token)
        
        # Extract user info from token payload
        user_id = payload.get('user_id')
        username = payload.get('username')
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        
        # Create user object with minimal info from token
        user = User(
            user_id=user_id,
            username=username or f"user_{user_id}",
            email=payload.get('email')
        )
        
        # Optional: Fetch full profile from Django (disabled by default)
        if FETCH_DJANGO_PROFILE:
            # TODO: Implement in Baby-step 3
            pass
        
        return user
        
    except HTTPException:
        # Re-raise HTTP exceptions from jwt_utils
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


# Optional dependency for endpoints that can work with or without auth
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[User]:
    """
    Optional authentication dependency.
    Returns User if valid token provided, None otherwise.
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None