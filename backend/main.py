import os
import base64
import shutil
from datetime import timedelta
from typing import Optional, List
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

import models
import auth
import chat as chat_module
from database import engine, get_db

load_dotenv()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="ElectroBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ─── Pydantic Schemas ────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    image_path: Optional[str] = None
    circuit_svg: Optional[str] = None
    generated_image: Optional[str] = None  # Persisted animated circuit
    created_at: str

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


# ─── Auth Routes ─────────────────────────────────────────────────────────────

@app.post("/api/auth/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if auth.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if auth.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth.get_password_hash(user_data.password)
    user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.create_access_token(data={"sub": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }


@app.get("/api/auth/me", response_model=UserResponse)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


# ─── Conversation Routes ──────────────────────────────────────────────────────

@app.get("/api/conversations", response_model=List[ConversationResponse])
def get_conversations(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    convos = (
        db.query(models.Conversation)
        .filter(models.Conversation.user_id == current_user.id)
        .order_by(models.Conversation.updated_at.desc())
        .all()
    )
    return [
        {
            "id": c.id,
            "title": c.title,
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat(),
        }
        for c in convos
    ]


@app.post("/api/conversations", response_model=ConversationResponse, status_code=201)
def create_conversation(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    convo = models.Conversation(user_id=current_user.id, title="New Conversation")
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return {
        "id": convo.id,
        "title": convo.title,
        "created_at": convo.created_at.isoformat(),
        "updated_at": convo.updated_at.isoformat(),
    }


@app.delete("/api/conversations/{conversation_id}", status_code=204)
def delete_conversation(
    conversation_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    convo = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(convo)
    db.commit()


@app.get("/api/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(
    conversation_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    convo = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .order_by(models.Message.created_at.asc())
        .all()
    )
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "image_path": m.image_path,
            "circuit_svg": m.circuit_svg,
            "generated_image": m.generated_image,  # Return persisted animated circuit
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]


# ─── Chat Route ───────────────────────────────────────────────────────────────

@app.post("/api/chat")
async def send_message(
    message: str = Form(...),
    conversation_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Get or create conversation
    if conversation_id:
        convo = db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == current_user.id
        ).first()
        if not convo:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        convo = models.Conversation(
            user_id=current_user.id,
            title=chat_module.generate_conversation_title(message)
        )
        db.add(convo)
        db.commit()
        db.refresh(convo)

    # Handle image upload
    image_data_b64 = None
    image_path = None

    if image and image.filename:
        allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        if image.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid image type")

        ext = Path(image.filename).suffix.lower()
        filename = f"{current_user.id}_{convo.id}_{len(convo.messages) + 1}{ext}"
        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        image_path = f"/uploads/{filename}"

        # Read image as base64 for OpenAI
        with open(file_path, "rb") as f:
            image_data_b64 = base64.b64encode(f.read()).decode("utf-8")

    # Load conversation history for context (reduced for token limits)
    history_messages = (
        db.query(models.Message)
        .filter(models.Message.conversation_id == convo.id)
        .order_by(models.Message.created_at.desc())
        .limit(6)  # Last 6 messages (3 exchanges) to stay within token limits
        .all()
    )
    # Reverse to get chronological order
    history_messages.reverse()
    history = [{"role": m.role, "content": m.content[:500]} for m in history_messages]  # Truncate long messages

    # Save user message
    user_msg = models.Message(
        conversation_id=convo.id,
        role="user",
        content=message,
        image_path=image_path
    )
    db.add(user_msg)
    db.commit()

    # Get AI response
    try:
        ai_text, circuit_svg, generated_image = await chat_module.get_ai_response(
            history, message, image_data_b64
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

    # Save assistant message (including generated_image for history)
    assistant_msg = models.Message(
        conversation_id=convo.id,
        role="assistant",
        content=ai_text,
        circuit_svg=circuit_svg,
        generated_image=generated_image  # Persist animated circuit in DB
    )
    db.add(assistant_msg)

    # Update conversation title if it's the first message
    if len(history_messages) == 0:
        convo.title = chat_module.generate_conversation_title(message)

    db.commit()
    db.refresh(assistant_msg)

    return {
        "conversation_id": convo.id,
        "conversation_title": convo.title,
        "message": {
            "id": assistant_msg.id,
            "role": "assistant",
            "content": ai_text,
            "circuit_svg": circuit_svg,
            "generated_image": generated_image,  # Add generated image
            "created_at": assistant_msg.created_at.isoformat(),
        }
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ElectroBot API"}
