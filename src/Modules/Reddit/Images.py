import discord
import requests
import random
from PIL import Image
from io import BytesIO


#Images
async def images_scalp(subreddit_name, ctx, limit=1000):
    """This function collects the images from the specified subreddit"""

    headers = {'User-Agent': 'GPT-Sama!/0.0.1'}
    url = f'https://www.reddit.com/r/{subreddit_name}/new.json?limit={limit}'
    res = requests.get(url, headers=headers)
    posts = res.json()['data']['children']

    collected_images = []
    for post in posts:
        image_url = post['data']['url']
        if image_url.endswith('.jpg') or image_url.endswith('.png'):
            collected_images.append({
                'title': post['data']['title'],
                'url': image_url
            })

    if collected_images == []: await ctx.respond("I couldn't find any images.")
    return collected_images

async def images_upload(ctx, images):
    """This takes the collected images, compiles them, and uploads them"""

    max_images = len(images)
    num_images = min(max_images, 6)

    # Create a blank image to compile the selected images into
    output = Image.new('RGB', (num_images * 800, 800), (random.randint(0, 155) + 25, random.randint(0, 222) + 100, random.randint(0, 422) + 50))

    # Download and add each selected image to the blank image
    for i, image in enumerate(random.sample(images, num_images)):
        response = requests.get(image['url'])
        img = Image.open(BytesIO(response.content))
        img.thumbnail((800, 800))
        output.paste(img, (i * 800, 0))

    # Convert the compiled image to bytes and send it
    buffer = BytesIO()
    output.save(buffer, format='PNG')
    buffer.seek(0)
    file = discord.File(buffer, filename='compiled_image.png')
    
    print(f"[Reddit Video] Subreddit: {input}")
    await ctx.respond(file=file)

async def images(ctx, input, quantity):
    """Our main entrypoint for the command"""
    await ctx.defer()
    subreddit_name = input.strip().lower()
    # Print the answer to the console
    images = await images_scalp(subreddit_name, ctx)

    # Randomly select and upload the specified number of images
    num_images = min(len(images), quantity)
    selected_images = random.sample(images, num_images)
    await images_upload(ctx, selected_images)