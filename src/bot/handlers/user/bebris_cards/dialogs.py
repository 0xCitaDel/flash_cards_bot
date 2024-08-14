import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Jinja, List
from aiogram_dialog.widgets.kbd import (
    Button,
    Checkbox,
    Group,
    ManagedCheckbox,
    Radio,
    Row,
    Select,
    ScrollingGroup
)

from . import getters
from . import handlers
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
    getter=getters.playlist_getter,
    state=BebrisDialogSG.start
)


choice_lesson_window = Window(
    Const('Выбери номер урока\n'),
    List(
        Format('№{item[0]} - {item[1]}'),
        page_size=8,
        id='lessons_scroll',
        items='lessons'
    ),
    ScrollingGroup(
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
    getter=getters.lesson_getter,
    state=BebrisDialogSG.choice_lesson
)

async def checkbox_clicked(callback: CallbackQuery, checkbox: ManagedCheckbox,
                           dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(is_checked=checkbox.is_checked())


# Геттер
async def getter(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.dialog_data.get('is_checked')
    return {'checked': checked,
            'not_checked': not checked}

preparation_window = Window(
    Jinja(
        'Сводка информации:\n\n'
        '⚙️ <b>Режимы тренировок:</b>\n'
        'RU2EN - <i>с русского на английский</i>\n'
        'EN2RU - <i>с английского на русский</i>\n'
    ),
    Checkbox(
        checked_text=Const('[✔️] Отключить'),
        unchecked_text=Const('[ ] Включить'),
        id='checkbox',
        default=False,
        on_state_changed=checkbox_clicked,
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
        Button(Const('👎'), id='wrong', on_click=handlers.next_card_or_completion),
        Button(Const('👍'), id='correct', on_click=handlers.next_card_or_completion),
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
