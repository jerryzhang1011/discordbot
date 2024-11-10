from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
channelId = 1291942715927429217

from greeting import Morning, Night
from weather import WeatherForecast
import discord
from discord.ext import commands, tasks
from datetime import datetime, time
from ai import Ai_bot




# Intents and Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="！", intents=intents)
morning = Morning()
night = Night()
weather_forecast = WeatherForecast()
ai_bot = Ai_bot()


@bot.command(name="这个家的主人在哪里呀")
async def 这个家的主人在哪里呀(ctx):
    await ctx.send("稍等，我去叫我家胖丁和船长！")

@bot.command(name="胖丁最喜欢谁呀")
async def 胖丁最喜欢谁呀(ctx):
    await ctx.send("船长！(宝可梦第二)")

@bot.command(name="船长最喜欢谁呀")
async def 船长最喜欢谁呀(ctx):
    await ctx.send("船长最喜欢胖丁！")

@bot.command(name="船长踢球要带上什么呀")
async def 船长踢球要带上什么呀(ctx):
    await ctx.send("袜子！")

@bot.command(name="我要亲亲了")
async def 我要亲亲了(ctx):
    await ctx.send("主人我去门口花园忙啦（捂眼）")

@bot.command(name="list",description="指令集")
async def list(ctx):
    cmds = r'''指令集
这个家的主人在哪里呀
胖丁最喜欢谁呀
船长最喜欢谁呀
船长踢球要带上什么呀
我要亲亲了
天气
管家
'''
    await ctx.send(cmds)

@bot.command(name="天气", description="Waterloo Toronto天气预报")
async def 天气(ctx):
    msg = "Hi, 小管家天气预报来喽：\n" + weather_forecast.get_weather_report()
    await ctx.send(msg)

@bot.command(name="管家", description="有亿点点聪明的小管家")
async def 管家(ctx, *, arg1: str):
    nameOfUserMap = {
        "j_04zzz": "船长",
        "pangdingmama": "胖丁"
    }
    try:
        nameOfUser = ctx.author.name
        prefix = nameOfUserMap.get(nameOfUser, "其他人")
        
        if ctx.message.attachments:
            image_data = await ctx.message.attachments[0].read()
            data = {
                "prompt": prefix + "：" + arg1,
                "image_data": image_data
            }
            response = ai_bot.getImgResponse(data=data)
        else:
            response = ai_bot.get_response(prefix + "：" + arg1)

        await ctx.reply(response)
    except Exception as e:
        await ctx.reply(f"An error occurred: {str(e)}")


@tasks.loop(minutes=1)
async def daily_hello():
    now = datetime.now().time()
    morning_time = time(7, 0)  
    night_time = time(23, 59)
    if now.hour == morning_time.hour and now.minute == morning_time.minute:
        channel = bot.get_channel(channelId)
        if channel:
            weather_report = weather_forecast.get_weather_report()
            msg = morning.greet() + "\n" + "\n" + weather_report
            await channel.send(msg)
    elif now.hour == night_time.hour and now.minute == night_time.minute:
        channel = bot.get_channel(channelId)
        if channel:
            await channel.send(night.greet())




# Start the task when the bot is ready
@bot.event
async def on_ready():
    daily_hello.start()  # Start the scheduled task
    print(f'Logged in as {bot.user.name}!')

bot.run(token)





