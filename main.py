# 必須ライブラリをインポート
from os import sync
import discord
from datetime import datetime, timedelta
import time
import requests
import os
import json
import subprocess
from datetime import datetime
import pytz
from discord import Intents
#from dotenv import dotenv_values

os.system("date")

client = discord.Client(intents=Intents.all())

#load_dotenv()
TOKEN = subprocess.check_output('/usr/bin/cat /home/labpixel/BeginnersSec/discord_bot/.env', shell=True)
TOKEN = TOKEN.decode("utf-8")
#TOKEN = os.environ.get["TOKEN"]
#CHANNEL_ID = os.environ["CHANNEL_ID"]

@client.event
async def on_ready():
	print("[+]	ログインしました")
	print()

	ctftime_limit = 15
	ctftime_start = int(time.time())
	ctftime_finish = int(time.time() + 86400 * 7)

	url = "https://ctftime.org/api/v1/events/?limit{}=&start={}&finish={}"
	payload = {"limit": ctftime_limit, "start": ctftime_start, "finish": ctftime_finish}
	api_url = url.format(ctftime_limit, ctftime_start, ctftime_finish)
	get_data = subprocess.check_output("curl " + api_url, shell=True)
	law = json.loads(get_data.decode("utf-8"))

	for l in law:
		ctf_info = {
			"title": l["title"],
			"description": '```' + l["description"] + '```',
			"url": l["url"],
			"logo": l["logo"],
			"weight": l["weight"],
			"start": l["start"],
			"start_jp": "",
			"finish": l["finish"],
			"finish_jp": ""
		}
		if l["logo"]:
			ctf_info["logo"] = l["logo"]
		start_time = l["start"]
		start_time_jp = datetime.fromisoformat(start_time)
		start_time_jp = start_time_jp.astimezone(pytz.timezone('Asia/Tokyo')).strftime("%Y/%m/%d (%A) %H:%M")
		finish_time = l["finish"]
		finish_time_jp = datetime.fromisoformat(finish_time)
		finish_time_jp = finish_time_jp.astimezone(pytz.timezone('Asia/Tokyo')).strftime("%Y/%m/%d (%A) %H:%M")
		ctf_info["start_jp"] = start_time_jp
		ctf_info["finish_jp"] = finish_time_jp
		
		if ctf_info["weight"] == 0:
			window_color = 0x00ff00
		else:
			window_color = 0xff0000
		embed = discord.Embed(
			title = ctf_info["title"],
			description = ctf_info["description"],
			url = ctf_info["url"],
			color = window_color,
		)
		embed.set_thumbnail(url = ctf_info["logo"])
		embed.add_field(name = "weight", value = ctf_info["weight"], inline = False)
		embed.add_field(name = "Start Time(JST)", value = ctf_info["start_jp"], inline = False)
		embed.add_field(name = "Finish Time(JST)", value= ctf_info["finish_jp"], inline = False)
		print("[+]	CTF情報を送信しました: " + ctf_info["title"])
		await client.get_channel(1091753208969445456).send(embed=embed)
	print("[+]	CTF情報の送信が完了しました")
	quit()

client.run(TOKEN)
