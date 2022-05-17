from turtle import up
from telegram import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
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
get_phone_text = "دوست عزیزم ☺️\nما برای اینکه بتونیم بهت خدمات بهتری بدیم ، و بتونیم رضایتتو بیشتر از قبل جلب کنیم ، نیاز داریم که شماره تو داشته باشیم ☎️\nلازم نیست نگران چیزی باشی ، چون ما با چشمامون 👀 از اطلاعاتت محافظت میکنیم 💪🏻\n🎁 فکر نکنی جایزه ش یادمون رفته ها ! بعد از این مرحله ، ما 40 سکه به عنوان تشکر بهت میدیم 💰\n\nبرای به اشتراک گذاشتن شماره تلفنت ، روی دکمه زیر کلیک کن 🛎"
end_text = "ممنون بابت تکمیل اطلاعاتت!"
first_login_text = "لطفا اول اطلاعاتت رو ثبت کن!"
change_name_text = "اسمت با موفقیت تغییر کرد!"
change_paye_text = "پایه ت با موفقیت تغییر کرد!"
change_reshte_text = "رشته ت با موفقیت تغییر کرد!"

all_reshte = ['ریاضی', 'تجربی', 'انسانی', 'هنر']
all_paye = ['دهم', 'یازدهم', 'دوازدهم', 'فارغ التحصیل']
MAIN_BUTTUN = ['مشاهده اطلاعات فردی',
               'مشاهده گزارش ۳ روز اخیر', 'افزودن فعالیت']

main_keyboard = [[KeyboardButton(MAIN_BUTTUN[0])],
                 [KeyboardButton(MAIN_BUTTUN[1])],
                 [KeyboardButton(MAIN_BUTTUN[2])]]
start_reply_markup = ReplyKeyboardMarkup(main_keyboard)

reshte_keyboard = [[KeyboardButton(all_reshte[0])], [KeyboardButton(all_reshte[1])], [
    KeyboardButton(all_reshte[2])], [KeyboardButton(all_reshte[3])]]
reshte_reply_markup = ReplyKeyboardMarkup(reshte_keyboard)

paye_keyboard = [[KeyboardButton(all_paye[0])], [KeyboardButton(all_paye[1])], [
    KeyboardButton(all_paye[2])], [KeyboardButton(all_paye[3])]]
paye_reply_markup = ReplyKeyboardMarkup(paye_keyboard)

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
        update.message.reply_text(
            text=get_name_text, reply_markup=ReplyKeyboardRemove())
        return NAME
    elif status == NAME:
        update.message.reply_text(
            text=get_name_text, reply_markup=ReplyKeyboardRemove())
        return NAME
    elif status == RESHTE:
        update.message.reply_text(text=get_reshte_text)
        return RESHTE
    elif status == PAYE:
        update.message.reply_text(text=get_paye_text)
        return PAYE
    elif status == PHONE:
        update.message.reply_text(
            text=get_phone_text, reply_markup=ReplyKeyboardRemove())
        return PHONE
    else:
        update.message.reply_text(
            text=home_text, reply_markup=start_reply_markup)

        return ConversationHandler.END


def get_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    name = update.message.text

    query = "UPDATE Student SET name = ? WHERE chat_id = ?"
    values = [name, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=get_reshte_text,
                              reply_markup=reshte_reply_markup)
    return RESHTE


def change_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    name = update.message.text

    query = "UPDATE Student SET name = ? WHERE chat_id = ?"
    values = [name, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=change_name_text,
                              reply_markup=start_reply_markup)
    return ConversationHandler.END


def get_reshte(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reshte = update.message.text

    if reshte not in all_reshte:
        update.message.reply_text(
            text=get_reshte_text)
        return RESHTE

    query = "UPDATE Student SET reshte = ? WHERE chat_id = ?"
    values = [reshte, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(
        text=get_paye_text, reply_markup=paye_reply_markup)
    return PAYE


def change_reshte(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reshte = update.message.text

    if reshte not in all_reshte:
        update.message.reply_text(
            text=get_reshte_text)
        return RESHTE

    query = "UPDATE Student SET reshte = ? WHERE chat_id = ?"
    values = [reshte, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=change_reshte_text,
                              reply_markup=start_reply_markup)
    return ConversationHandler.END


def get_paye(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    paye = update.message.text

    if paye not in all_paye:
        update.message.reply_text(
            text=get_paye_text)
        return PAYE

    query = "UPDATE Student SET paye = ? WHERE chat_id = ?"
    values = [paye, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(
        text=get_phone_text, reply_markup=ReplyKeyboardRemove())

    return PHONE


def change_paye(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    paye = update.message.text

    if paye not in all_paye:
        update.message.reply_text(
            text=get_paye_text)
        return PAYE

    query = "UPDATE Student SET paye = ? WHERE chat_id = ?"
    values = [paye, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(
        text=change_paye_text, reply_markup=start_reply_markup)

    return ConversationHandler.END


def get_phone(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    contact = update.effective_message.contact
    phone = contact.phone_number

    query = "UPDATE Student SET phone = ? WHERE chat_id = ?"
    values = [phone, str(chat_id)]
    do_sql_query(query, values)

    update.message.reply_text(text=new_user_text)
    return start(update, context)


def cancel(update: Update, context: CallbackContext):
    """Cancels and ends the conversation."""
    update.message.reply_text(text='با موفقیت کنسل شد!')
    return ConversationHandler.END


def get_info(update):
    chat_id = update.message.chat_id

    query = 'SELECT * FROM Student WHERE chat_id = ?'
    values = [chat_id]
    student = do_sql_query(query, values, True)
    if not student:
        update.message.reply_text(
            text=first_login_text, reply_markup=ReplyKeyboardRemove())
    else:
        keyboard = [
            [InlineKeyboardButton(
                "ویرایش نام و نام خانوادگی", callback_data='change_name')],

            [InlineKeyboardButton("ویرایش رشته", callback_data='change_reshte'),
             InlineKeyboardButton("ویرایش پایه", callback_data='change_paye')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        student = student[0]
        name = student[2]
        phone = student[5]
        reshte = student[4]
        paye = student[3]
        text = f"🧾دوست عزیزم اطلاعات کاربری تو به شرح زیره :\n\n🤓 نام و نام خانوادگی : {name}\n📞 شماره تلفن : {phone}\n🧐 رشته : {reshte}\n📊 پایه : {paye}\n\nاگه هر کدوم از اینا اشتباه ثبت شده ، یا اینکه پایت رفته بالاتر (بزنم به تخته 😎) یا اینکه تغییر رشته دادی ، میتونی اطلاعاتت رو ویرایش کنی ، برای اینکار فقط کافیه از همین دکمه های شیشه ای این پایین استفاده کنی 👇🏻"
        update.message.reply_text(text=text, reply_markup=reply_markup)


def message_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    if text not in MAIN_BUTTUN:
        update.message.reply_text(
            text="درخواست نامفهوم است.")

    elif text == MAIN_BUTTUN[0]:
        get_info(update)


def Inline_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    username = update.callback_query.from_user['username']

    if query.data == 'change_name':
        sql = "UPDATE Student SET name = ? WHERE chat_id = ?"
        values = [None, str(chat_id)]
        do_sql_query(sql, values)

        query.message.reply_text(
            text=get_name_text, reply_markup=ReplyKeyboardRemove())
        query.answer(text="تغییر نام و نام خانوادگی")

        return NAME

    elif query.data == 'change_reshte':
        sql = "UPDATE Student SET reshte = ? WHERE chat_id = ?"
        values = [None, str(chat_id)]
        do_sql_query(sql, values)

        query.message.reply_text(
            text=get_reshte_text, reply_markup=reshte_reply_markup)

        query.answer(text="تغییر رشته")

        return RESHTE

    elif query.data == 'change_paye':
        sql = "UPDATE Student SET paye = ? WHERE chat_id = ?"
        values = [None, str(chat_id)]
        do_sql_query(sql, values)

        query.message.reply_text(
            text=get_paye_text, reply_markup=paye_reply_markup)

        query.answer(text="تغییر پایه")

        return PAYE


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
            PHONE: [MessageHandler(Filters.contact, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(get_name_handler)

    Inline_buttons_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(Inline_buttons)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, change_name)],
            RESHTE: [MessageHandler(Filters.text & ~Filters.command, change_reshte)],
            PAYE: [MessageHandler(Filters.text & ~Filters.command, change_paye)],
            PHONE: [MessageHandler(Filters.contact, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(Inline_buttons_handler)

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
