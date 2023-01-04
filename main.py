import os
import requests
import io
import base64
import pickle
import datetime
from time import sleep
from PIL import Image, PngImagePlugin
from colorama import Fore, Style
from pathlib import Path
from instagrapi import Client

# Directory for images
dir_path = os.path.realpath("./Generated")
url = "http://127.0.0.1:7860"

with open("LOGIN.txt", "r") as file:
    username, password = file.read().splitlines()

with open("users.pkl", "rb") as file:
    users = pickle.load(file)

os.chdir(dir_path)

prompts = []
priority_prompts = []

def get_messages():
    threads = client.direct_threads(selected_filter='unread')
    messages = None
    for thread in threads:
        messages = client.direct_messages(thread.id)
        for message in messages:
            if not str(message.text).startswith('?'):
                prompt = (message.text, message.user_id)
                if message.user_id == int(client.user_id_from_username(username)) or message.user_id in users['blocked']:
                    continue
                elif message.user_id in users['admin']:
                    if prompt not in priority_prompts:
                        priority_prompts.insert(0, prompt)
                elif message.user_id in users['priority']:
                    if prompt not in priority_prompts:
                        if queue != 0:
                            queue = len(priority_prompts)
                            client.direct_send(f"You are the {queue}. person in the queue.")
                        priority_prompts.append(prompt)
                else:
                    if prompt not in prompts:
                        if queue != 0:
                            queue = len(priority_prompts) + len(prompts)
                            client.direct_send(f"You are the {queue}. person in the queue.")
                        prompts.append(prompt)
            else:
                uid = int(message.user_id)
                message = str(message.text)[1:]
                if message == 'usage':
                    msg = """Just send me a message to generate an image using that prompt. If you want to use a negative prompt, enter the prompt after a '!'. \nYou can get your images faster by following me, or you can run '?priority' to get more info. Type '?help' to see all available commands. \nIf you encounter any issues, send a message to @krizsan0956"""
                    for mesg in msg.split('\n'):
                        client.direct_answer(thread.id, mesg)  
                elif message == 'priority':
                    message = message.split(' ')
                    if len(message) == 1:
                        msg = "If you want to get your images faster, you can follow me to get ahead the queue. However, priority users will still be processed before followers."
                    elif len(message) == 2:
                        msg = "Argument missing: Username required."
                    elif len(message) == 3:
                        if int(uid) in users['admin']:
                            if message[1] == 'add':
                                users['priority'].append(client.user_id_from_username(message[2]))
                                msg = f"@{message[2]} added to priority list."
                            elif message[1] == 'remove':
                                users['priority'].append(client.user_id_from_username(message[2]))
                                msg = f"@{message[2]} removed from priority list."
                            else:
                                msg = "Invalid option.\nUsage: ?priority add/remove username"
                        else: msg = "Admin privileges required for that operation"
                elif message == "block":
                    if uid in users['admin']:
                        message = message.text.split(" ")
                        if len(message) == 1:
                            msg = "Argument missing: Username required"
                        elif len(message) == 2:
                            users['blocked'].append(client.user_id_from_username(message[1]))
                            msg = f"@{message[1]} has been blocked."
                    else: msg = "Admin privileges required for that operation"
                elif message == "unblock":
                    if uid in users['admin']:
                        message = message.text.split(" ")
                        if len(message) == 1:
                            msg = "Argument missing: Username required"
                        elif len(message) == 2:
                            users['blocked'].remove(client.user_id_from_username(message[1]))
                            msg = f"@{message[1]} has been unblocked."
                    else: msg = "Admin privileges required for that operation"
                elif message == "admin":
                    if uid in users['admin']:
                        message = message.split(" ")
                        if len(message) == 1:
                            msg = "Argument missing: Username required"
                        elif len(message) == 2:
                            users['admin'].append(client.user_id_from_username(message[1]))
                            msg = f"@{message[1]} added to admins. User can only be removed in the script."
                    
    print(datetime.datetime.now(), prompts, priority_prompts)

    return messages

def generate_image(prompt):
    if prompt[0].startswith('!'):
        payload={
            "negative_prompt": prompt[0][1:]
        }
    else:
        payload={
        "prompt": prompt[0]
        }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
        "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
    
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save('output.jpg', pnginfo=pnginfo)


print(f"{username} - {password}")
client = Client()
client.login(username, password)

messages = get_messages()

print(Fore.LIGHTGREEN_EX + "Listening for messages..." + Fore.RESET)

try:
    while True:
        sleep(30)
        while len(priority_prompts) != 0:
            for prompt in priority_prompts:
                client.direct_send(f"Processing of '{prompt[0]}' has started. ETA: 2 minutes.", [prompt[1]])
                generate_image(prompt)
                client.direct_send(f"Processing of '{prompt[0]}' complete, please unsend original message.", [prompt[1]])
                client.direct_send_photo(Path(os.path.realpath("output.jpg")), [prompt[1]])
                os.remove('output.jpg')
                for message in messages:
                    if message.user_id == int(client.user_id_from_username(username)):
                        if "ETA: 2 minutes" in str(message.text):
                            client.direct_message_delete(message.thread_id, message.id)
                priority_prompts.remove(prompt)
        messages = get_messages()
        if len(priority_prompts) != 0:
            continue
        for prompt in prompts:
            client.direct_send(f"Processing of '{prompt[0]}' has started. ETA: 2 minutes.", [prompt[1]])
            generate_image(prompt)
            client.direct_send(f"Processing of '{prompt[0]}' complete, please unsend original message.", [prompt[1]])
            client.direct_send_photo(Path(os.path.realpath("output.jpg")), [prompt[1]])
            os.remove('output.jpg')
            for message in messages:
                if message.user_id == int(client.user_id_from_username(username)):
                    print("UID")
                    if "ETA: 2 minutes" in str(message.text):
                        print("STR")
                        client.direct_message_delete(message.thread_id, message.id)
            prompts.remove(prompt)
            messages = get_messages()
            if len(priority_prompts) != 0:
                break 
except KeyboardInterrupt:
    print(Fore.RED + "Keyboard Interrupt detected. Exiting..." + Fore.RESET)
    os.chdir('..')
    with open("users.pkl", 'wb') as file:
        pickle.dump(users, file)

#?implement follower prompts?/Implement img2img/Implement help command(s)/
