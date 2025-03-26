import sqlite3
from flask import Flask, request, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

# 🔥 환경 변수 로드
load_dotenv()
client = OpenAI()

# 🔥 Flask 앱 생성
app = Flask(__name__)

# 🔥 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # 앱 실행 시 DB 초기화

# 🔥 대화 저장 함수
def save_chat(user_message, bot_response):
    print("🔥 [DEBUG] 저장된 질문:", user_message)  # ✅ 터미널에 출력
    print("🔥 [DEBUG] 저장된 응답:", bot_response)  # ✅ 터미널에 출력

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    conn.close()


# 🔥 최근 대화 기록 불러오기
def get_chat_history():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response FROM chats ORDER BY id DESC LIMIT 5")
    chats = cursor.fetchall()
    conn.close()
    return chats

# 🔥 메인 페이지
@app.route("/", methods=["GET", "POST"])
def home():
    chat_history = get_chat_history()
    
    if request.method == "POST":
        user_input = request.form["user_input"]

        messages = [{"role": "system", "content": "당신은 친절한 AI 챗봇입니다."}]
        for chat in chat_history:
            messages.append({"role": "user", "content": chat[0]})
            messages.append({"role": "assistant", "content": chat[1]})
        messages.append({"role": "user", "content": user_input})

        print("🔥 [DEBUG] GPT에게 전달되는 대화 내용:", messages)  # ✅ 터미널에 출력

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        answer = response.choices[0].message.content
        save_chat(user_input, answer)
        chat_history = get_chat_history()

        return render_template("index.html", chat_history=chat_history)

    return render_template("index.html", chat_history=chat_history)


# 🔥 Flask 실행 코드
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # 기본 포트 5000, Render에서 자동 할당된 포트 사용 가능
    app.run(host="0.0.0.0", port=port, debug=True)

