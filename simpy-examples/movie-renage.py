"""
场景过程： 买三场电影的票，如果某个票卖完了，买这个票的人都会走
包含：来源、条件事件、共享事件
"""
import collections
import random

import simpy


RANDOM_SEED = 40
TICKETS = 50  # 电影的票数
SIM_TIME = 120  # 仿真时间


def moviegoer(env, movie, num_tickets, theater):
    """
    顾客尝试购买一定数目的某场电影的票（1）如果没票了则离开（2）如果轮到了购买但是
    没有足够的票了也离开。如果只有最后一张票，出发事件所有顾客离开
    """
    with theater.counter.request() as my_turn:
        # 等待到该客户或者票卖完了（状态）
        result = yield my_turn | theater.sold_out[movie]

        # 如果卖完了就离开，统计离开的人数
        if my_turn not in result:
            theater.num_renegers[movie] += 1
            return

        # 检查是否还有足够的票剩余，如果没有了同样离开
        if theater.available[movie] < num_tickets:
            yield env.timeout(0.5)
            return

        # 买票
        theater.available[movie] -= num_tickets
        if theater.available[movie] < 2:
            # Trigger the "sold out" event for the movie
            theater.sold_out[movie].succeed()
            theater.when_sold_out[movie] = env.now
            theater.available[movie] = 0
        yield env.timeout(1)


def customer_arrivals(env, theater):
    """在模拟时间内，按照指数分布时间生成客户"""
    while True:
        yield env.timeout(random.expovariate(1 / 0.5))

        movie = random.choice(theater.movies)
        num_tickets = random.randint(1, 6)
        if theater.available[movie]:
            env.process(moviegoer(env, movie, num_tickets, theater))

# 剧场的基本定义
Theater = collections.namedtuple('Theater', 'counter, movies, available, sold_out, when_sold_out, num_renegers')


# 随机种子和环境设置
print('Movie renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

counter = simpy.Resource(env, capacity=1) # 安排服务柜台
movies = ['Python Unchained', 'Kill Process', 'Pulp Implementation'] # 全部低昂嘤
available = {movie: TICKETS for movie in movies} # 每个电影的票的数目
sold_out = {movie: env.event() for movie in movies} # 每个低昂嘤都有一个环境事件
when_sold_out = {movie: None for movie in movies} # 卖出
num_renegers = {movie: 0 for movie in movies}
theater = Theater(counter, movies, available, sold_out, when_sold_out,
                  num_renegers)

# 开始进程并运行
env.process(customer_arrivals(env, theater))
env.run(until=SIM_TIME)

# 结果与分析
for movie in movies:
    if theater.sold_out[movie]:
        print('Movie "%s" sold out %.1f minutes after ticket counter '
              'opening.' % (movie, theater.when_sold_out[movie]))
        print('  Number of people leaving queue when film sold out: %s' %
              theater.num_renegers[movie])