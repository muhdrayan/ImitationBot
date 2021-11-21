# Current Dicrectory
import os
curdir = os.getcwd()+"/"

# Imports
# Discord
import discord
from dotenv import load_dotenv

# Oth
import json
import time

# Discord API
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# Parameters
"""
Hey Rayan Can you do This Pls.
Database thingy.
- Two Tables

Dictionary or External Database (Not Table): All Info and Configuration Parameters
    - Prefix: ""
    - OthPersonId: ""
    - ImitationPersonId: ""
    - AutherizedTrainees: []
    - 
    - Dictionary of all the commands (from Discord-Bot.md) for [prefix.help]

Table 2: Recorded Data
    - Data is going be be in two colums
        - C1 Header: OthPersonName
        - C2 Header: ImitationPersonName

For testing now im making a variable for each of these values.
"""

with open(f"{curdir}NivedBot/discordbot/config.json") as f:
    CONFIG = json.load(f) 

@client.event
async def on_ready():
    print("Connected to Discord!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Globals
    global CONFIG

    prefix = CONFIG["PREFIX"]

    msg = message.content

    print(prefix)
    print(msg)
    print(msg[0:len(prefix)])

    iscmd = True if msg[0:len(prefix)+2] == f"!{prefix} " else False
    cmd = msg.split(" ")
    print(cmd)
    print(iscmd)
    if len(cmd)<=1:
        iscmd = False 
    del cmd[0]


    if iscmd:
        if cmd[0] == "config":
            try:
                if cmd[1] == "show":
                    # Show the config
                    await message.channel.send(CONFIG)

                elif cmd[1] == "prefix":
                    if cmd[2] == "show" or cmd[2] == "s":
                        await message.channel.send(f"""```
                        Prefix: {CONFIG['PREFIX']}\n
                        Other Person Id: {CONFIG['OTHPERSONID']}                    
                        ```""")
                        
                    elif cmd[2] == "change" or cmd[2] == "c":
                        await message.channel.send("Please enter the new Prefix")
                        CONFIG["PREFIX"] = await client.wait_for('message')
                        CONFIG["PREFIX"] = CONFIG["PREFIX"].content
                        await message.channel.send(f"Updated Prefix to **{CONFIG['PREFIX']}**")
                        
                elif cmd[1] == "othpersonid":
                    if cmd[2] == "show" or cmd[2] == "s":
                        await message.channel.send(CONFIG["OTHPERSONID"] if not CONFIG["OTHPERSONID"] == "" else "No Current User Id Specified")
                        
                    elif cmd[2] == "change" or cmd[2] == "c":
                        await message.channel.send("Please enter the new **User Id**")
                        CONFIG["OTHPERSONID"] = await client.wait_for('message')
                        try:
                            CONFIG["OTHPERSONID"] = int(CONFIG["OTHPERSONID"].content)
                            await message.channel.send(f"Updated User Id to **{CONFIG['OTHPERSONID']}**")
                        except ValueError:
                            await message.channel.send("Please enter a valid **USER ID**")


                elif cmd[1] == "imitationiersonid":
                    pass

                else:
                    await message.channel.send("Not a Valid SubCommand")

            except IndexError:
                await message.channel.send("No Valid SubCommand")

        elif cmd[0] == "terminate":
            # Anything that has to be done when the bot is shutdown
            with open(f"{curdir}discordbot/config.json", "w") as f:
                json.dump(CONFIG, f)
            await client.close()
            time.sleep(10)
            exit(1)

        elif cmd[0] == "give-role-friend":
            await message.channel.send("Please enter the **USER ID** of the person you want to give this role to.\nP.S. This command was made for testing and im lazy to remove it so ya.")
            userid = await client.wait_for('message')
            user = await message.guild.query_members(user_ids=[int(userid)]) # list of members with userid
            user = user[0] # there should be only one so get the first item in the list
            server = client.get_guild(911274711453925416)
            role = server.get_role(911489926783180860)
            
            await user.add_roles(role)



client.run(TOKEN)