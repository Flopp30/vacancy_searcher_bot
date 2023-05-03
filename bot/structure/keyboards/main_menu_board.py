from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Поиск вакансий',
            ),
            KeyboardButton(
                text='Посмотреть профиль',
            ),
            KeyboardButton(
                text='Изменить профиль',
                web_app=WebAppInfo(url='https://flopp30.github.io/')
            ),
        ],
    ],
    resize_keyboard=True
)
