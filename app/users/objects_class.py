from app.users.main_class import my_user
from icecream import ic

Eta = my_user("819514102","Воспитатель","4 Этаж","write")
Beta = my_user("6324858739","Классный советник","Бета","write")

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

 
  





        
          