import discord
import os
import random
import time

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
intents.message_content = True

serverContext = {}  # joined users across servers

def get_substring(text):
    index = text.index("<")
    outdex = text.index(">")
    return "<" + text[index+1:outdex+1]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):

        if message.content.startswith("/startroulette"): # adds server id to the context list
            serverId = message.guild.id
            if(serverId in serverContext):
                serverContext[serverId].clear()
            else:
                serverContext[serverId] = []
            print("Server: ", serverId, " has started a roulette.")
            await message.channel.send("") # message to display when roulette is started

        if message.content.startswith("/joinroulette"):
            serverId = message.guild.id
            if(not(serverId in serverContext)): # checks if roulette was started in server
                return
            
            for id in serverContext[serverId]: # checks if user has already joined
                if id == message.author.id:
                    return
            serverContext[serverId].append(message.author.id)  # adds user to the server's roulette
            print(message.author.id, " has joined the roulette in server ", serverId)
            await message.channel.send("") # message to display when user joins roulette

        if message.content.startswith("/kick"):
            
            serverId = message.guild.id
            if(not(serverId in serverContext)): # checks if roulette was started in server
                return
            
            print("Users joined for kicking: ", serverContext[serverId])
            if len(serverContext[serverId]) > 0:
                await message.channel.send("") # message to display when roulette is executed
                destroyeeIndex = random.randint(0, len(serverContext[serverId])-1)
                destroyeeId = serverContext[serverId][destroyeeIndex]
                
                delayTime = random.randint(2,5)
                time.sleep(delayTime)
                user = message.guild.get_member(destroyeeId)
                print(destroyeeId)

                if(user == message.guild.owner): # special case for server owner
                    await message.channel.send("") # message to display when server owner was chosen (cannot be kicked)
                else:
                    inviteLink = await message.channel.create_invite(max_age = 300)
                    await message.channel.send("" + "<@" + str(user.id) + ">") # message to display before the kick with mentioning the chosen user

                    try:
                        await user.send(inviteLink)
                    except Exception as e:
                        print(e)
                    try:
                        await user.kick(reason=None)
                    except Exception as e:
                        print(e)                      

                del serverContext[serverId]
                print("Dictionary after clearing: ", serverContext)

        if message.content.startswith("/stoproulette"):
            serverId = message.guild.id
            if(not(serverId in serverContext)): # checks if roulette was started in server
                return

            del serverContext[serverId]
            print("Dictionary after stopping roulette: ", serverContext)
            await message.channel.send("") # message to display when roulette is stopped
            


client = MyClient(intents=intents)

client.run(TOKEN)