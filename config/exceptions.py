# app/exceptions.py

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({
            "field": ".".join([str(loc) for loc in err["loc"] if loc != "body"]),
            "message": err["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "errors": errors
        }
    )
