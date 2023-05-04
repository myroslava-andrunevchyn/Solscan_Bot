### How to setup env and run bot

1. Install python 3.11
2. Install pip latest version
3. Install required dependencies with command *pip install -r requirements.txt*
4. Check if variable BOT_TOKEN contains correct value
5. Run bot.py from terminal like *python bot.py* or from PyCharm

### How to handle telegram bot account

#### Bot account creation
__________________________________________________________________________________________________________________________________________________
Below is a detailed guide to using @BotFather, Telegram’s tool for creating and managing bots.

Creating a new bot
Use the /newbot command to create a new bot. @BotFather will ask you for a name and username, then generate an authentication token for your new bot.

The name of your bot is displayed in contact details and elsewhere.

The username is a short name, used in search, mentions and t.me links. Usernames are 5-32 characters long and not case sensitive – but may only include Latin characters, numbers, and underscores. Your bot's username must end in 'bot’, like 'tetris_bot' or 'TetrisBot'.

The token is a string, like 110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw, which is required to authorize the bot and send requests to the Bot API. Keep your token secure and store it safely, it can be used by anyone to control your bot.

Unlike the bot’s name, the username cannot be changed later – so choose it carefully.
When sending a request to api.telegram.org, remember to prefix the word ‘bot’ to your token.

Commands to manage bot:
/setabouttext - to specify short bio that will be available on bot's profile
/token - to generate a new token
/mybots - to transfer ownership of the bot. Select your bot, then transfer ownership. You can only transfer a bot to users who have interacted with it at least once. Transferring ownership will give full control of the bot to another user – they will be able to access the bot’s messages and even delete it. The transfer is permanent, so please consider it carefully
__________________________________________________________________________________________________________________________________________________
