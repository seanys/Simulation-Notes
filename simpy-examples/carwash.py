"""
场景：有限数目的洗车机，随机到达车，如果有空闲车辆，则开始洗车，否则等待
"""
import random

import simpy


RANDOM_SEED = 42 
NUM_MACHINES = 2  # 可以用的洗车机
WASHTIME = 5      # 需要花费的洗车事件（分钟）
T_INTER = 7       # 每隔七分钟生成一辆车
SIM_TIME = 20     # 一共模拟20分钟


class Carwash(object):
    """有限数目的车辆去洗车，车辆向多个机器请求，找到一个可行的即刻"""
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime

    def wash(self, car):
        """洗车的过程"""
        yield self.env.timeout(WASHTIME)
        print("Carwash removed %d%% of %s's dirt." %
              (random.randint(50, 99), car))


def car(env, name, carwash):
    """车于随机时间到达，请求洗车机器，等待或直接开始"""

    print('%s arrives at the carwash at %.2f.' % (name, env.now))
    with carwash.machine.request() as request:
        yield request

        print('%s enters the carwash at %.2f.' % (name, env.now))
        yield env.process(carwash.wash(name))

        print('%s leaves the carwash at %.2f.' % (name, env.now))


def setup(env, num_machines, washtime, t_inter):
    """创建一辆洗车机，一些初始化的车每隔一段时间生成"""
    carwash = Carwash(env, num_machines, washtime)

    # 首先创建四辆车
    for i in range(4):
        env.process(car(env, 'Car %d' % i, carwash))

    # 每隔随机时间继续创建车
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 2))
        i += 1
        env.process(car(env, 'Car %d' % i, carwash))

print('Carwash')
random.seed(RANDOM_SEED) 

# 配置仿真环境
env = simpy.Environment()
env.process(setup(env, NUM_MACHINES, WASHTIME, T_INTER))

# 执行
env.run(until=SIM_TIME)