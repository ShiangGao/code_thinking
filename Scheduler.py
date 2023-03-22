# 静态优先级调度器类
import heapq
import time

from Flow import Flow, start_time


class StaPriScheduler(Flow):

    # 初始化流的队列
    def __init__(self):
        super().__init__(Flow.name, priority, period, interval)
        # 初始化任务队列
        # self.F_pri = None
        self.streams = []

    # 添加流实例到堆中
    def add_stream(self, name, priority, period, tran_time):
        stream = Flow(name, priority, period, tran_time)
        heapq.heappush(self.streams, stream)  # 以F_pri作为判断值，判断流是否应该位于堆根部

    # 删除流实例
    def remove_stream(self, name):
        for stream in self.streams:
            if stream.name == name:
                self.streams.remove(stream)
                heapq.heapify(self.streams)
                break

    def get_next_stream(self):
        while self.streams:
            stream = heapq.heappop(self.streams)
            return stream
        return None

    # 运行流(?)
    def run(self, duration):
        end_time = start_time + duration
        while time.time() < end_time:
            stream = self.get_next_stream()
            if stream is not None:
                print("Run stream: {} at {}".format(stream.name, time.monotonic()))
                if time.time() > stream.deadline:
                    print("Deadline missed for stream: {}".format(stream.name))
            else:
                # print(2)
                time.sleep(0.1)

