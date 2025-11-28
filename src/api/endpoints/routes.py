from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from src.api.models import Question
from src.api.controller.AskController import AskController
from src.api.dependencies.auth_dependency import get_current_user, User
import os

router = APIRouter()

ask = AskController()

# Authentication test endpoints
@router.get("/auth/ping")
async def auth_ping():
    """Public endpoint to test auth module is loaded."""
    return {"status": "ok", "message": "Auth module loaded"}


@router.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Protected endpoint that returns current user info from JWT token."""
    return {
        "status": "authenticated",
        "user": current_user.to_dict()
    }


@router.post("/ask")
async def ask_question(question: Question, current_user: User = Depends(get_current_user)):
    """
    Protected endpoint: Ask AI questions about GitHub data.
    Requires valid JWT authentication.
    """
    try:
        # Log the authenticated request (optional)
        print(f"User {current_user.username} (ID: {current_user.user_id}) asked: {question.question[:50]}...")
        
        # Call the existing ask controller
        result = ask.ask(question)
        
        # Add user context to response (optional)
        if isinstance(result, dict):
            result["user_context"] = {
                "user_id": current_user.user_id,
                "username": current_user.username
            }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Protected endpoint para servir arquivos de gráficos
@router.get("/static/graficos/{filename}")
def serve_grafico(filename: str, current_user: User = Depends(get_current_user)):
    """
    Protected endpoint: Serve chart/graph files.
    Requires valid JWT authentication for data access control.
    """
    # Log file access for audit trail
    print(f"User {current_user.username} (ID: {current_user.user_id}) accessing file: {filename}")
    
    path = os.path.join("src/api/static/graficos", filename)
    if os.path.exists(path):
        return FileResponse(path)
    else:
        raise HTTPException(status_code=404, detail="Gráfico não encontrado")