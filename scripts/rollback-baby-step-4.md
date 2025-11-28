# Rollback Instructions for Baby-step 4

If you need to rollback the endpoint protection changes, apply these patches:

## File: src/api/endpoints/routes.py

### Revert /ask endpoint protection:
```python
# Change FROM:
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

# Change TO:
@router.post("/ask")
async def ask_question(question: Question):
    try:
        return ask.ask(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Revert /static/graficos endpoint protection:
```python
# Change FROM:
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

# Change TO:
@router.get("/static/graficos/{filename}")
def serve_grafico(filename: str):
    path = os.path.join("src/api/static/graficos", filename)
    if os.path.exists(path):
        return FileResponse(path)
    else:
        raise HTTPException(status_code=404, detail="Gráfico não encontrado")
```

## Commands to rollback:
1. Apply the above changes to `src/api/endpoints/routes.py`
2. Restart FastAPI: `docker-compose restart back-end`
3. Test that endpoints work without authentication