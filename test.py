# import discord

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as', self.user)

#     async def on_message(self, message):
#         # don't respond to ourselves
#         if message.author == self.user:
#             return

#         if message.content == 'Привет':
#             await message.channel.send  ('До встречи') 

#         if message.content == 'Как дела?':
#             await message.channel.send  ('С кайфом')

#         if message.content == 'привет':
#             await message.channel.send  (f' { message.author.mention }, приветствую.')


# client = MyClient()
# client.run('OTI3OTc3NjY4NzYxMjUxOTYw.YdSEjQ.aJ1E_mmDUc3VvCRK6tUMutrlQa4')

import discord
from discord import Embed

from discord.ext import bot
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord_components import Button, ButtonStyle, Select, SelectOption, DiscordComponents

import sqlite3
import asyncio
import datetime

intents = discord.Intents.default()
intents.members = True

bot = bot.Bot(command_prefix = '!', case_insensitive = True, intents = discord.Intents.all())
bot.remove_command('help')

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

# @bot.command(aliases = ['go'])
# async def on_message(ctx):
#     message = 'Бот работает!'
#     await bot.get_channel(928363945432080385).send(message)
#     await asyncio.sleep(3) # 24 часов это 86400 секунд

# @bot.command(aliases = ['go'])
# async def background_task(ctx):
#     time = 5
#     await asyncio.sleep(time)
#     message = 'Бот работает!'
#     await bot.get_channel(928363945432080385).send(message)

@bot.event
async def on_ready():
    DiscordComponents(bot)
    bot.ready = True
    embed = discord.Embed(description = '**Бот работает!**')
    embed.timestamp = datetime.datetime.utcnow()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!хелп"))
    await bot.get_channel(930098745478099026).send(embed = embed)


@bot.event
async def on_member_join(member):
    # inviter = await self.tracker.fetch_inviter(member)
    embed1 = discord.Embed(
        title = 'Пользователь присоединился',
        description = f'{member.mention} {len(list(member.guild.members))} по счёту на сервере\nАккаунт создан ' + f"{member.created_at.strftime('%d %B %Yг.')}",
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed1.set_author(name = f'{member}', icon_url = member.avatar_url)
    embed1.set_footer(text = f'ID: {member.id}')
    embed1.timestamp = datetime.datetime.utcnow()
    embed = discord.Embed(
        description = '__Выбери свой сервер в канале <#884710136617250827> и тебе откроется полный доступ к серверу.__',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_author(name = 'Добро пожаловать на сервер!', icon_url = member.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await bot.get_channel(874756699435712542).send(embed = embed1)
    await bot.get_channel(904729869911490641).send(f'{member.mention}', embed = embed, delete_after = 60)


@bot.event
async def on_member_remove(member):
    rlist = []  
    for role in member.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)
    embed = discord.Embed(
        title = 'Пользователь вышел с сервера',
        description = f'{member.mention} зашёл на этот сервер ' + f"{member.joined_at.strftime('%d %B %Yг.')}\n" + f"**Роли({len(rlist)}):**" + ''.join([b]),
        color = discord.Color.from_rgb(255, 0, 0)
        )
    embed.set_author(name = f'{member}', icon_url = member.avatar_url)
    embed.set_footer(text = f'ID: {member.id}')
    embed.timestamp = datetime.datetime.utcnow()
    await bot.get_channel(874756699435712542).send(embed = embed)


@bot.command(aliases = ['команды', 'хелп', 'помощь'])
async def help(ctx):
    embed = discord.Embed(
        title = 'Famq & News помощь(команды)',
        description = '**Доступные команды на данный момент:**',
        color = discord.Color.from_rgb(244, 127, 255))
    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon_url)
    embed.add_field(name = '<a:st2:903087219802263592> Информация (!инфо Информация)', value = '`!help[!хелп, !помощь]` `!server[!сервер]` `!user[!юзер]` `!info[!инфо]`', inline = False)
    embed.add_field(name = '<a:st1:903087219777093642> Модерация (!инфо Модерация)', value = '`!clear[!очистить]`', inline = False)
    embed.add_field(name = '<a:st2:903087219802263592> Полезное (!инфо Полезное)', value = '`!ava[!ава]`', inline = False)
    await ctx.reply(embed = embed, components = [ [
        Button(style = ButtonStyle.green, label = 'Информация', emoji = '🥀'),
        Button(style = ButtonStyle.red, label = 'Модерация', emoji = '🥥'),
        Button(style = ButtonStyle.blue, label = 'Полезное', emoji = '👑')
    ] ])

    cycle = True
    while cycle:
        response = await bot.wait_for('button_click')
        if response.channel == ctx.channel:
            if response.component.label == 'Информация':
                embedinfo = discord.Embed(
                    title = 'Доступные команды подгруппы "Информация⭐"',
                    color = discord.Color.from_rgb(244, 127, 255)
                    )
                embedinfo.add_field(name = '!хелп - список всех команд бота', value = 'Использование: `!хелп`/`!help`', inline = False)
                embedinfo.add_field(name = '!сервер - основная информация о сервере', value = 'Использование: `!сервер`/`!server`', inline = False)
                embedinfo.add_field(name = '!юзер - основная информация о пользователе', value = 'Использование: `!юзер <упоминание пользователя>`/`!user <упоминание пользователя>`', inline = False)
                embedinfo.add_field(name = '!инфо - информация о боте/командах', value = 'Использование: `!инфо/!info - информация о боте\n!инфо <название команды>/!info <название команды> - информация о команде`', inline = False)
                await response.respond(embed = embedinfo)
            elif response.component.label == 'Полезное':
                embedutils = discord.Embed(
                    title = 'Доступные команды подгруппы "Полезное⭐"',
                    color = discord.Color.from_rgb(244, 127, 255)
                    )
                embedutils.add_field(name = '!ава - просмотр аватарки пользователя', value = 'Использование: `!ава <упоминание пользователя>`/`!ava <упоминание пользователя>`', inline = False)
                await response.respond(embed = embedutils)
            else:
                embedmod = discord.Embed(
                    title = 'Доступные команды подгруппы "Модерация⭐"',
                    color = discord.Color.from_rgb(244, 127, 255)
                    )
                embedmod.add_field(name = '!очистить - удаление сообщений', value = 'Использование: `!очистить/!clear - удаление 25 последних сообщений`\n`!очистить <число>/!clear <число> - удаление конкретного числа сообщений`', inline = False)
                await response.respond(embed = embedmod)


    # e1 = discord.Embed(
    # #     title = 'Доступные команды подгруппы "Информация"',
    # #     color = discord.Color.from_rgb(244, 127, 255)
    # #     )
    # # e1.add_field(name = '!хелп - список всех команд бота', value = 'Использование: `!хелп`/`!help`', inline = False)
    # # e1.add_field(name = '!сервер - основная информация о сервере', value = 'Использование: `!сервер`/`!server`', inline = False)
    # # e1.add_field(name = '!юзер - основная информация о пользователе', value = 'Использование: `!юзер <упоминание пользователя>`/`!user <упоминание пользователя>`', inline = False)
    # # e1.add_field(name = '!инфо - информация о боте/командах', value = 'Использование: `!инфо/!info - информация о боте\n!инфо <название команды>/!info <название команды> - информация о команде`', inline = False)

    # res = await bot.wait_for("select_option")
    # await res.respond(content = "Вы выбрали: "+str(res.component.emoji))

    # while True:
    #     try:
    #         event = await bot.wait_for('select_option', check = None)
    #         label = event.component[0].label
    #         if label == 'Информация':
    #             await event.respond(
    #                 type = InteractionType.ChannelMessageWithSource,
    #                 ephemeral = True,
    #                 embed = e1)

    #     except discord.NotFound:
    #         print('error.')


# @bot.command()
# async def select(ctx):
#     await ctx.reply("Список", components=[
#         Select(
#             placeholder="Выберите эмоджи",
#             options=[
#                 SelectOption(
#                     emoji="😎",
#                     label="Крутое эмоджи",
#                     description="Эмоджи1",
#                     value="e1"
#                 ),
#                 SelectOption(
#                     emoji="🍹",
#                     label="Коктейль эмоджи",
#                     description="Эмоджи2",
#                     value="e1"
#                 )
#             ]
#         )
#     ])
#     res = await bot.wait_for("select_option")
#     await res.respond(content="Вы выбрали: "+str(res.
# component.emoji))


@bot.command(aliases = ['инфо'])
async def info(ctx, arg = None):
    embed = discord.Embed(
        description = 'Приветствую! Я — бот-помощник для сервера Famq & News. Я умею многое, можешь посмотреть)\n\nМой префикс - `!`. Используй команду `!хелп` и увидишь, что я такое и мои возможности <a:st2:903087219802263592>',
        color = discord.Color.from_rgb(244, 127, 255))
    embed.add_field(name = 'Мои разработчики:', value = '<:dnd:929006191420514354> welcomeu#1337 <@909585478037155913>\n<:dnd:929006191420514354> Alexff(Сашуля)#0001')
    embed.set_footer(text = 'Ваш Famq&News Bot © 2022', icon_url = ctx.guild.icon_url)
    embed.set_author(name = 'Famq&News Bot', icon_url = ctx.guild.icon_url)
    
    embed1 = discord.Embed(
        title = 'Доступные команды подгруппы "Информация⭐"',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed1.add_field(name = '!хелп - список всех команд бота', value = 'Использование: `!хелп`/`!help`', inline = False)
    embed1.add_field(name = '!сервер - основная информация о сервере', value = 'Использование: `!сервер`/`!server`', inline = False)
    embed1.add_field(name = '!юзер - основная информация о пользователе', value = 'Использование: `!юзер <упоминание пользователя>`/`!user <упоминание пользователя>`', inline = False)
    embed1.add_field(name = '!инфо - информация о боте/командах', value = 'Использование: `!инфо/!info - информация о боте\n!инфо <название команды>/!info <название команды> - информация о команде`', inline = False)

    embed2 = discord.Embed(
        title = 'Доступные команды подгруппы "Модерация⭐"',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed2.add_field(name = '!очистить - удаление сообщений', value = 'Использование: `!очистить/!clear - удаление 25 последних сообщений`\n`!очистить <число>/!clear <число> - удаление конкретного числа сообщений`', inline = False)

    embed3 = discord.Embed(
        title = 'Доступные команды подгруппы "Полезное⭐"',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed3.add_field(name = '!ава - просмотр аватарки пользователя', value = 'Использование: `!ава <упоминание пользователя>`/`!ava <упоминание пользователя>`', inline = False)

    if arg == None:
        await ctx.reply(embed = embed)
    elif arg == 'информация':
        await ctx.reply(embed = embed1)
    elif arg == 'Информация':
        await ctx.reply(embed = embed1)
    elif arg == 'модерация':
        await ctx.reply(embed = embed2)
    elif arg == 'Модерация':
        await ctx.reply(embed = embed2)
    elif arg == 'полезное':
        await ctx.reply(embed = embed3)
    elif arg == 'Полезное':
        await ctx.reply(embed = embed3)
    else:
        await ctx.reply('чего?')


@bot.command(pass_context = True, aliases = ['очистить'])
@commands.has_any_role(884510313486098443, 910227213708836884, 905125141355319367, 875788818421256314)
async def clear(ctx, amount = 25):
    await ctx.channel.purge(limit = int(amount) + 1)
    
    author = str(ctx.author)
    embed = discord.Embed(
        title = 'Сообщения удалены!',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.add_field(name = 'Количество', value = amount, inline = False)
    embed.set_footer(text = 'Модератор: ' + author)
    await ctx.send(embed = embed, delete_after = 5)
    
    # text = str(ctx.message_delete) 
    channel = bot.get_channel(874520061069623388)
    embed1 = discord.Embed(
        title = 'Сообщения удалены!',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed1.add_field(name = 'Количество', value = amount, inline = True)
    # embed1.add_field(name = 'Содержимое', value = text, inline = True)
    embed1.set_footer(text = 'Модератор: ' + author)
    # await message.delete()
    await channel.send(embed = embed1)


@bot.command(aliases = ['ава'])
async def ava(ctx, user:discord.Member = None ):
    if user is None:
        user = ctx.author

    embed = discord.Embed(
        title = f'Аватар {user}',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.set_image(url = user.avatar_url)
    await ctx.reply(embed = embed)


@bot.command(aliases = ['юзер'])
async def user(ctx, user:discord.Member = None ):
    if user is None:
        user = ctx.author

    rlist = []
    for role in user.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)

    # roles = [role for role in user.roles]
    embed = discord.Embed(
        description = f'**__Основная информация__**\n<a:st2:903087219802263592> **Имя пользователя:** {user}\n<a:st1:903087219777093642> **Статус: ** {user.status}\n'
        f"<a:st2:903087219802263592> **Дата регистрации:** {user.created_at.strftime('%d %B %Yг.')}\n"
        f"<a:st1:903087219777093642> **Присоединился:** {user.joined_at.strftime('%d %B %Yг.')}\n"
        f'<a:st2:903087219802263592> **Имя на сервере:** {user.display_name}\n'
        f'<a:st1:903087219777093642> **Роли({len(rlist)}):**' + ''.join([b]),
        color = discord.Color.from_rgb(244, 127, 255),
        timestamp = ctx.message.created_at
        )
    embed.set_author(name = f'Информация о пользователе {user.name}', icon_url = user.avatar_url)
    embed.set_thumbnail(url = user.avatar_url)
    embed.set_footer(text = f'ID: {user.id}', icon_url = user.avatar_url)
    embed.set_image(url = ctx.guild.banner_url)
    await ctx.reply(embed = embed)
    

    # embed1 = discord.Embed(
    #     title = f'Информация о пользователе __{user.name}__',
    #     description = f'**__Основная информация__**\n<a:stars_black:839868847489417227> **Имя пользователя:** {user}\n<a:stars_white:839868847917367347> **Статус:**' + "<:online:929006151549452288>" + 'В сети\n' + f"<a:roza_black:839868851063226408> **Дата регистрации:** {user.created_at.strftime('%d %B %Yг')}\n" + '<a:roza_white:839868850908561418> **Присоединился:** ' + user.joined_at.strftime('%d %B %Yг'),
    #     color = discord.Color.from_rgb(244, 127, 255),
    #     timestamp = ctx.message.created_at
    #     )
    # embed1.set_thumbnail(url = user.avatar_url)
    # embed1.set_footer(text = f'ID: {user.id}   Вызвано для {user}', icon_url = user.avatar_url)

    # embed2 = discord.Embed(
    #     title = f'Информация о пользователе __{user.name}__',
    #     description = f'**__Основная информация__**\n<a:stars_black:839868847489417227> **Имя пользователя:** {user}\n<a:stars_white:839868847917367347> **Статус:**' + "<:idle:929006095995916288>" + 'Неактивен\n' + f"<a:roza_black:839868851063226408> **Дата регистрации:** {user.created_at.strftime('%d %B %Yг')}\n" + '<a:roza_white:839868850908561418> **Присоединился:** ' + user.joined_at.strftime('%d %B %Yг'),
    #     color = discord.Color.from_rgb(244, 127, 255),
    #     timestamp = ctx.message.created_at
    #     )
    # embed2.set_thumbnail(url = user.avatar_url)
    # embed2.set_footer(text = f'ID: {user.id}   Вызвано для {user}', icon_url = user.avatar_url)

    # embed3 = discord.Embed(
    #     title = f'Информация о пользователе __{user.name}__',
    #     description = f'**__Основная информация__**\n<a:stars_black:839868847489417227> **Имя пользователя:** {user}\n<a:stars_white:839868847917367347> **Статус:**' + "<:dnd:929006191420514354>" + 'Не беспокоить\n' + f"<a:roza_black:839868851063226408> **Дата регистрации:** {user.created_at.strftime('%d %B %Yг')}\n" + '<a:roza_white:839868850908561418> **Присоединился:** ' + user.joined_at.strftime('%d %B %Yг'),
    #     color = discord.Color.from_rgb(244, 127, 255),
    #     timestamp = ctx.message.created_at
    #     )
    # embed3.set_thumbnail(url = user.avatar_url)
    # embed3.set_footer(text = f'ID: {user.id}   Вызвано для {user}', icon_url = user.avatar_url)
#     # embed.add_field(name = '', value = , inline = True)
#     # embed.add_field(name = '', value = , inline = True)
    # embed.set_image(url = user.banner.url)

    # if user.status == offline:
    #     await ctx.reply(embed = embed)
    # if user.status == online:
    #     await ctx.reply(embed = embed1)
    # if user.status == idle:
    #     await ctx.reply(embed = embed2)
    # if user.status == dnd:
    #     await ctx.reply(embed = embed3)



@bot.command(aliases = ['сервер'])
async def server(ctx):
    owner = str(ctx.guild.owner_id) 
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    channel = str(ctx.guild.voice_channels)
    emojis = str(ctx.guild.emojis)
    mmembers = str(ctx.guild.max_members)
    banner = str(ctx.guild.banner_url)
    author = str(ctx.author)
    created = str(ctx.guild.created_at.strftime('%d %B %Yг. %H:%M:%S'))

    embed = discord.Embed(
        title = f'{ctx.guild.name}',
        description = f'*{ctx.guild.description}*\n \n**Владелец: **' + '<@' + owner + '>', 
        color = discord.Color.from_rgb(244, 127, 255),
        timestamp = ctx.message.created_at
        )
    embed.set_thumbnail(url = icon)
    # embed.add_field(name = 'Овнер', value = owner, inline = False)
    # embed.add_field(name = 'ID', value = id, inline = True)
    embed.add_field(name = 'Дата создания', value = created, inline = True)
    # embed.add_field(name = 'Эмодзи', value = emojis, inline = True)
    # embed.add_field(name = 'Максимальное кол-во', value = mmembers, inline = True)
    embed.add_field(name = 'Кол-во участников', value = memberCount, inline = True) 
    embed.add_field(name = 'ID сервера', value = id, inline = True)
    embed.set_footer(text = 'Вызвано для: ' + author)
    embed.set_image(url = banner)

    await ctx.reply(embed = embed)


@bot.command(aliases = ['заявка'])
async def zayavka(ctx):
    embed = discord.Embed(
        title = 'Заявление на пост модератора',
        description = '<@&903780351640469574> *- человек, занимающийся публикацией новостей Majestic RP на каждом сервере.*\n\n'
        '**__Для того, чтобы попасть на эту должность от вас требуестя:__**\n\n'
        '<a:st2:903087219802263592> *Желание и активность;*\n<a:st2:903087219802263592> *Адекватность и грамотность;*\n<a:st2:903087219802263592> *Знание основного функционала сервера.*\n\n'
        '**__Что тебя ждёт на данной должности:__**\n\n'
        '<a:st1:903087219777093642> Выплаты в ₽, Discord Nitro и т.п.;\n'
        '<a:st1:903087219777093642> Опыт и хорошее времяпровождение в коллективе;\n'
        '<a:st1:903087219777093642> Карьерный рост.\n\n'
        f'<a:stars_white:839868847917367347> *Считаешь, что подходишь? [Оставляй заявку!](https://docs.google.com/forms/d/1-1ofO2tixhp6uRM0ZeouyHYILQWoTEDXe5BUIsNTgJA/)*\n'
        '<:emoji_19:888086804085997568> **Будем рады увидеть вас в нашем составе** <:emoji_19:888086804085997568>', 
        color    = discord.Color.from_rgb(244, 127, 255)
        )
    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.set_image(url = ctx.guild.banner_url)
    embed.set_footer(text = ctx.guild.name)

    await ctx.send(embed = embed, components = [ [
        Button(style = ButtonStyle.URL, label = 'Оставить заявку!', url = 'https://docs.google.com/forms/d/1-1ofO2tixhp6uRM0ZeouyHYILQWoTEDXe5BUIsNTgJA/'),
        ] ])

@bot.command(aliases = ['фама'])
async def famq(ctx):
    channel = bot.get_channel(874398614892474409)
    embed = discord.Embed(
        description = '__Чтобы получить роль вашей фамы, вам нужно набрать минимум 10 плюсов с названием фамы.__', 
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.set_footer(text = ctx.guild.name)
    embed.timestamp = datetime.datetime.utcnow()

    await channel.send(embed = embed)
    
    
@bot.event
async def on_user_update(before, after):
    if before.avatar != after.avatar:
        channellog = bot.get_channel(874520061069623388)
        channel = bot.get_channel(930078480249544745)
        embed = discord.Embed(
            title ="Новая аватарка",
            color = discord.Color.from_rgb(244, 127, 255)
            )
        embed.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
        embed.set_thumbnail(url = after.avatar_url)
        embed.set_footer(text = 'Famq&News Bot')
        embed.timestamp = datetime.datetime.utcnow()

        embed1 = discord.Embed(
            title = 'Рандомная аватарка',
            color = discord.Color.from_rgb(244, 127, 255)
            )
        embed1.set_image(url = after.avatar_url)
        embed1.set_footer(text = 'Famq&News Bot')
        embed1.timestamp = datetime.datetime.utcnow()

        await channellog.send(embed = embed)
        await channel.send(embed = embed1)
        await asyncio.sleep(300)
                
    if before.name != after.name:
        channellog = bot.get_channel(874520061069623388)
        embedname = discord.Embed(
            title = "Ник пользователя изменен",
            description = f'**Ник до изменения:** {before.name}\n**Ник после изменения:** {after.name}',
            color = discord.Color.from_rgb(244, 127, 255),
            timestamp = datetime.datetime.utcnow()
            )
        embedname.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
        embedname.set_footer(text = 'Famq&News Bot')
        
        await channellog.send(embed = embedname)

# @bot.event
# async def on_member_update(before, after):
    


# @bot.event
# async def on_user_update(before, after):
#     if before.username != after.username:
#         channel = bot.get_channel(874520061069623388)
#         embed = discord.Embed(
#             title ="Новый ник на сервере",
#             description = f'**До:** {before.username}\n**После:** {after.username}',
#             color = discord.Color.from_rgb(244, 127, 255)
#             )
#         embed.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
#         embed.set_footer(text = 'Famq&News Bot')
#         embed.timestamp = datetime.datetime.utcnow()

#         await channel.send(embed = embed)


@bot.event
async def on_message_edit(before, after):
    kanal = before.channel
    time = after.created_at.strftime('%Y.%m.%d %H:%M:%S')
    embed = discord.Embed(
        title = 'Сообщение было изменено!',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.add_field(name = 'Сообщение до изменения:', value = before.content, inline = True)
    embed.add_field(name = 'Сообщение после изменения:', value = after.content, inline = True)
    embed.add_field(name = 'Канал:', value = kanal, inline = False)
    embed.set_footer(text = 'Cообщение отправлено: ' + time)
    channel = bot.get_channel(874520061069623388)
    if before.content == after.content:
        return
    await channel.send(embed = embed)


@bot.event
async def on_message_delete(message):
    kanal = message.channel
    time = message.created_at.strftime('%Y.%m.%d %H:%M:%S')
    embed = discord.Embed(
        title ="Сообщение было удалено!",
        description = f"__Автор:__ {message.author.mention} {message.author}",
        color = discord.Color.from_rgb(255, 0, 0)
        )
    embed.add_field(name = "Содержимое сообщения:", value = message.content)
    embed.add_field(name = 'Канал:', value = kanal, inline = False)
    embed.set_footer(text = 'Cообщение отправлено: ' + time)
    channel = bot.get_channel(874520061069623388)
    await channel.send(embed = embed)

# @bot.event
# async def on_ready():
#     cursor.execute("""CREATE TABLE users (
#         name TEXT,
#         id INT,
#         cash BIGINT,
#         rep INT,
#         lvl INT
#     )""")
#     connection.commit()

#     for guild in bot.guilds:
#         for member in guild.members:
#             if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
#                 cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0, 1)')
#                 connection.commit()
#             else:
#                 pass

#     connection.commit()
#     print('Bot connected')


# @bot.event
# async def on_member_join(member):
#     if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
#         cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0, 1)')
#         connection.commit()
#     else:
#         pass


# @bot.command(aliases = ['cash', 'баланс'])
# async def balance(ctx, member: discord.Member = None):
#     if member is None:
#         await ctx.send(embed = discord.Embed(
#             description = f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]} :dollar:**"""
#         ))
#     else:
#         await ctx.send(embed = discord.Embed(
#             description = f"""Баланс пользователя **{member}** составляет **{cursor.execute('SELECT cash FROM users WHERE id = {}'.format(member.id)).fetchone()[0]} :dollar:**"""
#         ))     

bot.run('OTI3OTc3NjY4NzYxMjUxOTYw.YdSEjQ.aJ1E_mmDUc3VvCRK6tUMutrlQa4')
