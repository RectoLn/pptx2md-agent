# app/agent/outline.py
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.services.llm_client import LLMClient

def generate_outline(slides_data: list) -> str:
    """
    输入: PPT 解析后的 list 数据
    输出: Markdown 格式的完整大纲
    """
    # 1. 准备上下文：为了节省 token，我们只提取 slide_idx, title 和部分内容
    context_text = ""
    for slide in slides_data:
        title = slide.get("title", "No Title")
        # 取前200个字符作为上下文，避免 token 溢出
        content_preview = " ".join([p["text"] for p in slide["paragraphs"]])[:200]
        context_text += f"Slide {slide['slide_idx']}: {title}\nContent: {content_preview}\n\n"

    # 2. 定义 Prompt
    # 这里的 Prompt 强调生成结构化的 Markdown 目录
    template = """
    你是一个专业的文档架构师。请根据以下 PPT 的页面内容，整理出一份逻辑清晰的 Markdown 大纲。
    
    要求：
    1. 结构必须包含层级，例如：
       # 报告标题
       ## 1. 第一部分标题
       ### 1.1 子标题
       ## 2. 第二部分标题
    2. 忽略由于分页导致的逻辑中断，将内容整合成连贯的章节。
    3. 只输出 Markdown 大纲内容，不要输出其他废话。
    
    PPT 内容摘要：
    {context}
    
    请生成大纲：
    """
    
    prompt = PromptTemplate.from_template(template)
    
    # 3. 调用 LLM
    llm = LLMClient.get_llm(temperature=0.3)
    chain = prompt | llm | StrOutputParser()
    
    print("--- 正在生成大纲 (Outline Agent) ---")
    outline = chain.invoke({"context": context_text})
    return outline