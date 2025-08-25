from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from controllers.user import user_router
from store.base import UserNotFound

app = FastAPI()

app.include_router(user_router)


@app.exception_handler(UserNotFound)
def user_not_found_handler(request: Request, exc: UserNotFound):
    return JSONResponse(status_code=418, content={"message": str(exc)})
