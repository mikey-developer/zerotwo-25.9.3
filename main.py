"""
from Mikey*dev
https://t.me/mrmikey_dev
02 Chat Manager
"""
import telebot 
from telebot.types import ReplyKeyboardMarkup
import random
import qrcode
import sqlite3
import wikipedia as wiki

bot = telebot.TeleBot("token")

########################
### Main Menu button ###
########################

main = ReplyKeyboardMarkup(
            one_time_keyboard = True,
            resize_keyboard = True
        )
main.row("Chats", "Profile", "Docs")
main.row("Diamonds", "QrCode")
main.row("Support")

global VERSION 
VERSION = "9.3"

# NOTE: Sqlite3 function 
# ! It's for SELECT INSERT functions
def sdb(databasename, sqlquery, parameter = None):
    db = sqlite3.connect(databasename)
    sql = db.cursor()
    sql.execute(sqlquery)
    db.commit() 

def chdb(databasename, sqlquery, parameter = None, u_id = None):
    db = sqlite3.connect(databasename)
    sql = db.cursor()
    for data in sql.execute(sqlquery).fetchone():
        if data[1] == u_id:
            return True
        else:
            return False
   

# NOTE: Simple sending messages without parameters
# ! Do not forget about parse mode
def send(chat_id, message, parse_mode = None):
    bot.send_message(chat_id, message, parse_mode)

# NOTE: Simple delete func
# ! Do not forget about chat and message id
def delete(chat_id, messageid):
    bot.delete_message(chat_id, messageid)

def get_banlist(dbname, sqlquery):
    db = sqlite3.connect(dbname)
    sql = db.cursor()
    sql.execute(sqlquery)
    rows = sql.fetchall()
    db.close()

    if not rows:
        return "Ban list is empty"

    message = "Banned users:*\n\n"
    for row in rows:
        message += f"🆔 {row[2]} — {row[3] if row[3] else 'No Cause'}\n"
    return message

@bot.message_handler(func=lambda message: message.text.lower() == "qrcode")
def ask_qr_input(m):
    mid = m.chat.id
    bot.send_message(mid, "Your QR code input:")
    bot.register_next_step_handler(m, nqr)

def nqr(m):
    qrdo = m.text
    img = qrcode.make(qrdo)
    filename = f"{m.from_user.id}.png"
    img.save(filename)

    with open(filename, "rb") as photo:
        bot.send_photo(
            m.chat.id,
            photo=photo,
            caption="from @zerotwo_cmbot"
        )

# NOTE: Start message bot will register user to database
@bot.message_handler(commands=['start'])
def start_message(m):
    import sqlite3

    def sdb(dbname, query, params=None):
        db = sqlite3.connect(dbname)
        sql = db.cursor()
        if params:
            sql.execute(query, params)
        else:
            sql.execute(query)
        db.commit()
        db.close()

    # Agar private chat bo‘lsa
    if m.chat.type == 'private':
        user_table = str(m.from_user.id)

        # Jadvalni yaratamiz (agar yo‘q bo‘lsa)
        create_table = f"""
            CREATE TABLE IF NOT EXISTS '{user_table}' (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                respects TEXT,
                diamonds TEXT,
                chat TEXT,
                channel TEXT
            )
        """
        sdb("base.db", create_table)

        # Faqat bitta yozuv borligini tekshiramiz
        db = sqlite3.connect("base.db")
        sql = db.cursor()
        sql.execute(f"SELECT COUNT(*) FROM '{m.from_user.id}'")
        count = sql.fetchone()[0]
        db.close()

        if count == 0:
            insert = f"""
                INSERT INTO '{user_table}' 
                (id, respects, diamonds, chat, channel) 
                VALUES 
                (NULL, 0, 100, 0, 0)
            """
            sdb("base.db", insert)

        bot.reply_to(
            m,
            f"02 version {VERSION}",
            reply_markup=main
        )

    # Agar guruh yoki kanal bo‘lsa
    else:
        group_table = f"{m.chat.id}_list"

        create_group_table = f"""
            CREATE TABLE IF NOT EXISTS '{group_table}' (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                username TEXT,
                status TEXT
            )
        """
        sdb("base.db", create_group_table)

        bot.reply_to(
            m,
            f"02 version {VERSION}"
        )


@bot.message_handler(content_types = ['text'])
def send_message(m):

    # * message.chat.id -> ()
    mid = m.chat.id
    # * message.text.lower -> ()
    msg = m.text.lower()
    # * message.message_id -> ()
    msg_id = m.message_id
    # * message.reply_to_message.message_id -> ()
    # mtd = m.reply_to_message.message_id
    


    # NOTE: version
    if msg == "--v":
        send(mid, VERSION)

    elif msg.startswith('.wiki '):
        try:
            wikipedia = wiki.page(msg[6:])
            send(mid, f"<blockquote>{wikipedia.title}</blockquote>\n<b>{wikipedia.summary}</b>", parse_mode = "HTML")
        except Exception as e:
            send(mid, e)

    elif msg == "02":
        send(mid, ".")

    elif msg == "me?":
        send(mid, m.from_user.id)
    
    elif msg == "*me?":
        send(mid, f"{m.from_user.first_name}\n{m.from_user.id}\n{m.from_user.username}")

    elif msg == "profile":
        send(mid, f"{m.from_user.first_name}\n{m.from_user.id}\n{m.from_user.username}")

    elif msg == "docs":
        send(mid, "t.me/mr_mikeydev")

    elif msg == "support":
        send(mid, "Support\nt.me/mikey_developer")

    elif msg == ".flip":
        flip = ["b2.webp", "b2.webp", "b2.webp", "b2.webp", "b2.webp", "b1.webp"]
        flip_random = random.choice(flip)
        bot.send_sticker(mid, sticker = open(f"flip/{flip_random}", "rb"))

    elif msg == ".s":
        to = [1, 2, 3, 4, 5]
        to_random = random.choice(to)
        send(mid, to_random)

    elif msg == "..s":
        to = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        to_random = random.choice(to)
        send(mid, to_random)

    elif msg == ".q":
        to = ["q", "y"]
        to_random = random.choice(to)
        send(mid, to_random)

    elif msg == "..q":
        to = ["🔴", "🟢"]
        to_random = random.choice(to)
        send(mid, to_random)

    elif msg == "+":
        sdb("base.db", f"UPDATE '{m.from_user.id}' SET respects = respects + 1 WHERE id = 1")
        bot.send_message(mid, f'✅ Aura ([+1](tg://user?id={m.reply_to_message.from_user.id}))', parse_mode = 'MarkDown')

    elif msg == "+1":
        sdb("base.db", f"UPDATE '{m.from_user.id}' SET respects = respects + 1 WHERE id = 1")
        bot.send_message(mid, f'✅ Aura ([+1](tg://user?id={m.reply_to_message.from_user.id}))', parse_mode = 'MarkDown')

    elif msg == "+2":
        sdb("base.db", f"UPDATE '{m.from_user.id}' SET respects = respects + 2 WHERE id = 1")
        bot.send_message(mid, f'✅ Aura ([+1](tg://user?id={m.reply_to_message.from_user.id}))', parse_mode = 'MarkDown')

    elif msg.startswith("+ "):
        sdb("base.db", f"UPDATE '{m.from_user.id}' SET respects = respects + 1 WHERE id = 1")
        bot.send_message(mid, f'✅ Aura ([+1](tg://user?id={m.reply_to_message.from_user.id}))', parse_mode = 'MarkDown')

    elif msg.startswith("++"):
        sdb("base.db", f"UPDATE '{m.from_user.id}' SET respects = respects + 1 WHERE id = 1")
        bot.send_message(mid, f'✅ Aura ([+1](tg://user?id={m.reply_to_message.from_user.id}))', parse_mode = 'MarkDown')

    elif msg == "?a $get::None$aura -> () :: -> None -> None -> None %% :: 10000 $":
        sdb("base.db", f"UPDATE '{m.from_user.id}' SET respects = respects + 10000 WHERE id = 1")
        bot.send_message(mid, f'✅ Aura ([+1](tg://user?id={m.reply_to_message.from_user.id}))', parse_mode = 'MarkDown')
        delete(mid, m.message_id)
        send(mid, "🟢 $:")

    elif msg == "-":
        sdb("base.db", f"UPDATE '{m.from_user.id}' SET respects = respects - 1 WHERE id = 1")
        bot.send_message(mid, f'✅ Aura ([+1](tg://user?id={m.reply_to_message.from_user.id}))', parse_mode = 'MarkDown')

    elif msg == "a?":
        db = sqlite3.connect("base.db")
        sql = db.cursor()

        for data in sql.execute(f"SELECT * FROM '{m.from_user.id}' WHERE id = 1").fetchall():
            send(mid, f"🟢 Auras {data[1]}")

    elif msg == "d?":
        db = sqlite3.connect("base.db")
        sql = db.cursor()

        for data in sql.execute(f"SELECT * FROM '{m.from_user.id}' WHERE id = 1").fetchall():
            send(mid, f"💎 {data[2]}")

    elif msg == "diamonds":
        db = sqlite3.connect("base.db")
        sql = db.cursor()

        for data in sql.execute(f"SELECT * FROM '{m.from_user.id}' WHERE id = 1").fetchall():
            send(mid, f"💎 {data[2]}")

    elif msg == "chats":
        db = sqlite3.connect("base.db")
        sql = db.cursor()

        for data in sql.execute(f"SELECT * FROM '{m.from_user.id}' WHERE id = 1").fetchall():
            send(mid, f"Group: {data[3]}\nChannel: {data[4]}")
        

    # NOTE: Chat moderation commands
    # pin/unpin chat message
    elif msg == "+!":
        member = bot.get_chat_member(mid, m.from_user.id)
        if member.status == "administrator":
            bot.pin_chat_message(mid, m.reply_to_message.message_id)
            delete(mid, msg_id)

    elif msg == "-!":
        member = bot.get_chat_member(mid, m.from_user.id)
        if member.status == "administrator":
            bot.unpin_chat_message(mid, m.reply_to_message.message_id)
            delete(mid, msg_id)

    elif msg == "?del":
        member = bot.get_chat_member(mid, m.from_user.id)
        if member.status == "administrator":
            delete(mid, msg_id)
            delete(mid, m.reply_to_message.id)

    # ban list 
    elif msg == "?bans":
        text = get_banlist()
        bot.send_message(mid, text, parse_mode="Markdown")
    # ban
    elif msg.startswith("?ban "): # ! 5
        member = bot.get_chat_member(mid, m.from_user.id)
        if member.status == "administrator":
            bot.ban_chat_member(mid, m.from_user.id)
            if chdb("base.db", f"SELECT * FROM '{m.chat.id}_list' WHERE user_id = '{m.from_user.id}'", f"{m.from_user.id}"):
                send(mid, "User already banned")
                delete(mid, msg_id)
            else:
                do = f"""
                        INSERT INTO '{m.chat.id}_list' 
                        (id, user_id, username, status)
                        VALUES
                        (NULL, ?, ?, ?)
                    """
                
                sdb("base.db", do, ({m.reply_to_message.from_user.id}, {m.from_user.username}, f"{m[5:]}"))
                send(mid, f"{m.from_user.first_name} banned\n"
                        f"Reason: {m[5:]}"
                    )
                delete(mid, msg_id)
        
    # mute 
    elif msg.startswith("?mute "): # ! 6:
        member = bot.get_chat_member(mid, m.from_user.id)
        if member.status == "administrator":
            bot.restrict_chat_member(mid, m.from_user.id)
            do = f"""
                    INSERT INTO '{m.chat.id}_list' 
                    (id, user_id, username, status)
                    VALUES
                    (NULL, ?, ?, ?)
                 """
            
            # sdb("base.db", do, ({m.reply_to_message.from_user.id}, {m.from_user.username}, "mute"))
            send(mid, f"{m.from_user.first_name} muted\n"
                    f"Reason: {m[6:]}"
                )
            delete(mid, msg_id)
        
    # kick
    elif msg.startswith("?kick "): # ! 6
        member = bot.get_chat_member(mid, m.from_user.id)
        if member.status == "administrator":
            bot.kick_chat_member(mid, m.from_user.id, m.date +1)
            send(mid, f"{m.from_user.first_name} kicked\n"
                    f"Reason: {m[5:]}"
                )
            delete(mid, msg_id)
        
    # unmute
    elif msg.startswith("?unmute "): # ! 8:
        member = bot.get_chat_member(mid, m.from_user.id)
        if member.status == "administrator":
            # * You can use promote function for unmute 
            # * user but you need to write without parameters
            bot.promote_chat_member(mid, m.from_user.id)
            send(mid, f"{m.from_user.first_name} unmuted\n"
                    f"Reason: {m[8:]}"
                )
            delete(mid, msg_id)
        
    # unban 
    elif msg.startswith("?unban "): # ! 7:
        member = bot.get_chat_member(mid, m.from_user.id)
        if member.status == "administrator":
            bot.unban_chat_member(mid, m.from_user.id)
            sdb("base.db", f"DELETE FROM '{m.chat.id} WHERE user_id = '{m.from_user.id}'")
            send(mid, f"{m.from_user.first_name} unbanned\n"
                    f"Reason: {m[7:]}"
                )
            delete(mid, msg_id)
 
bot.infinity_polling()

        
    



    
