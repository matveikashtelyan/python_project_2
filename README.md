# Проект 2, Телеграм Бот

Телеграм бот, который может шифровать/дешифровать файлы клиента шифрами Цезаря, Виженера и Вернама. Также дешифрует зашифрованные шифром Цезаря файлы методом частотного анализа.

```
$ git clone git@github.com:matveikashtelyan/python_project_2.git
```
Для запуска бота необходимо установить следующие модули:
```
pip install -U --pre aiogram
pip install python-dotenv
```
Склонировать репозиторий. Сама директория называется `python_project_2`. Зайти в эту директорию. Там находятся файлы `README.md`, `main.py`, `input.txt` и директория `src`, в которой лежат директории `tgbot` и `encryptor`. В директории `tgbot` лежат файлы `bot.py`, `types.py`, `variables.py`, `globals.py`. В директории `encryptor` лежат файлы `encryptapp.py` и `globals.py`.

## Запуск
```
$ python3 main.py
```

## Описание кода бота:

Весь код бота расположен в директории `src/tgbot/`

### src/tgbot/bot.py

В этом файле описаны обработчики событий.

```
class Dialogue(T.StatesGroup)
```
В этом файле описаны состояния для `FSM` - механизма `aiogram`, позволяющего вести последовательный диалог бота с клиентом.
```
begin - стартовое состояние, диалог ещё не начался. Именно в нём находится `FSM` после команды `/start`.
regime - выбор режима работы: шифрование, дишифрование, частотный анализатор.
file - выбор файла для обработки.
su_mode - выбор безопасного/небезопасного режима в смысле обработки данных.
method - выбор метода: Цезаря, Виженера, Вернама.
shift - ввод сдвига для шифра Цезаря.
sec_word - ввод секретного слова для шифра Виженера.
key_file - выбор файла с ключом для шифра Вернама (при расшифровке).
```
Список функций:
```
@V.router.message(T.Command("start"))
async def process_start_command(message: T.Message, state: T.FSMContext)

@V.router.message(T.Command("help"))
async def process_start_command(message: T.Message)

@V.router.message(Dialogue.begin, T.Command("begin"))
async def command_encrypt(message: T.Message, state: T.FSMContext)

@V.router.message(Dialogue.regime, T.F.text.in_(TBG.WORK_REGIMES))
async def regime_choice_handler(message: T.Message, state: T.FSMContext)

@V.router.message(Dialogue.file, T.F.document)
async def save_file_handler(message: T.Message, state: T.FSMContext)

@V.router.message(Dialogue.key_file, T.F.document)
async def save_file_handler(message: T.Message, state: T.FSMContext)

@V.router.message(Dialogue.su_mode, T.F.text.in_(TBG.SU_MODES))
async def su_mode_handler(message: T.Message, state: T.FSMContext)

@V.router.message(Dialogue.method, T.F.text.in_(TBG.METHODS))
async def method_choice_handler(message: T.Message, state: T.FSMContext)

@V.router.message(Dialogue.shift)
async def shift_handler(message: T.Message, state: T.FSMContext)

@V.router.message(Dialogue.sec_word)
async def sec_word_handler(message: T.Message, state: T.FSMContext)

@V.router.message(T.Command("cancel"))
async def cancel_handler(message: T.Message, state: T.FSMContext)

@V.router.message()
async def echo_message(message: T.Message)

async def process_args(chat_id, args_list, state: T.FSMContext)
```
Описание функций:
```
@V.router.message(T.Command("start"))
async def process_start_command(message: T.Message, state: T.FSMContext)
```
Обработка команды `/start`. Выводит приветственное сообщение.
```
@V.router.message(T.Command("start"))
async def process_start_command(message: T.Message, state: T.FSMContext)
```
Обработка команды `/help`. Выводит информацию о боте и краткие инструкции.
```
@V.router.message(Dialogue.begin, T.Command("begin"))
async def command_encrypt(message: T.Message, state: T.FSMContext)
```
Обработка команды `/begin`. С этой команды начинается непосредственно диалог бота с клиентом о шифровании. Переводит `FSM` в состояние `regime`.
```
@V.router.message(Dialogue.regime, T.F.text.in_(TBG.WORK_REGIMES))
async def regime_choice_handler(message: T.Message, state: T.FSMContext)
```
Обработка ввода пользователем режима работы. Переводит `FSM` в состояние `file`.
```
@V.router.message(Dialogue.file, T.F.document)
async def save_file_handler(message: T.Message, state: T.FSMContext)
```
Принятие файла для обработки от пользователя. Переводит `FSM` в состояние `su_mode`, но если пользователем на предыдущем шаге был выбран частотный анализ, то вызывает функцию `process_args` для вызова частотного анализатора (см. далее).
```
@V.router.message(Dialogue.key_file, T.F.document)
async def save_file_handler(message: T.Message, state: T.FSMContext)
```
Принятие файла с ключом для шифра Вернама от пользователя. Запускает функцию `process_args`.
```
@V.router.message(Dialogue.su_mode, T.F.text.in_(TBG.SU_MODES))
async def su_mode_handler(message: T.Message, state: T.FSMContext)
```
Обработка ввода пользователем режима безопасности. Переводит `FSM` в состояние `method`.
```
@V.router.message(Dialogue.method, T.F.text.in_(TBG.METHODS))
async def method_choice_handler(message: T.Message, state: T.FSMContext)
```
Обработка ввода пользователем метода шифрования. В случае метода Цезаря запрашивает сдвиг и переводит `FSM` в состояние `shift`. В случае метода Виженера запрашивает сдвиг и переводит `FSM` в состояние `sec_word`. В случае шифрования Вернама запускает `process_args`, в случае дешифрования Вернама запрашивает файл с ключом и переводит `FSM` в состояние `key_file`.
```
@V.router.message(Dialogue.shift)
async def shift_handler(message: T.Message, state: T.FSMContext)
```
Обработка ввода пользователем сдвига для шифра Цезаря. Запускает функцию `process_args`.
```
@V.router.message(Dialogue.sec_word)
async def sec_word_handler(message: T.Message, state: T.FSMContext)
```
Обработка ввода пользователем секретного слова для шифра Виженера. Запускает функцию `process_args`.
```
@V.router.message(T.Command("cancel"))
async def cancel_handler(message: T.Message, state: T.FSMContext)
```
Обработка команды пользователя на остановку работы. Переводит `FSM` в стартовое состояние `begin`.
```
@V.router.message()
async def echo_message(message: T.Message)
```
Ловит некорректный ввод пользователя, который не был обработан функциями выше.
```
async def process_args(chat_id, args_list, state: T.FSMContext)
```
Запускает шифроватор с заданным набором аргументов. Отсылает результат пользователю, после этого удаляет файлы, которые были использованы, с машины. Выводит сообщение об окончании работы. Переводит `FSM` в стартовое состояние `begin`.

### src/tgbot/variables.py
Здесь хранятся "глобальные" переменные, необходимые для работы бота. Используются в файле `bot.py`.
### src/tgbot/types.py
Здесь хранятся некоторые типы из импортированных библиотек, использующиеся в `bot.py`.
### src/tgbot/globals.py
Здесь хранятся текстовые сообщения бота и некоторые переменные, использующиеся в функциях `bot.py`, связанные с обработкой введённого пользователем текста.

## main.py
В этом файле в функции `main` запускается бот.

## Шифратор

Весь код расположен в `src/encryptor/`.

### Класс EncryptApp

Класс описан в файле `src/encryptor/encryptapp.py`. 

Он имеет поля, отвечающие за общие для всех методов шифрования настройки, и поля, являющиеся аргументами конкретных методов.
```
# general settings, SAFE by default
file_name = ""
alph_len = G.SAFE_ALPH_LEN
alph_bot_edge = G.SAFE_ALPH_BOT_EDGE
alph_top_edge = G.SAFE_ALPH_TOP_EDGE
safe_shift = G.SAFE_SHIFT

# caesar arguments
shift = 0

# vigenere arguments
secret_word = ""

# vernam arguments
key_file_name = "key.txt"
```

При вызове небезопасного метода шифрования общие настройки будут выставлены в небезопасный режим (см. далее) с помощью метода
```
def set_unsafe_settings(self)
```

Названия методов класса, отвечающих за реализацию шифров, построены по следующему принципу:
Вначале указано название шифра, затем шифрует этот метод файл или дешифрует. Методы могут работать в двух режимах: безопасном и небезопасном в смысле искажения данных.

```
def caesar_encrypt(self)
def caesar_decrypt(self)
def vigenere_encrypt(self)
def vigenere_decrypt(self)
def vernam_encrypt(self)
def vernam_decrypt(self)
```

Значения всех полей, используемых каждым конкретным методом, выставляются на этапе запуска.

```
@staticmethod
def get_chars_freq(data)
```

Статический метод `get_chars_freq(data)` возвращает словарь, в котором ключи - это символы из `data`, а значения - частота их появления в `data`. Словарь отсортирован по значениям.

```
def freq_caesar_analyser_text(self)
```

Метод `freq_caesar_analyser_text(self)` расшифровывает файл, зашифрованный безопасным шифром Цезаря. Нужно понимать, что частотный анализ хорошо работает только для обыкновенных текстов, так как существенно опирается на статистику использования видимых ascii символов, которая составлена по корпусу обычных текстов (скорее всего, литературы). Как правило, в описанных выше текстах пробел является самым часто встречающимся символом. На это и опирается работа метода: метод считает частоты появления символов в зашифрованном файле, затем сопоставляет самый часто встречающийся из них пробелу и высчитывает сдвиг.

```
def call_decrypt(self, argv)
def call_encrypt(self, argv)
def process_input(self, argv)
```

Данные методы предназначены для обработки аргументов командной строки, выставления значений нужных полей и запуска нужного метода шифрования / дешифрования.

### src/encryptor/globals.py

В данном файле описаны константы, которые используются в `src/encryptor/encryptapp.py`



Аргументы запуска encryptapp:
```
режим_работы путь_до_файла параметр
```
```
режим_работы
```
```
ecs - безопасное шифрование Цезаря.
dcs - безопасное дешифрование Цезаря.
ecu - небезопасное шифрование Цезаря.
dcu - небезопасное дешифрование Цезаря.
evigs - безопасное шифрование Виженера.
dvigs - безопасное дешифрование Виженера.
evigu - небезопасное шифрование Виженера.
dvigu - небезопасное дешифрование Виженера.
evers - безопасное шифрование Вернама.
dvers - безопасное дешифрование Вернама.
everu - небезопасное шифрование Вернама.
dveru - небезопасное дешифрование Вернама.
fc - расшифровка файла, зашифрованного шифром Цезаря, методом частотного анализа.
```
```
путь_до_файла
```
Полный или относительный путь до файла
```
параметр
```
В случае шифра Цезаря - сдвиг, целое число. В небезопасном шифровании берется по модулю 127, т.к алфавит состоит из 127 символов. В безопасном - по модулю 95, т.к шифруемый алфавит состоит из 95 символов.

В случае шифра Виженера - кодовое слово, строка из видимых ascii символов.

В случае шифра Вернама это может быть путь до файла, в котором нужно сохранить ключ (путь должен содержать название самого файла в конце). Можно его не указывать, тогда по умолчанию создастся файл `key.txt` в директории, где расположен `main.py`.

В случае расшифровки частотным анализом не нужен.
```
Примеры аргументов
```
Безопасный шифр Цезаря:
```
$ ecs file.txt -2343     
$ dcs file.txt -2343
```
Небезопасный шифр Виженера:
```
$ evigu file.txt LEMONLEMONLE
$ dvigu file.txt LEMONLEMONLE
```
Безопасный шифр Вернама:
```
$ evers file.txt
$ dvers file.txt
```
Дешифровка шифра Цезаря частотным анализом:
```
$ fc input.txt
```

### Замечание

Файл, зашифрованный безопасным шифром, нужно расшифровывать безопасным дешифратором, и наоборот, безопасный дешифратор может расшифровать только безопасно зашифрованный файл.

## Файл input.txt

Файл, на котором тестировался бот. 

