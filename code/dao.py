import pprint
from pymongo import MongoClient

# Only for testing
from dict_to_json import state

client = MongoClient()

client = MongoClient("localhost", 27017)

db = client["sih-demo"]

try:
    client.admin.command("ping")
    print("Connected to database")
except Exception as e:
    print(e)


def generate_state_from_scratch():
    state = {}
    for dept in db["departments"].find():
        state[dept] = {}
        for doctor in dept["doctors"]:
            state[dept][doctor] = {
                "waitlist": [],
                "length_of_waitlist": 0,
                "current": None,
                "presence": True,
            }

    return state


def generate_state_from_tokens():
    state = {}
    for token in db["tokens"].find():
        if token["departmentId"] not in state:
            state[token["departmentId"]] = {}
        if token["doctorId"] not in state[token["departmentId"]]:
            state[token["departmentId"]][token["doctorId"]] = {
                "waitlist": [],
                "length_of_waitlist": 0,
                "current": None,
                "presence": True,
            }
        state[token["departmentId"]][token["doctorId"]
                                     ]["waitlist"].append(token["_id"])
        state[token["departmentId"]][token["doctorId"]
                                     ]["length_of_waitlist"] += 1
        state[token["departmentId"]][token["doctorId"]]["current"] = state[token["departmentId"]][token["doctorId"]]["waitlist"][0] if len(
            state[token["departmentId"]][token["doctorId"]]["waitlist"]
        ) > 0 else None

    return state


def add_token_to_db(token):
    db["tokens"].insert_one(token)


def remove_token_from_db(tokenId):
    db["tokens"].delete_one({"_id": tokenId})


def get_from_state():
    return db["state"].find_one({})


def save_state(state):
    db["state"].delete_many({})
    db["state"].insert_one(state)


if __name__ == "__main__":
    pprint.pprint(generate_state_from_tokens())
    save_state(state)
    pprint.pprint(get_from_state())

    client.close()
