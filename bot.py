from telegram import (Update,
                      ParseMode,
                      InlineKeyboardMarkup,
                      InlineKeyboardButton)
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          CallbackContext,
                          CallbackQueryHandler,
                          ConversationHandler,)
import sqlite3

from datetime import datetime, timedelta


welcome_text = "به خفن ترین ربات کنکوری خوش اومدی🥳\n\nبرای این که بتونیم بهت خدمات متناسب با رشتت بدیم لطفا یکم بیشتر از خودت به ما بگو🤓"
get_name_text = "لطفا نام و نام خانوادگی قشنگت رو برای ما تایپ کن و بفرست👇🏻"
get_reshte_text = "لطفا آخرین رشته تحصیلیت رو انتخاب کن👇🏻"
get_paye_text = "کلاس چندی مادرجان؟"
home_text = "خوش‌ اومدی! گزینه مورد نظرت رو انتخاب کن"
new_user_text = " به ربات خودت خوش اومدی❤️\n🥳راستی همین اول کاری دوتا سورپرایز داریم برات:\n\nسورپرایز اول :\n🎊به مدت 24 ساعت وقت داری برای کتاب ها از ما 25 درصد تخفیف و برای کلاس های کاد از ما 10 درصد تخفیف بگیری \n\nبرای آشنایی با محصولات و دریافت کد تخفیف فقط کافیه همین الان این پیام رو به یکی از  آیدی های تلگرامی زیر ارسال کنی👇🏻\n\n🆔@kadadmin\n🆔@daryaftbot_admin\n\nسورپرایز دوم :\nبهت 50 تا سکه میدیم که میتونی داخل فروشگاه و ... خرجشون کنی"

NOT_FOUND = -1
NAME = 1
RESHTE = 2
PAYE = 3
PHONE = 4
SUCCESSFUL = 5


def do_sql_query(query, values, is_select_query=False):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute(query, values)
        if is_select_query:
            rows = cursor.fetchall()
            return rows
    finally:
        conn.commit()
        cursor.close()


def update_username(chat_id, username):
    query = "UPDATE Student SET username = ? WHERE chat_id = ?"
    values = [username, str(chat_id)]
    try:
        do_sql_query(query, values)
    except:
        pass


def get_status(chat_id, username):
    update_username(chat_id, username)

    query = "SELECT * FROM Student WHERE chat_id = ?"
    values = [chat_id]
    student = do_sql_query(query, values, True)

    if student:
        student = student[0]
        if not student[2]:
            return NAME
        elif not student[3]:
            return PAYE
        elif not student[4]:
            return RESHTE
        elif not student[5]:
            return PHONE
        else:
            return SUCCESSFUL
    else:
        return NOT_FOUND


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user['username']

    status = get_status(chat_id, username)

    if status == NOT_FOUND:
        query = "INSERT INTO Student (chat_id,username) VALUES (?,?)"
        values = [chat_id, username]
        do_sql_query(query, values)
        update.message.reply_text(text=welcome_text)
        update.message.reply_text(text=get_name_text)
        return NAME
    elif status == NAME:
        update.message.reply_text(text=get_name_text)
        return NAME
    elif status == RESHTE:
        update.message.reply_text(text=get_reshte_text)
        return RESHTE
    elif status == PAYE:
        update.message.reply_text(text=get_paye_text)
        return PAYE
    else:
        update.message.reply_text(text=home_text)
        return ConversationHandler.END


def get_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    name = update.message.text

    query = "UPDATE Student SET name = ? WHERE chat_id = ?"
    values = [name, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=get_reshte_text)
    return RESHTE


def get_reshte(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reshte = update.message.text

    query = "UPDATE Student SET reshte = ? WHERE chat_id = ?"
    values = [reshte, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=get_paye_text)
    return PAYE


def get_paye(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    paye = update.message.text

    query = "UPDATE Student SET paye = ? WHERE chat_id = ?"
    values = [paye, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=new_user_text)
    return ConversationHandler.END


def MAIN(update: Update, context: CallbackContext):
    pass


def cancel(update: Update, context: CallbackContext):
    """Cancels and ends the conversation."""
    update.message.reply_text(text='با موفقیت کنسل شد!')
    return ConversationHandler.END


def main():
    updater = Updater(
        "5346115877:AAHpOA_IRVBUcSl7bgBWf5we32kaqx7w-GI", use_context=True)

    dispatcher = updater.dispatcher

    get_name_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            RESHTE: [MessageHandler(Filters.text & ~Filters.command, get_reshte)],
            PAYE: [MessageHandler(Filters.text & ~Filters.command, get_paye)],
            SUCCESSFUL: [MessageHandler(Filters.text & ~Filters.command, MAIN)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(get_name_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
