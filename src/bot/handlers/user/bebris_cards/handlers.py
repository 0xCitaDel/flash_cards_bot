import random

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from bot.states import BebrisDialogSG
from db.database import Database
from services.bbr_cards import BebrisService


async def choice_lesson(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id
):
    """
    Handler switches the state to select the lesson number

    :param item_id: playlist primary key (playlist ID)
    """
    # Store the selected playlist ID in the dialog data
    manager.dialog_data['playlist_id'] = int(item_id)

    # Transition to the lesson selection state
    await manager.switch_to(BebrisDialogSG.choice_lesson)


async def prepare_lesson_data(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id
):
    """
    Prepares the lesson start by showing introductory info
    before flashcard review begins.

    :param item_id: lesson primary key (lesson ID)
    """
    # Remove existing lesson data from the dialog context
    manager.dialog_data.pop('lessons', None)

    # Fetch lesson data and flashcards from the database and update the context
    db: Database = manager.middleware_data['db']
    bebris_service = BebrisService(db)
    data: dict = await bebris_service.get_cards_and_create_dialog_data(
        lesson_id=int(item_id)
    )
    manager.dialog_data.update(data)         

    # Set the default radio button selection for the lesson mode
    await manager.find('radio_reverse_mode').set_checked(item_id='0')

    # Transition to the lesson preparation state
    await manager.switch_to(BebrisDialogSG.preparation)


async def lesson_exit(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager
):
    """
    Need here...
    """
    await manager.switch_to(BebrisDialogSG.lesson_exit)


async def show_all_cards(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager
):
    """
    Need here...
    """
    await manager.switch_to(BebrisDialogSG.show_all_cards)


async def play_cards(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager
):
    """
    Handler shuffle and switches the state to start playing flashcards.
    """
    all_cards = manager.dialog_data['all_cards']
    random.shuffle(all_cards)
    await manager.switch_to(BebrisDialogSG.next_card)


async def next_card_or_completion(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager
):
    """
    Handles the transition to the next flashcard or completes the lessons
    if all cards have been reviewed.
    """ 
    # Retrieve dialog data and database connection
    data = manager.dialog_data
    db = manager.middleware_data['db']

    # Get the current card index and its ID
    index_current_card = data['current_card_index']
    card_id = data['all_cards'][index_current_card][0]

    # Process the user's choice: correct or incorrect
    if widget.widget_id == 'correct':
        data['correct_answer_ids'].append(card_id)
    else:
        data['wrong_answer_ids'].append(card_id)

    # Increment the current card index to move to the next one   
    data['current_card_index'] += 1

    # Update flashcard data in the dialog_data
    data_update = await BebrisService(db).update_flashcards_data(data)
    data.update(data_update)

    # Check if there are more cards to review
    if data['current_card_index'] < data['total_cards']:
        await manager.switch_to(BebrisDialogSG.next_card)
    else:
        await manager.switch_to(BebrisDialogSG.conclusion)
