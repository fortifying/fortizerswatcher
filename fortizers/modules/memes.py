import asyncio
import textwrap
import base64
import glob
import io
import os
import random
import re
import string
import urllib.request
 
from io import BytesIO
from pathlib import Path
from typing import List
 
import nltk # shitty lib, but it does work
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
 
from PIL import Image, ImageEnhance, ImageOps, ImageFont, ImageDraw
from spongemock import spongemock
from telethon.tl.types import DocumentAttributeFilename
from telegram import Message, Update, Bot
from telegram.error import BadRequest
from telegram.ext import CommandHandler, run_async
from zalgo_text import zalgo
 
from deeppyer import deepfry
from fortizers.modules.disable import DisableAbleCommandHandler
from fortizers import dispatcher, spamcheck, DEEPFRY_TOKEN
from fortizers.modules.languages import tl
 
MAXNUMURL = 'https://raw.githubusercontent.com/atanet90/expression-pack/master/meta'
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
 
# D A N K modules by @deletescape vvv
 
@spamcheck
@run_async
def owo(update, context):
    chat = update.effective_chat
    message = update.effective_message
    args = context.args
 
    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tl(chat.id, "I need a message to meme.")
 
    faces = [
        '(・`ω´・)', ';;w;;', 'owo', 'UwU', '>w<', '^w^', '\(^o\) (/o^)/',
        '( ^ _ ^)∠☆', '(ô_ô)', '~:o', ';____;', '(*^*)', '(>_', '(♥_♥)',
        '*(^O^)*', '((+_+))'
    ]
    reply_text = re.sub(r'[rl]', "w", data)
    reply_text = re.sub(r'[ｒｌ]', "ｗ", data)
    reply_text = re.sub(r'[RL]', 'W', reply_text)
    reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
    reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
    reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
    reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
    reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
    reply_text += ' ' + random.choice(faces)
 
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)
 
 
@spamcheck
@run_async
def deepfryer(update, context):
    message = update.effective_message
    chat = update.effective_chat
    if message.reply_to_message:
        data = message.reply_to_message.photo
        data2 = message.reply_to_message.sticker
    else:
        data = []
        data2 = []
 
    # check if message does contain media and cancel when not
    if not data and not data2:
        message.reply_text(tl(chat.id, "What am I supposed to do with this?!"))
        return
 
    # download last photo (highres) as byte array
    if data:
        photodata = data[len(data) - 1].get_file().download_as_bytearray()
        image = Image.open(io.BytesIO(photodata))
    elif data2:
        sticker = context.bot.get_file(data2.file_id)
        sticker.download('sticker.png')
        image = Image.open("sticker.png")
 
    # the following needs to be executed async (because dumb lib)
    bot = context.bot
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        process_deepfry(image, message.reply_to_message, bot, context))
    loop.close()
 
 
async def process_deepfry(image: Image, reply: Message, bot: Bot, context):
    image = await deepfry(img=image,
                          token=DEEPFRY_TOKEN,
                          url_base='westeurope')
 
    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
 
    # send it back
    bio.seek(0)
    reply.reply_photo(bio)
    if Path("sticker.png").is_file():
        os.remove("sticker.png")
 
 
@spamcheck
@run_async
def stretch(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        count = random.randint(3, 10)
        reply_text = re.sub(
            r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])',
            (r'\1' * count),
            message.reply_to_message.text)
        message.reply_to_message.reply_text(reply_text)
 
 
@spamcheck
@run_async
def vapor(update, context):
    args = context.args
    message = update.effective_message
    chat = update.effective_chat  # type: Optional[Chat]
 
    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tl(chat.id, "I need a message to meme.")
 
    reply_text = str(data).translate(WIDE_MAP)
 
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)
 
 
# D A N K modules by @deletescape ^^^
# Less D A N K modules by @skittles9823 # holi fugg I did some maymays vvv
 
 
# based on
# https://github.com/wrxck/mattata/blob/master/plugins/copypasta.mattata
@spamcheck
@run_async
def copypasta(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        emojis = [
            "😂",
            "😂",
            "👌",
            "✌",
            "💞",
            "👍",
            "👌",
            "💯",
            "🎶",
            "👀",
            "😂",
            "👓",
            "👏",
            "👐",
            "🍕",
            "💥",
            "🍴",
            "💦",
            "💦",
            "🍑",
            "🍆",
            "😩",
            "😏",
            "👉👌",
            "👀",
            "👅",
            "😩",
            "🚰"]
        reply_text = random.choice(emojis)
        # choose a random character in the message to be substituted with 🅱️
        b_char = random.choice(message.reply_to_message.text).lower()
        for c in message.reply_to_message.text:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(emojis)
        message.reply_to_message.reply_text(reply_text)
 
 
@spamcheck
@run_async
def bmoji(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        # choose a random character in the message to be substituted with 🅱️
        b_char = random.choice(message.reply_to_message.text).lower()
        reply_text = message.reply_to_message.text.replace(
            b_char, "🅱️").replace(b_char.upper(), "🅱️")
        message.reply_to_message.reply_text(reply_text)
 
 
@spamcheck
@run_async
def forbesify(update, context):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = ''
 
    data = data.lower()
    accidentals = ['VB', 'VBD', 'VBG', 'VBN']
    reply_text = data.split()
    offset = 0
 
    # use NLTK to find out where verbs are
    tagged = dict(nltk.pos_tag(reply_text))
 
    # let's go through every word and check if it's a verb
    # if yes, insert ACCIDENTALLY and increase offset
    for k in range(len(reply_text)):
        i = reply_text[k + offset]
        if tagged.get(i) in accidentals:
            reply_text.insert(k + offset, 'accidentally')
            offset += 1
 
    reply_text = string.capwords(' '.join(reply_text))
    message.reply_to_message.reply_text(reply_text)
 
 
@spamcheck
@run_async
def spongemocktext(update, context):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = str('Haha yes, I know how to mock text.')
 
    reply_text = spongemock.mock(data)
    message.reply_text(reply_text)
 
 
@spamcheck
@run_async
def mmf(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text(
            "`Syntax: reply to an image with .mmf` 'text on top' ; 'text on bottom' "
        )
        return
 
    reply_message = message.reply_to_message()
    if not reply_message.media:
        context.bot.editMessageText("```reply to a image/sticker/gif```")
        return
    context.bot.download_file(reply_message.media)
    if context.bot.is_reply:
        data = check_media(reply_message)
        if isinstance(data, bool):
            context.bot.editMessageText("`Unsupported Files...`")
            return
 
        context.bot.editMessageText(
            "Memeifying this image.."
        )
        asyncio.sleep(5)
        text = context.bot.pattern_match.group(1)
        if context.bot.reply_to_msg_id:
            file_name = "meme.jpg"
            to_download_directory = ./downloads/
            downloaded_file_name = os.path.join(
                to_download_directory, file_name)
            downloaded_file_name = context.bot.download_media(
                reply_message, downloaded_file_name,
            )
            dls_loc = downloaded_file_name
        webp_file = draw_meme_text(dls_loc, text)
        context.bot.client.send_file(context.bot.chat_id, webp_file, reply_to=context.bot.reply_to_msg_id)
        context.bot.delete()
        os.remove(webp_file)
        os.remove(dls_loc)
 
 
async def draw_meme_text(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    m_font = ImageFont.truetype(
        "resources/MutantAcademyStyle.ttf", int((70 / 640) * i_width))
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ''
    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)
 
            draw.text(xy=(((i_width - u_width) / 2) - 1, int((current_h / 640)
                                                             * i_width)), text=u_text, font=m_font, fill=(0, 0, 0))
            draw.text(xy=(((i_width - u_width) / 2) + 1, int((current_h / 640)
                                                             * i_width)), text=u_text, font=m_font, fill=(0, 0, 0))
            draw.text(xy=((i_width - u_width) / 2,
                          int(((current_h / 640) * i_width)) - 1),
                      text=u_text,
                      font=m_font,
                      fill=(0,
                            0,
                            0))
            draw.text(xy=(((i_width - u_width) / 2),
                          int(((current_h / 640) * i_width)) + 1),
                      text=u_text,
                      font=m_font,
                      fill=(0,
                            0,
                            0))
 
            draw.text(xy=((i_width - u_width) / 2, int((current_h / 640)
                                                       * i_width)), text=u_text, font=m_font, fill=(255, 255, 255))
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)
 
            draw.text(
                xy=(((i_width - u_width) / 2) - 1, i_height - u_height - int((20 / 640) * i_width)),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=(((i_width - u_width) / 2) + 1, i_height - u_height - int((20 / 640) * i_width)),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=((i_width - u_width) / 2, (i_height - u_height - int((20 / 640) * i_width)) - 1),
                text=l_text, font=m_font, fill=(0, 0, 0))
            draw.text(
                xy=((i_width - u_width) / 2, (i_height - u_height - int((20 / 640) * i_width)) + 1),
                text=l_text, font=m_font, fill=(0, 0, 0))
 
            draw.text(
                xy=((i_width - u_width) / 2, i_height - u_height - int((20 / 640) * i_width)),
                text=l_text, font=m_font, fill=(255, 255, 255))
            current_h += u_height + pad
 
    image_name = "memify.webp"
    webp_file = os.path.join(./downloads/, image_name)
    img.save(webp_file, "WebP")
    return webp_file
 
 
@spamcheck
@run_async
def clapmoji(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        reply_text = "👏 "
        reply_text += message.reply_to_message.text.replace(" ", " 👏 ")
        reply_text += " 👏"
        message.reply_to_message.reply_text(reply_text)
 
 
@spamcheck
@run_async
def zalgotext(update, context):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
 
    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tl(chat.id, "I need a message to meme.")
 
    reply_text = zalgo.zalgo().zalgofy(data)
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)
 
 
# Less D A N K modules by @skittles9823 # holi fugg I did some maymays ^^^
# shitty maymay modules made by @divadsn vvv
 
 
@spamcheck
@run_async
def chinesememes(update, context):
    args = context.args
    message = update.effective_message
    maxnum = urllib.request.urlopen(MAXNUMURL)
    maxnum = maxnum.read().decode("utf8")
    if args:
        num = message.text.split(None, 1)[1]
    else:
        num = random.randint(0, int(maxnum))
    try:
        IMG = "https://raw.githubusercontent.com/atanet90/expression-pack/master/img/{}.jpg".format(
            num)
        maxnum = int(maxnum)
        maxnum -= 1
        context.bot.send_photo(chat_id=message.chat_id,
                       photo=IMG,
                       caption='Image: {} - (0-{})'.format(num,
                                                           maxnum),
                       reply_to_message_id=message.message_id)
    except BadRequest as e:
        message.reply_text("Image not found!")
        print(e)
 
 
# shitty maymay modules made by @divadsn ^^^
@spamcheck
@run_async
def shout(update, context):
    message = update.effective_message
    chat = update.effective_chat  # type: Optional[Chat]
    args = context.args
 
    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = " ".join(args)
    else:
        noreply = True
        data = tl(chat.id, "I need a message to meme.")
 
    msg = "```"
    result = []
    result.append(' '.join([s for s in data]))
    for pos, symbol in enumerate(data[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = data[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")
 
 
__help__ = "memes_help"
 
__mod_name__ = "Memes and etc."
 
COPYPASTA_HANDLER = DisableAbleCommandHandler("cp", copypasta, pass_args=True)
CLAPMOJI_HANDLER = DisableAbleCommandHandler("clap", clapmoji, pass_args=True)
BMOJI_HANDLER = DisableAbleCommandHandler("bify", bmoji, pass_args=True)
MOCK_HANDLER = DisableAbleCommandHandler("mock", spongemocktext, pass_args=True)
OWO_HANDLER = DisableAbleCommandHandler("owo", owo, pass_args=True)
FORBES_HANDLER = DisableAbleCommandHandler("forbes", forbesify, pass_args=True)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch, pass_args=True)
MEMEIFY_HANDLER = DisableAbleCommandHandler("mmf", mmf, pass_args=True)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor", vapor, pass_args=True)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext, pass_args=True)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, pass_args=True)
CHINESEMEMES_HANDLER = DisableAbleCommandHandler("dllm", chinesememes, pass_args=True)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry", deepfryer, admin_ok=True)
 
dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(ZALGO_HANDLER)
dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(CLAPMOJI_HANDLER)
dispatcher.add_handler(BMOJI_HANDLER)
dispatcher.add_handler(FORBES_HANDLER)
dispatcher.add_handler(CHINESEMEMES_HANDLER)
dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER)
dispatcher.add_handler(MEMEIFY_HANDLER)
 
