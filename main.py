if __name__ == "__main__":
    import os
    import sys
    sys.path.append('./aiqtEnv/lib/python3.12/site-packages/')
    from typing import Union
    from fastapi import FastAPI
    #from app.dataCollect import dataCollect

    app = FastAPI()

    @app.get("/")
    async def hello():
        return {"message": "Hello, AIQT!"}

    #@app.get("/items/{item_id}")
    #async def read_item(item_id: int, q: Union[str, None] = None):
    #    return {"item_id": item_id, "q": q}

    #@app.get("/dataCollect")
    #async def dataCollect():
    #    dataCollect()
    #    return {"message": "dataCollect!"}

    os.environ["AIQT_ENV"] = "production"

    uvicorn.run(app, host="0.0.0.0", port=8000)
