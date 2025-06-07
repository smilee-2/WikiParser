import uvicorn
from fastapi import FastAPI

from app.api.articles import articles_router

app = FastAPI()

app.include_router(articles_router)


@app.get("/", tags=["Main"])
async def main() -> dict[str, str]:
    return {"message": "hey, check swagger"}


if __name__ == "__main__":
    uvicorn.run("main:app")
