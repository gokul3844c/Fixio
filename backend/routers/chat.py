from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db
from backend.models import ChatHistory, User
from backend.schemas import ChatMessage, ChatResponse
from backend.ai_engine import FixioAIEngine
from backend.auth_utils import get_current_user

router = APIRouter(prefix="/api/chat", tags=["AI Assistant"])

@router.post("", response_model=ChatResponse)
def ask_assistant(
    payload: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id

    # Save User message
    user_msg = ChatHistory(
        user_id=user_id,
        session_id=payload.session_id,
        sender="user",
        message=payload.message
    )
    db.add(user_msg)
    db.commit()

    # Generate AI response
    ai_result = FixioAIEngine.answer_assistant_query(payload.message)

    # Save AI message
    ai_msg = ChatHistory(
        user_id=user_id,
        session_id=payload.session_id,
        sender="ai",
        message=ai_result["reply"]
    )
    db.add(ai_msg)
    db.commit()

    return ChatResponse(
        session_id=payload.session_id,
        reply=ai_result["reply"],
        suggested_actions=ai_result.get("suggested_actions"),
        timestamp=datetime.utcnow()
    )

@router.get("/history/{session_id}")
def get_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(ChatHistory).filter(
        ChatHistory.session_id == session_id,
        ChatHistory.user_id == current_user.id
    ).order_by(ChatHistory.timestamp.asc()).all()
    return history
