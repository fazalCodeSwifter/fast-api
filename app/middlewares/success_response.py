from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel 
from typing import Any, Dict

class JsonResponse:
    @staticmethod
    def success(
        data: Any = None,
        message: str = 'successfull',
        status_code: int = 200
    ) -> JSONResponse:
        # Check if data instance of pydentic model
        if isinstance(data, BaseModel):
            data = data.model_dump()
        
        # any data support str, int, list, and dict
        elif isinstance(data, list):
            data = [item.model_dump() if isinstance(item, BaseModel) else item for item in data] # type: ignore

        safe_data = jsonable_encoder(data)
        return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'message': message,
                'code': status_code,
                'data': safe_data
            }
        )
        
    @staticmethod
    def error(
        message: str = "An error occurred", 
        status_code: int = 400,
        errors: Any = None
    ) -> JSONResponse:
        content: Dict[str, Any] = {
            "success": False,
            "message": message,
            "code": status_code
        }
        if errors:
            content["errors"] = errors
            
        return JSONResponse(
            status_code=status_code,
            content=content
        )