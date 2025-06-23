import uvicorn
from fastapi import FastAPI

from app.config.env import get_env
from app.config.setup import init_app
from app.router import homepage
from app.router import talk

init_app()
app = FastAPI(title=get_env()["project.name"], version=get_env()["project.version"])

app.include_router(homepage.router_public)
app.include_router(homepage.router_protected)
app.include_router(talk.router_public)
app.include_router(talk.router_protected)


@app.get("/ping")
async def ping():
    return {"message": "Hello Meerkat!"}


# TODO cancellare NO COMMIT
@app.get("/ex-db")
async def ping():
    from firebase_admin import firestore
    db = firestore.client()

    doc_ref = db.collection('blog').document('c4p')
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"data": None}


if __name__ == "__main__":
    uvicorn.run(app, host=get_env()["project.host"], port=get_env()["project.port"])
