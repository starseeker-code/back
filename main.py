from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8081",
    "https://front-back--sparkly-medovik-2a690d.netlify.app"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/date")
async def get_date():
    now = datetime.now()
    if now:
        print(now)
        return {"date": str(now)}  # JSON with the info
    else:
        raise HTTPException(status_code=404, detail="No date stored")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
