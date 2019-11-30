import os
import simplejson as json
import discord
import requests
import re
import random
import ffmpeg
import asyncio

async def sendSwansonQuote():
  try:
    response = requests.get("http://ron-swanson-quotes.herokuapp.com/v2/quotes")
    return(json.loads(response.content)[0])
  except Exception as e:
    print(e)

async def makeDadNameJoke(message):
  cleanMessage = message.replace("im","i'm")
  dadJokeName = cleanMessage[cleanMessage.find("i'm")+3:(len(cleanMessage))]
  replyMessage = f"Hi{dadJokeName}, I'm dad!"
  return replyMessage

async def timeSpent(message):
  #this does nothing right now
  try:
    response = requests.get("https://wol.gg/stats/na/doctordinosaur/")
  except Exception as e:
    print(e)

async def rollTheDice(message):
  hasRange = re.search("(\!rtd (\d*),(\d*))", message)
  if hasRange:
    if int(hasRange[2]) > int(hasRange[3]):
      return f"Your lower bound \"{hasRange[2]}\" was greater than your upper bound \"{hasRange[3]}\"."
    else:
      return random.randint(int(hasRange[2]), int(hasRange[3]))
  else:
    randLower = random.randint(-10000, 10000)
    randUpper = random.randint(randLower, 10000)
    return random.randint(randLower, randUpper)
  
async def rollSpecifiedDice(message):
  roll = 0
  rollTotal = 0
  rollSummary = dict()
  rollSummary["rollHistory"] = []
  rollSummary["rollTotal"] = ""
  parsedMessage = re.search("(\/roll ((\d*d\d*)|(\d* d \d*)))", message)

  if parsedMessage:
    numSides = re.search("(d|d )(\d{1,})", parsedMessage[0])[2]
    numRolls = re.search("((\d{1,})(d| d))", parsedMessage[0])[2] if re.search("((\d{1,})(d| d))", parsedMessage[0]) is not None else 1

    if int(numRolls) > 100:
      rollSummary["rollTotal"] = f"I\'m not doing more than 100 rolls. Go ask your mother."
      rollSummary.pop("rollHistory")
      return rollSummary
    else:
      if 1 < int(numRolls) <= 10:
        while roll < int(numRolls):
          rollValue = random.randint(1, int(numSides))
          rollTotal = rollTotal + int(rollValue)
          rollSummary["rollHistory"].append(rollValue)
          roll += 1
        rollSummary["rollTotal"] = f"Roll total: {rollTotal}"
        return rollSummary
      else:
        while roll < int(numRolls):
          rollValue = random.randint(1, int(numSides))
          rollTotal = rollTotal + int(rollValue)
          roll += 1
        rollSummary["rollTotal"] = f"Roll total: {rollTotal}"
        rollSummary.pop("rollHistory")
        return rollSummary

async def makeLemonade(client, message, dirOrFile):
  sourcePath = dirOrFile if os.path.isfile(dirOrFile) else f"{dirOrFile}{random.choice(os.listdir(dirOrFile))}"
  print(f"Soure Path: {sourcePath}")
  audio_source = discord.FFmpegPCMAudio(sourcePath)
  voiceChannel = await getChannelToSend(message).connect()
  voiceChannel.play(audio_source, after=lambda e: print('done', e))

  def lookForStopRequest(reaction, user):
    return reaction.emoji == u"\u23F9"
    
  try:
    reaction, user = await client.wait_for('reaction_add', timeout=5, check=lookForStopRequest)
  except asyncio.TimeoutError:
    #await message.channel.send('👎')
    print(f"No Cancellation")
  else:
    await voiceChannel.disconnect()

  while voiceChannel.is_playing():
    continue
  await voiceChannel.disconnect()

def getChannelToSend(message):
  if message.author.voice is not None:
    return message.author.voice.channel
  else:
    try:
      channelToUse = ""
      voiceMemberCount = 0
      for channel in message.guild.voice_channels:
        print(channel.Id)
        if len(channel.members) > voiceMemberCount:
          channelToUse = channel
          voiceMemberCount = len(channel.members)
      if channelToUse is not None:
        return channelToUse
        #thiis except is doing nothing
    except Exception as e:
      message.channel.send(f"Hey, uhhh hi")

async def setDadGame(message, client):
  potentialMemberId = re.search("(<@349722474365190144> play with )(<@(\d*)>)", message.content)
  childAsMember = None
  if re.search("(<@349722474365190144> play with )(me)", message.content):
    childAsMember = message.author
  elif potentialMemberId:
    childAsMember = discord.utils.get(message.guild.members, id = int(potentialMemberId.group(3))) 
  else:
    await message.channel.send("That's not my kid. Make sure to use @mention or 'me'")
  if childAsMember is not None:
    if str(childAsMember.status).lower() == "online" or childAsMember.status == "idle":
      await client.change_presence(activity=discord.Game(f"with {childAsMember.display_name}"))
    else:
      await message.channel.send("I'm not waking the kids up. (they're not online)")