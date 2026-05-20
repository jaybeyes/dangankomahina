import os
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬ_СВОЙ_ТОКЕН_СЮДА")

# ─────────────────────────────────────────────
# СЛУЧАЙНЫЕ СООБЩЕНИЯ (оригинальные)
# ─────────────────────────────────────────────
MESSAGES = [
    "Obtained Hope Fragment.",
    "Nagito's Report Card has been updated based on your experience with him.",
    "Hajime's Report Card has been updated based on your experience with him.",
    "Invite Hajime to hang out.",
    "Invite Nagito to hang out.",
    "You have obtained a present: Nagito's Undergarments.",
    "You have obtained a present: Hajime's Undergarments.",
    "Hajime and I grew a little closer today.",
    "Nagito and I grew a little closer today.",
]

# ─────────────────────────────────────────────
# FREE TIME EVENTS
# ─────────────────────────────────────────────
FREE_TIME_CHARACTERS = ["Nagito", "Hajime"]

# ─────────────────────────────────────────────
# СЧЁТЧИК DESPAIR/HOPE
# ─────────────────────────────────────────────
DESPAIR_WORDS = {"despair", "sad", "kill", "pain", "hate", "weird", "awful", "hopeless"}
HOPE_WORDS    = {"happy", "love", "hope", "forward", "like", "great", "amazing", "wonderful"}

# ─────────────────────────────────────────────
# СПИСОК ПОДАРКОВ ДЛЯ MONOMONO MACHINE
# ─────────────────────────────────────────────
GIFTS = [
    "Mineral Water Monocoin", "Ramune Monocoin", "Coconut Juice", "Blue Ram Monocoin",
    "Civet Coffee", "Cinnamon Tea", "Non-Alcoholic Wine", "Prepackaged Orzotto",
    "Chocolate Chip Jerky", "Cod Roe Baguette", "Gugelhupf Cake", "Hardtack of Hope",
    "Sweet Bun Bag", "Potato Chips", "Viva Ice", "Jabba's Natural Salt", "Cocoshimi",
    "Sunflower Seeds", "Coconut", "Iroha T-Shirt", "Brightly Colored Jeans", "Apron Dress",
    "Falkor's Muffler", "Fresh Bindings", "Queen's Straitjacket", "Spy Spike",
    "Secret Boots", "Safety Half-Shoes", "Passionate Glasses", "Bvlbari's Gold",
    "Earring of Crushed Evil", "Silver Ring", "Hope's Peak Ring", "Spectre Ring",
    "Cloth Wrap Backpack", "Another Hope", "Jabbaian Jewelry", "Biggest Fantom",
    "Ubiquitous Handbook", "Millennium Prize Problems", "Tips and Tips 2nd Edition",
    "Ogami Clan Codex", "Men's Manma", "Kiss Note", "Black Rabbit Picture Book",
    "2.5D Headphones", "Radiosonde", "Male Cylinder", "Measuring Flask",
    "Razor Ramon HG", "Infrared Thermometer", "Flash Suppressor", "Lilienthal's Wings",
    "Kirlian Photography", "Mr Stapler", "Small Degenerated Reactor", "Many-Sided Dice Set",
    "The Funbox", "The Funplane", "American Clacker", "Power Gauntlet", "Mesopotamia",
    "Nitro Racer", "Slap Bracelet", "Gag Ball", "Kokeshi Dynamo", "Go Stone",
    "Message In a Bottle", "Old Timey Radio", "Antique Doll", "The Second Button",
    "Moon Rock", "Another Battle", "Desperation", "1000 Cherry Blossoms",
    "Paper '10th Act Verse'", "Marine Snow", "Gold Coated Sheath", "Mini Wave-Dissipaters",
    "Stardust", "Japanese Tea Cup", "Two-Sided Ukulele", "Collapsible Fishing Rod",
    "Bojobo Dolls", "Century Potpourri", "Absolute Tuning Fork", "Seven Sword",
    "Sand God's Storm Horn", "Memory Notebook", "Mukuro's Knife", "Broken Warhead",
    "Girl with the Bear Hairpin", "Bar", "Dip Pen", "Tissue", "Jabba the Frog",
    "Iguana Daughter", "Dull Kitchen Knife", "Occult Photo Frame", "Lust Setsugekka",
    "Rose In Vitro", "Skullhead Mask", "Compact Costume", "Angel's Fruit", "Bandage Wrap",
    "Secret Wind Sword Book", "Hagakure Crystal Ball", "Used Carrot",
    "Nagito's Undergarments", "Byakuya's Undergarments", "Gundham's Undergarments",
    "Kazuichi's Undergarments", "Teruteru's Undergarments", "Nekomaru's Undergarments",
    "Fuyuhiko's Undergarments", "Akane's Undergarments", "Chiaki's Undergarments",
    "Sonia's Undergarments", "Hiyoko's Undergarments", "Mahiru's Undergarments",
    "Mikan's Undergarments", "Ibuki's Undergarments", "Peko's Undergarments",
    "Toy Camera", "Replica Sword", "An An Aan", "Man's Nut", "Summer Festival Tree",
    "R/C 4WD Battler Taro", "Wooden Stick", "Usami Strap", "Danganronpa IF",
]

# ─────────────────────────────────────────────
# СЛУЧАЙНЫЕ ИВЕНТЫ (каждые 100 сообщений)
# ─────────────────────────────────────────────
RANDOM_EVENTS = [
    "You find a broken vending machine and someone immediately insists it can still be fixed by 'kicking it correctly.'",
    "A sudden rainstorm forces you both to share the only small piece of shelter on the beach.",
    "A washed-up crate contains something completely useless but weirdly expensive-looking.",
    "You discover someone has been organizing coconuts by size on the shore.",
    "A campfire is still warm, and someone clearly left it mid-cooking.",
    "A Monokuma plush is half-buried in the sand and slightly soggy.",
    "A note on a tree gives extremely confident advice about survival, but it's clearly wrong.",
    "A cave has neatly stacked stones that look like someone was bored for hours.",
    "A fishing rod is stuck in the sand and clearly hasn't caught anything in days.",
    "A strange fruit tree grows nearby, and someone insists it's 'definitely safe' with no proof.",
    "You find a makeshift base that looks like it was abandoned mid-argument.",
    "A radio plays static, and someone keeps trying to 'fix the signal by shaking it.'",
    "Footprints in the sand lead in a circle and end where they started.",
    "A locked suitcase is found, and everyone immediately disagrees on whether to open it.",
    "Butterflies gather near food and someone tries to 'train' them.",
    "A cave wall has doodles that are clearly drawn by someone with too much time.",
    "A broken Monobeast part is being used as a makeshift chair.",
    "A hammock is strung up badly and clearly about to fall apart.",
    "Seashells are arranged into random shapes for no clear reason.",
    "A metal object is buried in the sand and someone tries to claim it as 'their treasure.'",
    "A rope ladder is found, but no one knows who put it there or why.",
    "A backpack is left behind with random supplies mixed with garbage.",
    "A mirror is found in the jungle and immediately becomes a source of argument about appearance.",
    "Coconuts are stacked dangerously high and wobble whenever someone walks by.",
    "A broken watch still ticks, and someone insists it's 'probably fine.'",
    "A notebook is found with extremely dramatic survival plans written inside.",
    "A campfire circle is set up but no firewood is anywhere nearby.",
    "A bottle washes up containing something that turns out to be useless instructions.",
    "Tree marks look like someone was counting days but gave up halfway.",
    "A single shoe is found and someone immediately tries to find its 'tragic backstory.'",
    "A metal door in a cliff is slightly open, but nobody wants to go first.",
    "A bird keeps stealing food and one of you tries to negotiate with it.",
    "A cooking pot is left behind with something questionable still inside.",
    "Wet footprints lead into the ocean and disappear.",
    "A compass spins weirdly and someone blames the island's 'vibes.'",
    "A rope is tied between trees for no obvious reason.",
    "A radio tower is visible far away, but no one remembers seeing it before.",
    "A notebook is found with detailed, overly dramatic diary entries.",
    "A carved doll is placed near the beach like some kind of joke.",
    "Insects gather near food and someone tries to scare them off unsuccessfully.",
    "A set of keys is found, but no one knows what they open.",
    "A tree is split cleanly and someone immediately suspects a competition.",
    "A Monokuma mask is found and someone refuses to touch it.",
    "A stone path appears, but it clearly just leads to another part of the island.",
    "A shell makes clicking sounds when tapped and someone uses it to annoy others.",
    "A camp chair is left facing the ocean like someone was dramatically thinking.",
    "A broken flashlight still works 'sometimes,' but inconsistently.",
    "Stone markers in the water look like someone was practicing something.",
    "A burned symbol on a tree looks suspicious but turns out to be meaningless.",
    "A jar of insects is labeled in handwriting no one recognizes.",
    "A flag is stuck in a tree claiming territory nobody agreed on.",
    "Folded clothes are found and immediately become a source of embarrassment.",
    "A half-buried statue is discovered and someone tries to name it.",
    "A fishing net catches something unexpected and everyone argues over ownership.",
    "Music briefly plays from somewhere nearby, but no one admits hearing it clearly.",
    "A broken phone turns on but has no signal or useful apps.",
    "A small altar-like setup is found but turns out to be someone's 'joke project.'",
    "Footprints appear leading out of the ocean and immediately confuse everyone.",
    "A rope bridge is discovered but looks unsafe enough to cause debate for hours.",
    "A shadow passes quickly between trees and someone insists it was just 'the wind.'",
]

# ─────────────────────────────────────────────
# СОСТОЯНИЕ ЧАТОВ
# ─────────────────────────────────────────────
# message_counters[chat_id]        — счётчик до следующего случайного сообщения
# thresholds[chat_id]              — порог для случайного сообщения
# event_counters[chat_id]          — счётчик до следующего случайного ивента (каждые 100)
# despair_level[chat_id]           — уровень отчаяния (-100..+100, отрицательное = despair)
# gacha_counters[chat_id][user_id] — сколько сообщений написал каждый пользователь
# gacha_inventory[chat_id][user_id]— список выигранных подарков
# pending_free_time[chat_id]       — {character, waiting_reply: True/False}

message_counters: dict[int, int] = {}
thresholds: dict[int, int] = {}
event_counters: dict[int, int] = {}
despair_level: dict[int, int] = {}
gacha_counters: dict[int, dict[int, int]] = {}
gacha_inventory: dict[int, dict[int, list]] = {}
pending_free_time: dict[int, dict] = {}

def get_new_threshold() -> int:
    return random.randint(15, 60)

def init_chat(chat_id: int):
    if chat_id not in message_counters:
        message_counters[chat_id] = 0
        thresholds[chat_id] = get_new_threshold()
        event_counters[chat_id] = 0
        despair_level[chat_id] = 0
        gacha_counters[chat_id] = {}
        gacha_inventory[chat_id] = {}
        logging.info(f"Новый чат {chat_id}, первый порог: {thresholds[chat_id]}")

def init_user(chat_id: int, user_id: int):
    if user_id not in gacha_counters[chat_id]:
        gacha_counters[chat_id][user_id] = 0
        gacha_inventory[chat_id][user_id] = []

# ─────────────────────────────────────────────
# ОБРАБОТЧИК СООБЩЕНИЙ
# ─────────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_chat or not update.effective_user:
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text or ""
    text_lower = text.lower()

    init_chat(chat_id)
    init_user(chat_id, user_id)

    # ── FREE TIME: ждём ответ ──────────────────
    if pending_free_time.get(chat_id, {}).get("waiting"):
        character = pending_free_time[chat_id]["character"]
        if any(w in text_lower for w in ["да", "yes", "хочу", "sure", "yeah", "ok", "ок"]):
            await update.message.reply_text(
                f"You're spending time together! Cute! Is this a date? 💕\n"
                f"*{character}'s Report Card has been updated.*"
            )
        else:
            if character == "Nagito":
                await update.message.reply_text(
                    "Heartbreaking... 💔\n"
                    "\"That's okay. Trash like me doesn't deserve your time anyway. "
                    "I'll just go think about hope alone.\"\n— Nagito"
                )
            else:
                await update.message.reply_text(
                    "Heartbreaking... 💔\n"
                    "\"Oh. Alright then.\"\n— Hajime, trying to look unbothered"
                )
        pending_free_time[chat_id]["waiting"] = False
        return

    # ── СЧЁТЧИК DESPAIR/HOPE ──────────────────
    words = set(text_lower.split())
    despair_hits = words & DESPAIR_WORDS
    hope_hits    = words & HOPE_WORDS
    delta = len(hope_hits) - len(despair_hits)
    despair_level[chat_id] = max(-100, min(100, despair_level[chat_id] + delta))

    # ── GACHA COUNTER ─────────────────────────
    gacha_counters[chat_id][user_id] += 1
    if gacha_counters[chat_id][user_id] % 50 == 0:
        gift = random.choice(GIFTS)
        gacha_inventory[chat_id][user_id].append(gift)
        username = update.effective_user.first_name
        await update.message.reply_text(
            f"🎰 *Monomono Machine activated!*\n"
            f"Congratulations, {username}! You won:\n"
            f"✨ *{gift}*\n\n"
            f"Use /gift to give it to someone!"
        )

    # ── СЧЁТЧИК СООБЩЕНИЙ (случайное сообщение) ──
    message_counters[chat_id] += 1
    logging.info(f"Чат {chat_id}: {message_counters[chat_id]}/{thresholds[chat_id]}")

    if message_counters[chat_id] >= thresholds[chat_id]:
        # Шанс 30% — Free Time Event вместо обычного сообщения
        if random.random() < 0.30:
            character = random.choice(FREE_TIME_CHARACTERS)
            pending_free_time[chat_id] = {"character": character, "waiting": True}
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"[FREE TIME]\nDo you want to spend time with {character}? (yes/no)"
            )
        else:
            # Шанс 15% — бросить кубик вместо обычного сообщения
            if random.random() < 0.15:
                await context.bot.send_dice(chat_id=chat_id, emoji="🎲")
            else:
                msg = random.choice(MESSAGES)
                await context.bot.send_message(chat_id=chat_id, text=msg)

            # Редкий комментарий про уровень despair
            level = despair_level[chat_id]
            if level <= -20 and random.random() < 0.5:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="⚠️ The despair level in this chat is rising... Monokuma is pleased."
                )
            elif level >= 20 and random.random() < 0.5:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="✨ The hope level is unusually high today. Nagito is crying tears of joy somewhere."
                )

        message_counters[chat_id] = 0
        thresholds[chat_id] = get_new_threshold()

    # ── СЧЁТЧИК ИВЕНТОВ (каждые 100 сообщений) ──
    event_counters[chat_id] += 1
    if event_counters[chat_id] >= 100:
        event = random.choice(RANDOM_EVENTS)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🌴 *Island Event!*\n{event}"
        )
        event_counters[chat_id] = 0

# ─────────────────────────────────────────────
# КОМАНДЫ
# ─────────────────────────────────────────────
async def cmd_monostatus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает статус до следующей гачи и уровень despair."""
    if not update.effective_chat or not update.effective_user:
        return
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    init_chat(chat_id)
    init_user(chat_id, user_id)

    count = gacha_counters[chat_id][user_id]
    next_gacha = 50 - (count % 50)
    level = despair_level[chat_id]

    if level > 30:
        mood = "✨ Overflowing with hope!"
    elif level > 10:
        mood = "🙂 Mostly hopeful."
    elif level >= -10:
        mood = "😐 Neutral. Monokuma is watching."
    elif level >= -30:
        mood = "😟 Despair is creeping in..."
    else:
        mood = "💀 This chat is drowning in despair. Monokuma approves."

    gifts_count = len(gacha_inventory[chat_id][user_id])
    username = update.effective_user.first_name

    await update.message.reply_text(
        f"📊 *Mono Status — {username}*\n\n"
        f"🎰 Next Monomono Machine in: *{next_gacha}* messages\n"
        f"🎁 Gifts in inventory: *{gifts_count}*\n\n"
        f"🌡 Chat mood: {mood}\n"
        f"(Hope/Despair index: {level:+d})"
    )

async def cmd_gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выдаёт случайный подарок из инвентаря."""
    if not update.effective_chat or not update.effective_user:
        return
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    init_chat(chat_id)
    init_user(chat_id, user_id)

    inventory = gacha_inventory[chat_id][user_id]
    if not inventory:
        await update.message.reply_text(
            "You don't have any gifts yet! 😢\n"
            "Keep chatting — the Monomono Machine rewards every 50 messages."
        )
        return

    gift = random.choice(inventory)
    username = update.effective_user.first_name
    await update.message.reply_text(
        f"🎁 *{username}* presents:\n✨ *{gift}*\n\n"
        f"(A wonderful gift, worthy of a future Remnant of Hope... or Despair.)"
    )

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Jabberwock Island! 🌴\n\n"
        "I'm your Monomono Bot. Here's what I do:\n\n"
        "• Every 15–60 messages I'll send a little game notification\n"
        "• Every 50 messages you write, the Monomono Machine activates!\n"
        "• Every 100 messages, a random island event occurs 🌊\n"
        "• Chat mood shifts based on what you write...\n\n"
        "Commands:\n"
        "/monostatus — your gacha progress & chat mood\n"
        "/gift — give someone a gift from your inventory\n\n"
        "Puhuhuhu! Let's hope this island stays peaceful... ʕ•ᴥ•ʔ"
    )

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("monostatus", cmd_monostatus))
    app.add_handler(CommandHandler("gift", cmd_gift))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
