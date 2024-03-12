import dotenv
import os
import json

dotenv.load_dotenv()

BOT_TOKEN = (os.getenv('token'))
ADMIN = json.loads((os.getenv('admin')))