from dataclasses import dataclass

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

log_folder = 'data/log/'


# Qiwi
@dataclass
class Qiwi:
    token = env.str('qiwi')
    wallet = env.str('wallet')
    public_key = env.str('qiwi_p_pub')
    themeCode = 'Tymofei-KHIlIeciDt'