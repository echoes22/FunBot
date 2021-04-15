import discord
import os
import random
import asyncio


intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)


#global state and target variables
state = 0
target = None

@client.event
async def on_voice_state_update(member, before, after):
    """
    Main function, moves everyone but the target and sets a new one if state == 1.
    Called when a member changes their VoiceState.

    Parameters
    member (Member): Member whose voice states changed
    before (VoiceState): Voice State prior to the changes
    after (VoiceState): Voice state after the changes
    """
    if state != 0:
        if member.id == target.id:
            if after.channel is not None:
                await asyncio.sleep(1)
                await move_members(member, after.channel)
                if state == 1:
                    set_target(get_random_victim(member))

                  
async def move_members(member, current_channel):
    """
    Function used to move members one voice channel up

    Parameters
    member (Member): member who is to be moved
    current_channel (VoiceChannel): channel in which the member is located
    """
    this_index = member.guild.voice_channels.index(current_channel)
    vc_len = len((member.guild.voice_channels))
    if (this_index < (vc_len - 1)):
        target_channel = member.guild.voice_channels[this_index + 1]
    else:
        target_channel = member.guild.voice_channels[0]
    for member in member.voice.channel.members:
        if member != target:
            try:
                await member.move_to(target_channel)
            except:
                pass

     


def get_random_victim(member):
    """
    Function that chooses a new random victim from the member's voice channel

    Parameters:
    member (Member): target who is to be replaced
    """
    target_channel = member.voice.channel
    random_target = random.choice(target_channel.members)
    return random_target
       

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """
    Function that reacts to messages and sets the state and target (if state is 2)
    """
    #ignore messages from the bot itself
    if message.author == client.user:
        return

    #sets state to random (1)
    if message.content.startswith('$random'):
        set_target(get_random_victim(message.author))
        state_to_1()
        await move_members(message.author, message.author.voice.channel)
 
    #sets state to choose (2)
    if message.content.startswith('$choose') and len(message.mentions) == 1:
        set_target(message.mentions[0])
        state_to_2()
        await move_members(message.author, message.author.voice.channel) 
    
    #tool to check the state in the console
    if message.content.startswith('$state'):
        print('current state: ', state)
        print('current target: ', target)
    
   
def state_to_1():
    global state
    state = 1
    return state
    
def state_to_2():
    global state
    state = 2
    return state

def set_target(new_target):
    global target
    target = new_target
    return target



client.run(os.getenv('TOKEN'))