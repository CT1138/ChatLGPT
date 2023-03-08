import Modules.Models as Models, Modules.Media as Media, Modules.Messages as Messages, Modules.Chat as Chat,Initialize, discord, json, csv
from discord import option
with open("./Data/Token.json", "r") as f:
    data = json.load(f)
with open('./Data/Models.json', 'r') as f:
    model_data = json.load(f)
AImodel = [model['id'] for model in model_data]


#Initialize
client = Initialize.init(data)


# Thread listener
@client.event
async def on_message(message):
     return


###Run our command handler
#/ping
@client.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {client.latency}")

#/chat <query>
@client.slash_command(description="OpenAI chatbot Integration.")
@option("query", description="What would you like to talk about?")
async def chat(ctx: discord.ApplicationContext, query: str):
  await Chat.chat(ctx, query)

#/gpt <query> <model>
@client.slash_command(description="OpenAI chatbot Integration.")
@option("query", description="Your message to the bot")
async def gpt(ctx: discord.ApplicationContext, query: str):
  Models.generate_response(ctx, query)

#/info <model>
@client.slash_command(description="Info on the AI models compatible with /gpt.")
@option("model", description="Choose your AI model", choices=AImodel)
async def info(ctx: discord.ApplicationContext, model: str):
  await Models.info(ctx, model, model_data)

#/draw <query>
@client.slash_command(description="Dall-E image generation.")
@option("query", description="What would you like me to draw?")
async def draw(ctx: discord.ApplicationContext, query: str):
  await Models.dalle(ctx, query)

#/reddit images <subreddit> <quantity>
@client.slash_command(description="Pull images from a subreddit.")
@option("subreddit", description="What subreddit to scrape from? (case sensitive)")
@option("quantity", description="How many images to download? (Maximum 6)")
async def images(ctx: discord.ApplicationContext, subreddit: str, quantity: int):
  await Media.images(ctx, subreddit, quantity)

#/reddit video <subreddit> <quantity>
@client.slash_command(description="Pulls a video from a subreddit.")
@option("subreddit", description="What subreddit to scrape from? (case sensitive)")
@option("quantity", description="How many videos to download? (Maximum 6)")
async def videos(ctx: discord.ApplicationContext, subreddit: str, quantity: int):
  await Media.reddit_video_main(ctx, subreddit, quantity)

#/purge
@client.slash_command(description="Clears all messages.")
async def purge(ctx, channel: discord.TextChannel):
  await Messages.purge(ctx, channel)

# Start the bot
client.run(data["discord"])
