import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Access environment variables
TESTING_BUS_CSV = os.environ.get("TESTING_BUS_CSV")

