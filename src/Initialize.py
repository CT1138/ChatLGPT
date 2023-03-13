import discord, openai
from discord import Status, Activity, ActivityType
import Modules.Models as Models

def init(data):
    """This function logs into our two main API's"""
    # Sets the API key for OpenAI
    openai.api_key = data["davinci"]
    
    # Logging into the Discord API
    intents = discord.Intents.all()
    intents.members = True

    status = Models.completions("Give me a random news headline.")
    activity = discord.Activity(name=status, type=discord.ActivityType.custom)

    client = discord.Bot(intents=intents, activity=activity)
    
    # Provide some feedback so we know the bot has connected
    @client.event
    async def on_ready():
        print(f"{client.user} is connected.")
    return client