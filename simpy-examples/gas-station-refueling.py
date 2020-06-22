"""
内容：加油站仿真
场景：加油站随机接待需求加油不一定的车辆，车辆到达后开始加油，需要
一定的加油时间，周期性检查加油站剩余的油量，如果低于某个值，则需要
呼叫加油车来送油
"""
import itertools
import random

import simpy


RANDOM_SEED = 42
GAS_STATION_SIZE = 200     # 加油站的油辆
THRESHOLD = 10             # 最低的限度-低于该值触发火车送货
FUEL_TANK_SIZE = 50        # 车的油箱容量
FUEL_TANK_LEVEL = [5, 25]  # 车的最高最低剩余容量
REFUELING_SPEED = 2        # 加油的速度
TANK_TRUCK_TIME = 300      # 加油车的到达时间
T_INTER = [30, 300]        # 车的到达时间-随机数生成范围
SIM_TIME = 1000            # 仿真时间


def car(name, env, gas_station, fuel_pump):
    """车的定义，到达后开始加油"""
    fuel_tank_level = random.randint(*FUEL_TANK_LEVEL) # 现在还剩下多少油
    print('%s arriving at gas station at %.1f' % (name, env.now))
    with gas_station.request() as req:
        start = env.now
        yield req

        liters_required = FUEL_TANK_SIZE - fuel_tank_level # 需要加多少油
        
        yield fuel_pump.get(liters_required)

        yield env.timeout(liters_required / REFUELING_SPEED)

        print('%s finished refueling in %.1f seconds.' % (name, env.now - start))


def gas_station_control(env, fuel_pump):
    """周期检查是不是低于阈值，低于阈值则开始请求重新送油"""
    while True:
        if fuel_pump.level / fuel_pump.capacity * 100 < THRESHOLD:
            print('Calling tank truck at %d' % env.now)
            yield env.process(tank_truck(env, fuel_pump)) # 开始送油

        yield env.timeout(10)  # Check every 10 seconds


def tank_truck(env, fuel_pump):
    """油罐车送油"""
    yield env.timeout(TANK_TRUCK_TIME) # 等待一定的时间
    print('Tank truck arriving at time %d' % env.now)
    ammount = fuel_pump.capacity - fuel_pump.level
    print('Tank truck refuelling %.1f liters.' % ammount)
    yield fuel_pump.put(ammount) # 开始加油


def car_generator(env, gas_station, fuel_pump):
    """生成车的进程"""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(car('Car %d' % i, env, gas_station, fuel_pump))


print('Gas Station refuelling')
random.seed(RANDOM_SEED)

env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
fuel_pump = simpy.Container(env, GAS_STATION_SIZE, init=GAS_STATION_SIZE)
env.process(gas_station_control(env, fuel_pump))
env.process(car_generator(env, gas_station, fuel_pump))

env.run(until=SIM_TIME)