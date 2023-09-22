from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()

client = MongoClient("localhost", 27017)

db = client["sih-demo"]

# set dept. id's on doctors


def set_dept_id():
    for dept in db["departments"].find():
        for doctor in dept["doctors"]:
            db["doctors"].update_one(
                {"_id": ObjectId(doctor)}, {
                    "$set": {"departmentId": dept["_id"]}}
            )

# set doctor id's in an array on departments


def set_doctor_ids():
    for dept in db["departments"].find():
        dept["doctors"] = []
        for doctor in db["doctors"].find({"departmentId": dept["_id"]}):
            dept["doctors"].append(doctor["_id"])
        db["departments"].update_one(
            {"_id": dept["_id"]}, {"$set": {"doctors": dept["doctors"]}}
        )


# create tokens based on json file
def create_tokens():
    pass


set_doctor_ids()
