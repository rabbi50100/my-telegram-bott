import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8691161840:AAE-TXRoPpq5gwweVQBuILQANRQLk8PjV7c"
bot = telebot.TeleBot(TOKEN)

verified_users = set()   # অ্যাড দেখা ইউজারদের লিস্ট

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text = message.text.lower()

    # Confirm বাটন থেকে done এলে ভেরিফাইড + ভিডিও বাটন দেখাবে
    if "done" in text:
        verified_users.add(user_id)
        bot.send_message(
            message.chat.id,
            "✅ অ্যাড দেখা সম্পন্ন হয়েছে!\n\n"
            "নিচের বাটনে ক্লিক করে মুভি নিন 👇",
            reply_markup=get_video_keyboard()
        )
        return

    # মূল অ্যাড মেসেজ (দুটো বাটন)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔗 Watch Ad", url="https://www.profitablecpmratenetwork.com/uv78x22pja?key=f3ffba790fbb2ff3c308626730a2c9b3"),
        InlineKeyboardButton("✅ I Completed Ad", callback_data="check_completed")
    )

    bot.send_photo(
        message.chat.id,
        photo="https://dn721906.ca.archive.org/0/items/kis-kisko-pyaar-karoon/images%20%283%29.jpeg",
        caption="⚠️ প্রথমে অ্যাডটি **পুরো** দেখুন।\n\n"
                "অ্যাড দেখা শেষ হলে নিচের '✅ I Completed Ad' বাটনে ক্লিক করুন।",
        reply_markup=keyboard
    )


def get_video_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🎥 Get Video / মুভি নিন", callback_data="send_movie"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id

    if call.data == "check_completed":
        deep_link = f"https://t.me/{bot.get_me().username}?start=done"
        
        confirm_keyboard = InlineKeyboardMarkup()
        confirm_keyboard.add(InlineKeyboardButton("✅ Yes, I Watched the Ad", url=deep_link))

        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption="👀 অ্যাড দেখা শেষ হয়েছে?\n\nকনফার্ম করার জন্য নিচের বাটনে ক্লিক করুন:",
            reply_markup=confirm_keyboard
        )

    elif call.data == "send_movie":
        if user_id in verified_users:
            try:
                # চ্যানেলের পোস্ট কপি করে পাঠানো (সবচেয়ে ভালো পদ্ধতি)
                bot.copy_message(
                    chat_id=call.message.chat.id,
                    from_chat_id="@HD_Movieindia",   # আপনার চ্যানেলের username
                    message_id=305,                  # পোস্টের নাম্বার
                    caption="🎉 ধন্যবাদ! এই নিন আপনার মুভি।\n\nআবার চাইলে /start করুন।"
                )
            except Exception as e:
                bot.send_message(call.message.chat.id, f"❌ ভিডিও পাঠাতে সমস্যা হয়েছে।\nError: {str(e)}")
        else:
            bot.answer_callback_query(
                call.id,
                "❌ আপনি এখনো অ্যাড দেখেননি!\nপ্রথমে Watch Ad বাটনে ক্লিক করে অ্যাড দেখুন।",
                show_alert=True
            )


print("🤖 Bot is running successfully... (Confirm + Video Fixed)")
bot.infinity_polling()
