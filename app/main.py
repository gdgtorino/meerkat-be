import uvicorn
from fastapi import FastAPI

from app.config.env import get_env
from app.config.setup import init_app
from app.router import homepage

init_app()
app = FastAPI(title=get_env()["project.name"], version=get_env()["project.version"])

app.include_router(homepage.router_public)
app.include_router(homepage.router_protected)

@app.get("/ping")
async def ping():
    return {"message": "Hello Meerkat!"}


if __name__ == "__main__":
    uvicorn.run(app, host=get_env()["project.host"], port=get_env()["project.port"])
