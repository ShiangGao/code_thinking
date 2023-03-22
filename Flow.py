import heapq
import math
import time

# 设置全局变量，程序开始时间
start_time = time.time()


# 流的类实现：其中包含名字、优先级、周期以及时隙几个特征，另一个函数用对绝对优先级进行比较。
# 假定条件：所有的流均有其固定的优先级并按照固定的周期进行传输，不存在非周期性的时间触发流
# 该算法是通过两个方面进行判定流的优先序列，分别是优先级以及截止时间,理论上来说优先级越大，截止时间越短的触发流F_pri越大,参数x,y
class Flow:


    def __init__(self, name, priority, period, interval):
        self.name = name
        self.priority = priority
        self.period = period
        self.interval = interval  # 流的传输时间，即时隙
        self.now_time = time.time()  # 现在的时间
        self.next_trigger = math.ceil(self.now_time / self.period) * self.period  # 通过这种方式来确定流这一次的截止时间
        self.deadline = (self.now_time - start_time) % self.period

        self.F_pri = priority + self.deadline

    def __lt__(self, other):
        return self.F_pri < other.F_pri

    # def run(self):
    #     print(f"Task with period {self.period} and execution time {self.interval} is running...")
    #     time.sleep(self.interval)  # 在有任务处于执行时，run函数休眠，处于等待状态

# # 静态优先级调度器类
# class StaPriScheduler:
#
#     # 初始化流的队列
#     def __init__(self, name, priority, period, interval):
#         super().__init__(name, priority, period, interval)
#         self.streams = []
#
#     # 添加流实例到堆中
#     def add_stream(self, name, priority, period, tran_time):
#         stream = Flow(name, priority, period, tran_time)
#         heapq.heappush(self.streams, (self.F_pri, stream))  # 以F_pri作为判断值，判断流是否应该位于堆根部
#
#     # 删除流实例
#     def remove_stream(self, name):
#         for stream in self.streams:
#             if stream.name == name:
#                 self.streams.remove(stream)
#                 heapq.heapify(self.streams)
#                 break
#
#     def get_next_stream(self):
#         while self.streams:
#             stream = heapq.heappop(self.streams)
#         return None
#
#     # 运行流(?)
#     def run(self, duration):
#         end_time = start_time + duration
#         while time.monotonic() < end_time:
#             stream = self.get_next_stream()
#             if stream is not None:
#                 print("Run stream: {} at {}".format(stream.name, time.monotonic()))
#                 if time.monotonic() > stream.deadline:
#                     print("Deadline missed for stream: {}".format(stream.name))
#             else:
#                 time.sleep(0.001)

# 1.创建任务列表，包含需要调度的任务和它们的执行时间。
# 2.根据任务的执行时间，使用RM算法为每个任务分配一个固定的优先级，其中执行时间越短的任务优先级越高。
# 3.将任务放入调度队列中，按照其优先级进行排序。
# 4.创建一个网络拓扑，确定任务之间的依赖关系。
# 5.基于任务依赖关系，生成门控列表，以确保任务按照正确的顺序执行。
# 6.根据门控列表和调度队列，生成时隙调度表，确定任务在每个时隙中的执行时间和顺序。
# 7.将时隙调度表发送给任务执行器，以确保任务按照正确的顺序和时间执行。
# 8.可以通过可视化工具显示网络拓扑和时隙调度表。
