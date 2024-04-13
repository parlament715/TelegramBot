import dotenv
import os
import json
from datetime import datetime, timedelta

dotenv.load_dotenv()

BOT_TOKEN = (os.getenv('token'))
ADMIN = json.loads((os.getenv('admin')))


today = datetime.now().date() + timedelta(days=0)