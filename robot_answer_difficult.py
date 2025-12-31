import gradio as gr
from langchain_deepseek import ChatDeepSeek
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

# ──────────────────────────────────────────────
# 1️⃣ 初始化模型与系统设定
# ──────────────────────────────────────────────
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

system_message = SystemMessage(
    content=(
        "你现在不是 AI，而是在扮演一个真实的人。\n"
        "你的名字叫 laplace。\n"
        "对方的名字叫 xx。\n\n"
        "【强制规则】\n"
        "不管听雪第一句话问什么，你的第一条回复都必须：\n"
        "1）先祝她：xx同学，元旦快乐\n"
        "2）明确说明：我是 laplace\n\n"
        "之后再根据她的问题自然继续对话。\n\n"
        "说话风格：自然、真诚、像真人聊天，不要暴露自己是机器人或 AI。"
    )
)

# ──────────────────────────────────────────────
# 2️⃣ 定义 Gradio 界面
# ──────────────────────────────────────────────
CSS = """
.main-container {max-width: 1200px; margin: 0 auto; padding: 20px;}
.header-text {text-align: center; margin-bottom: 20px;}
"""

def create_chatbot() -> gr.Blocks:
    with gr.Blocks(title="DeepSeek Chat") as demo:
        with gr.Column(elem_classes=["main-container"]):
            gr.Markdown("#xx同学，元旦快乐！", elem_classes=["header-text"])
            gr.Markdown(" 🤖 Laplace对话机器人", elem_classes=["header-text"])

            chatbot = gr.Chatbot(
                height=500,
                avatar_images=(
                    "https://cdn.jsdelivr.net/gh/twitter/twemoji@v14.0.2/assets/72x72/1f464.png",
                    "https://cdn.jsdelivr.net/gh/twitter/twemoji@v14.0.2/assets/72x72/1f916.png",
                ),
            )

            msg = gr.Textbox(placeholder="请输入您的问题...", container=False, scale=7)
            submit = gr.Button("发送", scale=1, variant="primary")
            clear = gr.Button("清空", scale=1)

        # ✅ 只用一个 State：存 LangChain 的 messages
        state = gr.State([])

        # ─────────────── 主响应函数（Gradio 6.x 正确写法） ───────────────
        async def respond(user_msg: str, messages_list: list):
            if not user_msg.strip():
                yield "", [], messages_list
                return

            # 初始化 system prompt
            if not messages_list:
                messages_list = [system_message]

            # 1️⃣ LangChain：加入用户消息
            messages_list.append(HumanMessage(content=user_msg))

            # 2️⃣ Gradio Chatbot：消息格式（dict）
            chat_ui = [{"role": "user", "content": user_msg}]
            yield "", chat_ui, messages_list

            # 3️⃣ 流式生成
            partial = ""
            chat_ui.append({"role": "assistant", "content": ""})

            for chunk in model.stream(messages_list):
                if chunk.content:
                    partial += chunk.content
                    chat_ui[-1]["content"] = partial
                    yield "", chat_ui, messages_list

            # 4️⃣ 保存 AI 消息（LangChain）
            messages_list.append(AIMessage(content=partial))
            messages_list = messages_list[-50:]

            yield "", chat_ui, messages_list

        # ─────────────── 清空函数 ───────────────
        def clear_history():
            return [], []

        # ─────────────── 事件绑定（⚠️ 不把 chatbot 当输入） ───────────────
        msg.submit(respond, [msg, state], [msg, chatbot, state])
        submit.click(respond, [msg, state], [msg, chatbot, state])
        clear.click(clear_history, outputs=[chatbot, state])

    return demo

# ──────────────────────────────────────────────
# 3️⃣ 启动应用
# ──────────────────────────────────────────────
demo = create_chatbot()
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    css=CSS,
    debug=True,
    share=False
)
