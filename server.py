
from app.main import app
import uvicorn


@app.get("/")
def read_root():
    return {"Status": "Server is running"}



if __name__ == "__main__":
    uvicorn.run("app.main:app", host='localhost', port=8000, reload=True)