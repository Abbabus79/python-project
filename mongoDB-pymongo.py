import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["database"]

# Collection Name
col = db["MyCollection1"]

x = col.find()

for data in x:
    print(data)
