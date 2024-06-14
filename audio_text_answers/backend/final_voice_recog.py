from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from get_response import router as get_resp
from upload_resume import router as update_resumes
from Authentication import router as Authentication
import logging

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(get_resp)
app.include_router(update_resumes)
app.include_router(Authentication)

# Allow requests from all origins (replace "*" with your frontend domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
