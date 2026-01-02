from fastapi import APIRouter
from api.v1.endpoints import add_question, ask_agent
from source.archive import ask

router = APIRouter()
router.include_router(add_question.router, prefix="/add_question", tags=["add_question"])
router.include_router(ask.router, prefix="/ask", tags=["ask"])
router.include_router(ask_agent.router, prefix="/ask_agent", tags=["ask_agent"])