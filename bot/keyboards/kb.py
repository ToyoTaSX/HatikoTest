from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_kb(arr, cb_extractor=lambda x: x, text_extractor=lambda x: x):
    builder = InlineKeyboardBuilder()

    for obj in arr:
        builder.button(text=text_extractor(obj), callback_data=cb_extractor(obj))

    builder.adjust(1,repeat=True)
    return builder.as_markup()