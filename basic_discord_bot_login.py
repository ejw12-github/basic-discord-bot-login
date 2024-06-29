# |---------------------------------------------------------------------------------------|
# |                                                                                       |                  
# | Thanks for downloading the Basic Discord Bot Login program!                           | 
# |                                                                                       |
# | This is a simple bot login program designed to be easy to use.                        |
# |                                                                                       |
# | Support: Contact @ejw12 on Discord                                                    |
# |                                                                                       |
# | IMPORTANT: You must have Discord.py on your computer!                                 |
# |  - To install it, run "pip install discord.py" in the terminal                        |
# |                                                                                       |
# | NOTE: You must have the following intents enabled:                                    |
# |  - Server Members Intent                                                              |
# |  - Presence Intent                                                                    |
# |  - Message Content Intent                                                             |   
# |                                                                                       |
# | TIP: For a redirect url in 0Auth2, use:                                               |
# |  - "https://discordapp.com/oauth2/authorize?&client_id=[INSERT CLIENT ID]&scope=bot"  |
# |                                                                                       |
# | Thanks again for downloading!                                                         |
# |                                                                                       |
# |---------------------------------------------------------------------------------------|


import discord
import asyncio

intents = discord.Intents.default()
intents.messages = True
bot = discord.Client(intents=intents)

token = "[INSERT TOKEN HERE]"

target_channel_id = None
target_user_id = None

async def send_message():
    global target_channel_id, target_user_id
    await bot.wait_until_ready()
    
    target_type = input("Would you like to send the message to a channel or a user? ('channel' or 'user': ").strip().lower()
    
    if target_type not in ['channel', 'user']:
        print("Invalid choice. Please restart the program and type 'channel' or 'user'.")
        return

    if target_type == 'channel':
        channel_id = input("Please provide the channel ID: ").strip()
        try:
            channel = bot.get_channel(int(channel_id))
            if not channel:
                print("Invalid channel ID.")
                return
            target_channel_id = int(channel_id)
        except ValueError:
            print("Invalid channel ID format.")
            return

        print("Please enter your message line by line. Type '%STOP-MESSAGE%' to end.")
        message_lines = []
        while True:
            line = input()
            if line == '%STOP-MESSAGE%':
                break
            message_lines.append(line)
        
        for line in message_lines:
            await channel.send(line)
        
        print("Messages sent successfully.")

    elif target_type == 'user':
        user_id = input("Please provide the user ID: ").strip()
        try:
            user = await bot.fetch_user(int(user_id))
            target_user_id = int(user_id)
        except ValueError:
            print("Invalid user ID format.")
            return
        except discord.NotFound:
            print("User not found.")
            return

        print("Please enter your message line by line. Type '%STOP-MESSAGE%' to end.")
        message_lines = []
        while True:
            line = input()
            if line == '%STOP-MESSAGE%':
                break
            message_lines.append(line)

        for line in message_lines:
            await user.send(line)
        
        print("Messages sent successfully.")

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    asyncio.create_task(send_message())

@bot.event
async def on_message(message):
    global target_channel_id, target_user_id
    if message.author == bot.user:
        return
    
    if target_channel_id and message.channel.id == target_channel_id:
        print(f"Message from {message.author}: {message.content}")
    elif target_user_id and message.author.id == target_user_id:
        print(f"Message from {message.author}: {message.content}")

bot.run(TOKEN)