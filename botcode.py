import telebot
import config
from telebot import types # Импортирование функции random для рандомного рецепта
import random

# Создаем экземпляр бота с токеном из config.py
bot = telebot.TeleBot(config.token)

# Хранилища данных пользователей
user_current_recipe = {}  # хранит текущий просматриваемый рецепт для каждого пользователя
user_daily_recipe = {}    # хранит рецепт дня для каждого пользователя
user_waiting_for_photo = {}  # хранит пользователей, ожидающих отправки фото
user_registration = {}    # хранит данные регистрации пользователей
user_registration_state = {}  # хранит состояние регистрации пользователей 

# База данных рецептов, разделенная по категориям
breakfast = [
    "Омлет: яйца, молоко, соль, масло. Взбить яйца с молоком, посолить, жарить на сковороде 5-7 минут.", 
    "Овсяная каша: овсяные хлопья, молоко/вода, соль, сахар. Варить 10 минут, подавать с маслом.",
    "Яичница: яйца, соль, перец, масло. Разбить яйца на сковороду, жарить 3-4 минуты до готовности.",
    "Блины: мука, яйца, молоко, соль, сахар. Смешать ингредиенты, жарить на раскаленной сковороде с двух сторон.",
    "Сырники: творог, яйцо, мука, сахар. Замесить тесто, формировать лепешки, обжаривать до золотистой корочки.",
    "Гренки: хлеб, яйца, молоко, соль. Хлеб обмакнуть в яичную смесь, обжарить на сливочном масле до румяности.",
    "Мюсли: овсяные хлопья, орехи, сухофрукты, йогурт/молок. Смешать все ингредиенты, дать настояться 5 минут.",
    "Тост с авокадо: хлеб, авокадо, соль, лимонный сок. Хлеб поджарить, авокадо размять с солью и лимонным соком.",
    "Гречневая каша: гречка, вода, соль, масло. Варить крупу 15-20 минут до готовности, заправить маслом.",
    "Омлет с овощами: яйца, помидор, перец, лук, соль. Овощи обжарить, залить яйцами, готовить под крышкой 7 минут."
]

lunch = [
    "Суп: куриный бульон, картофель, морковь, лук, зелень. Варить овощи в бульоне 20 минут до готовности.", 
    "Борщ: свекла, капуста, картофель, мясо, сметана. Варить 1.5 часа, подавать со сметаной и зеленью.",
    "Щи: капуста, картофель, морковь, мясной бульон, томатная паста. Варить 40 минут, добавить зелень перед подачей.",
    "Грибной суп: грибы, картофель, лук, морковь, сливки. Обжарить грибы с овощами, добавить картофель, варить 25 минут.",
    "Куриный суп с лапшой: куриное филе, лапша, морковь, лук, зелень. Варить курицу 30 минут, добавить лапшу и овощи.",
    "Солянка: различные виды мяса, соленые огурцы, оливки, томатная паста. Варить 45 минут, подавать с лимоном.",
    "Тыквенный суп-пюре: тыква, картофель, лук, сливки. Овощи варить до мягкости, взбить блендером, добавить сливки.",
    "Рассольник: перловка, картофель, соленые огурцы, морковь. Варить 50 минут, заправить огуречным рассолом.",
    "Фасолевый суп: фасоль, копчености, картофель, томаты. Фасоль предварительно замочить, варить 1 час с овощами.",
    "Жаркое: свинина, картофель, морковь, лук, чеснок. Мясо обжарить до корочки, добавить овощи, тушить 40 минут."
]

dinner = [
    "Стейк: говядина, соль, перец, масло. Обжарить с двух сторон по 3-4 минуты, дать отдохнуть 5 минут.", 
    "Пельмени: мясной фарш, лук, тесто, сметана. Варить в подсоленной воде 7-10 минут после закипания, подавать со сметаной.",
    "Курица с картофелем: куриное филе, картофель, специи, масло. Запекать 40 минут при 200°C до румяной корочки.",
    "Паста с соусом: макароны, томатный соус, базилик, пармезан. Варить пасту 8-10 минут, смешать с подогретым соусом.",
    "Паста Карбонара: спагетти, бекон, яйца, пармезан, сливки. Варить пасту 8 минут, смешать с соусом из бекона и яиц.",
    "Жаркое: мясо, картофель, морковь, лук, специи. Обжарить мясо, добавить овощи, тушить 40 минут под крышкой.",
    "Овощное рагу: кабачки, баклажаны, перцы, томаты, лук. Овощи обжарить, тушить 25 минут с травами.",
    "Котлеты с пюре: фарш, лук, хлеб, картофель, молоко. Котлеты жарить 15 минут, пюре варить 20 минут.",
    "Плов: рис, мясо, морковь, лук, специи. Обжарить мясо с овощами, добавить рис, тушить 30 минут на медленном огне.",
    "Омлет с ветчиной: яйца, ветчина, сыр, молоко, зелень. Взбить яйца с молоком, добавить ветчину и сыр, жарить 10 минут под крышкой."
]

cocktail = [
    "Сок: апельсины. Выжать сок из апельсинов, подавать охлажденным.", 
    "Смузи: банан, ягоды, йогурт. Взбить в блендере до однородной консистенции.",
    "Мохито: лайм, мята, сахар, газированная вода. Размять мяту с лаймом, добавить лед и газировку.",
    "Лимонад: лимоны, сахар, вода, мята. Выжать сок лимонов, смешать с сахаром и водой, добавить лед.",
    "Клубничный коктейль: клубника, молоко, мороженое, сахар. Взбить все ингредиенты в блендере.",
    "Какао: молоко, какао-порошок, сахар. Молоко подогреть, добавить какао и сахар, размешать до растворения.",
    "Чай с имбирем: чай, имбирь, мед, лимон. Заварить чай, добавить тертый имбирь, мед и лимон.",
    "Кофе латте: эспрессо, молоко, сахар. Сварить кофе, вспенить молоко, аккуратно соединить.",
    "Морс: ягоды, вода, сахар. Ягоды размять, залить водой, добавить сахар, процедить.",
    "Молочный коктейль: молоко, мороженое, сироп. Взбить в блендере до пышной пены."
]

images = [
    "https://avatars.mds.yandex.net/i?id=f13e69c3f95d8b5295b91a0a715867d2-5516118-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=e80bac0132859677eba399e848412024-3390871-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=db82abfd50def519c8fce1a7a793e21dd4a157fb-9291460-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=96d0dad330a0d60d2aa87b359c77961767e81ffa-4232374-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=5a6fd13071d7b190babef219afe956dd32495d2c-12446123-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=a10adcfa27c0a929acc65f3306b054d248d7bb70-4234405-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=90f46d14d43131d0238f0f9ca476484e2520a5dd-5296093-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=529f2b458dce5197f86561dffbe977496fac2f83-8965182-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=61ed7877ee3b2e8e58ef04ca505e1e06fdc2c655-5848264-images-thumbs&n=13",
    "https://avatars.mds.yandex.net/i?id=c01df56737b066940baab2fcb1436ada8a8deb64-16445653-images-thumbs&n=13"
]

# Словарь для удобного доступа к категориям рецептов по названиям
recipe_categories = {"Завтрак": breakfast, "Обед": lunch, "Ужин": dinner, "Напиток": cocktail}

# Функция для получения случайного рецепта из любой категории
def get_random_recipe():
    # Создаем общий список всех рецептов из всех категорий
    all_recipes = []
    for category in recipe_categories.values(): # values вытаскивает значения словарей
        all_recipes.extend(category) 
    return random.choice(all_recipes) 
   
# Создает инлайн-клавиатуру для режима дня
def create_daily_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Сделать рецептом дня", callback_data="replace_daily"))
    keyboard.add(types.InlineKeyboardButton("Следующий рецепт", callback_data="next_recipe"))
    return keyboard

# Создает reply-клавиатуру для выбора категорий
def create_category_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопки для каждой категории
    buttons = [types.KeyboardButton(category) for category in recipe_categories.keys()]
    keyboard.add(buttons[0], buttons[1])
    keyboard.add(buttons[2], buttons[3])
    return keyboard

# Отправка следующего случайного рецепта пользователю
def send_next_recipe(user_id, chat_id):
    user_current_recipe[user_id] = get_random_recipe()
    bot.send_message(chat_id, f"Следующий рецепт:\n\n{user_current_recipe[user_id]}", 
                   reply_markup=create_daily_keyboard())


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет! Я бот, который поможет выбрать блюдо на день.
Нажмите /help для списка команд. \
""", reply_markup=types.ReplyKeyboardRemove())  # Убираем клавиатуру с экрана


# # Handle '/help'
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """\
Команды бота:
/start - начать работу
/help - список команд
/recipe - сгенерировать рецепт
/daily - рецепт дня
/image - обмен картинками
/sign - регистрация
/login - вход \
"""
    bot.reply_to(message, help_text, reply_markup=types.ReplyKeyboardRemove())


# Hendle '/sign'
@bot.message_handler(commands=['sign'])
def start_registration(message):
    user_id = message.from_user.id
    
    # Проверяем, не зарегистрирован ли пользователь уже
    if user_id in user_registration:
        user_data = user_registration[user_id]
        bot.reply_to(message, f"""\
Вы уже зарегистрированы!

Ваши данные:
- Имя: {user_data['first_name']}
- Фамилия: {user_data['last_name']}
- Год рождения: {user_data['birth_year']}\
""")
    else:
        # Устанавливаем состояние "ожидание имени" для этого пользователя
        user_registration_state[user_id] = "waiting_first_name"
        bot.reply_to(message, """\
Давайте зарегистрируем вас!
Пожалуйста, введите ваше имя: \
        """)


# Обработчик для регистрационных данных - ждет сообщения, когда пользователь находится в процессе регистрации
@bot.message_handler(func=lambda message: user_registration_state.get(message.from_user.id))
def handle_registration(message):
    user_id = message.from_user.id
    # Получаем текущее состояние регистрации пользователя
    current_state = user_registration_state[user_id]
    
    if current_state == "waiting_first_name":
        # Сохраняем имя и запрашиваем фамилию
        user_registration[user_id] = {}
        user_registration[user_id]['first_name'] = message.text
        user_registration_state[user_id] = "waiting_last_name"
        bot.reply_to(message, "Отлично! Теперь введите вашу фамилию:")
        
    elif current_state == "waiting_last_name":
        # Сохраняем фамилию и запрашиваем год рождения
        user_registration[user_id]['last_name'] = message.text
        user_registration_state[user_id] = "waiting_birth_year"
        bot.reply_to(message, "Отлично! Теперь введите ваш год рождения:")
        
    elif current_state == "waiting_birth_year":
        # Сохраняем год рождения и завершаем регистрацию
        user_registration[user_id]['birth_year'] = message.text
        # Удаляем пользователя из состояния регистрации
        del user_registration_state[user_id]
        user_data = user_registration[user_id]
        bot.reply_to(message, f"""\
Регистрация завершена!

Ваши данные:
- Имя: {user_data['first_name']}
- Фамилия: {user_data['last_name']}
- Год рождения: {user_data['birth_year']} \
""")


# Handle '/login'
@bot.message_handler(commands=['login'])
def login_user(message):
    user_id = message.from_user.id
    # Если пользователь уже зарегистрирован
    if user_id in user_registration:
        data = user_registration[user_id]
        bot.reply_to(message, f"""\
Добро пожаловать назад!

Ваши данные:
- Имя: {data['first_name']}
- Фамилия: {data['last_name']}
- Год рождения: {data['birth_year']} \
""")
    else:
        # Если пользователь не зарегистрирован
        bot.reply_to(message, """\
Вы еще не зарегистрированы!

Используйте команду /sign для регистрации.\
""")
    

# Handle '/recipe'
@bot.message_handler(commands=['recipe'])
def send_recipe(message):
    bot.send_message(message.chat.id, "Выберите категорию блюда:", reply_markup=create_category_keyboard())


# Обработчик нажатий на кнопки категорий рецептов
@bot.message_handler(func=lambda message: message.text in recipe_categories)
def handle_recipe_buttons(message):
    recipe = random.choice(recipe_categories[message.text])
    user_current_recipe[message.from_user.id] = recipe

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Сделать рецептом дня", callback_data="add_to_daily"))
    
    bot.send_message(message.chat.id, recipe, reply_markup=keyboard)


# Handle '/daily'
@bot.message_handler(commands=['daily'])
def send_daily_recipe(message):
    user_id = message.from_user.id
    
    # Если у пользователя еще нет рецепта дня - создаем случайный
    if user_id not in user_daily_recipe:
        user_daily_recipe[user_id] = get_random_recipe()
    
    user_current_recipe[user_id] = user_daily_recipe[user_id]
    
    text = "Ваш текущий рецепт дня:"
    bot.send_message(message.chat.id, f"{text}\n\n{user_daily_recipe[user_id]}", reply_markup=create_daily_keyboard())


# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: call.data in ["add_to_daily", "replace_daily", "next_recipe"])
def handle_daily_buttons(call):
    user_id = call.from_user.id
    
    # Обработка кнопок установки рецепта дня
    if call.data in ["add_to_daily", "replace_daily"]:
        user_daily_recipe[user_id] = user_current_recipe[user_id]
        bot.send_message(call.message.chat.id, f"У нас новый рецепт дня!\n\n{user_current_recipe[user_id]}")
        
        # Если кнопка нажата в режиме выбора дня - показываем следующий рецепт
        if call.data == "replace_daily":
            send_next_recipe(user_id, call.message.chat.id)
    
    # Обработка кнопки "Следующий рецепт"
    elif call.data == "next_recipe":
        send_next_recipe(user_id, call.message.chat.id)


# Handle '/image'
@bot.message_handler(commands=['image'])
def start_image_exchange(message):
    user_id = message.from_user.id
    # Помечаем пользователя как ожидающего фото
    user_waiting_for_photo[user_id] = True
    bot.reply_to(message, "Жду вашу фотографию!")


# Обработчик для фотографий в режиме обмена
@bot.message_handler(content_types=['photo'], func=lambda message: user_waiting_for_photo.get(message.from_user.id, False))
def handle_image_exchange_photo(message):
    user_id = message.from_user.id
    # Убираем пользователя из списка ожидания
    user_waiting_for_photo[user_id] = False
    
    # Получаем случайную картинку из списка
    random_image_url = random.choice(images)
    
    # Отправляем случайную картинку в ответ
    bot.send_photo(message.chat.id, random_image_url)


# Обработчик для обычных фотографий (не в режиме /image)
@bot.message_handler(content_types=['photo'])
def handle_regular_photos(message):
    bot.reply_to(message, "Используйте /help для списка команд")


# Обработчик для всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "Используйте /help для списка команд")


bot.infinity_polling()