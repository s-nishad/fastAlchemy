from fastapi import FastAPI
from config.exceptions import validation_exception_handler
from fastapi.exceptions import RequestValidationError
from config.setup import get_app_config
from fastapi.staticfiles import StaticFiles
from core.config import BASE_DIR



from api import docs, auth

app = FastAPI(**get_app_config())

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Mount entire `public` directory as static root
app.mount("/static", StaticFiles(directory="static"), name="static")



# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {"status": "ok", "message": "Welcome to ContextIQ - Knowledge Q&A System"}


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(docs.router, prefix="/api/v1/docs", tags=["Documents"])

# app.include_router(predefined.router, prefix="/api/v1/ask-predefined", tags=["Predefined QA"])
# app.include_router(knowledge_based.router, prefix="/api/v1/upload-ask", tags=["Knowledge Based QA"])