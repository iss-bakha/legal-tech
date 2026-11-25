from fastapi import APIRouter

from app.db import SessionDep
from app.schemas import ChatRequest, ChatResponse
from app.services.answer import answer_question

router = APIRouter(prefix="/chat", tags=["ядро: ИИ-юрист"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, session: SessionDep) -> ChatResponse:
    return await answer_question(session, req.question)
