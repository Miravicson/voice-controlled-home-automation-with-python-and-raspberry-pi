from random import random
from multiprocessing import Process
from sys import exit
from time import sleep

def add_something(i):

    # Sleep to simulate the long calculation
    sleep(random() * 30)

    exitcode = i + 1
    print(exitcode)
    exit(exitcode)

def run_my_process():

    # Start up all of the processes
    processes = []
    for i in range(100):
        proc = Process(target=add_something, args=[i])
        processes.append(proc)
        proc.start()

    # Wait for the desired process result
    done = False
    while not done:
        for proc in processes:
            if proc.exitcode == 90:
                done = True
                break

    # Kill any processes that are still running
    for proc in processes:
        if proc.is_alive():
            proc.terminate()

if __name__ == '__main__':
    run_my_process()
