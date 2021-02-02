import discord
import os
import random
from replit import db 


intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

victim_test = 178997121737949184
target_id = 229060723550978051

try:
    f = open('state', 'x')
    f.close()
except:
    print('state has already been created')

    



    


@client.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        if member.id == target_id:
            if before.channel != after.channel:
                this_index = member.guild.voice_channels.index(after.channel)
                vc_len = len(member.guild.voice_channels)
                if this_index < vc_len - 1:
                    target_channel = member.guild.voice_channels[this_index + 1]
                else:
                    target_channel = member.guild.voice_channels[0]
                for member in member.voice.channel.members:
                    if member.id != target_id:
                        try:
                            await member.move_to(target_channel)
                        except:
                            pass
    return


        

# @client.event
# async def on_voice_state_update(member, before, after):
#     if member.id == victim_test:

#         print('member.id == victim_test: ', member.id == victim_test)

#         if before.channel != after.channel:
#             print('before.channel is None and after.channel is not None:', before.channel is None and after.channel is not None)

#             this_channel = after.channel

#             for i in range(len(member.guild.voice_channels)):
#                 if member.guild.voice_channels[i] == this_channel:
                 

#                     if i < len(member.guild.voice_channels):
#                         target_channel = member.guild.voice_channels[i+1]
#                     else:
#                         target_channel = member.guild.voice_channels[0]

             


#                     for member in member.guild.voice_channels[i].members:
#                         print('member name: ', member.name)
#                         print('member.id != victim_test: ', member.id != victim_test)
#                         if member.id != victim_test:
#                             print('member to move: ', member)
#                             await member.move_to(target_channel)
           
#     return

def get_victim(message):
    troller = message.author
    target_channel = troller.voice.channel
    random_target = random.choice(target_channel.members)
    print('target_channel: ', target_channel)
    print('random_target: ', random_target)
    return random_target
       

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    try:
        f = open('state', 'w')
        f.write('0\nNone')
        f.close()
    except:
        pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        print(message.author.voice)

        await message.channel.send('Hello!')

    if message.content.startswith('$random'):
        random_target = get_victim(message)
        f = open('state', 'w')
        f.write(f"1\n{random_target}")
        f.close()
        
    
    if message.content.startswith('$choose') and len(message.split()) == 2:
        f = open
        

    
    #if message.content.startswith('$connect'):
    #    first_channel = message.channel.guild.voice_channels[0]
    #    await first_channel.connect(timeout=10.0, reconnect=True)

client.run(os.getenv('TOKEN'))