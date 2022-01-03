from nextcord.ext import commands
import discord, configparser as cp

BOT_CHANNEL_CATEGORY = 'Tar-Key-Bot'
LIST_CHANNEL = 'key-list'
REQ_CHANNEL = 'key-request'

cfg = cp.ConfigParser()
cfg.read('.env')
TOKEN = cfg['secrets']['TOKEN']

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.reply('Pong!')

@bot.command()
async def init(ctx):

    #TODO gather initial time here
    
    await log(ctx, 'Running init operations!')
    cat = discord.utils.get(ctx.guild.categories, name=BOT_CHANNEL_CATEGORY)
    if not cat:
        await ctx.message.guild.create_category(BOT_CHANNEL_CATEGORY)
        cat = discord.utils.get(ctx.guild.categories, name=BOT_CHANNEL_CATEGORY)

    # Check if list channel exists and create if not
    key_list_channel = discord.utils.get(ctx.guild.channels, name=LIST_CHANNEL)
    if key_list_channel:
        await log(ctx, f'Channel already exists: {key_list_channel}')
    else:
        log(ctx, f'Creating channel: {key_list_channel}')
        await ctx.message.guild.create_text_channel(LIST_CHANNEL,category=cat)
    
    # Check if request channel exists and create if not
    key_request_channel = discord.utils.get(ctx.guild.channels, name=REQ_CHANNEL)
    if key_request_channel:
        await log(ctx, f'Channel already exists: {key_request_channel}')
    else:
        log(ctx, f'Creating channel: {key_request_channel}')
        await ctx.message.guild.create_text_channel(REQ_CHANNEL,category=cat)

    log(ctx, "Initial setup has finished in XXX")

async def log(ctx, message):
    await ctx.channel.send(message)

bot.run(TOKEN)
