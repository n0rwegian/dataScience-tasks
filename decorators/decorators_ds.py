import requests
import time
import re
from functools import wraps

BOOK_PATH = 'https://www.gutenberg.org/files/2638/2638-0.txt'


def benchmark(func):
    """
    Декоратор, выводящий время, которое заняло выполнение декорируемой функции
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'Время выполнения функции {func.__name__}: {time.perf_counter() - start}')
        return result
    return wrapper


def logging(func):
    """
    Декоратор, который выводит параметры с которыми была вызвана функция
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'Функция вызвана с параметрами: {args}, {kwargs}')
        return result
    return wrapper


def counter(func, cnt={}):
    """
    Декоратор, считающий и выводящий количество вызовов декорируемой функции
    """
    cnt[func] = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        cnt[func] += 1
        result = func(*args, **kwargs)
        print(f'Функция была вызвана: {cnt[func]} раз')
        return result
    return wrapper


@counter
@logging
@benchmark
def another_func():
    return ("Another func")


@counter
@logging
@benchmark
def word_count(word, url=BOOK_PATH):
    """
    Функция для подсчета указанного слова на html-странице
    """

    # отправляем запрос в библиотеку Gutenberg и забираем текст
    raw = requests.get(url).text

    # заменяем в тексте все небуквенные символы на пробелы
    processed_book = re.sub(r'[\W]+', ' ', raw).lower()

    # считаем
    cnt = len(re.findall(word.lower(), processed_book))

    return f"Cлово {word} встречается {cnt} раз"


def memo(func):
    """
    Декоратор, запоминающий результаты исполнения функции func, чьи аргументы args должны быть хешируемыми
    """
    cache = {}
    def fmemo(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    fmemo.cache = cache
    return fmemo



def fib(n):
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)



@memo
def fib1(n):
    if n < 2:
        return n
    return fib1(n - 2) + fib1(n - 1)

print('Tasks 1-3:')
print(word_count('whole'))
print()
print(another_func())
print()
print(word_count('a'))
print()

print('Task 4:')
t0 = time.perf_counter()
print(f'Результат вычисления 35го члена последовательности Фибоначчи: {fib(35)}')
t1 = time.perf_counter()
print(f'Время выполнения функции fib без мемоизации (+print) = {t1 - t0}')

t3 = time.perf_counter()
print(f'Результат вычисления 35го члена последовательности Фибоначчи: {fib1(35)}')
t4 = time.perf_counter()
print(f'Время выполнения функции fib c мемоизацией (+print) = {t4 - t3}')

print(f'Вычисление 35го члена последовательности Фибоначчи с мемоизацией быстрее в {(t1 - t0) / (t4 - t3)} раз')
