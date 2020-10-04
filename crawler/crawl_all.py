import threading
import os
import sys
import discord
sys.path.append(os.environ['NOTI_PATH'] + '/crawler/departs/')
sys.path.append(os.environ['NOTI_PATH'] + '/lib')
import cse_crawl
#import free_crawl
#import german_crawl
#import cse_notice_crawl
import dorm_crawl
import french_crawl
import traceback
import time

crawlers = []

crawlers.append(cse_crawl.crawl_all)
#crawlers.append(free_crawl.crawl_all)
#crawlers.append(german_crawl.crawl_all)
crawlers.append(dorm_crawl.crawl_all)
#crawlers.append(french_crawl.crawl_all)

TOKEN = 'NzQ3MDQ3MTI2MjM5ODA1NDUx.X0JL2g.c52_yiksbJsuBcdgx3kFRD0CJ0w'
client = discord.Client()

async def run(channel):
	while True:
		for crawl in crawlers:
			try:
			    await crawl(channel)
			except:
			    traceback.print_exc()
			time.sleep(5)

@client.event
async def on_ready():
	await client.wait_until_ready()
	print('Logging in...')
	print(client.user.name)
	print(client.user.id)

@client.event
async def on_message(message):
	if message.author.bot:
		return None
	if message.content.startswith('!run'):		
		channel = message.channel
		await channel.send('starting crawler...!')
		await run(channel)

client.run(TOKEN)

