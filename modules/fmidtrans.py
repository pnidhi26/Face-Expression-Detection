import uuid

# Creating 16 digit transition ID
def transition_id_generator(string_length):
   random = str(uuid.uuid4())
   random = random.upper()
   random = random.replace("-","")
   return random[0:string_length]
# print(my_random_string(18))
