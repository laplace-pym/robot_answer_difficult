# 🤖 Laplace Chatbot（DeepSeek × LangChain × Gradio）

一个基于 **DeepSeek 大模型**、**LangChain 1.0 标准接口** 和 **Gradio 6.x** 构建的流式对话聊天机器人。

该项目支持：
- 自定义人设（System Prompt）
- 流式回复（打字机效果）
- 多轮对话上下文记忆
- 本地运行 + 公网分享（Cloudflare Tunnel）

---

## ✨ 项目特色

- 🧠 **人设驱动**  
  通过 `SystemMessage` 精确定义角色、性格和行为规则（如第一句话强制祝福 + 自我介绍）。

- ⚡ **流式输出**  
  使用 LangChain `stream()` 接口，实时展示模型生成过程。

- 🔗 **上下文记忆**  
  自动维护多轮对话历史，支持截断防止上下文无限增长。

- 🌐 **易于分享**  
  支持通过 Cloudflare Tunnel 将本地服务暴露到公网，方便朋友体验。

---

## 🛠 技术栈

- **LLM**：DeepSeek Chat
- **框架**：LangChain 1.0
- **前端/UI**：Gradio 6.x
- **语言**：Python 3.9+
- **隧道工具**：Cloudflare Tunnel（可选）

---

## 📂 项目结构

```text
.
├── robot_answer_difficult.py   # 主程序（Gradio + LangChain）
├── .env                        # 环境变量（不上传）
├── .gitignore
└── README.md
