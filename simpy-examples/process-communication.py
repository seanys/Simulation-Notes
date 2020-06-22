"""
内容：进程沟通案例
过程：如何进行一对一的信息传递和一对多的信息广播
"""
import random
import simpy

RANDOM_SEED = 42
SIM_TIME = 100


class BroadcastPipe(object):
    """广播通道类的定义"""
    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.pipes = []

    def put(self, value):
        """广播的过程"""
        if not self.pipes:
            raise RuntimeError('There are no output pipes.') # 没有传播的通道
        events = [store.put(value) for store in self.pipes]
        return self.env.all_of(events)

    def get_output_conn(self):
        """获得新的传播管道的输出连接，获得后再进行传递"""
        pipe = simpy.Store(self.env, capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe


def message_generator(name, env, out_pipe):
    """随机生成信息"""
    while True:
        yield env.timeout(random.randint(6, 10)) # 随机等待时间

        msg = (env.now, '%s says hello at %d' % (name, env.now)) # 生成信息
        out_pipe.put(msg) # 传递信息


def message_consumer(name, env, in_pipe):
    """处理信息的进程"""
    while True:
        msg = yield in_pipe.get()

        if msg[0] < env.now:
            print('LATE Getting Message: at time %d: %s received message: %s' %
                  (env.now, name, msg[1]))
        else:
            print('at time %d: %s received message: %s.' %
                  (env.now, name, msg[1]))

        yield env.timeout(random.randint(4, 8)) # 随机等待部分时间


print('Process communication')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# 通过管道进行一对一的传递
pipe = simpy.Store(env)
env.process(message_generator('Generator A', env, pipe))
env.process(message_consumer('Consumer A', env, pipe))

print('\nOne-to-one pipe communication\n')
env.run(until=SIM_TIME)

# 通过广播通道进行一对多信息传递
env = simpy.Environment()
bc_pipe = BroadcastPipe(env)

env.process(message_generator('Generator A', env, bc_pipe))
env.process(message_consumer('Consumer A', env, bc_pipe.get_output_conn()))
env.process(message_consumer('Consumer B', env, bc_pipe.get_output_conn()))

print('\nOne-to-many pipe communication\n')
env.run(until=SIM_TIME)