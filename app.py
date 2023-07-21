from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey 

responses = "responses"

app = Flask(__name__)
app.config['secret_key']= "shiii!"
app.config['debug_tb_intercept_redirects'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    '''select survey'''

    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods = ["POST"])
def start_survey():
    """clear session responses"""

    session[responses] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """save response and redirect to next question"""

    choice = request.form['answer']
    responses = session[responses]
    responses.append(choice)
    session[responses] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    else:
        return redirect(f'/question/{len(responses)}')
    

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(responses)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")

