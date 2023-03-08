import discord, openai, csv
thread_counter = 0

def generate_response(query):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            max_tokens=1800,
            n=1,
            stop=["Me:"],
            temperature=0.9,
        )
        message = response.choices[0].text.strip()
        print(f"[Davinci] Query: {query[:20]}...\nResponse: {message[:20]}...")
        return message

#Image Model
async def dalle(ctx, input):
  await ctx.defer(); 
  try:
    response = openai.Image.create(
    prompt=f"{input}",
    n=1,
    size="1024x1024"
  )
  except Exception:
    await ctx.respond(f"An error occured, make sure your query is not NSFW and try again.")
    return

  image_url = response['data'][0]['url']
  print(f"[Dall-E] Query: {input[:20]}...\nImage URL: {image_url}")

  embed = discord.Embed(title=input[:256], description="Processed Image:", color=0xd90f9a)
  embed.set_image(url=image_url)
  embed.set_footer(text="Powered by OpenAI DALL-E.")
  embed.set_author(name=ctx.author)

  await ctx.respond(embed=embed)

async def info(ctx, input, model_data):
  await ctx.defer()
  for model in model_data:
    if input in model['id']:
        
        embed=discord.Embed(title=model['name'], url=model['url'], description=model['description'], color=0xd90f9a)
        embed.set_thumbnail(url="https://openai.com/content/images/2022/05/openai-avatar.png")
        embed.add_field(name="Type", value=model['type'], inline=True)
        embed.add_field(name="Version", value=model['version'], inline=True)
        embed.set_footer(text=f"Price per query: {model['cost']} per 1k tokens")
        await ctx.respond(embed=embed)

        print(f"[Dall-E] Query: {input[:20]}")
        return