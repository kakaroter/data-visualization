import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.uploadfile import app1
app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(app1, tags=["文件上传接口"])


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)