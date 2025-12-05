# -*- coding: utf-8 -*-

from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


async def not_found_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.detail,
            "timestamp": datetime.now().isoformat(),
            "status": "failure",
        },
    )


def add_handlers(api: FastAPI) -> None:
    """Реєструємо обробники помилок"""
    api.add_exception_handler(404, not_found_handler)
