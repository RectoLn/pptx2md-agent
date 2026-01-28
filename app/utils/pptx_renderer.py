import win32com.client
import os
from pathlib import Path

def export_slides_as_images(pptx_path, output_folder):
    """将 PPT 的每一页导出为单独的 JPG 图片"""
    abs_pptx_path = str(Path(pptx_path).resolve())
    abs_output_folder = str(Path(output_folder).resolve())

    # 初始化 PowerPoint 应用
    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    # 0 表示后台运行，不弹出窗口
    presentation = ppt_app.Presentations.Open(abs_pptx_path, WithWindow=False)

    try:
        # 每一页导出。JPG 格式对应枚举值 17
        # 注意：SaveAs 会在 output_folder 下创建一个以文件名命名的文件夹，
        # 里面放着 Slide1.JPG, Slide2.JPG...
        presentation.SaveAs(abs_output_folder, 17) 
        print(f"成功导出图片至: {abs_output_folder}")
    finally:
        presentation.Close()
        ppt_app.Quit()