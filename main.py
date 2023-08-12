from fastapi import FastAPI, HTTPException, Response
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import DatabaseURL, Database
from datetime import datetime
import uvicorn

app = FastAPI()

DATABASE_URL = "postgresql://olrecsen:GSwLUKvuXIGNywMj6MSaEyiwY5ZqGDAY@mel.db.elephantsql.com/olrecsen"
database_url = DatabaseURL(DATABASE_URL)

database = Database(database_url)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(bind=engine)

class DateRecord(Base):  # Modelo tabla dates
    __tablename__ = "dates"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all()

@app.on_event("startup")
async def startup_db():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db():
    await database.disconnect()

# Endpoints
@app.post("/store")
async def store_date():
    async with database.transaction():
        record = DateRecord(date=datetime.utcnow())  # Create a record with the current datetime
        await database.execute(query=DateRecord.__table__.insert().values(date=record.date))
    return Response(status_code=200, detail="Date stored successfully")  # RESTful response

@app.get("/date")
async def get_date():
    async with database.transaction():
        record = await database.fetch_one(query=DateRecord.__table__.select().order_by(DateRecord.id.desc()))
    if record:
        return {"date": record['date']}  # JSON with the info
    else:
        raise HTTPException(status_code=404, detail="No date stored")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
