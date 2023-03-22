# This is a sample Python script.
import heapq
from heapq import heappush, heappop
import time
import Flow
import Scheduler

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(1)
    scheduler = Scheduler.StaPriScheduler()
    # 格式：流的名字，优先级，周期，时隙
    scheduler.add_stream("Stream1", 1, 4, 1)
        # print("success")
    scheduler.add_stream("Stream2", 2, 4, 2)
    scheduler.add_stream("stream3", 3, 10, 1)

    scheduler.run(20)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
