# PPTX2MD Agent

智能 PPT 深度解析工具 - 将 PowerPoint 演示文稿转换为结构化的 Markdown 文档，并利用 AI 进行内容理解、摘要生成和文献推荐。

## 功能特点

- **PPT 渲染**：将 PPT 每页渲染为高清图片
- **文本解析**：提取 PPT 中的文本内容
- **AI 摘要**：利用 LLM 生成连贯的文档摘要
- **大纲生成**：自动生成文档大纲结构
- **标签提取**：智能提取内容标签
- **文献推荐**：基于内容推荐相关文献

## 环境要求

- Python 3.10+
- Windows/macOS/Linux

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd pptx2md-agent
```

### 2. 创建虚拟环境（可选）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```env
# DeepSeek API 配置
# 请访问 https://platform.deepseek.com 获取 API Key
DEEPSEEK_API_KEY=your-api-key-here

# 可选配置（默认值如下）
DEEPSEEK_MODEL_NAME=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## 运行项目

### 方式一：直接运行

```bash
cd pptx2md-agent
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 方式二：使用 Python 运行

```bash
cd pptx2md-agent
python app/main.py
```

服务启动后，访问 http://127.0.0.1:8000 即可使用。

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 主页 |
| `/analyze` | POST | 解析 PPT 文件 |
| `/get-md-content/{filename}` | GET | 获取 Markdown 内容 |
| `/download/{filename}` | GET | 下载 Markdown 文件 |

## 目录结构

```
pptx2md-agent/
├── app/
│   ├── main.py              # FastAPI 应用入口
│   ├── agent/
│   │   ├── core.py          # Agent 核心逻辑
│   │   ├── outline.py       # 大纲生成
│   │   ├── summarizer.py    # 摘要生成
│   │   └── hashtag.py       # 标签提取
│   ├── services/
│   │   ├── llm_client.py    # LLM 客户端
│   │   └── rag_client.py    # RAG 客户端
│   └── utils/
│       ├── file_ops.py      # 文件操作
│       ├── pptx_parser.py   # PPT 解析
│       ├── pptx_renderer.py # PPT 渲染
│       └── md_parser.py     # Markdown 解析
├── templates/               # HTML 模板
├── output/                  # 输出目录
│   ├── images/              # 渲染的图片
│   └── md/                  # 生成的 Markdown
├── uploads/                 # 上传的 PPT 文件
├── requirements.txt         # Python 依赖
└── .env                     # 环境变量
```

## 使用 Docker 运行

```bash
docker build -t pptx2md-agent .
docker run -p 8000:8000 --env-file .env pptx2md-agent
```

## 技术栈

- **FastAPI** - Web 框架
- **python-pptx** - PPT 解析
- **LangChain** - AI 代理框架
- **DeepSeek** - LLM 服务

## 许可证

MIT License
