import os
import concurrent.futures  # 1. 引入标准并发库
from app.utils.pptx_parser import parse_pptx
from app.utils.pptx_renderer import export_slides_as_images
from app.agent.outline import generate_outline
# 注意：我们需要导入具体的单页总结函数
from app.agent.summarizer import summarize_single_slide 
from app.agent.literature import get_hashtag_with_literature
from app.utils.md_parser import compose_final_markdown
from app.utils.file_ops import MD_OUTPUT_DIR, IMG_OUTPUT_DIR

class PPTXAgent:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]

    def run(self):
        """
        全自动化工作流调度中心 - 并行加速版
        """
        # 1. 预处理：幻灯片高清渲染
        ppt_img_dir = IMG_OUTPUT_DIR / self.file_name
        ppt_img_dir.mkdir(parents=True, exist_ok=True)
        print(f"[*] 正在渲染 PPT 为图片: {self.file_name}...")
        export_slides_as_images(self.file_path, ppt_img_dir)

        # 2. ETL阶段：解析文本内容
        print(f"[*] 正在解析 PPT 文本...")
        parsed_data = parse_pptx(self.file_path)
        
        # 3. 数据关联：路径适配
        for slide in parsed_data:
            idx = slide["slide_idx"]
            image_filename = f"幻灯片{idx}.JPG"
            full_img_path = ppt_img_dir / image_filename
            if not full_img_path.exists():
                if (ppt_img_dir / f"幻灯片{idx}.jpg").exists():
                    image_filename = f"幻灯片{idx}.jpg"
            slide["full_slide_img"] = f"../../output/images/{self.file_name}/{image_filename}"
            
        # 4. LLM 认知阶段 (并行重组)
        
        # 4.1 生成全局大纲 (静态上下文锚点)
        print(f"[*] Agent 正在理解全局逻辑并生成大纲...")
        outline = generate_outline(parsed_data)

        # 4.2 【核心修改】并行执行逐页讲解生成
        print(f"[*] Agent 开启并行流水线，正在同时解析 {len(parsed_data)} 页幻灯片...")
        
        # 预分配列表以保证顺序一致
        summaries = [None] * len(parsed_data)
        
        # 使用线程池加速 LLM 请求
        # max_workers=5 是兼顾速度与 API 稳定性（Rate Limit）的平衡点
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # 创建任务字典：{Future对象: 索引idx}
            future_to_idx = {
                executor.submit(summarize_single_slide, slide, outline): i 
                for i, slide in enumerate(parsed_data)
            }
            
            # 按完成顺序处理结果，但放回原定的索引位置
            for future in concurrent.futures.as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    summaries[idx] = future.result()
                    print(f"[+] Slide {idx+1} 解析完成")
                except Exception as e:
                    summaries[idx] = f"⚠️ 该页解析失败: {str(e)}"
                    print(f"[x] Slide {idx+1} 解析异常: {e}")

        # 4.3 文献推荐
        print(f"[*] Agent 正在检索文献并生成 Hashtags...")
        recommendations = get_hashtag_with_literature(outline)

        # 5. 输出生成
        print(f"[*] 正在拼装最终报告...")
        final_md = compose_final_markdown(
            outline=outline, 
            slides_data=parsed_data, 
            summaries=summaries, 
            recommendation_text=recommendations
        )

        # 6. 持久化
        output_path = MD_OUTPUT_DIR / f"{self.file_name}_final.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_md)
            
        print(f"[√] 任务完成！报告已生成: {output_path}")
        return str(output_path)