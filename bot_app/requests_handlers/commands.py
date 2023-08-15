import telebot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot_app.models import User, Savings, UserState


def register_command(message: Message, bot: telebot.TeleBot):
    cancel_command(message=message, bot=bot)
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    if user_id:
        existing_user = User.objects.filter(user_id=user_id).first()
        if existing_user:
            bot.reply_to(message, "Your information was already recorded to our database.\n"
                                  "There is no need to use the /register command again!")
        new_user = User(user_id=user_id, username=username, first_name=first_name, last_name=last_name)
        new_user.save()
        bot.reply_to(message, "Thanks for using our bot!\n"
                              "Your information was kindly recorded!")


def start_command(message: Message, bot: telebot.TeleBot):
    cancel_command(message=message, bot=bot)
    user_id = message.from_user.id
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return
    bot.reply_to(message, "Hello! To offer you a tailored experience and provide our services,"
                          "we kindly ask you to use the /register command if you haven`t already used it yet!\n"
                          "It allows bot to work properly, and handle your commands!"
                          "Available commands:\n"
                          "/add_savings - adds new type of savings\n"
                          "/show_savings - show your current savings\n"
                          "/cancel - cancel ongoing commands (for now only /add_savings)\n"
                          "/register - register your telegram ID to database")

def add_savings_command(message: Message, bot: telebot.TeleBot):
    user_id = message.from_user.id
    command = "/add_savings"
    message_text = message.text
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
            user_state = UserState.objects.get_state(user=user)

            if user_state is None:
                UserState.objects.create_state(user=user, command=command, current_state=1)
                bot.reply_to(message, "Please provide me with your savings type!")
            elif user_state.current_state == 1:
                if message_text == command:
                    cancel_command(message=message, bot=bot)
                    add_savings_command(message, bot)
                    return
                user_state.update_data_state({"savings_type": message_text})
                UserState.objects.update_state(user=user, new_state=2)
                bot.reply_to(message, "Please provide me with your quantity! The type of should be number!")
            elif user_state.current_state == 2:
                if message_text == command:
                    cancel_command(message=message, bot=bot)
                    add_savings_command(message, bot)
                    return
                if not message_text.isdigit():
                    bot.reply_to(message, "Please send me the actual number!")
                else:
                    previous_state = user_state.get_data_state()
                    new_data = {"quantity": message_text}
                    update_value = {**previous_state, **new_data}
                    user_state.update_data_state(update_value)
                    UserState.objects.update_state(user=user, new_state=3)
                    bot.reply_to(message, "Confirm the changes! (y/n)")

            elif user_state.current_state == 3:
                if message_text == command:
                    cancel_command(message=message, bot=bot)
                    add_savings_command(message, bot)
                    return
                if message_text.lower() == "y":
                    current_state = UserState.objects.get_state(user=user)
                    data = current_state.get_data_state()
                    Savings.objects.create(
                        user=user,
                        savings_type=data.get("savings_type"),
                        quantity=data.get("quantity")
                    )
                    UserState.objects.delete_state(user=user)
                    bot.reply_to(message, f"The Savings: {data.get('savings_type')}\n"
                                          f"With Quantity: {data.get('quantity')}\n"
                                          f"Was saved to database!")
                else:
                    bot.reply_to(message, "You cancelled adding savings!")
                    UserState.objects.delete_state(user=user)
        except User.DoesNotExist:
            bot.reply_to(message, "Please use the /register command first to record your credentials and use the bot.")
            return


def show_savings_command(message: Message, bot: telebot.TeleBot):
    cancel_command(message=message, bot=bot)
    user_id = message.from_user.id
    try:
        user = User.objects.get(user_id=user_id)
        if not user:
            bot.reply_to(message, "Please use the /register command first to record your credentials and use the bot!")
            return
        savings_list = Savings.objects.filter(user=user)
        if not savings_list:
            bot.reply_to(message, "You don't have any savings recorded yet.")
            return
        keyboard = [
            [InlineKeyboardButton(savings.savings_type, callback_data=f"showSaving_{savings.id}")]
            for savings in savings_list
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.reply_to(message, "Select a savings to view:", reply_markup=reply_markup)
    except User.DoesNotExist:
        bot.reply_to(message, "Please use the /register command first to record your credentials and use the bot.")
        return


def cancel_command(message: Message, bot: telebot.TeleBot):
    user_id = message.from_user.id
    existing_user = User.objects.filter(user_id=user_id).first()
    if not existing_user:
        bot.reply_to(message, "Please use the /register command first to record your credentials and use the bot!")
        return
    user_state = UserState.objects.get_state(existing_user)
    if user_state is not None:
        UserState.objects.delete_state(existing_user)
        bot.reply_to(message, f"The ongoing {user_state.command} command has been stopped!")
        return
