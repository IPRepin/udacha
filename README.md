# Бот информационный Telegram для гостевого дома. #
# Version 0.1 #

![Static Badge](https://img.shields.io/badge/Python-3.11-blue)
![Static Badge](https://img.shields.io/badge/Aiogram-3.3.0-blue)
![Static Badge](https://img.shields.io/badge/AiogramСalendar-0.5.0-blue)
![Static Badge](https://img.shields.io/badge/SQLAlchemy-2.0.30-blue)
![Static Badge](https://img.shields.io/badge/urllib3-2.2-blue)
![Static Badge](https://img.shields.io/badge/SQLite-3.45.2-blue)
![Static Badge](https://img.shields.io/badge/Redis-5.0.3-blue)


## Описание проекта ##

Бот информационный Telegram для гостевого дома. Бот изначально настроен на работу с SQLite, но возможно изменение на любую СУБД.
#### Функции пользователя: ####
* возможность узнать подробнее о гостевом доме и его номерах
* подать заявку на бронирование
* узнать о текущих бронированиях
* оставить отзыв о гостевом доме
* возможность вызвать такси до гостевого дома
#### Функции администратора: ####
* возможность добавления редактирования и удаления акций и скидок
* создание рассылок внутри бота по группам пользователей
* просмотр бронирований и работа сними
* в дальнейшем планируется создание автоматических уведомлений пользователей
Также имеется возможность отправки сообщений (логов) об ошибках в телеграм.


## Описание обновлений ##
### Version 0.1 ###
MVP версия бота. Бот в стадии разработки.

## Требования к окружению ##

* Python==3.11
* aiogram==3.3.0
* python-dotenv==1.0.0
* urllib3==2.2.1
* sqlite == 3.45.2
* redis==5.0.3
* SQLAlchemy~=2.0.30
* aiogram-calendar==0.5.0

## Структура проекта ##

📦udacha
 * ┣ 📦data _(пакет модулей для работы с БД)_
 * ┣ 📦filters _(пакет модулей фильтров)_
 * ┣ 📦handlers _(пакет работы с handlers бота)_
 * ┣ 📦keyboards _(пакет работы с клавиатурами бота)_
 * ┣ 📦middleware _(пакет работы с middlewares)_
 * ┣ 📦utils _(вспомогательный пакет с дополнительными модулями)_
 * ┣ 📜bot.py _(модуль запуска телеграм бота)_
 * ┣ 📜config.py _(модуль инициализации переменных)_
 * ┣ 📜.gitignore
 * ┗ 📜requirements.txt

## Запуск на локальном компьютере

Следуя этим инструкциям, вы получите копию проекта, которая будет запущена на вашем локальном компьютере для целей разработки и тестирования.

### Инструкция по запуску
1. Клонировать копию проекта на локальный компьютер командой
```
https://github.com/IPRepin/udacha.git
```
2. В используемой вами IDE в корне проекта создаем виртуальную среду командой
```
python3.11 -m venv venv
```
И активируем ее 
```
source venv/bin/activate
```
3. В корне проекта создаем файл переменных окружения .env с параметрами
```
TELEGRAM_TOKEN=<Токен вашего телеграм бота>
ADMINS=<Список id телеграм пользователей, администраторов бота через запятую>
REDIS_URL=False(True) Использование Redis (при значении False используется MemoryStorage)
LOGS_PATH=<путь к паке с логами>
DB_URL=<URL_к базе данных>
```
Для создания телеграм бота и получения токена воспользуйтесь [инструкцией](https://chatlabs.ru/botfather-instrukcziya-komandy-nastrojki/)

4. Устанавливаем зависимости
```
pip install -r requirements.txt
```


## Запуск бота Телеграм ##
`python bot.py`