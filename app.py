from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "segreto123"

# Configurazione del database SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Modello della tabella Domande
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    options = db.Column(db.String(500), nullable=False)  # es: "Roma;Milano;Torino;Napoli"
    answer = db.Column(db.String(100), nullable=False)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/start")
def start():
    session["score"] = 0
    session["current"] = 1   # partiamo dalla domanda con id=1
    return redirect(url_for("question", qid=1))

@app.route("/question/<int:qid>", methods=["GET", "POST"])
def question(qid):
    q = Question.query.get(qid)
    if not q:  # se non esiste, quiz finito
        return redirect(url_for("result"))

    if request.method == "POST":
        answer = request.form.get("answer", "")
        if answer == q.answer:
            session["score"] += 1
        return redirect(url_for("question", qid=qid+1))

    options = q.options.split(";")
    return render_template("question.html", q=q, qid=qid, options=options)

@app.route("/result")
def result():
    score = session.get("score", 0)
    total = Question.query.count()
    return render_template("result.html", score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)