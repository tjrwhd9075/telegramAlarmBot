import telegram as tel
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

myToken = '텔레그램 토큰'
telbot = tel.Bot(token=myToken)
channel_id = "@ha_alarm"  # 채널 명

# 버튼 만드는 함수 1. 버튼이름과 버튼 반환값을 다르게 지정 할 수 있음.
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

# 버튼 만드는 함수 2. 버튼 이름 = 버튼 반환값. 수식을 간단하게 만들 수 있음.
def build_button(text_list, callback_header = "") : # make button list
    button_list = []
    text_header = callback_header
    
    if callback_header != "" : # 비어있는게 아니라면
        text_header += ","   # 제목 + 콤마 붙임

    for text in text_list :
        button_list.append(InlineKeyboardButton(text, callback_data=text_header + text))

    return button_list

# 최근 입력된 텍스트를 읽어와 처리하는 함수
def get_name(bot, update):
    print("get_name")    
    chat_id = bot.channel_post.chat.id         # 최근 입력된 메시지의 챗아이디
    msg = bot.channel_post.text[1:].upper()               #  최근 입력된 메시지의 텍스트 "/" 떼고, 대문자로변환
    print(msg)

    update.bot.send_message(text="💲💲\n" , chat_id=chat_id)
    telbot.send_photo(chat_id=chat_id, photo=open('fig1.png', 'rb'))   

# 명령어 응답
def get_command(bot, update):
    print("get command")
    chat_id = bot.channel_post.chat.id         # 최근 입력된 메시지의 챗아이디
    msg = bot.channel_post.text[1:].upper()               #  최근 입력된 메시지의 텍스트 "/" 떼고, 대문자로변환
    print(msg)

    # 버튼 만들고, 버튼 누르면 반환되는 값 지정
    show_list = []
    show_list.append(InlineKeyboardButton("binance", callback_data="binance")) # add on button
    show_list.append(InlineKeyboardButton("upbit", callback_data="upbit")) # add off button
    show_list.append(InlineKeyboardButton("cancel", callback_data="cancel")) # add cancel button
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup

    bot.effective_message.reply_text("BTC 선택됨. 거래소를 선택하세요.", reply_markup=show_markup)


# 버튼 누르면 다시 호출되는
def callback_get(bot, update):
    data_selected = bot.callback_query.data
    print("callback : ", data_selected)

    # 버튼 만들고 싶은만큼 텍스트 입력하면 됨. 반환되는 값은 버튼이름과 같음.
    button_list = build_button(["1d", "4h", "1h", "30m", "15m", "5m", "1m","cancel"], data_selected)
    show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
    update.bot.edit_message_text(text="봉을 선택해 주세요.",
                                chat_id=bot.callback_query.message.chat_id,
                                message_id=bot.callback_query.message.message_id,
                                reply_markup=show_markup)




# 메시지 받아오는 곳 : 메시지를 받으면 get_name 함수를 호출한다. 
message_handler = MessageHandler(Filters.text & (~Filters.command), get_name)
updater.dispatcher.add_handler(message_handler)
# 명령어 받아오는 곳 : "/" 슬래시가 포함된 메시지를 받으면 get_command 함수를 호출한다.
message_handler2 = MessageHandler(Filters.command, get_command)
updater.dispatcher.add_handler(message_handler2)
# 버튼 콜백 : 버튼을 누르면 callback_get 함수를 불러온다.
updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))

updater.start_polling(timeout=3)
updater.idle()