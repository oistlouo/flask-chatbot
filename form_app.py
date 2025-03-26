from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]  # 사용자 입력 받기
        uppercase_text = user_input.upper()  # 대문자로 변환
        return render_template_string("""
            <h1>결과 페이지로 이동 중...</h1>
            <meta http-equiv="refresh" content="0;url=/result?data={{ uppercase_text }}">
        """, uppercase_text=uppercase_text)

    return render_template_string("""
        <h1>입력해보세요!</h1>
        <form method="POST">
            <input type="text" name="user_input" placeholder="아무거나 입력해보세요">
            <button type="submit">전송</button>
        </form>
    """)

@app.route("/result")
def result():
    data = request.args.get("data", "값이 없습니다.")
    return render_template_string(f"""
        <h1>결과 페이지</h1>
        <p>당신이 입력한 값(대문자 변환): <strong>{data}</strong></p>
        <a href="/">돌아가기</a>
    """)

if __name__ == "__main__":
    app.run(debug=True)
