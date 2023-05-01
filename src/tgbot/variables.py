
import dotenv
import logging
import os
import src.encryptor.encryptapp
import src.tgbot.types as types


dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = types.Bot(os.environ.get("TOKEN"))
dispatcher = types.Dispatcher()
router = types.Router()
dispatcher.include_router(router)
encryptor = src.encryptor.encryptapp.EncryptApp()
args = []

