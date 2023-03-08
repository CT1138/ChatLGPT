import discord
import requests
import random
from PIL import Image
from io import BytesIO

#Images
async def images_scalp(subreddit_name, ctx, limit=1000):
    print("[Reddit] Collecting Images")
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
    print("[Reddit] Uploading")
    max_images = len(images)
    num_images = min(max_images, 6) # maximum number of images to compile

    # Create a blank image to compile the selected images into
    output = Image.new('RGB', (num_images * 200, 200), (random.randint(0, 220) + 25, random.randint(0, 155) + 100, random.randint(0, 205) + 50))

    # Download and add each selected image to the blank image
    for i, image in enumerate(random.sample(images, num_images)):
        response = requests.get(image['url'])
        img = Image.open(BytesIO(response.content))
        img.thumbnail((200, 200))
        output.paste(img, (i * 200, 0))

    # Convert the compiled image to bytes and send it
    buffer = BytesIO()
    output.save(buffer, format='PNG')
    buffer.seek(0)
    file = discord.File(buffer, filename='compiled_image.png')
    await ctx.respond(file=file)

async def images(ctx, input, quantity):
    ctx.defer()
    subreddit_name = input.strip().lower()
    # Print the answer to the console
    print(f'[Reddit] {ctx.author} is scanning "{subreddit_name}"')
    images = await images_scalp(subreddit_name, ctx)

    # Randomly select and upload the specified number of images
    num_images = min(len(images), quantity)
    selected_images = random.sample(images, num_images)
    await images_upload(ctx, selected_images)

    print("[Reddit] Done!")

#Video downloader
async def reddit_video_upload(ctx, url):
    print("[Reddit] Uploading")
    await ctx.respond(url)

async def reddit_video_main(ctx, input, quantity, limit=1000):
    await ctx.defer()
    # Print the answer to the console
    print(f'[Reddit] {ctx.author} is scanning "{input}"')

    headers = {'User-Agent': 'GPT-Sama!/0.0.1'}
    url = f'https://www.reddit.com/r/{input}/new.json?limit={limit}'
    res = requests.get(url, headers=headers)
    posts = res.json()['data']['children'][:50]
    collected_videos = []
    for post in posts:
        video_url = post['data']['url']
        if video_url.endswith('.mp4') or video_url.endswith('.gifv'):
            collected_videos.append(video_url)

    if collected_videos == []: await ctx.respond("I couldn't find any videos.")
    print(collected_videos)

    # Randomly select the specified number of videos
    selected_videos = random.sample(collected_videos, min(quantity, len(collected_videos)))
    
    # Upload each selected video to Discord
    for video_url in selected_videos:
        await reddit_video_upload(ctx, video_url)

    print("[Reddit] Done!")
