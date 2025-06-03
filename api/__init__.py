import os
import certifi
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Set SSL_CERT_FILE to certifi CA bundle
os.environ["SSL_CERT_FILE"] = certifi.where()
