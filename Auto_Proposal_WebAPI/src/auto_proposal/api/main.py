from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

from .routes import clients, proposals, users, companies, auth, boq_items, proposal_items

app = FastAPI(
    title="Auto Proposal API",
    description="API for generating and managing business proposals, users, and companies",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for PDF access
os.makedirs("pdf_files", exist_ok=True)
app.mount("/files/proposals", StaticFiles(directory="pdf_files"), name="proposals")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(proposals.router, prefix="/api/proposals", tags=["proposals"])
app.include_router(proposal_items.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(boq_items.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Auto Proposal API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)