from fastapi import FastAPI


app = FastAPI()


@app.get("")
async def main() -> dict[str, str]:
    return {"message": "hey"}
