from flask import Flask, request, render_template_string
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
client = OpenAI()  # 최신 OpenAI API 방식

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]  # 사용자 입력 받기

        # GPT에 질문 보내기 (최신 방식 적용)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        answer = response.choices[0].message.content  # AI 응답 가져오기

        return render_template_string("""
            <h1>GPT 챗봇</h1>
            <p><strong>당신:</strong> {{ user_input }}</p>
            <p><strong>GPT:</strong> {{ answer }}</p>
            <a href="/">다시 질문하기</a>
        """, user_input=user_input, answer=answer)

    return render_template_string("""
        <h1>GPT 챗봇</h1>
        <form method="POST">
            <input type="text" name="user_input" placeholder="GPT에게 질문하세요">
            <button type="submit">전송</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)
