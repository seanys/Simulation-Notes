"""
内容：机器车间，包括扰动和预占资源的仿真
场景：一个车间有n个机器，一系列工作到来，每个机器都会周期性损坏，然后维修工人
将进行维修，同时维修工人也有其他不那么重要的的工作，这些工作将被损坏了的机器
预占，当维修好之后机器就会继续工作
"""
import random

import simpy


RANDOM_SEED = 42
PT_MEAN = 10.0         # 处理时间均值（正态分布）
PT_SIGMA = 2.0         # 处理时间方差（正态分布）
MTTF = 300.0           # 机器出问题的平均时间
BREAK_MEAN = 1 / MTTF  # 指数分布的参数
REPAIR_TIME = 30.0     # 维修工作的时间
JOB_DURATION = 30.0    # 其他工作的时间
NUM_MACHINES = 10      # 机器车间的机器数目
WEEKS = 4              # 仿真时间/周
SIM_TIME = WEEKS * 7 * 24 * 60  # 仿真时间/分钟


def time_per_part():
    """实际的处理时间"""
    return random.normalvariate(PT_MEAN, PT_SIGMA)


def time_to_failure():
    """等待多久机器会再次失效"""
    return random.expovariate(BREAK_MEAN)


class Machine(object):
    """ 机器定义
    生产：只要不损坏就会持续生产
    机器故障：部分情况出现故障，将等待进行维修
    """
    def __init__(self, env, name, repairman):
        self.env = env # 运行环节
        self.name = name # 机器的命名
        self.parts_made = 0 # 已经生产的组件
        self.broken = False # 初始设定没有损坏

        self.process = env.process(self.working(repairman)) # 生产的进程
        env.process(self.break_machine()) # 机器故障的进程

    def working(self, repairman):
        """ 工作说明
        开始生产产品，生产过程中可能会损坏，然后需要维修工人维修
        """
        while True:
            done_in = time_per_part() # 生产的时间预设
            while done_in:
                try: # 正常情况会工作到结束
                    start = self.env.now
                    yield self.env.timeout(done_in)
                    done_in = 0 
                except simpy.Interrupt:
                    self.broken = True
                    done_in -= self.env.now - start

                    # 请求维修人员维修，维修人员会停下收下的工作过来
                    with repairman.request(priority=1) as req:
                        yield req
                        yield self.env.timeout(REPAIR_TIME)

                    self.broken = False
            
            # 多计一件已经完成了
            self.parts_made += 1

    def break_machine(self):
        """到达了预设的宕机时间"""
        while True:
            yield self.env.timeout(time_to_failure())
            if not self.broken:
                self.process.interrupt() # 进程中断

def other_jobs(env, repairman):
    """维修工人的其他工作"""
    while True:
        # 开始新工作
        done_in = JOB_DURATION
        while done_in:
            # 维修人员开始维修，等待维修完成，或者出现异常请求
            with repairman.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt: # 机器损坏需要去修了
                    done_in -= env.now - start


print('Machine shop')
random.seed(RANDOM_SEED)

env = simpy.Environment()
repairman = simpy.PreemptiveResource(env, capacity=1) # 预占所有的资源
machines = [Machine(env, 'Machine %d' % i, repairman)
            for i in range(NUM_MACHINES)]
env.process(other_jobs(env, repairman))

env.run(until=SIM_TIME)

print('Machine shop results after %s weeks' % WEEKS)
for machine in machines:
    print('%s made %d parts.' % (machine.name, machine.parts_made))