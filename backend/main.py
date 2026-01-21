from fastapi import FastAPI

app = FastAPI(title="Git Diary")

@app.get("/health")
def health():
    return {"status": "ok"}
