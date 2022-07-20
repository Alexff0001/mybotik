import discord
from discord import Embed

from discord import guild
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

# from discord.ext import bot
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord_components import Button, ButtonStyle, Select, SelectOption, DiscordComponents

import sqlite3
import asyncio
import datetime
import os
import json

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '!', case_insensitive = True, intents = discord.Intents.all())
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands = True)

connection = sqlite3.connect('server.db')
cursor = connection.cursor()


@bot.event
async def on_ready():
    DiscordComponents(bot)
    bot.ready = True
    embed = discord.Embed(description = '**Бот работает!**')
    embed.timestamp = datetime.datetime.utcnow()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!хелп🇷🇺"))
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
    embed.add_field(name = '<a:st1:903087219777093642> Модерация (!инфо Модерация)', value = '`!clear[!очистить]` `!ban[!бан]` `!kick[!кик]`', inline = False)
    embed.add_field(name = '<a:st2:903087219802263592> Полезное (!инфо Полезное)', value = '`!ava[!ава]`', inline = False)
    embed.add_field(name = '<a:st2:903087219802263592> Для овнеров (!инфо Для овнеров)', value = '`!create[!создать]` `!give[!выдать]` `!remove[!забрать]`', inline = False)
    await ctx.reply(embed = embed, components = [ [
        Button(style = ButtonStyle.green, label = 'Информация', emoji = '🥀'),
        Button(style = ButtonStyle.red, label = 'Модерация', emoji = '🥥'),
        Button(style = ButtonStyle.green, label = 'Полезное', emoji = '👑'),
        Button(style = ButtonStyle.red, label = 'Для овнеров', emoji = '💯')
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
            elif response.component.label == 'Модерация':
                embedmod = discord.Embed(
                    title = 'Доступные команды подгруппы "Модерация⭐"',
                    color = discord.Color.from_rgb(244, 127, 255)
                    )
                embedmod.add_field(name = '!очистить - удаление сообщений', value = 'Использование: `!очистить/!clear - удаление 25 последних сообщений`\n`!очистить <число>/!clear <число> - удаление конкретного числа сообщений`', inline = False)
                embedmod.add_field(name = '!бан - бан участника', value = 'Использование: `!бан/!ban <пользователь> <причина> - бан пользователя с причиной`', inline = False)
                embedmod.add_field(name = '!кик - кик участника', value = 'Использование: `!кик/!kick <пользователь> <причина> - кик пользователя с причиной`', inline = False)
                await response.respond(embed = embedmod)
            else:
                embedowm = discord.Embed(
                    title = 'Доступные команды подгруппы "Для овнеров⭐"',
                    color = discord.Color.from_rgb(244, 127, 255)
                    )
                embedowm.add_field(name = '!создать - создать роль семьи', value = 'Использование: `!создать`/`!create <цвет> <название фамы>`', inline = False)
                embedowm.add_field(name = '!выдать - выдать роль члену семьи', value = 'Использование: `!give/!выдать <id роли> <id пользователя>`', inline = False)
                embedowm.add_field(name = '!забрать - забрать роль семьиу пользователя', value = 'Использование: `!remove/!забрать <id роли> <id пользователя>`', inline = False)
                await response.respond(embed = embedowm)

@bot.command(aliases = ['инфо'])
async def info(ctx, *, arg = None):
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

    embed4 = discord.Embed(
        title = 'Доступные команды подгруппы "Для овнеров⭐"',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed4.add_field(name = '!создать - создать роль семьи', value = 'Использование: `!создать`/`!create <цвет> <название фамы>`', inline = False)
    embed4.add_field(name = '!выдать - выдать роль члену семьи', value = 'Использование: `!give/!выдать <id роли> <id пользователя>`', inline = False)
    embed4.add_field(name = '!забрать - забрать роль семьиу пользователя', value = 'Использование: `!remove/!забрать <id роли> <id пользователя>`', inline = False)

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
    elif arg == 'для овнеров':
        await ctx.reply(embed = embed4)
    elif arg == 'Для овнеров':
        await ctx.reply(embed = embed4)
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
        color = discord.Color.from_rgb(255, 0, 0)
        )
    embed1.add_field(name = 'Количество', value = amount, inline = True)
    # embed1.add_field(name = 'Содержимое', value = text, inline = True)
    embed1.set_footer(text = 'Модератор: ' + author)
    # await message.delete()
    await channel.send(embed = embed1)


@bot.command(aliases = ['бан'])
@commands.has_any_role(874406341127573554, 910227213708836884, 905125141355319367, 875788818421256314)
async def ban(ctx, member: discord.Member = None, *, reason = 'Не указана'):
    if member is None:
        embed0 = discord.Embed(
            description = 'Укажи пользователя, которого хочешь забанить!',
            color = discord.Color.from_rgb(255, 0, 0)
            )
        embed0.set_footer(text = 'Famq&News Bot')
        embed0.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed = embed0)
    
    elif member is ctx.author:
        embed1 = discord.Embed(
            description = 'Ты не можешь забанить самого себя..!',
            color = discord.Color.from_rgb(255, 0, 0)
            )
        embed1.set_footer(text = 'Famq&News Bot')
        embed1.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed = embed1)
   
    elif member != ctx.author:
        channel = bot.get_channel(874520061069623388)
        em = discord.Embed(
            title = 'Пользователь был забанен!',
            description = f'**Пользователь:** {member.mention}',
            color = discord.Color.from_rgb(255, 0, 0)
            )
        em.add_field(name = 'ID', value = member.id, inline = True)
        em.add_field(name = 'Причина', value = reason, inline = True)
        em.add_field(name = 'Модератор', value = f'{ctx.author.mention} {ctx.author}', inline = True)
        em.set_footer(text = 'Famq&News Bot')
        em.timestamp = datetime.datetime.utcnow()
        
        embed = discord.Embed(
            description = 'Пользователь забанен!',
            color = discord.Color.from_rgb(244, 127, 255)
            )
        embed.set_footer(text = 'Famq&News Bot')
        embed.timestamp = datetime.datetime.utcnow()
        await member.ban(reason = reason)
        await ctx.reply(embed = embed)
        await channel.send(embed = em)
    


@bot.command(aliases = ['кик'])
@commands.has_any_role(884510313486098443, 910227213708836884, 905125141355319367, 875788818421256314)
async def kick(ctx, member: discord.Member = None, *, reason = 'Не указана'):
    if member is None:
        embed0 = discord.Embed(
            description = 'Укажи пользователя, которого хочешь кикнуть!',
            color = discord.Color.from_rgb(255, 0, 0)
            )
        embed0.set_footer(text = 'Famq&News Bot')
        embed0.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed = embed0)
    
    elif member is ctx.author:
        embed1 = discord.Embed(
            description = 'Ты не можешь кикнуть самого себя..!',
            color = discord.Color.from_rgb(255, 0, 0)
            )
        embed1.set_footer(text = 'Famq&News Bot')
        embed1.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed = embed1)
    
    elif member != ctx.author:
        channel = bot.get_channel(874520061069623388)
        em = discord.Embed(
            title = 'Пользователь был кикнут!',
            description = f'**Пользователь:** {member.mention}',
            color = discord.Color.from_rgb(255, 0, 0)
            )
        em.add_field(name = 'ID', value = member.id, inline = True)
        em.add_field(name = 'Причина', value = reason, inline = True)
        em.add_field(name = 'Модератор', value = f'{ctx.author.mention} {ctx.author}', inline = True)
        em.set_footer(text = 'Famq&News Bot')
        em.timestamp = datetime.datetime.utcnow()

        embed = discord.Embed(
            description = 'Пользователь кикнут!',
            color = discord.Color.from_rgb(244, 127, 255)
            )
        embed.set_footer(text = 'Famq&News Bot')
        embed.timestamp = datetime.datetime.utcnow()
        await member.kick(reason = reason)
        await ctx.reply(embed = embed)
        await channel.send(embed = em)


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
    

@bot.command(aliases = ['сервер'])
async def server(ctx):
    owner = str(ctx.guild.owner_id) 
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    emojis = str(ctx.guild.emojis)
    mmembers = str(ctx.guild.max_members)
    banner = str(ctx.guild.banner_url)
    author = str(ctx.author)
    created = str(ctx.guild.created_at.strftime('%d %B %Yг.'))
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels

    bot = [bot.mention for bot in ctx.guild.members if bot.bot]
    people = [Member for Member in ctx.guild.members if not Member.bot]

    members = set(ctx.message.guild.members)
    offline = filter(lambda m: m.status is discord.Status.offline, members)
    offline = set(offline)
    bots = filter(lambda m: m.bot, members)
    bots = set(bots)
    users = members - bots

    embed = discord.Embed(
        title = f'{ctx.guild.name}',
        description = f'*{ctx.guild.description}*\n \n**Владелец: **' + '<@' + owner + '>', 
        color = discord.Color.from_rgb(244, 127, 255),
        timestamp = ctx.message.created_at
        )
    embed.set_thumbnail(url = icon)
    # embed.add_field(name = 'Овнер', value = owner, inline = False)
    # embed.add_field(name = 'ID', value = id, inline = True)
    # embed.add_field(name = 'Эмодзи', value = emojis, inline = True)
    # embed.add_field(name = 'Максимальное кол-во', value = mmembers, inline = True)
    embed.add_field(name = 'Активность', value = f'<:online:929006151549452288>Онлайн: **{len(users - offline)}**\n<:offline:929005971248934922>Оффлайн: **{len(users & offline)}**', inline = True)
    # embed.add_field(name = "Online Users", value = str(len(users - offline)))
    # embed.add_field(name = "Offline Users", value = str(len(users & offline)))
    embed.add_field(name = 'Кол-во участников', value = f'<:image11:931630270417862656> Всего: **{memberCount}**\n<:image12:931630269767753788> Людей: **{len(people)}**\n<:bot:931623329050288229> Ботов: **{len(bot)}**', inline = True) 
    embed.add_field(name = 'Каналы и категории', value = f'<a:st2:903087219802263592> Категорий: **{categories}**\n<:channel:931570849838952488> Каналов: **{channels}**\n<:text:931570884999778304> Текстовых: **{text_channels}**\n<:voice:931570641717571675> Голосовых: **{voice_channels}**', inline = True)
    embed.add_field(name = 'Дата создания', value = created, inline = True)
    # embed.add_field(name = 'Высшая роль', value = ctx.guild.roles[-1], inline = False)
    embed.add_field(name='Уровеь проверки', value = str(ctx.guild.verification_level), inline = True)
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
        '<a:st1:903087219777093642> Розыгрыши и поощрения для активных модеров;\n'
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
async def famq(ctx, user:discord.Member = None):
    channel = bot.get_channel(874398614892474409)
    embed = discord.Embed(
        description = '__Чтобы получить роль вашей фамы, вам нужно набрать минимум 10 плюсов с названием фамы.__\n\n__Чтобы открыть доступ к каналам - нажмите на реакцию в <#884710136617250827>__', 
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.set_footer(text = ctx.guild.name)
    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()

    if user is None:
        await channel.send(embed = embed)
    else:
        await channel.send(user.mention, embed = embed)


@bot.command(aliases = ['выдача'])
async def giverole(ctx, user:discord.Member = None):
    channel = bot.get_channel(874398614892474409)
    embed = discord.Embed(
        description = '__Чтобы получить роль уже существующей на этом сервере фамы, вам нужно обратиться к овнеру фамы (ЛС или тегнуть).__,',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.set_footer(text = ctx.guild.name)
    embed.timestamp = datetime.datetime.utcnow()

    if user is None:
        await channel.send(embed = embed)
    else:
        await channel.send(user.mention, embed = embed)


@bot.command(aliases = ['овнер'])
async def owner(ctx, user:discord.Member = None):
    channel = bot.get_channel(931497100485746688)
    embed = discord.Embed(
        title = 'Информация для овнеров',
        description = '__План действий:__\n<a:01:884718335776948234> Самостоятельно создать роль фамы - жми на кнопку **"Создание роли"**\n<a:02:884718334644477982> Самостоятельно выдать роли всем членам своей фамы - жми на кнопку **"Выдача ролей"**', 
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon_url)
    if user is None:
        await channel.send(embed = embed, components = [ [
        Button(style = ButtonStyle.green, label = 'Создание роли', emoji = '1️⃣'),
        Button(style = ButtonStyle.red, label = 'Выдача ролей', emoji = '2️⃣')
    ] ])
    else:
        await channel.send(user.mention, embed = embed, components = [ [
        Button(style = ButtonStyle.green, label = 'Создание роли', emoji = '1️⃣'),
        Button(style = ButtonStyle.red, label = 'Выдача ролей', emoji = '2️⃣')
    ] ])

    cycle = True
    while cycle:
        response = await bot.wait_for('button_click')
        # if response.channel == ctx.channel:
        if response.component.label == 'Создание роли':
            embed = discord.Embed(
                title = 'Создание роли',
                description = '__Чтобы создать роль своей фамы нужно прописать слеш команду__ `/создать `\n\nВ аргументе `<color>` нужно выбрать любой цвет по вашему желанию для роли фамы.\nВ аргументе `<name>` нужно указать название твоей фамы с большой буквы и ОБЯЗАТЕЛЬНО приписать Famq **(Пример: Union Famq)**', 
                color = discord.Color.from_rgb(244, 127, 255)
            )
            embed.set_footer(text = ctx.guild.name)
            embed.timestamp = datetime.datetime.utcnow()
            await response.respond(embed = embed)
        elif response.component.label == 'Выдача ролей':
            embed1 = discord.Embed(
                title = 'Выдача ролей',
                description = '__Чтобы выдать роль своей фамы нужно прописать слеш команду__ `/выдать`\n\nВ аргументе `<role>` нужно указать роль, которую вы только что создали.\nВ аргументе `<user>` - упоминание одного из членов фамы.',
                color = discord.Color.from_rgb(244, 127, 255)
                )
            embed1.set_footer(text = ctx.guild.name)
            embed1.timestamp = datetime.datetime.utcnow()
            await response.respond(embed = embed1)


# @bot.command(aliases = ['создать'])
# @commands.has_any_role(910227213708836884, 884510313486098443, 903783220066258945)
# async def create(ctx, color, *, arg):
#     guild = ctx.guild
#     role = await guild.create_role(name = arg, colour = discord.Colour(int(color, 0)), hoist = True)
#     embed = discord.Embed(
#         title = 'Роль успешно создана!',
#         description = f'Роль фамы **{role.mention}** создана!\nЦвет **{color}** применён!\n\nID роли фамы: **{role.id}**\n\nОвнер фамы: {ctx.author.mention}',
#         color = discord.Color(int(color, 0)),
#         timestamp = datetime.datetime.utcnow()
#         )
#     embed.set_thumbnail(url = ctx.guild.icon_url)
#     embed.set_footer(text = 'Famq&News Bot')
#     await ctx.reply(embed = embed)


# @bot.command(aliases = ['выдать'])
# @commands.has_any_role(910227213708836884, 884510313486098443, 903783220066258945)
# async def give(ctx, role: discord.Role, user: discord.Member):
#     if user is None:
#         user = ctx.author
#         await ctx.message.add_reaction('<a:ok6:903086917371965450>')
#         await user.add_roles(role)
#     if role in user.roles:
#         em = discord.Embed(
#             description = 'Пользователь уже имеет эту роль!',
#             color = discord.Color.from_rgb(255, 0, 0)
#             )
#         em.set_footer(text = 'Famq&News Bot')
#         em.timestamp = datetime.datetime.utcnow()
#         await ctx.reply(embed = em)
#     else:
#         await ctx.message.add_reaction('<a:ok6:903086917371965450>')
#         await user.add_roles(role)


@bot.command(aliases = ['забрать'])
@commands.has_any_role(910227213708836884, 884510313486098443, 903783220066258945)
async def remove(ctx, role: discord.Role, user: discord.Member):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.message.add_reaction('<a:ok6:903086917371965450>')
    else:
        em = discord.Embed(
            description = ' Пользователь не имеет эту роль!',
            color = discord.Color.from_rgb(255, 0, 0)
            )
        em.set_footer(text = 'Famq&News Bot')
        em.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed = em)
    

@bot.command(aliases = ['предл'])
async def predl(ctx):
    channel = bot.get_channel(921033910899605526)
    embed = discord.Embed(
        title = 'Предложка Famq&News',
        description = '*Если вы хотите проинформировать модерацию о каком-либо событии/итоге МП/новом лидере и т.д. на сервере, то напишите в этот канал сообщение по форме, предоставленной ниже. После того, как вы отправите сообщение, оно удалится, а содержимое отправится в модерский канал на проверку.*\n\n**Примерная форма сообщения:**\n**1.** __№ сервера;__\n**2.** __Тип события (итог МП, новый лидер, событие и т.п.);__\n**3.** __Док-ва в виде видео или скрин, а также время происшедшего (если есть)__\n\nЗа каждую правильно отправленную информацию вам будут начисляться виртуальные деньги в экономике бота <@292953664492929025>, на которые можно купить различные роли и плюшки.',
        color = discord.Color.from_rgb(244, 127, 255)
        )
    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.set_footer(text = ctx.guild.name)
    embed.set_image(url = ctx.guild.banner_url)

    await channel.send(embed = embed)


@bot.event
async def on_message(message):
    if message.channel.id == 921033910899605526:
        time = message.created_at.strftime('%Y.%m.%d %H:%M:%S')
        embed = discord.Embed(
            title ="Предложка пополнена!",
            description = f"__Автор:__ {message.author.mention} {message.author}",
            color = discord.Color.from_rgb(244, 127, 255)
            )
        embed.add_field(name = "Содержимое сообщения:", value = message.content)
        embed.set_footer(text = 'Cообщение отправлено: ' + time)
        channel = bot.get_channel(931497036249980928)
        await channel.send('<@&903780351640469574>', embed = embed)
        await message.delete()

    else:
        pass

    await bot.process_commands(message)


@bot.event
async def on_user_update(before, after):
    if before.avatar != after.avatar:
        channellog = bot.get_channel(874520061069623388)
        channel = bot.get_channel(930078480249544745)
        embed = discord.Embed(
            title ="Новая аватарка",
            color = discord.Color.from_rgb(65, 121, 78)
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
            color = discord.Color.from_rgb(65, 121, 78),
            )
        embedname.timestamp = datetime.datetime.utcnow()
        embedname.set_thumbnail(url = after.avatar_url)
        embedname.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
        embedname.set_footer(text = 'Famq&News Bot')
        
        await channellog.send(embed = embedname)

    if before.discriminator != after.discriminator:
        channellog = bot.get_channel(874520061069623388)
        embedtag = Embed(
            title = "Тэг пользователя изменен",
            color = discord.Color.from_rgb(65, 121, 78),
            )
        embedtag.timestamp = datetime.datetime.utcnow()
        embedtag.set_thumbnail(url = after.avatar_url)
        embedtag.add_field(name = 'До изменения', value = before.discriminator, inline = True)
        embedtag.add_field(name = 'После изменения', value = after.discriminator, inline = True)
        embedtag.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
        embedtag.set_footer(text = 'Famq&News Bot')
            
        await channellog.send(embed = embedtag)


@bot.event
async def on_member_update(before, after):
        if before.display_name != after.display_name:
            channellog = bot.get_channel(874520061069623388)
            embed = Embed(title = "Ник на сервере изменен",
                          color = discord.Color.from_rgb(65, 121, 78),
                          )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_thumbnail(url = after.avatar_url)
            embed.add_field(name = 'До изменения', value = before.display_name, inline = True)
            embed.add_field(name = 'После изменения', value = after.display_name, inline = True)
            embed.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
            embed.set_footer(text = 'Famq&News Bot')

            await channellog.send(embed = embed)

        elif before.roles != after.roles:
            channellog = bot.get_channel(874520061069623388)
            embed1 = Embed(title = "Роль изменена",
                          color = discord.Color.from_rgb(65, 121, 78),
                          )
            embed1.timestamp = datetime.datetime.utcnow()
            embed1.set_thumbnail(url = after.avatar_url)
            embed1.add_field(name = 'До изменения', value = ", ".join([r.mention for r in before.roles]), inline = True)
            embed1.add_field(name = 'После изменения', value = ", ".join([r.mention for r in after.roles]), inline = True)
            embed1.set_author(name = f'{after.name}#{after.discriminator}', icon_url = after.avatar_url)
            embed1.set_footer(text = 'Famq&News Bot')

            await channellog.send(embed = embed1)


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
    embed.add_field(name = 'Канал:', value = message.channel, inline = False)
    embed.set_footer(text = 'Cообщение отправлено: ' + time)
    channel = bot.get_channel(874520061069623388)
    await channel.send(embed = embed)


@slash.slash(
    name = "создать",
    description = "Создать роль своей фамы!",
    guild_ids = [833342247432355840],
    options = [create_option(
        name = 'color',
        description = 'Выбери цвет роли!',
        required = True,
        option_type = 3,
        choices = [
            create_choice(
                name = 'Чёрный',
                value = '0x000001'
            ),
            create_choice(
                name = 'Белый',
                value = '0xFFFFFF'
            ),
            create_choice(
                name = 'Серый',
                value = '0x808080'
            ),
            create_choice(
                name = 'Фиолетовый',
                value = '0x800080'
            ),
            create_choice(
                name = 'Розовый',
                value = '0xFF1493'
            ),
            create_choice(
                name = 'Пурпурный',
                value = '0xFF00FF'
            ),
            create_choice(
                name = 'Красный',
                value = '0xFF0000'
            ),
            create_choice(
                name = 'Оранжевый',
                value = '0xFF4500'
            ),
            create_choice(
                name = 'Коричневый',
                value = '0x8B4513'
            ),
            create_choice(
                name = 'Жёлтый',
                value = '0xFFFF00'
            ),
            create_choice(
                name = 'Зелёный',
                value = '0x008000'
            ),
            create_choice(
                name = 'Лаймовый',
                value = '0x00FF00'
            ),
            create_choice(
                name = 'Голубенький',
                value = '0x00FFFF'
            ),
            create_choice(
                name = 'Синий',
                value = '0x0000FF'
            ),
            create_choice(
                name = 'Морской',
                value = '0x191970'
            )
        ]
    ),
    create_option(
        name = 'name',
        description = 'Пропиши название фамы! После названия обязательно приписать "Famq". (Пример: Primer Famq)',
        required = True,
        option_type = 3,
        )
    ]
)
async def create(ctx: SlashContext, color: str, name: str):  
    role = await ctx.guild.create_role(name = name, colour = discord.Colour(int(color, 0)), hoist = True)
    
    owner_role1 = ctx.guild.get_role(903783220066258945)
    admin1 = ctx.guild.get_role(884510313486098443)

    if owner_role1 or admin1 in ctx.author.roles:
        em = discord.Embed(
            title = 'Роль успешно создана!',
            description = f'Роль фамы **{role.mention}** создана!\nЦвет **{color}** применён!\n\nID роли фамы: **{role.id}**\n\nОвнер фамы: {ctx.author.mention}\n\n`Если имеется желание поменять цвет роли, то пишите` - <@909585478037155913>, <@494833692909502485>, <@437865730332033024>',
            color = discord.Color(int(color, 0)),
            timestamp = datetime.datetime.utcnow()
        )
        em.set_thumbnail(url = ctx.guild.icon_url)
        em.set_footer(text = 'Famq&News Bot')
        await ctx.reply(embed = em)
        await ctx.author.add_roles(role)
    else:
        em1 = discord.Embed(
            title = 'Ошибка!',
            description = f'Ты не имеешь права использовать эту команду!\nУ тебя нет роли {owner_role1.mention}',
            timestamp = datetime.datetime.utcnow()
        )
        em1.set_thumbnail(url = ctx.guild.icon_url)
        em1.set_footer(text = 'Famq&News Bot')
        
        await ctx.reply(embed = em1, hidden = True)



@slash.slash(
    name = "выдать",
    description = "Выдайте роль членам своей фамы!",
    guild_ids = [833342247432355840],
    options = [create_option(
        name = 'role',
        description = 'Выбери роль!',
        required = True,
        option_type = 8
    ),
    create_option(
        name = 'user',
        description = 'Кому выдать роль?',
        required = True,
        option_type = 6,
        )
    ]
)
async def give(ctx: SlashContext, role: str, *, user: str):    
    owner_role = ctx.guild.get_role(903783220066258945)
    admin = ctx.guild.get_role(884510313486098443)
    if role.position >= ctx.author.top_role.position:
        em0 = discord.Embed(
            title = 'Ошибка!',
            description = 'Ты не имеешь права выдать роль как у тебя или выше!',
            timestamp = datetime.datetime.utcnow()
        )
        em0.set_thumbnail(url = ctx.guild.icon_url)
        em0.set_footer(text = 'Famq&News Bot')
        
        await ctx.reply(embed = em0, hidden = True)
    elif owner_role or admin in ctx.author.roles:
        em = discord.Embed(
            description = f'Роль {role.mention} выдана {user.mention}!',
            timestamp = datetime.datetime.utcnow()
        )
        em.set_footer(text = 'Famq&News Bot')
        await ctx.reply(embed = em)
        await user.add_roles(role)
    else:
        em1 = discord.Embed(
            title = 'Ошибка!',
            description = f'Ты не имеешь права использовать эту команду!\nУ тебя нет роли {owner_role.mention}',
            timestamp = datetime.datetime.utcnow()
        )
        em1.set_thumbnail(url = ctx.guild.icon_url)
        em1.set_footer(text = 'Famq&News Bot')
        
        await ctx.reply(embed = em1, hidden = True)

        
bot.run('OTkyNTI0OTYyMTQ3NjE0NzIw.Gh78qO.ECeYQXV3Stc9tbhPbE5aqIjuZqtX_yMnSqJPFI')
