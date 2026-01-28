from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.services.llm_client import LLMClient

def summarize_single_slide(slide_data: dict, outline: str) -> str:
    """
    并行解析函数：
    输入: 单个 slide 数据、全局大纲 (outline)
    输出: 具备逻辑定位的当前页深度解析
    """
    title = slide_data.get("title", "无标题页面")
    # 提取本页文本
    paragraphs = slide_data.get("paragraphs", [])
    text_content = "\n".join([p.get("text", "") for p in paragraphs])
    slide_idx = slide_data.get("slide_idx", 0)
    
    if not text_content.strip() and not title.strip():
        return "本页主要为视觉展示，请结合前后文逻辑理解。"

    # 针对并行化优化的 Prompt
    # 删除了 prev_summary，增加了 idx 定位
    template = """
你正在将 PPT 内容整理成一份连续的 Markdown 学习笔记。

注意：当前页只是整份笔记中的一个小片段，不是独立文章，字数控制在300字以内，
不要使用太多结构（如#等小标题），
尽量用换行文本与
**加深文本**增加可读性。
避免使用“本页为xx页”、“本课程为..”等自引用表述。直接切入内容。


=========================
【课程全局大纲】
{outline}

【当前页序号】
第 {idx} 页

【当前页标题】
{title}

【当前页原始内容】
{text}
=========================


## 一、页面类型自动识别

判断该页属于：

- 标题页
- 目录页
- 知识讲解页
- 图示 / 实验结果页


---

## 二、通用写作规则（强约束）

✅ 输出为学习笔记片段（不是文章）  
✅ 默认简洁（通常 5–12 行以内）  
✅ 不写开场白、不写总结段  
✅ 不复读原文  

❌ 不写“课程导语”“讲师点评”“一句话总结”  
❌ 不写成报告或博客  
❌ 不扩展到无关知识  

风格参考：

👉 大学生高质量课堂笔记  
👉 技术重点速记 + 简要解释  


---

## 三、各页面类型写法（必须简短）


### ▶ 标题页：

写成简短背景说明，例如：

- 研究主题关注什么问题  
- 为什么重要  
- 大致研究方向  

不超过 3–5 行。


---

### ▶ 目录页：

转成简洁学习路线：

- 每一部分一句话说明重点  
- 使用无序列表  

不展开解释。


---

### ▶ 知识讲解页：

输出：

- 核心概念要点（列表形式）  
- 每点给一句简要解释  

如涉及原理，可补充：

- 一个简短公式 或  
- 2–4 行极简伪代码  

保持紧凑。


---

### ▶ 图示 / 实验结果页：

输出：

- 图中对比对象  
- 主要趋势  
- 得出的关键结论  

用 3–6 行概括。


---

## 四、扩展控制规则（非常重要）

只有在以下情况才补充说明：
在课程框架中
- 新模型首次出现  
- 新机制首次出现  
且：
👉 每次补充不超过 2–3 行  
👉 只讲核心思想  


---

## 五、格式要求

使用 Markdown：

- 合理加粗关键词
- 多用列表
- 避免长段落


---

现在请生成当前页对应的 Markdown 学习笔记片段：
"""



    
    prompt = PromptTemplate.from_template(template)
    # 获取 LLM 实例
    llm = LLMClient.get_llm(temperature=0.3) 
    chain = prompt | llm | StrOutputParser()
    
    try:
        # 执行解析
        summary = chain.invoke({
            "outline": outline, 
            "idx": slide_idx,
            "title": title, 
            "text": text_content
        })
        return summary.strip()
    except Exception as e:
        print(f"Error in parallel summary for Slide {slide_idx}: {e}")
        return f"（Slide {slide_idx} 讲解生成异常，请参考大纲）"

def summarize_all_slides(slides_data: list, outline: str):
    """
    兼容性封装：如果其他地方还在调用旧函数名，它会自动适配
    """
    return {s["slide_idx"]: summarize_single_slide(s, outline) for s in slides_data}