from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain.chains import create_sql_query_chain
from app.utils import get_sql_database, get_llm

router = APIRouter()

# Request body schema
class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        # Get DB and LLM
        db = get_sql_database()
        llm = get_llm()

        # Create chain
        chain = create_sql_query_chain(llm, db)

        # Run the chain (generate SQL + execute)
        result = chain.invoke({"question": request.question})

        # Extract the SQL query (debug logging)
        sql_query = result.get("intermediate_steps", "SQL not available")

        return {
            "question": request.question,
            "sql": sql_query,
            "answer": result.get("result", result)
        }

    except Exception as e:
        error_msg = str(e)

        # Handle DB connection errors
        if "psycopg2" in error_msg or "sqlalchemy" in error_msg:
            raise HTTPException(status_code=500, detail="Database connection failed. Check DB settings.")

        # Handle Hugging Face / model errors
        if "403" in error_msg or "gated repo" in error_msg:
            raise HTTPException(status_code=403, detail="Model access denied. Request access on Hugging Face.")

        if "timeout" in error_msg.lower():
            raise HTTPException(status_code=504, detail="Model request timed out. Please try again later.")

        # Generic fallback
        raise HTTPException(status_code=500, detail=f"Unexpected error: {error_msg}")
