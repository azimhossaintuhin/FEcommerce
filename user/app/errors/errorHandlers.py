from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.schemas.Base import ErrorResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    simplified_errors = {}
    for error in errors:
        loc = error.get("loc", [])
        field = loc[-1] if loc else "unknown"
        if field not in simplified_errors:
            simplified_errors[field] = error.get("msg", "Invalid input")

    error_response = ErrorResponse(
        status="false",
        message="Validation Error",
        errors=simplified_errors
    )

    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()  # convert to dict here
    )


async def generic_exception_handler(request: Request, exc: Exception):

    error_response = ErrorResponse(
        status="false",
        message="Internal server error",
        errors=str(exc)  # or just "An unexpected error occurred"
    )
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )