from app.users.main_class import my_user
from icecream import ic

Eta = my_user("6252541727","Классный руководитель","eta","write")
Beta = my_user("819514102","Классный руководитель","beta","read")

all_list = [Eta,Beta]

read_list = []

write_list = []

for i in all_list:
  if i.func == "write":
    write_list.append(i.id)
  elif i.func == "read":
    read_list.append(i.id)
def find_user_name_by_id(user_id):
        """
        Given a user ID, iterates over all imported user objects and returns the name of the user with that ID.
        """
        for user in all_list:
            if user.id == user_id:
                return user.table_name
        return None

 
  





        
          