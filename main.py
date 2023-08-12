from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn

app = FastAPI()

@app.get("/date")
async def get_date():
    now = datetime.now()
    if now:
        return {"date": str(now)}  # JSON with the info
    else:
        raise HTTPException(status_code=404, detail="No date stored")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
