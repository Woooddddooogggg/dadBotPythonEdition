import sys
import os
import discord
import simplejson as json
import flask
import utils
import ffmpeg
import asyncio
from keep_alive import keep_alive

client = discord.Client()

swansonQuoteKey = "swansong"
needAdultKey = "i need an adult"
dadNameJokeKey = ["i'm ","im "]
helpKey = "help"
rtdKey = "!rtd"
timeSpentKey = "time spent"
rollDiceKey = "/roll"
caveKey = "playcave"
memekey = "!meme"
airhornKey = "!airhorn"
cenaKey = "!cena"
playWithKey = "<@349722474365190144> play with "

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game("Daddy's Home"))
  for guild in client.guilds:
    member = guild.get_member(349722474365190144)
    if member.voice is not None:
      resumedVoiceClient = await client.get_channel(member.voice.channel.id).connect(reconnect = True)
      await resumedVoiceClient.disconnect()
  print("There are no strings on me")

@client.event
async def on_message(message):
  cleanMessage = message.content.lower()
  if message.author != client.user:
    if swansonQuoteKey in cleanMessage:
      await message.channel.send(await utils.sendSwansonQuote())
    if any(x in cleanMessage for x in dadNameJokeKey):
      await message.channel.send(await utils.makeDadNameJoke(cleanMessage))
    if needAdultKey in cleanMessage:
      await message.channel.send("Adults are just as lost as you are. Have faith in yourself and what you can do.")
    if helpKey in cleanMessage:
      await message.channel.send(f"Available commands are: 'play with @mention or me', !meme', '!airhorn', '!cena', 'playcave', '!rtd,'!rtd lower,upper', '/roll xdn', 'swansong', 'help'\nYou can stop audio playback by adding the :stop_button: reaction")
      #NOTE you can probably use a dictionary for this so you don't have to manually update the known commands every time
    if rtdKey in cleanMessage:
      await message.channel.send(await utils.rollTheDice(cleanMessage))
    if timeSpentKey in cleanMessage:
      await utils.timeSpent(cleanMessage)
      #don't forget to come back to this
    if rollDiceKey in cleanMessage:
      rolls = await utils.rollSpecifiedDice(cleanMessage)
      for item in rolls:
        await message.channel.send(rolls[item])
    if caveKey in cleanMessage:
      asyncio.create_task(utils.makeLemonade(client, message, "C:\\Users\\Wooody\\Documents\\Development\\dadBotPython\\audioSources\\caveQuotes\\"))
    if memekey in cleanMessage:
      asyncio.create_task(utils.makeLemonade(client, message, "C:\\Users\\Wooody\\Documents\\Development\\dadBotPython\\audioSources\\memes\\"))
    if airhornKey in cleanMessage:
      asyncio.create_task(utils.makeLemonade(client, message, "C:\\Users\\Wooody\\Documents\\Development\\dadBotPython\\audioSources\\memes\\mlg-airhorn.mp3"))
    if cenaKey in cleanMessage:
      asyncio.create_task(utils.makeLemonade(client, message, "C:\\Users\\Wooody\\Documents\\Development\\dadBotPython\\audioSources\\memes\\JOHN CENA.mp3"))
    if playWithKey in cleanMessage:
      asyncio.create_task(utils.setDadGame(message, client))

@client.event
async def on_member_update(before, after):
  status = str(after.status).lower()
  if after.display_name in str(discord.utils.get(client.get_all_members(), name = client.user.name).activity) and (status is not "online" or status is not "idle"):
    await client.change_presence(activity=discord.Game("Daddy's Home"))


token = os.environ.get("dadToken")
client.run(token)

'''
NEXT UP:
let user send sound requests to dadbot directly
fix "try/except" in makeLemonade
Add time spent functionality
dont let "him" trigger dadjoke even though it ends with "im"
'''