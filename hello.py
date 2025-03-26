from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World! 🎉"

@app.route("/about")
def about():
    return "나는 AI 에이전트를 공부 중이야 😎"

@app.route("/game")
def game():
    return "나는 천재야"

if __name__ == "__main__":
    app.run(debug=True)