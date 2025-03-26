from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML 폼을 포함한 홈페이지
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
    user_input = request.form["user_input"]  # 사용자 입력 받기
    uppercase_text = user_input.upper()  # 🔥 대문자로 변환!
    return f"당신이 입력한 값(대문자 변환): {uppercase_text}"


    # 기본적으로 처음 접속할 때 폼을 보여줌
    return render_template_string("""
        <h1>입력해보세요!</h1>
        <form method="POST">
            <input type="text" name="user_input" placeholder="아무거나 입력해보세요">
            <button type="submit">전송</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)
