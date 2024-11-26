from app.users.main_class import my_user
from icecream import ic
from config import VOSP, TEACHER, MAIN_VOSP


ID_VOSP = [elem["id"] for elem in VOSP]
ID_TEACHER = [elem["id"] for elem in TEACHER]
ID_MAIN_VOSP = [elem["id"] for elem in MAIN_VOSP]

all_list = []
print(ID_MAIN_VOSP)
_temp = MAIN_VOSP + TEACHER + VOSP
for user in _temp:
    if user not in all_list:
        all_list.append(user)


def find_user_name_by_id(user_id):
    for user in all_list:
        if user["id"] == str(user_id):
            return user["name"]
    return None


def find_user_classroom_number_by_id(user_id):
    for user in all_list:
        if user["id"] == str(user_id):
            ic(user)
            return user["classroom_number"]
    return None
