import sys
import os
import discord
import simplejson as json
import flask
import utils
import ffmpeg
import asyncio
#import firebase_admin
#from google.cloud import storage
#from firebase_admin import credentials
#from firebase_admin import storage
#add these vvv when doing firebase
#firebase_admin
#google-cloud==0.34.0
from keep_alive import keep_alive

#cred = credentials.Certificate(json.loads(os.environ.get("firebaseAuth")))
#firebase_admin.initialize_app(cred,{"storageBucket":"dadbot-a840b.appspot.com"})
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
#stopAllAudio = "execute order 66"
testStopKey = "start"

#can I do pings to servers?

@client.event
async def on_ready():
  game = discord.Game("Daddy's Home")
  await client.change_presence(activity=game)
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
      await message.channel.send(f"Available commands are: '!meme', '!airhorn', '!cena', 'playcave', '!rtd,'!rtd lower,upper', '/roll xdn', 'swansong', 'help'\nYou can stop audio playback by adding the :stop_button: reaction")
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

'''
@client.event
async def on_reaction_add(reaction, user):
'''



token = os.environ.get("dadToken")
client.run(token)

'''
NEXT UP:
get git functionality up and running
let user send sound requests to dadbot directly
#kill me and the women and the children
fix "try/except" in makeLemonade
Add time spent functionality
Add play with me/play with x functionality to change status/game
dont let "him" trigger dadjoke even though it ends with "im"
'''