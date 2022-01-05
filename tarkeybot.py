from nextcord.ext import commands
import time, discord, configparser as cp

BOT_CHANNEL_CATEGORY = 'Tar-Key-Bot'
LIST_CHANNEL = 'key-list'
REQ_CHANNEL = 'key-request'
IN_MEMORY_DATA = []

cfg = cp.ConfigParser()
cfg.read('.env')
TOKEN = cfg['secrets']['TOKEN']

bot = commands.Bot(command_prefix='!')

test_keys = {'Customs':['Tarcone Directors Office', 'Dorms 206']}


@bot.command()
async def ping(ctx):
    await ctx.reply('Pong!')

@bot.command()
async def init(ctx, reset_bot=False):

    reset_bot = (True if reset_bot == 'reset' else False)
    
    await remote_log(ctx, 'Running init operations!')
    start_time = time.time()

    cat = discord.utils.get(ctx.guild.categories, name=BOT_CHANNEL_CATEGORY)
    if not cat:
        await ctx.message.guild.create_category(BOT_CHANNEL_CATEGORY)
        cat = discord.utils.get(ctx.guild.categories, name=BOT_CHANNEL_CATEGORY)
    else:
        await remote_log(ctx, f'{BOT_CHANNEL_CATEGORY} Category already exists')

    # Check if list channel exists and create if not
    key_list_channel = discord.utils.get(ctx.guild.channels, name=LIST_CHANNEL)
    if key_list_channel:
        await remote_log(ctx, f'Channel already exists: {key_list_channel}')
        first_run = False
    else:
        await remote_log(ctx, f'Creating channel: {key_list_channel}')
        await ctx.message.guild.create_text_channel(LIST_CHANNEL, category=cat)
        key_list_channel = discord.utils.get(ctx.guild.channels, name=LIST_CHANNEL)
        first_run = True
    
    # Check if request channel exists and create if not
    key_request_channel = discord.utils.get(ctx.guild.channels, name=REQ_CHANNEL)
    if key_request_channel:
        await remote_log(ctx, f'Channel already exists: {key_request_channel}')
    else:
        await remote_log(ctx, f'Creating channel: {key_request_channel}')
        await ctx.message.guild.create_text_channel(REQ_CHANNEL,category=cat)
        key_request_channel = discord.utils.get(ctx.guild.channels, name=REQ_CHANNEL)

    # create mesages with keylist
    if first_run or reset_bot:
        await create_key_list(ctx, key_list_channel)

    end_time = time.time()
    await remote_log(ctx, "Initial setup has finished in %s seconds" % (round(end_time - start_time, 2)))

async def remote_log(ctx, message):
    await ctx.channel.send(message)

async def create_key_list(ctx, key_list_channel):

    await key_list_channel.set_permissions(ctx.guild.default_role, read_messages=False)

    # this could be done better but lets try like this
    for tmap in test_keys:
        await key_list_channel.send(f'---------------------------{tmap}---------------------------')
        for key in test_keys[tmap]:
            await key_list_channel.send(key)

bot.run(TOKEN)
