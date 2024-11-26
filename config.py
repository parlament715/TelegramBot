import dotenv
import os
import json
from datetime import datetime, timedelta

dotenv.load_dotenv()

BOT_TOKEN = (os.getenv('token'))
ADMIN = json.loads((os.getenv('admin')))
VOSP = json.loads(os.getenv("vosp"))
TEACHER = json.loads(os.getenv("teacher"))
MAIN_VOSP = json.loads(os.getenv("main_vosp"))
_TIME = (os.getenv("time"))

time_from = time(int(_TIME.split(";")[0].split(
    ":")[0]), int(_TIME.split(";")[0].split(":")[1]))
time_to = time(int(_TIME.split(";")[1].split(
    ":")[0]), int(_TIME.split(";")[1].split(":")[1]))

print(time_from, time_to)
