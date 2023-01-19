from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def root_route():
    """Start the Survey"""
    return render_template("survey_root.html", survey = satisfaction_survey)


@app.route("/questions/<int:ques_id>")
def questions_route(ques_id):
    """Show current question"""
    question = satisfaction_survey.questions[ques_id]

    if (ques_id != len(responses)):
        flash(f"Question {ques_id} not available")
        return redirect(f"/questions/{len(responses)}")

    if (len(satisfaction_survey.questions) == len(responses)):
        return redirect("/finished")

    return render_template("question.html", ques_id = ques_id, question = question)


@app.route("/answer", methods=["POST"])
def answer_route():
    """ Save the answer to the responses list and redirect to next question"""
    ans = request.form["answer"]

    responses.append(ans)

    if (len(satisfaction_survey.questions) == len(responses)):
        return redirect("/finished")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/finished")
def finished_survey():
    """ Survery Completion Message"""
    print(responses)
    return render_template("finished.html")