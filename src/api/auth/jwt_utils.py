"""
Minimal JWT verification utilities for FastAPI-Django integration.
"""
import os
import jwt
from datetime import datetime
from fastapi import HTTPException, status
from typing import Dict, Any


def get_jwt_secret() -> str:
    """Get JWT secret key from environment."""
    secret = os.getenv('JWT_SECRET_KEY')
    if not secret:
        raise ValueError("JWT_SECRET_KEY environment variable not set")
    return secret


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate JWT token issued by Django.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid, expired, or malformed
    """
    try:
        # Decode token with HS256 algorithm and clock skew tolerance
        payload = jwt.decode(
            token,
            get_jwt_secret(),
            algorithms=["HS256"],
            leeway=30  # 30 seconds clock skew tolerance
        )
        
        # Validate token type (must be 'access')
        token_type = payload.get('token_type')
        if token_type != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Validate expiration (PyJWT handles this automatically, but we double-check)
        exp = payload.get('exp')
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
            
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed"
        )