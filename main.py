from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from typing import Dict, Any, List
from app.routes import router
from app.config.prisma import db
from app.exception.validation_error import AppBaseException
from app.middlewares.auth_middleware import get_current_user
from app.middlewares.success_response import JsonResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    print('Database Connected')

    yield
    
    await db.disconnect()
    print('Database Disconnected')

app = FastAPI(title='Advanced FastAPI MVC' ,lifespan=lifespan)

@app.exception_handler(AppBaseException)
async def central_exception_handler(request: Request, exc: AppBaseException):
    content: Dict[str, Any] = {
        "success": False,
        "message": exc.message,
        "code": exc.status_code
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_errors: List[Dict[str, Any]] = []
    
    for error in exc.errors():
        # Check karein agar error type JSON decode error hai
        if error["type"] == "json_invalid":
            field_name = "body"
            msg = "Invalid JSON format in request body"
        else:
            # Normal validation errors (missing fields, wrong types)
            field_name = error["loc"][-1]
            msg = error["msg"]
            
        custom_errors.append({
            "field": field_name,
            "message": msg
        })

    content: Dict[str, Any] = {
        'success': False,
        'message': 'Validation Failed',
        'code': 422,
        'errors': custom_errors
    }
    return JSONResponse(status_code=422, content=content)


app.include_router(router.api_router, prefix="/api")
@app.get("/")
def root():
    return {"message": "SOLID MVC Pattern is active!"}

@app.get('/me')
def get_profile(current_user = Depends(get_current_user)): # type: ignore
    return JsonResponse.success(
        data=current_user,
        message='profile fetched successfull'
    )