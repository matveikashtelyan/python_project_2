
import random
import src.encryptor.globals as G


class EncryptApp:
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

    def set_unsafe_settings(self):
        self.alph_len = G.UNSAFE_ALPH_LEN
        self.alph_bot_edge = G.UNSAFE_ALPH_BOT_EDGE
        self.alph_top_edge = G.UNSAFE_ALPH_TOP_EDGE
        self.safe_shift = G.UNSAFE_SHIFT

    def call_decrypt(self, args):
        if args[0] == 'dcs':
            self.shift = int(args[2])
            self.caesar_decrypt()
        elif args[0] == 'dcu':
            self.set_unsafe_settings()
            self.shift = int(args[2])
            self.caesar_decrypt()
        if args[0] == 'dvigs':
            self.secret_word = args[2]
            self.vigenere_decrypt()
        if args[0] == 'dvigu':
            self.set_unsafe_settings()
            self.secret_word = args[2]
            self.vigenere_decrypt()
        if args[0] == 'dvers':
            if len(args) > 3:
                self.key_file_name = args[2]
            self.vernam_decrypt()
        if args[0] == 'dveru':
            self.set_unsafe_settings()
            if len(args) > 3:
                self.key_file_name = args[2]
            self.vernam_decrypt()

    def call_encrypt(self, args):
        if args[0] == 'ecs':
            self.shift = int(args[2])
            self.caesar_encrypt()
        elif args[0] == 'ecu':
            self.set_unsafe_settings()
            self.shift = int(args[2])
            self.caesar_encrypt()
        elif args[0] == 'evigs':
            self.secret_word = args[2]
            self.vigenere_encrypt()
        elif args[0] == 'evigu':
            self.set_unsafe_settings()
            self.secret_word = args[2]
            self.vigenere_encrypt()
        elif args[0] == 'evers':
            if len(args) > 3:
                self.key_file_name = args[2]
            self.vernam_encrypt()
        elif args[0] == 'everu':
            self.set_unsafe_settings()
            if len(args) > 3:
                self.key_file_name = args[2]
            self.vernam_encrypt()

    def process_input(self, args):
        self.file_name = args[1]
        if args[0][0] == 'e':
            self.call_encrypt(args)
        elif args[0][0] == 'd':
            self.call_decrypt(args)
        elif args[0] == 'fc':
            self.freq_caesar_analyser()

    def caesar_encrypt(self):
        self.shift %= self.alph_len
        with open(self.file_name, 'r') as file:
            data = list(file.read())
            for idx in range(len(data)):
                if (self.alph_bot_edge <= ord(data[idx])
                        <= self.alph_top_edge):
                    data[idx] = chr((ord(data[idx]) - self.safe_shift
                                     + self.shift) % self.alph_len
                                    + self.safe_shift)
        with open(self.file_name, 'w') as file:
            file.write("".join(data))

    def caesar_decrypt(self):
        self.shift %= self.alph_len
        with open(self.file_name, 'r') as file:
            data = list(file.read())
            for idx in range(len(data)):
                if (self.alph_bot_edge <= ord(data[idx])
                        <= self.alph_top_edge):
                    data[idx] = chr((ord(data[idx]) - self.safe_shift
                                     - self.shift) % self.alph_len
                                    + self.safe_shift)
        with open(self.file_name, 'w') as file:
            file.write("".join(data))

    def vigenere_encrypt(self):
        with open(self.file_name, 'r') as file:
            data = list(file.read())
            sw_idx = 0
            for idx in range(len(data)):
                fst_cond = (self.alph_bot_edge <= ord(data[idx])
                            <= self.alph_top_edge)
                scd_cond = (self.alph_bot_edge
                            <= ord(self.secret_word[sw_idx])
                            <= self.alph_top_edge)
                if fst_cond and scd_cond:
                    data[idx] = chr((ord(data[idx]) - self.safe_shift
                                     + ord(self.secret_word[sw_idx])
                                     - self.safe_shift) % self.alph_len
                                    + self.safe_shift)
                sw_idx += 1
                sw_idx %= len(self.secret_word)
        with open(self.file_name, 'w') as file:
            file.write("".join(data))

    def vigenere_decrypt(self):
        with open(self.file_name, 'r') as file:
            data = list(file.read())
            sw_idx = 0
            for idx in range(len(data)):
                fst_cond = (self.alph_bot_edge <= ord(data[idx])
                            <= self.alph_top_edge)
                scd_cond = (self.alph_bot_edge <= ord(self.secret_word[sw_idx])
                            <= self.alph_top_edge)
                if fst_cond and scd_cond:
                    data[idx] = chr((ord(data[idx]) - self.safe_shift -
                                     (ord(self.secret_word[sw_idx])
                                      - self.safe_shift)) % self.alph_len
                                    + self.safe_shift)
                sw_idx += 1
                sw_idx %= len(self.secret_word)
        with open(self.file_name, 'w') as file:
            file.write("".join(data))

    def vernam_encrypt(self):
        with open(self.file_name, 'r') as file:
            data = list(file.read())
            key = [chr(random.randrange(self.alph_bot_edge,
                                        self.alph_top_edge, 1))
                   for idx in range(len(data))]
            for idx in range(len(data)):
                xor_res = (((ord(data[idx]) - self.safe_shift) + (ord(key[idx])
                            - self.safe_shift)) % self.alph_len
                          + self.safe_shift)
                fst_cond = (self.alph_bot_edge <= ord(data[idx])
                            <= self.alph_top_edge)
                scd_cond = (self.alph_bot_edge <= xor_res
                            <= self.alph_top_edge)
                if fst_cond and scd_cond:
                    data[idx] = chr(xor_res)
                else:
                    key[idx] = '\n'
        with open(self.file_name, 'w') as file:
            file.write("".join(data))
        with open(self.key_file_name, 'w') as key_file:
            key_file.write("".join(key))

    def vernam_decrypt(self):
        with open(self.key_file_name, 'r') as key_file:
            key = list(key_file.read())
        with open(self.file_name, 'r') as file:
            data = list(file.read())
            for idx in range(len(data)):
                fst_cond = (self.alph_bot_edge <= ord(data[idx])
                            <= self.alph_top_edge)
                scd_cond = (self.alph_bot_edge <= ord(key[idx])
                            <= self.alph_top_edge)
                if fst_cond and scd_cond:
                    xor_modm_res = (((ord(data[idx]) - self.safe_shift)
                                    - (ord(key[idx]) - self.safe_shift))
                                   % self.alph_len + self.safe_shift)
                    data[idx] = chr(xor_modm_res)
        with open(self.file_name, 'w') as file:
            file.write("".join(data))

    @staticmethod
    def get_chars_freq(data):
        freq_dict = {}
        for char in data:
            freq_dict[char] = data.count(char) / len(data)
        sorted_values = sorted(freq_dict.values(), reverse=True)
        sorted_freq_dict = {}
        for value in sorted_values:
            for key in freq_dict.keys():
                if freq_dict[key] == value:
                    sorted_freq_dict[key] = value
        return sorted_freq_dict

    def freq_caesar_analyser(self):
        with open(self.file_name, 'r') as file:
            data = list(file.read())
            freq_dict = EncryptApp.get_chars_freq(data)
            for char in freq_dict.keys():
                first_char = char
                break
            self.shift = (((ord(first_char) - self.safe_shift) - (ord(' ')
                                - self.safe_shift)) % self.alph_len)
            self.caesar_decrypt()

