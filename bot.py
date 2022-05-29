import asyncio
from multiprocessing.connection import wait
import subprocess
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import date, datetime, timedelta
from constants import NUM_EMOJIS
from functions import END_TIME, NOW, ceil_dt, check_output_from_reserve, times_between_xy
import json

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
    print(ctx.author, type(ctx.author))

    users_json = None
    with open('users.json') as f:
        users_json = json.load(f)

    if str(ctx.author) in users_json:
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
    else:
        await ctx.send(f"{ctx.author.name}, you're not in the database, check your DMs!")
        user_dm = await ctx.author.create_dm()
        await user_dm.send("**FOR LEGAL PURPOSES I WILL NEVER SHARE YOUR DATA**\nHow do you want me to reserve you a room if you're not in the database? Answer these next questions so I can add you!")

        first = None
        last = None
        user_id = None
        user_email = None
        
        def check(message):
            return message.author == ctx.author
        try:
            await asyncio.sleep(2)
            await user_dm.send("Whats your first name?")
            first = await client.wait_for('message', timeout=60, check=check)
            # await asyncio.sleep(0.75)

            await user_dm.send("Whats your last name?")
            last = await client.wait_for('message', timeout=60, check=check)
            # await asyncio.sleep(0.75)

            await user_dm.send("Whats your 989 number?")
            user_id = await client.wait_for('message', timeout=60, check=check)
            # await asyncio.sleep(0.75)

            await user_dm.send("Whats your student email?")
            user_email = await client.wait_for('message', timeout=60, check=check)
            # await asyncio.sleep(0.75)
        except asyncio.TimeoutError:
            await user_dm.send("You ran out of time to answer!")

        first = str(first.content)
        last = str(last.content)
        user_id = str(user_id.content)
        user_email = str(user_email.content)

        user_dict = {str(ctx.author): {
                        "first_name": first,
                        "last_name": last,
                        "email": user_email,
                        "univ_id": user_id 
                        }
                    } 
        
        data = None
        with open('users.json') as f:
            data = json.load(f)
        data.update(user_dict)
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4, separators=(", ", ": "), sort_keys=True)
        
        await user_dm.send("Successfully added you to the database. If at any point you messed up, call '-delete_me' in the discord server and repeat the steps. Or if you just don't want to be in the database, then that's okay too.")

@client.event
async def on_reaction_add(reaction, user):
    # TODO Add a check that only counts the emojis added by person who invoked -reserve
    #? reaction.me might help for reaction check add
    if user.bot == False:
        if reaction.emoji == '\U0000274C': # if X emoji
            await reaction.message.channel.send(f"Cancelled the reservation process!")
            await reaction.message.clear_reactions()
        elif reaction.emoji == '\U00002705':
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
            await reaction.message.channel.send(f"Making the reservation between {times_selected[0]} and {times_selected[-1]}! Check your email for confirmation!") #! add times selected to print
            print(times_selected)

            print(user)
            now = datetime.now()
            nearest_thirty = ceil_dt(now, timedelta(minutes=30))

            output = subprocess.check_output(f"{PATH_TO_RESERVE} {times_selected[0]} {times_selected[-1]} {user}", shell=True)
            # await reaction.channel.send(f"Result from calling reservation: {str(output)}")
            # if check_output_from_reserve(output) == False:
            #     await reaction.channel.send(f"{reaction.message.author.name} you fuck, you're not in the database, add yo shit. (check your DMs!)")
            #     user_channel = await user.create_dm()
            #     await user_channel.send("How do you want me to reserve you a room if you're not in the database?")
            #     await user_channel.send("Answer these next few questions so I can add you!")
            #     await user_channel.send("TODO")
            # else:
            #     times_to_print = times_between_xy(nearest_thirty)
            #     str_of_times = [str(i).split(' ')[1] for i in times_to_print]
            #! MAKE RESERVATION HERE WITH SUBPROCESS CALL

client.run(TOKEN)