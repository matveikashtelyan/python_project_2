
import logging
import os
import src.tgbot.globals as TBG
import src.tgbot.types as T
import src.tgbot.variables as V


class Dialogue(T.StatesGroup):
    begin = T.State()
    regime = T.State()  # encrypt/decrypt/frequency
    file = T.State()  # get file to process
    su_mode = T.State()  # safe/unsafe
    method = T.State()  # c/vig/ver
    shift = T.State()  # get shift for caesar
    sec_word = T.State()  # get sec_word for vigenere
    key_file = T.State()  # get file with key for vernam


@V.router.message(T.Command("start"))
async def process_start_command(message: T.Message, state: T.FSMContext):
    await message.answer(TBG.START_MESSAGE)
    await state.set_state(Dialogue.begin)


@V.router.message(T.Command("help"))
async def process_start_command(message: T.Message):
    await message.answer(TBG.HELP_MESSAGE)


@V.router.message(Dialogue.begin, T.Command("begin"))
async def command_encrypt(message: T.Message, state: T.FSMContext):
    await state.set_state(Dialogue.regime)
    await message.answer(TBG.REGIME_CHOICE)


@V.router.message(Dialogue.regime, T.F.text.in_(TBG.WORK_REGIMES))
async def regime_choice_handler(message: T.Message, state: T.FSMContext):
    V.args.append(message.text)
    await state.set_state(Dialogue.file)
    await message.answer(TBG.FILE_CHOICE)


@V.router.message(Dialogue.file, T.F.document)
async def save_file_handler(message: T.Message, state: T.FSMContext):
    file = message.document
    await V.bot.download(file, TBG.DEFAULT_FILE_NAME)
    V.args.append(TBG.DEFAULT_FILE_NAME)
    if V.args[0] == 'f':
        V.args[0] = V.args[0] + 'c'
        await process_args(message.chat.id, V.args, state)
    else:
        await state.set_state(Dialogue.su_mode)
        await message.answer(TBG.SU_MODE_CHOICE)


@V.router.message(Dialogue.key_file, T.F.document)
async def save_file_handler(message: T.Message, state: T.FSMContext):
    file = message.document
    await V.bot.download(file, TBG.DEFAULT_KEY_FILE_NAME)
    V.args.append(TBG.DEFAULT_KEY_FILE_NAME)
    await process_args(message.chat.id, V.args, state)


@V.router.message(Dialogue.su_mode, T.F.text.in_(TBG.SU_MODES))
async def su_mode_handler(message: T.Message, state: T.FSMContext):
    if message.text == 'safe':
        V.args[0] = V.args[0] + 's'
    elif message.text == 'unsafe':
        V.args[0] = V.args[0] + 'u'
        V.encryptor.set_unsafe_settings()
    await state.set_state(Dialogue.method)
    await message.answer(TBG.METHOD_CHOICE)


@V.router.message(Dialogue.method, T.F.text.in_(TBG.METHODS))
async def method_choice_handler(message: T.Message, state: T.FSMContext):
    V.args[0] = V.args[0][0] + message.text + V.args[0][1]
    if message.text == 'c':
        await state.set_state(Dialogue.shift)
        await message.answer(TBG.SHIFT_CHOICE)
    elif message.text == 'vig':
        await state.set_state(Dialogue.sec_word)
        await message.answer(TBG.SEC_WORD_CHOICE)
    elif message.text == 'ver':
        if V.args[0][0] == 'e':
            await process_args(message.chat.id, V.args, state)
        else:
            await state.set_state(Dialogue.key_file)
            await message.answer(TBG.KEY_FILE_CHOICE)


@V.router.message(Dialogue.shift)
async def shift_handler(message: T.Message, state: T.FSMContext):
    V.args.append(int(message.text))
    await process_args(message.chat.id, V.args, state)


@V.router.message(Dialogue.sec_word)
async def sec_word_handler(message: T.Message, state: T.FSMContext):
    V.args.append(message.text)
    await process_args(message.chat.id, V.args, state)


@V.router.message(T.Command("cancel"))
async def cancel_handler(message: T.Message, state: T.FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info("Cancelling state %r", current_state)
    await state.set_state(Dialogue.begin)
    await message.answer(TBG.CANCEL_MESSAGE)


@V.router.message()
async def echo_message(message: T.Message):
    await V.bot.send_message(message.from_user.id, TBG.WRONG_INPUT)


async def process_args(chat_id, args_list, state: T.FSMContext):
    V.encryptor.process_input(args_list)
    res_file = T.FSInputFile(TBG.DEFAULT_FILE_NAME, "res_file.txt")
    await V.bot.send_message(chat_id, "Обработанный файл:")
    await V.bot.send_document(chat_id, res_file)
    os.remove(TBG.DEFAULT_FILE_NAME)
    if args_list[0][1:-1] == "ver":
        if args_list[0][0] == 'e':
            key_file = T.FSInputFile(TBG.DEFAULT_KEY_FILE_NAME, "key_file.txt")
            await V.bot.send_message(chat_id, "Файл, содержащий ключ:")
            await V.bot.send_document(chat_id, key_file)
        os.remove(TBG.DEFAULT_KEY_FILE_NAME)
    V.args.clear()
    await state.set_state(Dialogue.begin)
    await V.bot.send_message(chat_id, TBG.END_MESSAGE)

