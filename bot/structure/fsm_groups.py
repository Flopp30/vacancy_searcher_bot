from aiogram.fsm.state import StatesGroup, State


class ProfileCreateStates(StatesGroup):
    waiting_for_choose_create_type = State()
    waiting_for_firstname = State()
    waiting_for_lastname = State()
    waiting_for_email = State()
    waiting_for_professional_role = State()
    waiting_for_experience = State()

    waiting_for_choose_field = State()
    waiting_for_partial_update_data = State()
    waiting_for_choose_edit_type = State()


class ProfileUpdateStates(StatesGroup):
    waiting_for_choose_field = State()
    waiting_for_partial_update_data = State()
    waiting_for_choose_edit_type = State()
    waiting_for_next_step = State()


