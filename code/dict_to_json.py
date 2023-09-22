import json

state = {
    "General": {
        "doc1": {
            "waitlist": ["token1"],
            "current": "token1",
            "presence": True,
            "length_of_waitlist": 1,
        },
        "doc2": {
            "waitlist": ["token2", "token4"],
            "current": "token2",
            "presence": True,
            "length_of_waitlist": 2,
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
            "waitlist": ["token3"],
            "current": "token3",
            "presence": True,
            "length_of_waitlist": 1,
        },
        "doc4": {
            "waitlist": [],
            "current": None,
            "presence": True,
            "length_of_waitlist": 0,
        },
    },
}

if __name__ == "__main__":
    with open("state.json", "w") as f:
        json.dump(state, f, indent=4)
    print(json.dumps(state, indent=4))
