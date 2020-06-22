"""
场景：银行柜台有随机的服务时间，超时会离开
"""
import random
import simpy

RANDOM_SEED = 42
NEW_CUSTOMERS = 5  # 客户总人数
INTERVAL_CUSTOMERS = 10.0  # 客户的间隔时间/秒
MIN_PATIENCE = 1  # 客户的最小的忍受时间
MAX_PATIENCE = 3  # 客户的最大的忍受时间


def source(env, number, interval, counter):
    """随机生成乘客"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0) # 生成一个客户
        env.process(c) # 环境开始处理该客户
        t = random.expovariate(1.0 / interval) # 生成随机事件
        yield env.timeout(t) # 需要等待该事件再处理下一个

def customer(env, name, counter, time_in_bank):
    """客户到达、服务和离开"""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE) # 生成随机的等待事件

        results = yield req | env.timeout(patience) # 等待事件发生

        wait = env.now - arrive # 当前事件减去等待事件

        if req in results:
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait)) # 等待的事件

            tib = random.expovariate(1.0 / time_in_bank) # 生成服务时间-指数分析
            yield env.timeout(tib) # 等待一段时间后开始释放
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # 等待的事件超过了忍耐事件-退出
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))


print('Bank Renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

counter = simpy.Resource(env, capacity=1) # 定义服务的平台
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()