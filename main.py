from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces.api import router

app = FastAPI(
    title="Clinica-Router AI",
    description="Medical intelligent router MVP",
    version="1.1.0"
)

# Enable CORS for external agent discovery
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
