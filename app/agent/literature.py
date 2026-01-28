# app/agent/literature.py
from app.services.llm_client import LLMClient
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_hashtag_with_literature(outline_text: str):
    llm = LLMClient.get_llm(temperature=0.7)
    
    template = """
    根据以下 PPT 大纲，生成 3 个核心 Hashtags，并为每个 Hashtag 推荐一篇相关的真实学术文献或权威来源。
    
    PPT 大纲：
    {outline}
    
    请严格按照以下格式输出：
    #标签名
    >相关文献: [作者]. "[标题]". [年份/期刊] - 简短一句话介绍
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({"outline": outline_text})