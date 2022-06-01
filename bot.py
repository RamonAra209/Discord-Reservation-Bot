import asyncio
from multiprocessing.connection import wait
import subprocess
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import date, datetime, timedelta
from constants import NUM_EMOJIS
from functions import NOW, ceil_dt, check_output_from_reserve, find_last_time_of_day, get_time_slots, times_between_xy
import json

load_dotenv("info.env")
TOKEN = os.getenv('DISCORD_TOKEN')
# PATH_TO_RESERVE = "/Users/tahpramen/Developer/Personal\ Projects/LRT_V2/main.py"
PATH_TO_RESERVE = "/home/tahpramen/Developer/Library-Reservation-Tool-V2/main.py"

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='-', intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} is connected to guilds:")
    active_servers = client.guilds
    for guild in active_servers:
        print("\t", guild.name)

@client.command()
async def reserve(ctx):
    users_json = None
    with open('users.json') as f:
        users_json = json.load(f)

    if str(ctx.author) in users_json:
        last_time_of_day_dt_obj = find_last_time_of_day(get_time_slots())
        print(NOW)
        if last_time_of_day_dt_obj == None:
            await ctx.send("Can't reserve a room, since theres no more room available for today!")
            return
        
        list_of_times = times_between_xy(ceil_dt(dt=datetime(NOW.year, NOW.month, NOW.day, hour=NOW.hour, minute=NOW.minute, second=NOW.second),
                                delta=timedelta(minutes=30)), last_time_of_day_dt_obj)
        str_of_times = [str(i).split(' ')[1] for i in list_of_times]
        str_of_times = [f"{str(i)} {list_of_times[i]}" for i in range(len(list_of_times))]
        
        time_dict = {}
        for i in range(len(str_of_times)):
            split = str_of_times[i].split(' ')
            if i >= 11:
                break
            time_dict[split[0]] = split[2]
            
        for i, val in time_dict.items():
            print(i, val)

        str_to_print = ""
        for key, val in time_dict.items():
            str_to_print += f"{NUM_EMOJIS[int(key)]} {val}\n"
         
        message = await ctx.send(f"{ctx.author.mention} React to two time slots, and press check mark when ready, or X to cancel. Remember you can only schedule in 3 hour blocks per library rules\n{str_to_print}") 
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
            return

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
        
        database = None
        with open('users.json') as f:
            database = json.load(f)
        database.update(user_dict)
        with open('users.json', 'w') as f:
            json.dump(database, f, indent=4, separators=(", ", ": "), sort_keys=True)

        await user_dm.send("Successfully added you to the database. If at any point you messed up, call '-deleteme' in the discord server and repeat the steps. Or if you just don't want to be in the database, then that's okay too. \n\nNow go back to the server and call '-reserve' again to complete the reservation!")

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
#           print("TIMES")
#           for i in sent_message:
#               print(i)
            times_selected = []
#            print()
            for react in reaction.message.reactions:
                if react.count > 1:
                    for i in sent_message: 
                        if react.emoji in i:
                            times_selected.append(i.split(' ')[-1])
            await reaction.message.clear_reactions()
            await reaction.message.channel.send(f"Making the reservation between {times_selected[0]} and {times_selected[-1]}! Check your email for confirmation!") #! add times selected to print
            print(times_selected)
            
            output = subprocess.check_output(f"python3 {PATH_TO_RESERVE} {times_selected[0]} {times_selected[-1]} {user}", shell=True)
            print(output)
            with open('log.txt', 'a') as f:
                f.write(f"{NOW} - {user}: {times_selected[0]} to {times_selected[-1]}\n")
                f.close()

@client.command()
async def deleteme(ctx):
    database:dict = None
    with open('users.json') as f:
        database = json.load(f)

    database.pop(str(ctx.author))
    
    with open('users.json', 'w') as f:
        json.dump(database, f, indent=4, separators=(", ", ": "), sort_keys=True)

    await ctx.send("Deleted you from database!")
    

client.run(TOKEN)
