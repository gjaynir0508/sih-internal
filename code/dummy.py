import datetime
import random
from pymongo import MongoClient
client = MongoClient()

client = MongoClient("localhost", 27017)

db = client["sih-demo"]

patients = db["patients"].find()
departments = db["departments"].find()

for patient in patients:
    dept = random.choice(departments)
    client["sih-demo"]["tokens"].insert({
        "patientId": patient["_id"],
        "tokenId": datetime.datetime.now().timestamp(),
        "departmentId": dept["_id"],
        "doctorId": random.chosice(list(dept["doctors"])),
    })
