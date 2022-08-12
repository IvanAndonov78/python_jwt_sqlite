import random
import string
from src.core_module import core


class CsrfTokenService:
    def __init__(self):
        pass

    # @staticmethod
    # def generate_csrf_token():
    #     first = string.ascii_letters
    #     letters = ''.join(random.choice(first) for i in range(10))
    #
    #     second = string.digits
    #     digits = ''.join(random.choice(second) for i in range(10))
    #
    #     list_sp_symbols = ['^', '!', '~']
    #     sp_symbols = ''.join(list_sp_symbols)
    #
    #     pre_token = letters + str(digits) + str(sp_symbols)
    #     token = ''.join(random.sample(pre_token, len(pre_token)))
    #
    #     return token

    @staticmethod
    def generate_csrf_token():
        data = core.get_json_file('src/conf/csrf_tokens.json')
        csrf_tokens = data["csrf_tokens"]
        min = 0
        max = len(csrf_tokens) - 1
        rand_index = random.randint(min, max)
        return csrf_tokens[rand_index]

    @staticmethod
    def check_csrf_token(csrf_token):
        data = core.get_json_file('src/conf/csrf_tokens.json')
        csrf_tokens = data['csrf_tokens']
        # if csrf_token in csrf_tokens:
        #     return True
        # return False

        # better solution:
        return True if csrf_token in csrf_tokens else False





