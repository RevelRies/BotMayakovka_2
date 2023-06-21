# отдельные иморты
import pathlib

# файлы проекта
from keyboards.menu_for_location_keyboard import location_keyboard, location_keyboard_without_next_button
from keyboards.second_lvl_keyboards import walk_keyboard
from keyboards.fifth_location_keyboard import fifth_location_keyboard
from crud.all_location_info import get_location_info_by_number, get_images_location_info_by_number
from crud.add_action import add_action
from other.additional_functions import parsing_images

# импорты aiogram
from aiogram.filters import Text
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile



# роутер (сын диспетчера)
router = Router()

# обработка кнопки 'Я на месте'
@router.message(Text(text='Я на месте'))
async def in_place_handler(message: Message, state: FSMContext):
    # при каждом нажатии этой кнопки номер локации пользователя в ФСМ состоянии увеличивается на 1

    # получаем номер локации из состояния
    data = await state.get_data()
    location_number = data['location_number']

    # увеличиваем его на 1
    location_number += 1

    # записываем в состояние новый номер локации
    await state.update_data(location_number=location_number)

    # получаем информацию о локации и информацию о каждой фотографии локации
    location_info = await get_location_info_by_number(location_number)
    images_info = await get_images_location_info_by_number(location_number)

    # парсим и записываем информацию о локации в ФСМ состояние
    await state.update_data(
        location_name=location_info['location_name'],
        next_location_latitude=location_info['next_location_latitude'],
        next_location_longitude=location_info['next_location_longitude'],
        main_text=location_info['main_text'],
        detailed_description=location_info['detailed_description'],
        audio_guide_text=location_info['audio_guide_text'],
        audio_guide=location_info['audio_guide'],
        additionally=location_info['additionally'],
        additionally_button=location_info['additionally_button'],
        next_button_text=location_info['next_button_text']
    )

    # записываем в состояние список словарей с информацией о фотографиях
    await state.update_data(
        images_info=images_info
    )


    # изображения для вывода в чат
    # список с кортежами путей изображений и их описанием
    images_tuple = await parsing_images(images_info, 'Я на месте')

    # перебираем циклом инфо о изображениях, делаем из них FSInputFile-объекты и выводим в чат
    for image_tuple in images_tuple:

        # получаем полный путь к изображению
        current_path = str(pathlib.Path(__file__).resolve().parents[2])
        image_path = pathlib.Path(current_path, 'Django', *image_tuple[0].split('/'))
        image = FSInputFile(image_path)

        # получаем описание изображения
        image_description = image_tuple[1]

        try:
            await message.answer_photo(photo=image, caption=image_description)
        except:
            pass


    # текст для вывода в чат
    text = location_info['main_text']

    # проверяем последняя ли это локация
    # если последняя, то возвращаем клавиатуру без кнопки "Дальше"
    if location_number == 13:
        markup = await location_keyboard_without_next_button(location_info['additionally_button'])

    # если это 5 локация - возвращаем клавиатуру специально для нее
    elif location_number == 5:
        markup = await fifth_location_keyboard()

    # если нет - то обычную
    else:
        markup = await location_keyboard(location_info['additionally_button'])

    await message.answer(text=text, reply_markup=markup)

    # добавляем действие в БД
    await add_action(user_tg_id=message.from_user.id,
                     msg_name='Я на месте',
                     location_number=location_number)


# обработка кнопки 'Дальше'
@router.message(Text(text='Дальше'))
async def next_location_handler(message: Message, state: FSMContext):

    # получаем данные из состояния
    data = await state.get_data()

    # текст выводимый при нажатии на кнопку
    text = data['next_button_text']

    # широта и долгода следующей локации
    next_location_latitude = data['next_location_latitude']
    next_location_longitude = data['next_location_longitude']

    # получам клавиатуру
    markup = await walk_keyboard()

    await message.answer(text=text, reply_markup=markup)
    await message.answer_location(latitude=next_location_latitude, longitude=next_location_longitude)