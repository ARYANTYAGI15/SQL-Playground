from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

@router.post("/query")
def run_query(payload:dict,db:Session = Depends(get_db)):
    sql = payload.get("sql")
    if not sql:
        raise HTTPException(status_code=400,detail = "Sql Query is Required")
    try:
        result = db.execute(text(sql))
        rows = [dict(row) for row in result.mappings()]
        return {"result":rows}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))