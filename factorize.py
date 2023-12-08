
from multiprocessing import Process, Value, Manager,  RLock, current_process, cpu_count
from time import  time
import logging
import sys


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

print(cpu_count())


def factorize_mlt(number,  val: Manager):
    logger.debug(f'Started {current_process().name}')
    lst = {}
    lst[number] = []
    for i in range(1, number+1):
        if not number % i:
            lst[number].append(i)
    val[number] = lst.values()
    logger.debug(f'Done {current_process().name}')


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


if __name__ == '__main__':

    lst = [128, 255, 99999, 99651061, 99651060]


    start = time()
    a, b, c, d, e = factorize(*lst)
    print(f"{time()- start} one core time") # 0.550


    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]



    start = time()
    with Manager() as manager:
        m = manager.dict()
        processes = []
        for i in lst:
            pr = Process(target=factorize_mlt, args=(i, m))
            pr.start()
            processes.append(pr)

        [pr.join() for pr in processes]

        a = m[128]
        b = m[255]
        c = m[99999]
        # d = m[10651060]

        print(f"{time()- start} 4 core time")  

        assert a[0] == [1, 2, 4, 8, 16, 32, 64, 128]
        assert b[0] == [1, 3, 5, 15, 17, 51, 85, 255]
        assert c[0] == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
        # assert d[0] == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
        #             380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
