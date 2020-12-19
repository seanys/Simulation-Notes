'''
事件驱动的事件仿真
'''
from random import seed, randint
import simpy
seed(23)

class EV:
    def __init__(self, env):
        self.env = env
        self.drive_proc = env.process(self.drive(env)) # 运行开车程序
        self.bat_ctrl_proc = env.process(self.bat_ctrl(env)) # 运行充电控制程序
        self.bat_ctrl_reactivate = env.event() # 触发时间设置

    def drive(self, env):
        while True:
            # Drive for 20-40 min
            yield env.timeout(randint(20, 40))

            # Park for 1–6 hours
            print('Start parking at', env.now)
            self.bat_ctrl_reactivate.succeed() # 触发事件
            self.bat_ctrl_reactivate = env.event() # 重新定义新的事件
            yield env.timeout(randint(60, 360))
            print('Stop parking at', env.now)

    def bat_ctrl(self, env):
        while True:
            print('Bat. ctrl. passivating at', env.now)
            yield self.bat_ctrl_reactivate  # "passivate"
            print('Bat. ctrl. reactivated at', env.now)
            yield env.timeout(randint(30, 90))

env = simpy.Environment()
ev = EV(env)
env.run(until=1500)
