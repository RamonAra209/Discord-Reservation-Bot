from multiprocessing.connection import wait
import subprocess
import sys
import os
import time
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import date, datetime, timedelta
from constants import NUM_EMOJIS
from functions import END_TIME, NOW, ceil_dt, check_output_from_reserve, times_between_xy

load_dotenv("info.env")
TOKEN = os.getenv('DISCORD_TOKEN')
PATH_TO_RESERVE = "python3 /Users/tahpramen/Developer/Personal\ Projects/LRT_V2/main.py"

intents = discord.Intents.default()
intents.members = True
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='-', intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} is connected to guilds")
    active_servers = client.guilds
    for guild in active_servers:
        print(guild.name)
    print()

@client.command()
async def reserve(ctx):
    now = datetime.now()
    nearest_thirty = ceil_dt(now, timedelta(minutes=30))

    await ctx.send(f"{ctx.channel}: {ctx.author}")
    output = subprocess.check_output(f"{PATH_TO_RESERVE} 12:00:00 14:00:00 {ctx.author}" , shell=True)
    await ctx.send(f"Result from calling reservation: {str(output)}")
    if check_output_from_reserve(output) == False:
        await ctx.send(f"{ctx.author.name} you fuck, you're not in the database, add yo shit. (check your DMs!)")
        user_channel = await ctx.author.create_dm()
        await user_channel.send("How do you want me to reserve you a room if you're not in the database?")
        await user_channel.send("Answer these next few questions so I can add you!")
        await user_channel.send("TODO")
    else:
        times_to_print = times_between_xy(nearest_thirty)
        str_of_times = [str(i).split(' ')[1] for i in times_to_print]

@client.command()
async def emoji(ctx):
    channel = ctx.channel
    list_of_times = times_between_xy(ceil_dt(dt=datetime(NOW.year, NOW.month, NOW.day, hour=16, minute=00, second=0),
                            delta=timedelta(minutes=30)))
    str_of_times = [str(i).split(' ')[1] for i in list_of_times]
    str_of_times = [f"{str(i)} {list_of_times[i]}" for i in range(len(list_of_times))]

    time_dict = {}
    for i in str_of_times:
        split = i.split(' ')
        time_dict[split[0]] = split[2]

    str_to_print = ""
    for key, val in time_dict.items():
        str_to_print += f"{NUM_EMOJIS[int(key)]} {val}\n"
    
    message = await ctx.send(f"↓↓↓{ctx.author.mention} React to two time slots, and press check mark when ready↓↓↓ \n{str_to_print}") 
    for key in time_dict.keys():
        await message.add_reaction(NUM_EMOJIS[int(key)])
    await message.add_reaction("\U0000274C") # X Emoji
    await message.add_reaction("\U00002705") # Check mark emoji

@client.event
async def on_reaction_add(reaction, user):
    # TODO Add a check that only counts the emojis added by person who invoked -reserve
    #? reaction.me might help for reaction check add
    if user.bot == False:
        if reaction.emoji == '\U0000274C': # if X emoji
            await reaction.message.channel.send(f"Cancelled the reservation process!")
            await reaction.message.clear_reactions()
        elif reaction.emoji == '\U00002705':
            await reaction.message.channel.send(f"Making the reservation!") #! add times selected to print
            sent_message:str = (reaction.message.content).split('\n')[1:] 
            print("TIMES")
            for i in sent_message:
                print(i)
            times_selected = []
            print()
            for react in reaction.message.reactions:
                if react.count > 1:
                    for i in sent_message: 
                        if react.emoji in i:
                            times_selected.append(i.split(' ')[-1])
            await reaction.message.clear_reactions()
            print(times_selected)
client.run(TOKEN)