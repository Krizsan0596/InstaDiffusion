# InstaDiffusion

Instagram bot to generate images using stable-diffusion.

It uses the api of AUTOMATIC1111's [webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

## Installation

The stable diffusion repo
`git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui`

Go to the [repo](https://github.com/AUTOMATIC1111/stable-diffusion-webui) and follow the setup instructions. [Here](https://www.youtube.com/watch?v=d1lPvI0T_go&t=327s) is a video if that's your thing.

After that's set up. Open `webui-user.bat` and add the following line: `set COMMANDLINE_ARGS=--api`.

Clone this repo: `git clone https://github.com/Krizsan0596/InstaDiffusion`

Install dependencies using poetry

```bash
pip install poetry
poetry install
```

create a `LOGIN.txt` file next to `main.py` with the following format:

```bash
bot_username
bot_password
```

You should create a sepparate account for the bot as it might get banned.

Run the .bat file and wait for it to give you a link.
In `main.py` change the `url` variable to match that link. (You most likely won't need to change it, it is set to the default value.)

In `users_setup.py` add your main instagram account's user_id to the admin list, you can add the rest with commands. Run `users_setup.py`.

Run `main.py`. If you get `Listening for messages...` in your console, it's working. Test it with a message.

## Commands

**Currently commands included**:

`?usage` - Prints usage instructions.

`?priority add/remove` - Adds or removes users from the priority list.

`?block` - Blocks user. (Can't actually block them so just adds them to an 'ignore list'.)

`?unblock` - Unblocks user.

`?admin` - Adds user to admin list.

**Commands to be added**:

`?help` - Prints available commands.
