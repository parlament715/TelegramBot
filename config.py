import dotenv
import os
import json
from datetime import datetime, timedelta
from icecream import ic

dotenv.load_dotenv()

BOT_TOKEN = (os.getenv('token'))
ADMIN = json.loads((os.getenv('admin')))
VOSP = json.loads(os.getenv("vosp"))
TEACHER = json.loads(os.getenv("teacher"))
MAIN_VOSP = json.loads(os.getenv("main_vosp"))

ic(TEACHER)


today = datetime.now().date() + timedelta(days=0)
