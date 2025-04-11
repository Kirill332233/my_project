import telebot
from telebot import types
import random
from abc import ABC, abstractmethod
import logging
from datetime import datetime

bot = telebot.TeleBot('7588340886:AAHVXt-tCySj7T1CKS4ZbpEmMMAiCwU5HQE')

last_message_id = None

anime_list = {
    'Shonen': ['Naruto', 'One Piece', 'Dragon Ball Z', 'My Hero Academia'],
    'Seinen': ['Attack on Titan', 'Death Note', 'Tokyo Ghoul', 'Fullmetal Alchemist'],
    'Shojo': ['Sailor Moon', 'Fruits Basket', 'Ouran High School Host Club', 'Cardcaptor Sakura'],
    'Isekai': ['Sword Art Online', 'Re:Zero', 'No Game No Life', 'That Time I Got Reincarnated as a Slime']
}

upcoming_anime = {
    'Demon Slayer: Kimetsu no Yaiba': 'C:/Users/Кирилл/Desktop/tg bot/Фотки для бота/klinok.jpg',
    'Jujutsu Kaisen Season 2': 'C:/Users/Кирилл/Desktop/tg bot/Фотки для бота/магбитв.jpg',
    'Bleach: Thousand-Year Blood War': 'C:/Users/Кирилл/Desktop/tg bot/Фотки для бота/bleach.jpg',
    'Attack on Titan: Final Season Part 3': 'C:/Users/Кирилл/Desktop/tg bot/Фотки для бота/attack.jpg'
}

genre_descriptions = {
    'Shonen': 'Аниме для молодежи с приключениями и боевыми искусствами.',    'Seinen': 'Аниме для взрослых с глубокими темами.',
    'Shojo': 'Романтические и драматические истории для женщин.',
    'Isekai': 'Герой попадает в другой мир с магией и фантастикой.'
}

# Абстрактный класс для вывода сообщения о запуске бота
class BotStartupLogger(ABC):
    @abstractmethod
    def log_startup(self):
        pass

# Реализация класса вывода сообщения о запуске бота
class BotLogger(BotStartupLogger):
    @staticmethod
    def log_startup():
        print("Бот успешно запущен!")

# Класс для работы с массивами объектов
class Anime:
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre

    def __repr__(self):
        return f"{self.name} ({self.genre})"


class AnimeCollection:
    def __init__(self, anime_list):
        self.anime_list = anime_list
        self.anime_grid = []

    def add_anime_to_grid(self, row):
        self.anime_grid.append(row)

    def find_max_attribute_anime(self):
        max_anime = None
        for row in self.anime_grid:
            for anime in row:
                if not max_anime or len(anime.name) > len(max_anime.name):
                    max_anime = anime
        return max_anime


# Абстрактный класс с методами, которые будут переопределены в наследуемых классах
class BotHandler(ABC):

    @abstractmethod
    def handle_message(self, message):
        pass

    @staticmethod
    def create_back_button():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        back_button = types.KeyboardButton("🔙 Назад")
        markup.add(back_button)
        return markup

    @staticmethod
    def delete_previous_message(message):
        global last_message_id
        if last_message_id:
            try:
                bot.delete_message(message.chat.id, last_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
        last_message_id = message.message_id

    #raise и finally
    @staticmethod
    def handle_exception():
        try:
            raise ValueError("Ошибка при удалении сообщения:")
        except ValueError as e:
            print(f"Произошла ошибка: {e}")
        finally:
            print("Этот часть меню временно не раотает.")


# Меню
class MenuHandler(BotHandler):
    @staticmethod
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        BotHandler.delete_previous_message(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton("🔍 Реки аниме")
        item2 = types.KeyboardButton("💥 Популярные аниме")
        item3 = types.KeyboardButton("🎲 Рандомное аниме")
        item4 = types.KeyboardButton("🎭 Жанры")
        item5 = types.KeyboardButton("⏳ Ожидаемые")
        item6 = types.KeyboardButton("📚 О жанрах")
        item7 = types.KeyboardButton("❤️ Любимое аниме")
        item8 = types.KeyboardButton("📝 Отзыв")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8)
        bot.send_message(message.chat.id, "Привет! Я бот по теме аниме. Чем могу помочь?", reply_markup=markup)

    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "🔙 Назад")
    def back_to_menu(message):
        BotHandler.delete_previous_message(message)
        MenuHandler.send_welcome(message)


# Обработка кнопки "🔍 Реки аниме"
class RecommendedAnimeHandler:
    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "🔍 Реки аниме")
    def send_recommendations(message):
        BotHandler.delete_previous_message(message)
        bot.send_message(message.chat.id,
                         "Рекомендации по аниме:\n1. Naruto\n2. One Piece\n3. Attack on Titan\n4. My Hero Academia\n5. Fullmetal Alchemist",
                         reply_markup=BotHandler.create_back_button())

# Обработка жанров
class GenreHandler:
    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "🎭 Жанры")
    def ask_genre(message):
        BotHandler.delete_previous_message(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton("Shonen")
        item2 = types.KeyboardButton("Seinen")
        item3 = types.KeyboardButton("Shojo")
        item4 = types.KeyboardButton("Isekai")
        back_button = types.KeyboardButton("🔙 Назад")
        markup.add(item1, item2, item3, item4, back_button)
        bot.send_message(message.chat.id, "Выберите жанр аниме:", reply_markup=markup)

    @staticmethod
    @bot.message_handler(func=lambda message: message.text in ["Shonen", "Seinen", "Shojo", "Isekai"])
    def send_anime_by_genre(message):
        BotHandler.delete_previous_message(message)
        genre = message.text
        recommended_animes = anime_list[genre]
        markup = BotHandler.create_back_button()
        bot.send_message(message.chat.id, f"Рекомендованные аниме для жанра {genre}:\n" + "\n".join(recommended_animes),
                         reply_markup=markup)

    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "🔙 Назад")
    def back_to_main_menu(message):
        BotHandler.delete_previous_message(message)
        MenuHandler.send_welcome(message)


# Обработка случайного аниме
class RandomAnimeHandler:
    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "🎲 Рандомное аниме")
    def send_random_anime(message):
        BotHandler.delete_previous_message(message)
        random_genre = random.choice(list(anime_list.keys()))
        random_anime = random.choice(anime_list[random_genre])
        bot.send_message(message.chat.id, f"Случайное аниме: {random_anime} \n Жанра: {random_genre}",
                         reply_markup=BotHandler.create_back_button())

# Обработка популярных аниме
class PopularAnimeHandler:
    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "💥 Популярные аниме")
    def send_popular_anime(message):
        BotHandler.delete_previous_message(message)
        popular_animes = "\n".join(["Naruto", "One Piece", "Attack on Titan", "My Hero Academia", "Demon Slayer"])
        bot.send_message(message.chat.id, f"Популярные аниме:\n{popular_animes}", reply_markup=BotHandler.create_back_button())

# Обработка ожидаемых аниме
class UpcomingAnimeHandler:
    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "⏳ Ожидаемые")
    def send_upcoming_anime(message):
        try:
            BotHandler.delete_previous_message(message)
            response = "Самые ожидаемые аниме:\n"
            for anime, image_path in upcoming_anime.items():
                response += f"{anime}\n"
                try:
                    with open(image_path, 'rb') as image:
                        bot.send_photo(message.chat.id, image, caption=anime,
                                       reply_markup=BotHandler.create_back_button())
                except Exception as e:
                    bot.send_message(message.chat.id, f"Ошибка при отправке изображения для {anime}: {str(e)}")
            bot.send_message(message.chat.id, response, reply_markup=BotHandler.create_back_button())
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}", reply_markup=BotHandler.create_back_button())

# Обработка информации о жанрах
class GenreInfoHandler:
    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "📚 О жанрах")
    def send_genre_info(message):
        BotHandler.delete_previous_message(message)
        genre_info = "\n".join([f"{genre}: {description}" for genre, description in genre_descriptions.items()])
        bot.send_message(message.chat.id, f"Информация о жанрах:\n{genre_info}", reply_markup=BotHandler.create_back_button())

# Обработка любимого аниме
class FavoriteAnimeHandler:
    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "❤️ Любимое аниме")
    def ask_favorite_anime(message):
        BotHandler.delete_previous_message(message)
        bot.send_message(message.chat.id, "Напишите название вашего любимого аниме:", reply_markup=BotHandler.create_back_button())
        bot.register_next_step_handler(message, FavoriteAnimeHandler.save_favorite_anime)

    @staticmethod
    def save_favorite_anime(message):
        BotHandler.delete_previous_message(message)
        favorite_anime = message.text
        bot.send_message(message.chat.id, f"Ваше любимое аниме: {favorite_anime}", reply_markup=BotHandler.create_back_button())

# Обработка отзывов
class FeedbackHandler:
    @staticmethod
    @bot.message_handler(func=lambda message: message.text == "📝 Отзыв")
    def ask_feedback(message):
        BotHandler.delete_previous_message(message)
        bot.send_message(message.chat.id, "Напишите свой отзыв!", reply_markup=BotHandler.create_back_button())
        bot.register_next_step_handler(message, FeedbackHandler.save_feedback)

    @staticmethod
    def save_feedback(message):
        BotHandler.delete_previous_message(message)
        user_name = message.from_user.username if message.from_user.username else f"Пользователь {message.from_user.id}"
        feedback_text = message.text
        print(f"Отзыв от {user_name}: {feedback_text}")
        bot.send_message(message.chat.id, f"Спасибо за ваш отзыв, {user_name}!",
                         reply_markup=BotHandler.create_back_button())

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AnimeBase(ABC):
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre
        logging.info(f"Создан объект {self.__class__.__name__}: {self.title}, жанр: {self.genre}")

    @abstractmethod
    def get_info(self):
        pass


class TVAnime(AnimeBase):
    def __init__(self, title, genre, episodes):
        super().__init__(title, genre)
        self.episodes = episodes

    def get_info(self):
        info = f"Сериал: {self.title} ({self.genre}), эпизодов: {self.episodes}"
        logging.info(f"Вызов get_info у TVAnime: {info}")
        return info


class MovieAnime(AnimeBase):
    def __init__(self, title, genre, duration):
        super().__init__(title, genre)
        self.duration = duration

    def get_info(self):
        info = f"Фильм: {self.title} ({self.genre}), длительность: {self.duration} мин"
        logging.info(f"Вызов get_info у MovieAnime: {info}")
        return info

class AnimeInfoProvider(ABC):
    @abstractmethod
    def get_info(self):
        pass


class AnimeBase(AnimeInfoProvider):
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre
        logging.info(f"Создан объект {self.__class__.__name__}: {self.title}, жанр: {self.genre}")


anime_objects = [
    TVAnime("Naruto", "Shonen", 220),
    TVAnime("Attack on Titan", "Seinen", 75),
    MovieAnime("Your Name", "Romance", 112),
    MovieAnime("Spirited Away", "Fantasy", 125)
]


sorted_anime = sorted(anime_objects, key=lambda a: len(a.title), reverse=True)

filter_seinen = list(filter(lambda a: a.genre == "Seinen", anime_objects))

for anime in sorted_anime:
    print(anime.get_info())

for anime in filter_seinen:
    print(f"[Seinen фильтр] {anime.get_info()}")

if __name__ == '__main__':
    BotLogger.log_startup()
bot.polling(none_stop=True)