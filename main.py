from fastapi import FastAPI, HTTPException, Response
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import DatabaseURL
from datetime import datetime

app = FastAPI()

DATABASE_URL = "postgres://olrecsen:GSwLUKvuXIGNywMj6MSaEyiwY5ZqGDAY@mel.db.elephantsql.com/olrecsen"
database_url = DatabaseURL(DATABASE_URL)

database = Database(database_url)
metadata = database.metadata
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DateRecord(Base):  # Modelo tabla dates
    __tablename__ = "dates"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_db():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db():
    await database.disconnect()

# Endpoints
@app.post("/store")
async def store_date():
    db = SessionLocal()  # Conexion a BBDD
    record = DateRecord()  # Usamos el modelo
    db.add(record)  # Añadimos una fecha (la de ahora)
    db.commit()  # Completamos la transaccion
    db.refresh(record)  # Actualizar la base de datos de acuerdo a la info
    db.close()  # Cerramos conexion
    return Response(status_code=200, detail="Date stored successfully")  # Principio REST

@app.get("/date")
async def get_date():
    db = SessionLocal()  # Conexion a BBDD
    record = db.query(DateRecord).order_by(DateRecord.id.desc()).first()
    db.close()  # Cerrada conexion a BBDD
    if record:
        return {"date": record.date}  # JSON con la info
    else:
        raise HTTPException(status_code=404, detail="No date stored")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)