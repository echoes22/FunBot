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
target = None
state = 0

try:
    f = open('state', 'x')
    f.close()
except:
    print('state has already been created')

    



    


@client.event
async def on_voice_state_update(member, before, after):
    if state == 0:
        return
    if state == 1:
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
        state_to_1()
        f = open('state', 'w')
        f.write(f"1\n{random_target}")
        f.close()
    
    if message.content.startswith('$state'):
        print('current state: ', state)
    
    if message.content.startswith('$choose') and len(message.mentions) == 1:
        set_target(message.mentions[0])
        state_to_2()
        
def state_to_1():
    global state
    state = 1
    print('state to: ', state)
    return state
    
def state_to_2():
    global state
    state = 2
    print('state to: ', state)
    return state

def set_target(new_target):
    global target
    target = new_target
    print('new target: ', new_target)
    return target


print('state global: ', state)

client.run(os.getenv('TOKEN'))