from app.users.main_class import my_user
from icecream import ic

Eta = my_user(id = "819514102", func ="write", role = "Классный советник", name = "Бета",classroom_number = "10")
# Beta = my_user(id = "504535913", func = "read")
Beta = my_user(id = "6324858739", func = "read")

all_list = [Eta,Beta]
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

 
  





        
          