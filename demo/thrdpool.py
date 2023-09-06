import time
from concurrent.futures import ThreadPoolExecutor

def worker(number):
    print(f"Calculating the number {number}")
    time.sleep(2)
    print(number ** 2)

if __name__ == "__main__":
    pool = ThreadPoolExecutor(3)
    work1 = pool.submit(worker, 7)
    work2 = pool.submit(worker, 3)
    work3 = pool.submit(worker, 4)
    work4 = pool.submit(worker, 6)
    work5 = pool.submit(worker, 8)
    work6 = pool.submit(worker, 9)
    work7 = pool.submit(worker, 11)
    work8 = pool.submit(worker, 12)