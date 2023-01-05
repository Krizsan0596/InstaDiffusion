import pickle
import os

if os.path.exists('users.pkl'):
    with open("users.pkl", 'rb') as file:
        users = pickle.load(file)

users = {
    'admin' : [],
    'priority' : [],
    'blocked' : []
}

with open("users.pkl", "wb") as file:
    pickle.dump(users, file)