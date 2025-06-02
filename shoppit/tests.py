from pymongo.mongo_client import MongoClient
import certifi

uri = "mongodb+srv://novaherawan:admin123@cluster0.wr5xy70.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Gunakan certifi untuk CA bundle
client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)