"""ДЗ Декораторы."""
import json
import jsonschema
import re
from typing import Callable, Any

with open("test.json", "r", -1, encoding="utf-8") as f:
    data = json.load(f)

with open("goods.schema.json", "r", -1, encoding="utf-8") as file:
    schema = json.load(file)

str_valid = ""


class InputParameterVerificationError(Exception):
    """Исключение входных параметров."""

    def __init__(self, text: str) -> None:
        """Исключение."""
        self.txt = text


class ResultVerificationError(Exception):
    """Исключение результатов верификации."""

    def __init__(self, text: str) -> None:
        """Исключение."""
        self.txt = text


class VerificationError(Exception):
    """Исключение количества повторений."""

    def __init__(self, text: str) -> None:
        """Исключение."""
        self.txt = text


def input_validation(data: dict, schema: dict) -> bool:
    """Валидация JSON."""
    try:
        jsonschema.validate(data, schema)
        print("Попытка валидации JSON-файла")
    except Exception:
        print("Ошибка валидации JSON-файла")
        exit()
    return True


def result_validation(str_valid: str) -> str:
    """Функция с регуляркой."""
    result = str(re.match(r"Success", str(str_valid)))
    return result


def default_behavior() -> None:
    """Функция, если ничего не работает."""
    print("Попробуйте загрузить другой файл")


def my_decorator(
    input_validation: Callable,
    result_validation: Callable,
    default_behavior: Callable,
    on_fail_repeat_times: int,
) -> Callable:
    """Декоратор."""
    def decoration(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if input_validation(*args, **kwargs) is False:
                raise InputParameterVerificationError(
                    "Ошибка в валидации входных данных!"
                )
            else:
                result = func(*args, **kwargs)
                if result_validation(func(*args, *kwargs)) is None:
                    if default_behavior is None:
                        raise ResultVerificationError(
                            "Не указан параметр default_behavior!"
                        )
                    else:
                        if on_fail_repeat_times == 0:
                            raise VerificationError(
                                "on_fail_repeat_times не может быть равен 0!"
                            )
                        if on_fail_repeat_times < 0:
                            while result_validation(func(*args, *kwargs)) is None:
                                result = func(*args, **kwargs)
                        else:
                            for i in range(on_fail_repeat_times):
                                result = func(*args, **kwargs)
                                default_behavior()
            return result

        return wrapper

    return decoration


@my_decorator(input_validation, result_validation, default_behavior, 1)
def func(data: dict, schema: dict) -> str:
    """Исходная функция."""
    if data is None and schema is None:
        str_valid = "Fail! Ошибка в чтении файла"
    else:
        str_valid = "Success! Файлы успешно прочитаны"
    print(str_valid)
    return str_valid


func(data, schema)
