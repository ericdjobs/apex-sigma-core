import asyncio
import hashlib
import secrets

import discord

status_cache = []


def random_capitalize(text):
    new_text = ''
    char_list = list(text)
    while char_list:
        char_choice = char_list.pop(0)
        cap_roll = secrets.randbelow(2)
        if cap_roll == 0:
            char_choice = char_choice.upper()
        new_text += char_choice
    return new_text


async def status_rotation(ev):
    if ev.bot.cfg.pref.status_rotation:
        ev.bot.loop.create_task(status_clockwork(ev))


async def status_clockwork(ev):
    while True:
        if ev.bot.cfg.pref.status_rotation:
            if not status_cache:
                status_files = await ev.db[ev.db.db_cfg.database].StatusFiles.find().to_list(None)
                for status_file in status_files:
                    status_text = status_file.get('Text')
                    status_cache.append(status_text)
            if status_cache:
                status = status_cache.pop(secrets.randbelow(len(status_cache)))
                mode_roll = secrets.randbelow(10)
                if mode_roll == 0:
                    hgen = hashlib.new('md5')
                    hgen.update(status.encode('utf-8'))
                    digest = hgen.hexdigest()
                    max_end = abs(len(digest) - 10)
                    cut = secrets.randbelow(max_end)
                    cut_text = digest[cut:(cut + 10)]
                    status = random_capitalize(cut_text)
                game = discord.Game(name=status)
                try:
                    await ev.bot.change_presence(game=game)
                except discord.ConnectionClosed:
                    pass
        await asyncio.sleep(60)
