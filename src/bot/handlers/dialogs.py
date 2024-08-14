from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from . import getters
from . import handlers
from bot.states import MainSG


main_window = Window(
    Const('Главное меню, выберите нужный вам раздел'),
    Button(
        Const('Английский по плейлистам'),
        id='bebris_btn',
        on_click=handlers.bebris_dialog_start
    ),
    state=MainSG.start
)

main_dialog = Dialog(
    main_window
)
