from flask import Flask, request
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

# OpenAI API 클라이언트 생성
client = OpenAI()

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, AI Agent!"

@app.route("/ask")
def ask():
    prompt = request.args.get("q", "Hello!")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"에러 발생: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
