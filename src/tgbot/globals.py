
CANCEL_MESSAGE = "Операция отменена. Для совершения операции введите /begin."
DEFAULT_FILE_NAME = "file.txt"
DEFAULT_KEY_FILE_NAME = "key.txt"
END_MESSAGE = "Операция завершена. Для совершения новой операции введите " \
              "/begin."
FILE_CHOICE = "Пожалуйста, отправьте файл, который хотите обработать:"
HELP_MESSAGE = "Добро пожаловать в EncryptionBot.\n" \
               "Этот бот может зашифровать/расшифровать Ваши текстовые ascii " \
               "файлы, используя шифры Цезаря, Виженера и Вернама.\n" \
               "Бот может работать в двух режимах: безопасном и небезопасном " \
               "в смысле искажения данных.\n\n" \
               "Для начала работы введите /begin.\n" \
               "Для того, чтобы начать сначала, введите /cancel.\n\n" \
               "Обращаем Ваше внимание, что файлы, зашифрованные безопасным/" \
               "небезопасным методом, могут быть расшифрованы только " \
               "соотвественно безопасным/небезопасным методом."
KEY_FILE_CHOICE = "Пожалуйста, отправьте файл, содержащий ключ:"
METHOD_CHOICE = "Пожалуйста, выберите метод шифрования:\n" \
                "' c ' - шифр Цезаря,\n" \
                "' vig ' - шифр Виженера,\n" \
                "' ver ' - шифр Вернама."
REGIME_CHOICE = "Пожалуйста, выберите желаемый режим:\n" \
                "' e ' - шифрование,\n" \
                "' d ' - дешифрование,\n" \
                "' f ' - расшифровка файла, зашифрованного безопасным " \
                "шифром Цезаря, с помощью частотного анализа."
SEC_WORD_CHOICE = "Пожалуйста, введите секретное слово:"
SHIFT_CHOICE = "Пожалуйста, введите сдвиг:"
START_MESSAGE = "EncryptionBot.\nВведите /help для получения подробной " \
                "информации.\n"
SU_MODE_CHOICE = "Пожалуйста, выберите режим в смысле искажения данных:\n" \
                 "' safe ' - безопасный режим,\n" \
                 "' unsafe ' - небезопасный режим."
WRONG_INPUT = "Введённые данные некорректны. Пожалуйста, повторите попытку."

METHODS = {'c', 'vig', 'ver'}
SU_MODES = {'safe', 'unsafe'}
WORK_REGIMES = {'e', 'd', 'f'}
