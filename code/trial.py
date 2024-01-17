import datetime
import pprint

from dao import add_token_to_db, remove_token_from_db

TIME_PER_PATIENT = 15

state = {
    "General": {
        "doc1": {
            "waitlist": ["token0"],
            "current": "token1",
            "presence": True,
            "length_of_waitlist": 1,
            "expertise": dict([["Allergy", 0.7], ["Drug Reaction", 0.8], ["Acne", 0.8]])
        },
        "doc2": {
            "waitlist": ["token4"],
            "current": "token2",
            "presence": True,
            "length_of_waitlist": 1,
            "expertise": dict([["Migraine", 0.9], ["Jaundice", 0.75], ["Acne", 0.9]])
        },
        "doc5": {
            "waitlist": ["token5", "token6"],
            "current": None,
            "presence": False,
            "length_of_waitlist": 2,
            "expertise": dict([["Dengue", 0.8], ["Malaria", 0.85]])
        },
    },
    "Cardiology": {
        "doc3": {
            "waitlist": [],
            "current": "token3",
            "presence": True,
            "length_of_waitlist": 0,
            "expertise": dict([["Heart Attack", 0.7], ["Aorta Disease", 0.8]])
        },
        "doc4": {
            "waitlist": [],
            "current": None,
            "presence": True,
            "length_of_waitlist": 0,
            "expertise": dict([["Angina", 0.96], ["Coronary artery disease", 0.89]])
        },
    },
}


def create_token(dept, doc):
    token = f"token{datetime.datetime.now().timestamp()}"
    try:
        add_token_to_db({"_id": token, "departmentId": dept, "doctorId": doc})
    except Exception as e:
        print(e)
        return None
    return token


def get_doc(dept, disease=None):
    min_len = float("inf")
    min_presence = True
    min_docId = None
    min_doc_success_rate = 0

    for doc in state[dept]:
        l = state[dept][doc]["length_of_waitlist"]
        p = state[dept][doc]["presence"]
        expertise = state[dept][doc]["expertise"]
        e = expertise[disease] if disease in expertise else 0
        if l < min_len:
            min_presence = p
            min_len = l
            min_docId = doc
            min_doc_success_rate = e
        elif l == min_len and ((min_presence == False and p == True) or (e > min_doc_success_rate)):
            min_presence = p
            min_doc_success_rate = e
            min_docId = doc

    return min_docId


def add_patient(dept, disease=None, doc=None):
    if doc is None:
        doc = get_doc(dept, disease)
    if doc == None:
        return None
    token = create_token(dept, doc)
    if state[dept][doc]["presence"] and state[dept][doc]["current"] == None:
        state[dept][doc]["current"] = token
        return token
    state[dept][doc]["waitlist"].append(token)
    state[dept][doc]["length_of_waitlist"] += 1

    return token


def session_over(dept, doc, token=None, next=True):
    if token == None:
        token = state[dept][doc]["current"]
    elif token != state[dept][doc]["current"] and token not in state[dept][doc]["waitlist"]:
        return state[dept][doc]["current"]

    try:
        remove_token_from_db(token)
    except Exception as e:
        print(e)
        return None
    if next:
        if state[dept][doc]["current"] == token:
            state[dept][doc]["current"] = state[dept][doc]["waitlist"].pop(
                0) if state[dept][doc]["length_of_waitlist"] > 0 else None
            state[dept][doc]["length_of_waitlist"] -= 1 if state[dept][doc]["length_of_waitlist"] > 0 else 0
        else:
            state[dept][doc]["waitlist"].remove(token)
            state[dept][doc]["length_of_waitlist"] -= 1 if state[dept][doc]["length_of_waitlist"] > 0 else 0
    else:
        state[dept][doc]["current"] = None
        return f"Doctor {doc} is out. Cabin is empty"

    return state[dept][doc]["current"] or "Cabin is empty"


def estimate_time(dept, doc, token):
    if token == None or token == state[dept][doc]["current"]:
        more = datetime.timedelta(minutes=0)
    else:
        more = datetime.timedelta(
            minutes=(state[dept][doc]["waitlist"].index(token) + 1) * TIME_PER_PATIENT)

    return datetime.datetime.now() + more


def print_state():
    pprint.pprint(state)


if __name__ == "__main__":
    add_patient("General", "Acne")
    add_patient("Cardiology", "Heart Attack")
    tok = add_patient("Cardiology", "Heart Attack", "doc4")
    print_state()
    print(estimate_time("Cardiology", "doc3", "token3"))
    print(estimate_time("Cardiology", "doc4", tok))
    session_over("Cardiology", "doc3")
    session_over("Cardiology", "doc4", tok)
    print_state()
