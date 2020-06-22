"""
场景：拆分各个进程中各个事件的时间延时
用途：进程通信
原作者: Keith Smith
"""
import simpy

SIM_DURATION = 100

class Cable(object):
    """信息通道"""
    def __init__(self, env, delay):
        self.env = env
        self.delay = delay
        self.store = simpy.Store(env)

    def latency(self, value):
        yield self.env.timeout(self.delay)
        self.store.put(value)

    def put(self, value):
        self.env.process(self.latency(value))

    def get(self):
        return self.store.get()


def sender(env, cable):
    """随机生成和发出信息"""
    while True:
        # 等待一定事件重复该过程
        yield env.timeout(5)
        cable.put('Sender sent this at %d' % env.now)


def receiver(env, cable):
    """接收生成了的信息"""
    while True:
        # 获得上述的通知信息
        msg = yield cable.get()
        print('Received this at %d while %s' % (env.now, msg))

print('Event Latency')
env = simpy.Environment()

# 开始仿真过程，发出消息和接收消息
cable = Cable(env, 10)
env.process(sender(env, cable))
env.process(receiver(env, cable))

env.run(until=SIM_DURATION)