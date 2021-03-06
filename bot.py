from khayyam import *
from telegram import (KeyboardButton, ReplyKeyboardMarkup,
                      Update, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext, CallbackQueryHandler, ConversationHandler,)
import sqlite3
from datetime import *

CHANNEl = "@daryaft_mhhasani"
# TEXTS
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
unknown_text = "ای وای😱\nاین پیام برای ربات ما قابل فهم نیست.😕\n\nاگر اشکالی وجود داره و با فشردن دستور /start حل نشد ، به ما از طریق آیدی @mhhasani خبر بده."
cancel_text = "با موفقیت کنسل شد!"
add_task_text = "🔺برای افزودن فعالیت درسی جدید نام درس و عنوان را به شکل زیر وارد کنید:\n\nنام درس\nعنوان "
added_activity_text = "✅فعالیت با موفقیت افزوده شد!\nبیشینه زمان ممکن برای هر فعالیت ۲ ساعت می باشد.\nهر موقع فعالیتت تموم شد میتونی روی دکمه ' اتمام فعالیت ' کلیک کنی👇"
backtomain_text = "به صفحه اصلی برگشتی!"
end_task_text = "اتمام این فعالیت ثبت شد!"
task_not_ended_text = "❌ شما فعالیتی دارید که به پایان نرسیده است!\nابتدا آن را به پایان رسانده و دوباره تلاش کنید..."
no_task_text = "فعالیتی وجود ندارد!"
task_already_ended_text = "این فعالیت قبلا به پایان رسیده است!"


def force_end_task_text(report):
    mabhas = report[3]
    dars = report[2]
    text = f"🔺 از شروع فعالیت مبحث {mabhas} از درس {dars} بیشتر از دو ساعت گذشته...\nما اتمام این فعالیت رو برات ثبت کردیم :)"
    return text


# BUTTONS
all_reshte = ['ریاضی', 'تجربی', 'انسانی', 'هنر']
all_paye = ['دهم', 'یازدهم', 'دوازدهم', 'فارغ التحصیل']
MAIN_BUTTON = ['مشاهده اطلاعات فردی', 'مشاهده گزارش ۳ روز اخیر',
               'افزودن فعالیت', 'مشاهده فعالیت جاری']
# KEYBOARDS
main_keyboard = [[KeyboardButton(MAIN_BUTTON[0])],
                 [KeyboardButton(MAIN_BUTTON[1])],
                 [KeyboardButton(MAIN_BUTTON[2])],
                 [KeyboardButton(MAIN_BUTTON[3])]]
start_reply_markup = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True)

reshte_keyboard = [[KeyboardButton(all_reshte[0])], [KeyboardButton(all_reshte[1])], [
    KeyboardButton(all_reshte[2])], [KeyboardButton(all_reshte[3])]]
reshte_reply_markup = ReplyKeyboardMarkup(
    reshte_keyboard, one_time_keyboard=True)

paye_keyboard = [[KeyboardButton(all_paye[0])], [KeyboardButton(all_paye[1])], [
    KeyboardButton(all_paye[2])], [KeyboardButton(all_paye[3])]]
paye_reply_markup = ReplyKeyboardMarkup(paye_keyboard, one_time_keyboard=True)

phone_keyboard = [
    [KeyboardButton(text="اشتراک گذاری شماره تلفن", request_contact=True)]]
phone_reply_markup = ReplyKeyboardMarkup(
    phone_keyboard, one_time_keyboard=True)
# INLINE KEYBOARDS
keyboard = [
    [InlineKeyboardButton(
        "ویرایش نام و نام خانوادگی", callback_data='change_name')],

    [InlineKeyboardButton("ویرایش رشته", callback_data='change_reshte'),
        InlineKeyboardButton("ویرایش پایه", callback_data='change_paye')],
]
change_reply_markup = InlineKeyboardMarkup(keyboard)
# INFO STEPS
NOT_FOUND = -1
NAME = 1
RESHTE = 2
PAYE = 3
PHONE = 4
SUCCESSFUL = 5
# TASKS STEPS
ADD_TASK = 0


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
    elif status == PHONE:
        update.message.reply_text(text=get_phone_text)
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
        text=get_phone_text, reply_markup=phone_reply_markup)

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


def get_info(update: Update):
    chat_id = update.message.chat_id

    query = 'SELECT * FROM Student WHERE chat_id = ?'
    values = [chat_id]
    student = do_sql_query(query, values, True)
    if not student:
        update.message.reply_text(text=first_login_text)
    else:
        student = student[0]
        name = student[2]
        phone = student[5]
        reshte = student[4]
        paye = student[3]
        text = f"🧾دوست عزیزم اطلاعات کاربری تو به شرح زیره :\n\n🤓 نام و نام خانوادگی : {name}\n📞 شماره تلفن : {phone}\n🧐 رشته : {reshte}\n📊 پایه : {paye}\n\nاگه هر کدوم از اینا اشتباه ثبت شده ، یا اینکه پایت رفته بالاتر (بزنم به تخته 😎) یا اینکه تغییر رشته دادی ، میتونی اطلاعاتت رو ویرایش کنی ، برای اینکار فقط کافیه از همین دکمه های شیشه ای این پایین استفاده کنی 👇🏻"
        update.message.reply_text(text=text, reply_markup=change_reply_markup)


def end_time_keyboard(rep_id):
    keyboard = [[InlineKeyboardButton(
        "اتمام فعالیت", callback_data='end_time '+str(rep_id))]]
    return InlineKeyboardMarkup(keyboard)


def todays_task_text(chat_id, day=0):
    sql = "SELECT * FROM Student WHERE chat_id = ?"
    student = do_sql_query(sql, [chat_id], True)[0]

    now = JalaliDate.today() + timedelta(hours=4.5)
    sql = "SELECT R.* FROM Student S JOIN Report R ON S.chat_id = R.chat_id WHERE S.chat_id = ?"
    reports = do_sql_query(sql, [chat_id], True)
    now = now - timedelta(days=day)
    text = f"📆 تاریخ : {now.strftime('%d / %m / %Y')}\n"
    name = student[2].replace(' ', "_")
    paye = student[3].replace(' ', "_")
    reshte = student[4]
    sum_time = 0
    text += f"👤 #{name} ➖ #{paye} ➖ #{reshte}"
    text += "\n\n➖➖➖➖➖\n👓 برنامه مطالعاتی امروز :\n\n"
    for report in reports:
        start_time = JalaliDate(datetime.strptime(
            report[4], '%Y-%m-%d %H:%M:%S'))
        if start_time.strftime('%Y-%m-%d') == now.strftime('%Y-%m-%d'):
            text += f"🔸 نام درس: {report[2]} \n"
            text += f"🔹 نام مبحث: {report[3]} \n"
            st = datetime.strptime(report[4], '%Y-%m-%d %H:%M:%S')
            if report[5]:
                et = datetime.strptime(report[5], '%Y-%m-%d %H:%M:%S')
                time = (et-st).seconds // 60
                text += f"🕒 مدت مطالعه: {time} دقیقه"
                sum_time += time
            else:
                text += '🕒 در حال مطالعه...'
            text += "\n\n"
    hour = sum_time // 60
    minute = sum_time - hour * 60
    if hour != 0:
        if minute != 0:
            sum_time = f"{hour} ساعت و {minute} دقیقه"
        else:
            sum_time = f"{hour} ساعت"
    else:
        sum_time = f"{minute} دقیقه"
    text += f"➖➖➖➖➖\n🕰 مجموع ساعات مطالعه امروز : {sum_time}"

    return text


def update_channel(chat_id=None, update=None, query=None, context=None):
    new_message = False
    today = JalaliDate.today() + timedelta(hours=4.5)
    today = JalaliDate(today).strftime('%Y-%m-%d')
    sql = "SELECT * FROM Student WHERE chat_id = ?"
    student = do_sql_query(sql, [chat_id], True)
    user_date = student[0][7]
    if user_date:
        if today != user_date:
            new_message = True
    else:
        new_message = True

    user_date = today

    if new_message:
        if update:
            message_id = update.message.bot.send_message(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
            ).message_id
        elif query:
            message_id = query.message.bot.send_message(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
            ).message_id
        elif context:
            message_id = context.bot.send_message(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
            ).message_id
        sql = "UPDATE Student SET (day,message_id) = (?,?) WHERE chat_id = ?"
        do_sql_query(sql, [user_date, message_id, chat_id])
    else:
        message_id = student[0][6]
        if update:
            update.message.bot.edit_message_text(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
                message_id=message_id)
        elif query:
            query.message.bot.edit_message_text(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
                message_id=message_id
            )
        elif context:
            context.bot.edit_message_text(
                text=todays_task_text(chat_id),
                chat_id=CHANNEl,
                message_id=message_id
            )


def add_task(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    les_top = update.message.text.split("\n")

    if len(les_top) != 2:
        update.message.reply_text(text=add_task_text)
        return ADD_TASK

    lname = les_top[0]
    topic = les_top[1]
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = "INSERT INTO Report (chat_id,lname,topic,start_time) VALUES (?,?,?,?)"
    values = [chat_id, lname, topic, start_time]
    do_sql_query(query, values)

    query = "SELECT seq FROM sqlite_sequence WHERE name = ?"
    rep_id = do_sql_query(query, ['Report'], True)[0][0]
    end_time_reply_markup = end_time_keyboard(rep_id)

    update.message.reply_text(text=added_activity_text,
                              reply_markup=end_time_reply_markup)
    update_channel(chat_id, update=update)
    return ConversationHandler.END


def view_current_task(update: Update):
    chat_id = update.message.chat_id

    now_time = datetime.now()

    query = "SELECT * FROM Report WHERE chat_id = ? AND end_time IS NULL"
    Reports = do_sql_query(query, [chat_id], True)

    if Reports:
        for report in Reports:
            start_time = datetime.strptime(
                report[4], '%Y-%m-%d %H:%M:%S')
            time = now_time - start_time
            minute = time.seconds // 60
            hour = (JalaliDatetime(start_time) +
                    timedelta(hours=4.5)).strftime('%H:%M')
            text = f"⭕️ شما مبحث {report[3]} از درس {report[2]} را در ساعت {hour} آغاز کرده اید و {minute} دقیقه از شروع آن گذشته است.\nبیشینه زمان ممکن برای هر فعالیت ۲ ساعت می باشد.\nهر موقع فعالیتت تموم شد میتونی روی دکمه ' اتمام فعالیت ' کلیک کنی👇"
            update.message.reply_text(
                text=text, reply_markup=end_time_keyboard(report[0]))
    else:
        update.message.reply_text(text=no_task_text)


def check_end_task(context: CallbackContext):
    now_time = datetime.now()

    query = "SELECT * FROM Report WHERE end_time IS NULL"
    Reports = do_sql_query(query, [], True)

    if Reports:
        for report in Reports:
            rep_id = report[0]
            chat_id = report[1]
            start_time = datetime.strptime(
                report[4], '%Y-%m-%d %H:%M:%S')
            time = now_time - start_time
            minute = time.seconds // 60
            if minute >= 120:
                end_time = start_time + timedelta(hours=2)
                end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
                query = "UPDATE Report SET end_time = ? WHERE id = ?"
                do_sql_query(query, [end_time, rep_id])
                context.bot.send_message(
                    text=force_end_task_text(report), chat_id=chat_id)
                update_channel(chat_id, context=context)


def message_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    if text not in MAIN_BUTTON:
        update.message.reply_text(text=unknown_text)

    elif text == MAIN_BUTTON[0]:
        get_info(update)

    elif text == MAIN_BUTTON[2]:
        query = "SELECT * FROM Report WHERE chat_id = ? AND end_time IS NULL"
        Reports = do_sql_query(query, [chat_id], True)

        if Reports:
            update.message.reply_text(text=task_not_ended_text)
            return ConversationHandler.END

        update.message.reply_text(text=add_task_text)
        return ADD_TASK

    elif text == MAIN_BUTTON[3]:
        view_current_task(update)

    elif text == MAIN_BUTTON[1]:
        update.message.reply_text(text=todays_task_text(chat_id, day=2))
        update.message.reply_text(text=todays_task_text(chat_id, day=1))
        update.message.reply_text(text=todays_task_text(chat_id, day=0))
    return ConversationHandler.END


def Inline_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    username = update.callback_query.from_user['username']

    if query.data == 'change_name':
        sql = "UPDATE Student SET name = ? WHERE chat_id = ?"
        values = [None, str(chat_id)]
        do_sql_query(sql, values)

        query.message.reply_text(text=get_name_text)
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

    elif query.data.split()[0] == 'end_time':
        id = query.data.split()[1]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "SELECT end_time FROM Report WHERE id = ?"
        values = [id]
        end_time = do_sql_query(sql, values, True)
        if not end_time[0][0]:
            sql = "UPDATE Report SET end_time = ? WHERE id = ?"
            values = [now, id]
            do_sql_query(sql, values)

            query.message.bot.edit_message_text(
                text=end_task_text, message_id=message_id, chat_id=chat_id)
            update_channel(chat_id, query=query)
        else:
            query.message.bot.edit_message_text(
                text=task_already_ended_text, message_id=message_id, chat_id=chat_id)

        query.answer(text="اتمام فعالیت")


def cancel(update: Update, context: CallbackContext):
    """Cancels and ends the conversation."""
    update.message.reply_text(text=cancel_text)
    return ConversationHandler.END


def main():
    updater = Updater(
        "5346115877:AAHpOA_IRVBUcSl7bgBWf5we32kaqx7w-GI", use_context=True)

    dispatcher = updater.dispatcher
    j = updater.job_queue
    j.run_repeating(check_end_task, interval=300, first=1)

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
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(Inline_buttons_handler)

    Message_handler = ConversationHandler(
        entry_points=[MessageHandler(
            Filters.text & ~Filters.command, message_handler)],
        states={
            ADD_TASK: [MessageHandler(Filters.text & ~Filters.command, add_task)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(Message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
