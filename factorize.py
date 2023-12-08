
from multiprocessing import Process, Value, RLock, current_process, cpu_count
from time import  time
import logging
import sys


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

# print(cpu_count())

def factorize(*number):
    result = []
    logger.debug(f'Started {current_process().name}')
    for number in number:
        lst = []
        for i in range(1, number+1):
            if not number % i:
                lst.append(i)
        result.append(lst)
    logger.debug(f'Done {current_process().name}')
    return result


def factorize_multi(number, val:Value):
    result = 0
    logger.debug(f'Started {current_process().name}')
    for i in range(1, number+1):
        if not number % i:
            result += 1
    with val.get_lock():
        val.value += result
    logger.debug(f'Done {current_process().name}')
    sys.exit(0)

if __name__ == '__main__':

    start = time()
    lock = RLock()
    value = Value('d', 0, lock=lock)
    pr1 = Process(target=factorize_multi, args=(99999999, value))
    pr1.start()
    pr2 = Process(target=factorize_multi, args=(99999999, value))
    pr2.start()
    pr3 = Process(target=factorize_multi, args=(99999999, value))
    pr3.start()
    pr4 = Process(target=factorize_multi, args=(99999999, value))
    pr4.start()

    pr1.join()
    pr2.join()
    pr3.join()
    pr4.join()

    print(f"values =  {value.value} ")  # 4.0

    print(f"{time()- start} 4 core time")  # 0.550


    start = time()
    a, b, c, d = factorize(99999999, 99999999, 99999999, 99999999, )
    print(f"{time()- start} one core time") # 0.550

