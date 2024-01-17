from flask import Flask

import trial

app = Flask(__name__)


@app.route("/doctor-out/<dept>/<doc>")
def doctor_out(dept, doc):
    trial.state[dept][doc]["presence"] = False
    if trial.state[dept][doc]["current"] == None:
        return "No current session"
    return trial.session_over(dept, doc, next=False)


@app.route("/doctor-in/<dept>/<doc>")
def doctor_in(dept, doc):
    trial.state[dept][doc]["presence"] = True
    trial.state[dept][doc]["current"] = trial.state[dept][doc]["waitlist"].pop(
        0) if trial.state[dept][doc]["length_of_waitlist"] > 0 else None
    trial.state[dept][doc]["length_of_waitlist"] -= 1 if trial.state[dept][doc]["length_of_waitlist"] > 0 else 0
    return f"{doc} in - {trial.state[dept][doc]['current']} is the current patient"


@app.route("/add-patient/<dept>/<disease>")
def add_patient(dept, disease):
    doc = trial.get_doc(dept, disease)
    token = trial.add_patient(dept, doc)
    return f"{token} is the token"


@app.route("/add-patient/<dept>/<doc>")
def add_patient_doc(dept, doc):
    token = trial.add_patient(dept, doc=doc)
    return f"{token} is the token"


@app.route("/session-over/<dept>/<doc>/<token>")
def session_over(dept, doc, token):
    return trial.session_over(dept, doc, token)


@app.route("/get-state")
def get_state():
    return trial.state


@app.route("/get-state/<dept>")
def get_state_dept(dept):
    return trial.state[dept]


@app.route("/get-state/<dept>/<doc>")
def get_state_dept_doc(dept, doc):
    return trial.state[dept][doc]


# For testing purposes
def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
