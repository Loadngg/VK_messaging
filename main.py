import os
import time

import vk_api
from dotenv import load_dotenv
from vk_api.utils import get_random_id

from users_list import users_list

load_dotenv()


def measure_time(func):
    def wrapper(message):
        start_time = time.time()
        func(message)
        print(f"Рассылка выполнена за {time.time() - start_time:.2f}c")

    return wrapper


def captcha_handler(captcha):
    key = input(f"Enter captcha code {captcha.get_url()}: ").strip()

    return captcha.try_again(key)


@measure_time
def main(message):
    token = os.environ.get("TOKEN")

    try:
        vk = vk_api.VkApi(token=token, captcha_handler=captcha_handler).get_api()
        print("Вошли")

        ids = []
        users = vk.users.get(user_ids=users_list)

        for user in users:
            ids.append(user["id"])

        for user_id in ids:
            vk.messages.send(
                user_id=user_id, message=message, random_id=get_random_id()
            )

    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    except vk_api.exceptions.ApiError as error_msg:
        print(error_msg)
        return


if __name__ == "__main__":
    MESSAGE = os.environ.get("MESSAGE")
    main(MESSAGE)
