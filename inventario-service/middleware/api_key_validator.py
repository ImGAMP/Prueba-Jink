import os
from fastapi import Request
from starlette.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

async def api_key_middleware(request: Request, call_next):
    if request.headers.get("X-API-KEY") != API_KEY:
        return JSONResponse(status_code=401, content={"error": "API Key inválida"})
    response = await call_next(request)
    return response


