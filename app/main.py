# app/main.py
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from app.utils.file_ops import init_directories, save_upload_file
from app.agent.core import PPTXAgent
import os

app = FastAPI(title="PPTX2MD Agent - 智能深度解析")

# 1. 初始化系统目录 (uploads, output/md, output/images)
init_directories()

# 2. 静态资源挂载
# 这样前端可以通过 <img src="/output/images/xxx.jpg"> 直接访问图片
app.mount("/output", StaticFiles(directory="output"), name="output")
# 如果有额外的 css/js 文件，也可以挂载 static 目录
# app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. 模板引擎设置
# 确保你的 HTML 文件放在项目根目录的 templates 文件夹下
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    """渲染主页"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_ppt(file: UploadFile = File(...)):
    """
    核心解析接口：接收 PPTX，运行 Agent 工作流，返回 MD 文件名
    """
    try:
        # 保存上传的文件到 uploads 目录
        content = await file.read()
        file_path = save_upload_file(content, file.filename)
        
        # 实例化并运行 PPTX Agent
        # Agent 内部会完成：全图渲染、文本解析、连贯性总结、文献推荐
        agent = PPTXAgent(file_path)
        final_md_path = agent.run() 
        
        return {
            "status": "success",
            "md_file": os.path.basename(final_md_path)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/get-md-content/{filename}")
async def get_md_content(filename: str):
    """
    预览增强接口：根据文件名读取 MD 文本源码
    """
    # 路径拼接需与 file_ops 中的 MD_OUTPUT_DIR 保持一致
    file_path = os.path.join("output", "md", filename)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return PlainTextResponse(content)
    
    return PlainTextResponse("Error: File not found", status_code=404)

# 如果需要直接下载文件的接口（可选，前端目前通过 Blob 下载）
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("output", "md", filename)
    return FileResponse(path=file_path, filename=filename, media_type='text/markdown')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)