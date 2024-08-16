import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Jinja, List
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Radio,
    Row,
    Select,
    ScrollingGroup
)

from bot.aiogram_dialog.scrolling_group import ScrollingGroupCustom

from . import getters
from . import handlers
from bot.handlers.handlers import main_menu 
from bot.states import BebrisDialogSG


choice_playlist_window = Window(
    Const('Выбри цвет плейлиста'),
    ScrollingGroup(
        Group(
            Select(
                Format('{item[2]} {item[1]}'),
                id='playlist_btns',
                items='playlists',
                item_id_getter=lambda x: x[0],
                on_click=handlers.choice_lesson
            ),
        ),
        id='playlist_scroll',
        width=1,
        height=5,
        hide_on_single_page=True,
    ),
    Button(Const('◀ Назад'), id='main_menu', on_click=main_menu),
    getter=getters.playlist_getter,
    state=BebrisDialogSG.start
)


choice_lesson_window = Window(
    Jinja(
        '<b>--- Памятка ---</b>\n\n'
        # '<blockquote>Прогресс - это усреднённый процент правильных ответов за последние три урока.</blockquote>\n\n'
        '<blockquote>Прогресс показывает средний процент правильных ответов за последние три урока.</blockquote>\n\n'
        '🔴 - <i>Прогресс меньше 60%</i>\n'
        '🟠 - <i>Прогресс 60-90%</i>\n'
        '🟢 - <i>Прогресс 90-100%</i>\n\n'
        '<b>--- Выбери урок ---</b>\n\n'
    ),
    List(
        Format('{item[3]} <b>№{item[0]}</b>  {item[1]} {item[2]}'),
        page_size=8,
        id='lessons_scroll',
        items='lessons'
    ),
    ScrollingGroupCustom(
        Group(
            Select(
                Format('{item[0]}'),
                id='lesson_btns',
                items='lessons',
                item_id_getter=lambda x: x[0],
                on_click=handlers.prepare_lesson_data
            ),
        ),
        id='lessons_scroll',
        width=8,
        height=1,
        hide_on_single_page=True,
    ),
    Button(Const('☰ Mеню'), id='main_menu', on_click=main_menu),
    parse_mode='HTML',
    getter=getters.lesson_getter,
    state=BebrisDialogSG.choice_lesson
)

preparation_window = Window(
    Jinja(
        'Сводка информации:\n\n'
        '⚙️ <b>Режимы тренировок:</b>\n'
        'RU2EN - <i>с русского на английский</i>\n'
        'EN2RU - <i>с английского на русский</i>\n'
    ),
    Radio(
        checked_text=Format('🔘 {item[0]}'),
        unchecked_text=Format('⚪️ {item[0]}'),
        id='radio_reverse_mode',
        item_id_getter=operator.itemgetter(1),
        items=[('RU to EN', '0'), ('EN to RU', '1')],
    ),
    Button(Const('Начать'), id='start', on_click=handlers.play_cards),
    parse_mode='HTML',
    getter=getters.preparation_getter,
    state=BebrisDialogSG.preparation
)


flashcard_window = Window(
    Jinja(
        '{{ position }}/{{total_cards}} (#{{ current_card_id }})\n\n'
        '{{ front_text }}\n\n'
        '<tg-spoiler>{{ back_text }}</tg-spoiler>\n\n'
        '🔴 {{ total_wrong_answers }} - {{ total_correct_answers }} 🟢 ({{ accuracy_percent }}%)'
    ),
    Row(
        Button(Const('Не помню'), id='wrong', on_click=handlers.next_card_or_completion),
        Button(Const('Помню'), id='correct', on_click=handlers.next_card_or_completion),
    ),
    parse_mode='HTML',
    getter=getters.next_card_getter,
    state=BebrisDialogSG.next_card
)


conclusion_window = Window(
    Format('{data} = {data2}'),
    getter=getters.conclusion_getter,
    state=BebrisDialogSG.conclusion
)


bebris_dialog = Dialog(
    choice_playlist_window, choice_lesson_window,
    preparation_window, flashcard_window,
    conclusion_window)
