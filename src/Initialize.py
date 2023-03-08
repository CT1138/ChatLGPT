import discord, openai
def init(data):
    #log in to OpenAI and Discord.py
    openai.api_key = data["davinci"]
    
    intents = discord.Intents.all()
    intents.members = True
    client = discord.Bot(intents=intents)

    #Send a message when the bot is connected
    @client.event
    async def on_ready():
        print(f"{client.user} is connected.")
    return client