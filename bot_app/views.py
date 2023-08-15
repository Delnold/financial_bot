import pickle
from telebot.types import Message, CallbackQuery
from bot import bot
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from bot_app.requests_handlers.commands import register_command, start_command, cancel_command, add_savings_command, \
    show_savings_command
from bot_app.requests_handlers.messages import handling_messages
from bot_app.requests_handlers.callback_query import handling_callback_query


@csrf_exempt
def index(request):
    return JsonResponse({"message": "Visit admin panel!"})


@csrf_exempt
def commands(request) -> JsonResponse:
    if request.method == "POST":
        try:
            serialized_message = request.body
            message: Message = pickle.loads(serialized_message)

            command_name = message.text
            if command_name == "/start":
                start_command(message=message, bot=bot)
            elif command_name == "/register":
                register_command(message=message, bot=bot)
            elif command_name == "/cancel":
                result_bool, message_text = cancel_command(message=message)
                if not result_bool:
                    bot.reply_to(message, message_text)
            elif command_name == "/add_savings":
                add_savings_command(message=message, bot=bot)
            elif command_name == "/show_savings":
                show_savings_command(message=message, bot=bot)
            else:
                bot.reply_to("The following command does not exist yet!")
            return JsonResponse({"operation": message.text, "status_code": 200})
        except json.JSONDecodeError:
            print("Invalid JSON data received")
            return JsonResponse({"error": "Invalid JSON data"})
    else:
        print("Invalid request method")
        return JsonResponse({"error": "Invalid request method"})


@csrf_exempt
def messages(request) -> JsonResponse:
    if request.method == "POST":
        try:
            serialized_message = request.body
            message: Message = pickle.loads(serialized_message)
            handling_messages(message=message, bot=bot)
            return JsonResponse({"operation": message.text, "status_code": 200})
        except json.JSONDecodeError:
            print("Invalid JSON data received")
            return JsonResponse({"error": "Invalid JSON data"})
    else:
        print("Invalid request method")
        return JsonResponse({"error": "Invalid request method"})


@csrf_exempt
def callback_query(request) -> JsonResponse:
    if request.method == "POST":
        try:
            serialized_message = request.body
            query: CallbackQuery = pickle.loads(serialized_message)
            handling_callback_query(query=query, bot=bot)
            return JsonResponse({"operation": query.message.text, "status_code": 200})
        except json.JSONDecodeError:
            print("Invalid JSON data received")
            return JsonResponse({"error": "Invalid JSON data"})
    else:
        print("Invalid request method")
        return JsonResponse({"error": "Invalid request method"})
