# app/utils/md_parser.py

def compose_final_markdown(outline, slides_data, summaries, recommendation_text):
    """
    拼装最终的 Markdown 报告 - 并行兼容版
    """
    md_content = []

    # 第一部分：标题与大纲
    md_content.append("# PPT 智能深度解析报告\n")
    md_content.append("## 📑 内容大纲")
    
    # 格式化大纲层级
    formatted_outline = outline.replace("### ", "### ").replace("## ", "## ").replace("# ", "### ")
    md_content.append(formatted_outline)
    md_content.append("\n---\n")

    # 第二部分：逐页详情
    md_content.append("## 🔍 逐页详情")
    
    for i, slide in enumerate(slides_data):
        # 核心修复：兼容列表 (List) 和 字典 (Dict) 两种 summaries 格式
        idx = slide.get("slide_idx")
        
        if isinstance(summaries, dict):
            # 如果是字典，按键值取
            slide_summary = summaries.get(idx, "*(该页解析内容缺失)*")
        elif isinstance(summaries, list):
            # 如果是列表，按当前循环索引取
            slide_summary = summaries[i] if i < len(summaries) else "*(解析索引越界)*"
        else:
            slide_summary = "*(数据格式异常)*"

        md_content.append(f"### 第 {idx} 页：")
        
        # 渲染图片
        img_path = slide.get("full_slide_img", "")
        if img_path:
            # 增加对图片加载失败的容错描述
            md_content.append(f"![Slide {idx} 全图]({img_path})\n")
        
        # 总结部分
        md_content.append(f"{slide_summary}\n")
        md_content.append("---\n")

    # 第三部分：话题与扩展
    md_content.append("## 🏷️ 话题与扩展")
    md_content.append(recommendation_text)

    # 最终合并
    return "\n".join(md_content)