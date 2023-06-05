import os

filename = 'abcd'

directory = os.path.dirname(__file__)
print(os.path.join(directory, "static\\image" , filename))