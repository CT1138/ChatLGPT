import requests
import random

async def reddit_video_upload(ctx, input, url):
    print(f"[Reddit Video] Subreddit: {input}\nURL: {url}")
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

    # Randomly select the specified number of videos
    selected_videos = random.sample(collected_videos, min(quantity, len(collected_videos)))
    
    # Upload each selected video to Discord
    for video_url in selected_videos:
        await reddit_video_upload(ctx, input, video_url)
