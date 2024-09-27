import asyncio
import discord
import os
import random
import re
import requests

from quart import Quart, request
from discord.ext import tasks

server_url = "https://ss14.mira-sector.xyz"
status_channel = 1269720649589588019

ooc_channel = 1269794259574194257
ooc_url = "https://ooc.mira-sector.xyz"
ooc_password = os.environ["OOC_PASSWORD"]

discord_token = os.environ["DISCORD_TOKEN"]

intents = discord.Intents(messages=True, message_content=True, guilds=True)
client = discord.Client(intents=intents)

ooc_message = ""
event = asyncio.Event()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    update_status.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot:
        return

    response = message_response(message)

    if response:
        await message.channel.send(response)
        # no return as it hasnt been sent to ooc

    if message.channel.id != ooc_channel:
        return

    await ooc_send_ooc(message)

@tasks.loop(seconds = 120)
async def update_status():
    get_request = server_url + "/status"
    request = requests.get(get_request)

    if request.status_code == 200: # sucess YIPEEE
        name = request.json()["name"]
        players = request.json()["players"]
        maxplayers = request.json()["soft_max_players"]

        name = re.sub(r'\[.*?\]\ *', '', name)
        channel_name = name + "(" + str(players) + "/" + str(maxplayers) + ")"

        channel = client.get_channel(status_channel)
        await channel.edit(name = channel_name)

def message_response(message):
    # full message responses
    match message.content:
        case ":3":
            return ":3"
        case "graytide":
            return "robust"

    # partial message responses
    if re.match("(?i)based",message.content):
        if random.randint(1, 6) <= 3:
            return "based on what?"
        else:
            return "sigma even"

    if "1984" in message.content:
        return """"⠀⠀⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠤⠤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣟⠳⢦⡀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠉⠉⠉⠉⠉⠒⣲⡄
⠀⠀⠀⠀⠀⣿⣿⣿⡇ ⡱⠲⢤⣀⠀⠀⠀⢸⠀⠀⠀1984⠀⣠⠴⠊⢹⠁
⠀⠀⠀⠀⠀⠘⢻⠓⠀⠉⣥⣀⣠⠞⠀⠀⠀⢸⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⢸⠀
⠀⠀⠀⠀⢀⣀⡾⣄⠀⠀⢳⠀⠀⠀⠀⠀⠀⢸⢠⡄⢀⡴⠁2024⠀ ⡞⠀
⠀⠀⠀⣠⢎⡉⢦⡀⠀⠀⡸⠀⠀⠀⠀⠀⢀⡼⣣⠧⡼⠀⠀⠀⠀⠀⠀⢠⠇⠀
⠀⢀⡔⠁⠀⠙⠢⢭⣢⡚⢣⠀⠀⠀⠀⠀⢀⣇⠁⢸⠁⠀⠀⠀⠀⠀⠀⢸⠀⠀
⠀⡞⠀⠀⠀⠀⠀⠀⠈⢫⡉⠀⠀⠀⠀⢠⢮⠈⡦⠋⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀
⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⣀⡴⠃⠀⡷⡇⢀⡴⠋⠉⠉⠙⠓⠒⠃⠀⠀
⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⡼⠀⣷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡞⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢧⠀⠀⠀⠀⠀⠀⠀⠈⠣⣀⠀⠀⡰⠋⠀⠀⠀⠀⠀⠀"""

    return

async def ooc_send_ooc(message):
    name = message.author.name
    content = message.content

    # MoMMILink.cs OOCPostMessage
    ooc_message = { "password": str(ooc_password), "sender": str(name), "contents": str(content) }
    requests.post(server_url + "/ooc", json=ooc_message)
    return

# HTTP API
app = Quart(__name__)

@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await client.login(discord_token)
    loop.create_task(client.connect())

@app.route('/ooc',methods = ['POST'])
async def ooc_http():
    if request and request.method == 'POST':
        # MoMMILink.cs MoMMIMessageBase
        post_request = await request.get_json()
        request_content = post_request["contents"]

        # MoMMILink.cs MoMMIMessageBase
        name = request_content["sender"]
        content = request_content["contents"]

        if "@everyone" not in content:
            message = str(name) + ": " + str(content)
            channel = client.get_channel(ooc_channel)
            await channel.send(message)

    return str(ooc_message), 200

# some intern wrote this
# i have no idea what this does
if __name__ == '__main__':
    app.run()
