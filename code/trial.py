import datetime
import pprint

from dao import add_token_to_db, remove_token_from_db

TIME_PER_PATIENT = 15

state = {
    "General": {
        "doc1": {
            "waitlist": [],
            "current": "token1",
            "presence": True,
            "length_of_waitlist": 0,
        },
        "doc2": {
            "waitlist": ["token4"],
            "current": "token2",
            "presence": True,
            "length_of_waitlist": 1,
        },
        "doc5": {
            "waitlist": ["token5", "token6"],
            "current": None,
            "presence": False,
            "length_of_waitlist": 2,
        },
    },
    "Cardiology": {
        "doc3": {
            "waitlist": [],
            "current": "token3",
            "presence": True,
            "length_of_waitlist": 0,
        },
        "doc4": {
            "waitlist": [],
            "current": None,
            "presence": True,
            "length_of_waitlist": 0,
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


def get_doc(dept):
    min_len = float("inf")
    min_presence = True
    min_docId = None

    for doc in state[dept]:
        l = state[dept][doc]["length_of_waitlist"]
        p = state[dept][doc]["presence"]
        if l < min_len:
            min_presence = p
            min_len = l
            min_docId = doc
        elif l == min_len and min_presence == False and p == True:
            min_presence = p
            min_docId = doc

    return min_docId


def add_patient(dept, doc=None):
    if doc is None:
        doc = get_doc(dept)
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
    add_patient("General")
    add_patient("Cardiology")
    tok = add_patient("Cardiology", "doc4")
    print_state()
    print(estimate_time("Cardiology", "doc3", "token3"))
    print(estimate_time("Cardiology", "doc4", tok))
    session_over("Cardiology", "doc3")
    session_over("Cardiology", "doc4", tok)
    print_state()
