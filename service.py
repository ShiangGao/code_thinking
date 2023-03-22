import random
from z3 import *
from Flow import *
from net_work import *
from func_timeout import func_set_timeout
from functools import reduce

TRANSMISSION_DURATION = 1


def get_lcm(L):
    def lcm(a, b):
        gcd = lambda a, b: a if b == 0 else gcd(b, a % b)
        return a * b // gcd(a, b)

    return reduce(lcm, L)


def get_TTFlows(hosts: list, TTFlow_num: int):  # 生成一个流的集合
    TTFlow_list = []  # TT流的集合
    periods = []  # 用于计算超周期
    T = [100, 200, 300]

    for i in range(TTFlow_num):
        host_src = random.choice(hosts)
        host_dst = random.choice(hosts)
        while host_dst == host_src:
            host_dst = random.choice(hosts)  # 选择开始节点和结束节点的两个节点

        period = random.choice(T)  # 随机选择一个流的周期
        if period not in periods:
            periods.append(period)
        # 流列表加入新元素
        TTFlow_list.append(  # 把生成的流加入到一个集合
            Flow(
                i,
                host_src,
                host_dst,
                500,
                period,
                period,
                random.randint(1, 2)
            ))
    hp = periods[0]
    if len(periods) > 1:
        hp = get_lcm(periods)

    return TTFlow_list, hp


def get_TT_paths(G, TT_flows: list[Flow], N: list):
    TT_paths1 = {}
    TT_paths2 = {}
    n1 = 0
    n2 = 0
    for i in range(len(TT_flows)):
        if TT_flows[i].F_pri == 1:
            n1 = N[0]
            n2 = N[2]
        elif TT_flows[i].F_pri == 2:
            n1 = N[1]
            n2 = N[3]
        routes = getRoutes(G, n1, TT_flows[i].flow_start, TT_flows[i].flow_end)
        TT_paths1[TT_flows[i].F_id] = routes
        # print("设定的路由数量：", n1, ", 找到的路由数量：", len(routes), ", \n路由有：", routes)
        routes = getRoutes(G, n2, TT_flows[i].flow_start, TT_flows[i].flow_end)
        TT_paths2[TT_flows[i].F_id] = routes
        # print("设定的路由数量：", n2, ", 找到的路由数量：", len(routes), ", \n路由有：", routes)
        # print()
    return TT_paths1, TT_paths2


@func_set_timeout(600)
def TS(TTFlow_list, hp, TT_paths):
    num = 15000
    for i in range(num):  # 批量声明offset的变量
        locals()['off' + str(i)] = Int(('off' + str(i)))

    TTFrame_list = []  # 帧的集合
    total_frame_id_in_frame = 0
    for i in range(len(TTFlow_list)):
        path = TT_paths[TTFlow_list[i].F_id]
        pri = random.randrange(3, 8, 1)
        len_path = len(path)

        # print("F_pri=",list1[i].F_pri, " len_path=", len_path)
        for j in range(len_path):
            for k in range(len(path[j]) - 1):
                TTFrame_list.append(Frame(TTFlow_list[i].F_id,
                                          TTFlow_list[i].flow_start,
                                          TTFlow_list[i].flow_end,
                                          TTFlow_list[i].L,
                                          TTFlow_list[i].t,
                                          TTFlow_list[i].e2e,
                                          TTFlow_list[i].F_pri,
                                          0,  # list1[i].flow_id,
                                          0,  # list1[i].init_time,
                                          j,
                                          k,
                                          total_frame_id_in_frame,
                                          path[j][k],
                                          path[j][k + 1],
                                          eval('off' + str(total_frame_id_in_frame)),
                                          pri
                                          ))
                total_frame_id_in_frame = total_frame_id_in_frame + 1

    TTFrameListLength = len(TTFrame_list)
    print('TT帧经过的链路数量是：', TTFrameListLength)

    # SMT算法开始
    s = Solver()

    # 限制1，2，13 截止期和pri限制  Frame Constraint
    for i in range(len(TTFrame_list)):
        s.add(TTFrame_list[i].offset >= 0)
        s.add(TTFrame_list[i].offset <= TTFrame_list[i].t - TRANSMISSION_DURATION)

    # 限制4，5即同一个帧实例在链路上Φ的大小关系 Flow Transmission Constraint
    for i in range(TTFrameListLength):
        for j in range(TTFrameListLength):
            if i != j:
                # print("333 ", TTFrame_list[i].F_id, TTFrame_list[i].frame_start, TTFrame_list[i].frame_end)
                # print("444 ", TTFrame_list[j].F_id, TTFrame_list[j].frame_start, TTFrame_list[j].frame_end)
                if TTFrame_list[i].F_id == TTFrame_list[j].F_id and TTFrame_list[i].frame_end == \
                        TTFrame_list[j].frame_start:
                    s.add(TTFrame_list[j].offset >= TTFrame_list[i].offset + TRANSMISSION_DURATION)

    #  （限制3）我们假设一条路径同时只传输一个实例。更具体地说，属于不同流但通过相同路径共享相同队列的两个实例的传输持续时间不能重叠。
    #    Link Constraint
    list_t = []
    for i in range(TTFrameListLength):
        for j in range(TTFrameListLength):
            if i != j:
                if TTFrame_list[i].frame_id_in_frame not in list_t:
                    if TTFrame_list[i].frame_start == TTFrame_list[j].frame_start and TTFrame_list[i].frame_end == \
                            TTFrame_list[j].frame_end:
                        list_t.append(TTFrame_list[j].frame_id_in_frame)
                        a = math.floor(hp / TTFrame_list[i].t)
                        b = math.floor(hp / TTFrame_list[j].t)
                        for k in range(a):
                            for x in range(b):
                                p, q = Bools('p q')
                                p = TTFrame_list[i].offset + TRANSMISSION_DURATION + k * TTFrame_list[i].t <= \
                                    TTFrame_list[j].offset + x * \
                                    TTFrame_list[
                                        j].t
                                q = TTFrame_list[j].offset + TRANSMISSION_DURATION + x * TTFrame_list[j].t <= \
                                    TTFrame_list[i].offset + k * \
                                    TTFrame_list[
                                        i].t
                                if k * TTFrame_list[i].t > x * TTFrame_list[j].t:
                                    s.add(q)
                                else:
                                    s.add(p)

    # 限制6,7，即帧隔离 Frame Isolation Constraint
    for i in range(1, TTFrameListLength):
        for j in range(TTFrameListLength):
            if i != j:
                if TTFrame_list[i].F_id != TTFrame_list[j].F_id and TTFrame_list[i].frame_start == TTFrame_list[
                    j].frame_start \
                        and TTFrame_list[i].frame_end == TTFrame_list[j].frame_end and TTFrame_list[i - 1].frame_end == \
                        TTFrame_list[j].frame_start:
                    # print("111")
                    p, q = Bools('p q')
                    p = (TTFrame_list[i].pri != TTFrame_list[j].pri)
                    q = (TTFrame_list[j].offset >= TTFrame_list[i - 1].offset)
                    s.add(Or(p, q))
                    # print(p, q)

    result = s.check()
    # print(result)
    ts = 0
    if result:
        # print("进入if")
        m = s.model()
        list_model_name = []
        list_model_value = []
        for d in m.decls():
            list_model_name.append(d.name())
            list_model_value.append(eval(str(m[d])))
            # print(d.name(), "=", m[d])
        ts = max(list_model_value) - min(list_model_value) + 1
        # print(ts)
    return result, ts
