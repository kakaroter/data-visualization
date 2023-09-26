from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union, Optional, List
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from uos_statistics.uosstatistics import UosStatistics
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import aiofiles
import asyncio

app1 = APIRouter()
templates = Jinja2Templates(directory="static/html")
lock = asyncio.Lock()  # 创建一个锁对象
count = 1000


@app1.get("/upload", response_class=HTMLResponse)
async def get_upload_page(request: Request):
    async with lock:
        global count
        count += 1
    return templates.TemplateResponse(
        "uploadx.html",
        {
            "request": request,
            "count": count
        }
    )


@app1.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    print('filename', filename)
    # 将文件保存到项目本地
    file_path = os.path.join(os.getcwd(), filename)
    print('file_path', file_path)
    byte_data = await file.read()
    # file.file.getvalue()
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(byte_data)
    # 然后调用你的函数解析文件，例如：
    u = UosStatistics(file_path)
    module_data = u.get_module_data()
    print(module_data)
    u.generate_pie_chart([(key, value) for key, value in module_data.items()])
    # 最后返回文件响应，例如：
    html_path = os.path.join(os.getcwd(), 'render.html')
    u.read_html()
    print(html_path)
    print('生成新html-title成功')
    return FileResponse(html_path)

