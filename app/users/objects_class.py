from app.users.main_class import my_user
from icecream import ic

user_1 = my_user(id = "6324858739", func ="write", role = "Воспитатель", name = "user_1")
user_2 = my_user(id = "819514102d", func = "read")
user_3 = my_user(id = "819514102d", func ="write", role = "Классный советник", name = "user_3",classroom_number = 11)
user_4 = my_user(id = "819514102d", func ="write", role = "Классный советник", name = "user_4",classroom_number = 10)

all_list = [user_1,user_2,user_3,user_4]
# all_list = [Beta]

read_list = []

write_list = []

for i in all_list:
  if i.func == "write":
    write_list.append(i.id)
  elif i.func == "read":
    read_list.append(i.id)
def find_user_name_by_id(user_id):
  for user in all_list:
    if user.id == str(user_id):
      return user.name
  return None
def find_user_role_by_id(user_id):
  for user in all_list:
    if user.id == str(user_id):
      return user.role
  return None
def find_user_classroom_number_by_id(user_id):
  for user in all_list:
    if user.id == str(user_id):
      return user.classroom_number
  return None
### хранить данные в словаре

 
  





        
          