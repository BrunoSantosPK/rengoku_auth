from typing import Callable
from auth.utils.response import Response


class Pipeline:

    @staticmethod
    def run(*args: Callable[[], Response]):
        for func in args:
            res = func()
            if res.get_status() != 200:
                break

        return res.get_json()
