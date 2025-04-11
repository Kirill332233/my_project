import telebot
from telebot import types
import random
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import threading

bot = telebot.TeleBot('7588340886:AAHVXt-tCySj7T1CKS4ZbpEmMMAiCwU5HQE')

anime_list = {
    'Shonen': ['Naruto', 'One Piece', 'My Hero Academia'],
    'Seinen': ['Attack on Titan', 'Death Note'],
    'Shojo': ['Sailor Moon', 'Fruits Basket'],
    'Isekai': ['Re:Zero', 'No Game No Life']
}

genre_info = {
    'Shonen': 'Для подростков, экшн, дружба, упорство',
    'Seinen': 'Для взрослых, глубокий сюжет, драма',
    'Shojo': 'Для девушек, романтика, отношения',
    'Isekai': 'Попаданцы, фантастические миры'
}

bot_running = False
bot_thread = None


class BotUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Anime Bot Interface")
        self.window.geometry("700x800")
        self.window.configure(bg="#1e1e1e")

        self.users = set()
        self.user_logs = {}

        self.user_label = Label(self.window, text="Выберите пользователя:", bg="#1e1e1e", fg="white")
        self.user_label.pack(padx=10, pady=(10, 0), anchor='w')

        self.user_combobox = ttk.Combobox(self.window, values=[], state="readonly")
        self.user_combobox.pack(fill=X, padx=10, pady=5)
        self.user_combobox.bind("<<ComboboxSelected>>", self.on_user_selected)

        self.chat_output = scrolledtext.ScrolledText(
            self.window,
            wrap=WORD,
            font=("Consolas", 12),
            bg="#2d2d2d",
            fg="#f2f2f2",
            insertbackground="#ffffff"
        )
        self.chat_output.pack(padx=10, pady=10, fill=BOTH, expand=True)
        self.chat_output.config(state=DISABLED)

        button_frame = Frame(self.window, bg="#1e1e1e")
        button_frame.pack(pady=10)

        self.start_button = Button(button_frame, text="▶️ Запуск бота", command=self.start_bot, width=20)
        self.start_button.pack(side=LEFT, padx=10)

        self.stop_button = Button(button_frame, text="⛔ Остановить бота", command=self.stop_bot, width=20, state=DISABLED)
        self.stop_button.pack(side=LEFT, padx=10)

        self.log_message("📦 Бот не запущен...")

    def update_user_list(self, user_id):
        if user_id not in self.users:
            self.users.add(user_id)
            self.user_combobox['values'] = list(self.users)

    def log_message(self, message, user_id=None):
        if user_id is not None:
            if user_id not in self.user_logs:
                self.user_logs[user_id] = []
            self.user_logs[user_id].append(message)

        self.chat_output.config(state=NORMAL)
        self.chat_output.insert(END, message + "\n")
        self.chat_output.see(END)
        self.chat_output.config(state=DISABLED)

    def on_user_selected(self, event):
        selected_user = self.user_combobox.get()
        if selected_user and selected_user in self.user_logs:
            self.chat_output.config(state=NORMAL)
            self.chat_output.delete('1.0', END)
            for line in self.user_logs[selected_user]:
                self.chat_output.insert(END, line + "\n")
            self.chat_output.config(state=DISABLED)

    def run(self):
        self.window.mainloop()

    def start_bot(self):
        global bot_running, bot_thread
        if not bot_running:
            bot_running = True
            self.start_button.config(state=DISABLED)
            self.stop_button.config(state=NORMAL)
            self.log_message("✅ Запуск бота...")
            bot_thread = threading.Thread(target=run_bot, daemon=True)
            bot_thread.start()

    def stop_bot(self):
        global bot_running
        if bot_running:
            self.log_message("⛔ Остановка бота...")
            stop_bot()
            self.start_button.config(state=NORMAL)
            self.stop_button.config(state=DISABLED)


bot_ui = BotUI()


def log(msg, user_id=None):
    print(msg)
    bot_ui.log_message(msg, user_id=user_id)


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = str(message.chat.id)
    bot_ui.update_user_list(chat_id)
    log(f"👤 [{chat_id}] ввёл /start", user_id=chat_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔍 Реки аниме", "💥 Популярные аниме")
    markup.row("🎲 Рандомное аниме", "🎭 Жанры")
    markup.row("⏳ Ожидаемые", "📚 О жанрах")
    markup.row("❤️ Любимое аниме", "📝 Отзыв")

    bot.send_message(message.chat.id, "Привет! Я аниме-бот. Чем могу помочь?", reply_markup=markup)


@bot.message_handler(func=lambda msg: True)
def handle_all(message):
    chat_id = str(message.chat.id)
    text = message.text.strip()

    bot_ui.update_user_list(chat_id)
    log(f"🧑 [{chat_id}]: {text}", user_id=chat_id)

    if text == "🎲 Рандомное аниме":
        genre = random.choice(list(anime_list.keys()))
        anime = random.choice(anime_list[genre])
        response = f"🎬 Случайное аниме: {anime} ({genre})"

    elif text == "🔍 Реки аниме":
        response = "\n".join(["📌 Рекомендации:", "1. Naruto", "2. One Piece", "3. Attack on Titan"])

    elif text == "💥 Популярные аниме":
        popular = ["Naruto", "One Piece", "Demon Slayer", "Attack on Titan"]
        response = "🔥 Популярные аниме:\n" + "\n".join(popular)

    elif text == "🎭 Жанры":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for genre in anime_list.keys():
            markup.add(types.KeyboardButton(genre))
        markup.add("🔙 Назад")
        bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=markup)
        log(f"🤖 [{chat_id}]: Предложены жанры", user_id=chat_id)
        return

    elif text in anime_list:
        response = f"🎥 Аниме в жанре {text}:\n" + "\n".join(anime_list[text])

    elif text == "⏳ Ожидаемые":
        response = "📅 Ожидаемые аниме:\n1. Jujutsu Kaisen S2\n2. Demon Slayer новый сезон\n3. Bleach: Final Arc"

    elif text == "📚 О жанрах":
        response = "\n".join([f"{k}: {v}" for k, v in genre_info.items()])

    elif text == "❤️ Любимое аниме":
        bot.send_message(message.chat.id, "Напиши своё любимое аниме:")
        bot.register_next_step_handler(message, handle_favorite)
        return

    elif text == "📝 Отзыв":
        bot.send_message(message.chat.id, "Оставь свой отзыв:")
        bot.register_next_step_handler(message, handle_feedback)
        return

    elif text == "🔙 Назад":
        handle_start(message)
        return

    else:
        response = "⚠️ Неизвестная команда. Нажми /start"

    bot.send_message(message.chat.id, response)
    log(f"🤖 [{chat_id}]: {response}", user_id=chat_id)


def handle_favorite(message):
    chat_id = str(message.chat.id)
    response = f"❤️ Спасибо! Твоё любимое аниме: {message.text}"
    bot.send_message(message.chat.id, response)
    log(f"🤖 [{chat_id}]: {response}", user_id=chat_id)


def handle_feedback(message):
    chat_id = str(message.chat.id)
    response = "📝 Спасибо за отзыв! Мы ценим это."
    log(f"✉️ Отзыв от {chat_id}: {message.text}", user_id=chat_id)
    bot.send_message(message.chat.id, response)
    log(f"🤖 [{chat_id}]: {response}", user_id=chat_id)


def run_bot():
    try:
        log("🚀 Bot polling запущен.")
        bot.infinity_polling()
    except Exception as e:
        log(f"⚠️ Ошибка при запуске polling: {e}")
    log("🛑 Polling завершён.")


def stop_bot():
    try:
        bot.stop_polling()
    except Exception as e:
        log(f"⚠️ Ошибка при остановке бота: {e}")
    finally:
        global bot_running
        bot_running = False


bot_ui.run()
