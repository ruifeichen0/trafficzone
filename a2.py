"""
ENGG 1001 Assignment 2
2025 Semeseter 2
"""
"""import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray"""

__name__ = "CHEN RUIFEI"
__number__ = "s4985433"
__email__ = "s4985433@uq.edu.au"
__date__ = "2024/10/24"

#Write your code below:



# Task1 Acceleration

import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray

def accelerate(road_in,v_max):

    """Accelerates each vehicle on the road by 1,
provided the maximum speed is not exceeded.
i.e. vehicle_speed = min(vehicle_speed + 1, v_max)
for each element in the array
Parameters:
-----------
road_in : ndarray[int]
The current state of the road, with vehicle speeds.
If a vehicle is not present in the cell,
the speed is -1.
v_max: int
The maximum speed a vehicle can reach.
Returns:
--------
ndarray[int]
The new state of the road after applying acceleration.
"""

    n = len(road_in)
    #This ensures that every vehicle makes its decision based on the same old snapshot.not affected by cars updating previously.
    new_road = road_in.copy()    
   
    for i in range (n):
        #Only update occupied cells (skip empty cells).
        if new_road[i] != -1:
            #Increase the speed by 1 but cap it at v_max.
            new_road[i] = min(new_road[i] + 1, v_max)
    return new_road
    
#Task2(1) Deceleration


#road_in = 1D NumPy array of integers representing the road (–1 means empty, nonnegative means vehicle speed).
#signals_in = 1D boolean NumPy array of the same length, where True means there’s a red light at that cell.
# road_in = 一维 NumPy 数组，整数代表道路格子状态（-1 表示空格，非负数表示车辆速度）
# signals_in = 一维布尔型 NumPy 数组，与 road_in 长度相同，True 表示该格有红灯
def gaps_ahead(road_in,signals_in):
    
    """Determines the number of clear cells ahead of each vehicle on the road.
Parameters:
-----------
road_in: ndarry[int]
The current state of the road with vehicle speeds.
signals_in: ndarray[bool]
True for any cell containing a red traffic signal, False otherwise.
Returns:
--------
ndarry[int]
The number of clear cells ahead of the vehicle, containing neither another
,
→ vehicle nor red traffic signal. Empty cells contain the value -1.
"""
    
    #Get the road length n and create an array filled with –1 for output.
    n = len(road_in)
    #np.full(shape, fill_value, dtype=None) more efficient
    gaps = np.full(n,-1)
    for cell_position in range(n):
        #If the current cell is empty (–1), skip it (continue)
        #because there’s no vehicle to measure the gap for.
        if road_in[cell_position] == -1:
            continue
        #Start counting from the next cell after the vehicle, and initialize the counter to 0.
        start = cell_position + 1
        count = 0
        for i in range(n):
            # The modulo operator (%) makes the road circular.
            # When we move past the last cell (index n-1), we wrap around to index 0.
            next_index = (start + i) % n
            if road_in[next_index] == -1 and signals_in[next_index] == False:
                count += 1
            else:
                break
        # Store the gap count in the same index as the car's position.
        gaps[cell_position] = count
    return gaps

#Task2(2)
def decelerate(road_in, signals_in):

    """Applies deceleration rule to each vehicle on the road.
Parameters:
-----------
road_in: ndarry[int]
The current state of the road with vehicle speeds.
signals_in: ndarray[bool]
True for any cell containing a red traffic signal, False otherwise.
Returns:
--------
road_out: road[int]: The new state of the road, after applying deceleration.
"""
    
    n = len(road_in)
    #This ensures that every vehicle makes its decision based on the same old snapshot.
    #not affected by cars updating previously.
    #复制当前道路数组，避免在同一时间步直接修改原状态（防止干扰后续车辆计算）
    new_road = np.copy(road_in)
    gaps_formulate = gaps_ahead(road_in,signals_in)
    #Loop through each cell on the road.
    #If the cell is empty (-1), skip it since there’s no vehicle to decelerate.
    for i in range(n):
        if road_in[i] == -1:
            continue
        #Otherwise (there is a vehicle), record its current speed as v,
        #and get the number of empty cells ahead from gaps_formulate[i].
        else:
            v = road_in[i]
            gap = gaps_formulate[i]
            #If the car’s speed is greater than the available space in front (v > gap),
            #reduce the speed to equal the gap — it stops just before the obstacle.
            #Otherwise, keep the same speed.
            if v > gap:
                new_road[i] = gap
            else:
                new_road[i] = v

    return new_road

#Task3 Movement
def move(road_in):

    """Moves vehicles along the road based on their speeds.
Parameters:
-----------
road_in : ndarry[int]
The current state of the road, with vehicle speeds
Returns:
--------
ndarray[int]
The new state of the road after applying movement.
"""
    
    n = len(road_in)
    #Create a new road array filled with -1 (empty cells).
    #This ensures we build the next state from scratch.
    new_road = np.full(n,-1)
    for i in range(n):
        if road_in[i] == -1:
            continue
        else:
            v = road_in[i]
            #circulation movement(different from task2, the initial position is included)
            new_position = (i + v) % n
            #put the car in a new position
            #eg new_road = [-1, -1, -1, -1, -1, -1, -1, -1]  new_road[2] = 2   new_road = [-1, -1, 2, -1, -1, -1, -1, -1]   
            new_road[new_position] = v

    return new_road

#Task4 Make road and traffic signals
def make_road(n_cells, vehicle_speed, vehicle_gap):

    """Creates a road of length n_cells,
with vehicles travelling at speed vehicle_speed.
A vehicle is in the first cell, all
subsequent vehicles are separated by vehicle_gap.
Parameters:
-----------
n_cells: int
The length of the road (number of cells) must be in the range 5-50.
If it is outside the range, the default value n_cells = 12 is used,
and an error message is returned.
vehicle_speed: int
The speed of all vehicles on the road.
vehicle_gap: int
This is the spacing between each vehicle and the subsequent vehicle.
If there is insufficient gap to fit at last two vehicles on the road,
or if the gap is less than 2,
an error message is returned and a default value vehicle_gap = 2 is used
Returns:
--------
ndarray[int]
The current state of the road, with vehicle speeds.
"""
    
    #Set fallback values in case the user enters invalid road length or gap.
    limit_length = 12
    limit_gap = 2
    #check road length
    #If the user gives a road shorter than 5 cells or longer than 50,
    #show a warning and set road length to the default (12).
    if n_cells < 5 or n_cells > 50:
        print("Warning! Road length not in range(5, 50): road length of 12 used")
        n_cells = limit_length
    #check vehicle gap
    #if the gap is too small(<2) or too big(can not contain 2 vehicles)
    if vehicle_gap < 2:
        print("Warning! Vehicle gap too small: value of 2 used")
        vehicle_gap = limit_gap
    elif vehicle_gap >= n_cells - 1:
        print("Warning! Vehicle gap too large: value of 2 used")
        vehicle_gap = limit_gap
    #create road
    road = np.full(n_cells, -1)
    #Start placing cars from the beginning of the road (index 0).
    position = 0
    #As long as the current position is within the road:
    #place a car (with speed = vehicle_speed) at this position.
    while position < n_cells:
        road[position] = vehicle_speed
        # because 'vehicle_gap' refers to the number of empty cells between cars.
        # For example, a gap of 2 means two empty cells, so the next car
        # should be placed 3 cells (2 + 1) ahead.
        #eg vehicle_speed = 2 vehicle_gap = 2
        # 1st round: road[0] = 2 [2,-1,-1,-1,-1,-1,-1,-1,-1,-1]  position += 2+1 → 3
        # 2nd round: road[3] = 2 [2,-1,-1,2,-1,-1,-1,-1,-1,-1] position += 3 → 6
        # “vehicle_gap” 表示两车之间的空格数量
        # 所以下一辆车的位置 = 当前车位置 + 空格数 + 1。
        position += vehicle_gap + 1

    return road

def make_signals(road_in,sig_loc,sig_timing,t):

    """Determines which cells in the road have a red traffic signal at time t.
Parameters:
-----------
road_in : ndarry[int]
The current state of the road, with vehicle speeds.
sig_loc: ndarry[int]
Cell numbers where traffic signals are located
sig_timing: tuple(int):
Tuple of signal timing (red_duration, cycle_time)
t:int
Number of timesteps since start of simulation (starts from 0)
Returns:
--------
ndarry[bool]: 1-d array, same size as road_in,
True for each cell containing a red traffic signal.
"""
    
    n = len(road_in)
    #Extract the red signal duration and the total signal cycle from the tuple.
    #从 sig_timing 元组中取出红灯持续时间和总周期。
    red_length = sig_timing[0]
    cycle_time = sig_timing[1]
    #Initialise the whole road as green signals (False) — a “safe” default state.
    # Later, only specific signal locations will be changed to red (True).
    #先将整条道路初始化为“全绿灯”(False)
    #这样后面只需要把有红灯的位置改为 True。
    signals = np.full(n,False,dtype=bool)
    #Calculate the current moment within the signal cycle by taking t mod cycle_time.
    #if cycle_time = 10 and t = 13, time in cycle = 3
    #计算当前时间在信号周期中的位置。
    time_in_cycle = t % cycle_time
    #If the current time is within the red phase (< red_length), then lights are red;
    #otherwise green.
    #若当前时间小于红灯持续时间，表示红灯亮。否则是绿灯亮。
    if time_in_cycle < red_length:
        red_now = True
    else:
        red_now = False
    #If there are no signal locations on the road, return all-green array.
    #如果道路上没有信号灯位置，直接返回全绿数组。
    if len(sig_loc) == 0:
        return signals
    #Check if this signal position is valid —
    #it must be between 0 and n–1 (within the road length).
    #确认信号灯位置在合法范围内（0 ≤ i < n）
    for i in sig_loc:
        if 0 <= i < n:
            # For each signal position i, set that cell's light to the current state (red_now).
            # If red_now = True, that position becomes red; if False, it's green.
            # Set this signal cell's value to current state (red or green)
            signals[i] = red_now

    return signals

#Task5  Putting it all together



def simulate(road_in, v_max, sig_loc, sig_timing, num_steps):
    
    #Make a copy of the input road so that we don’t overwrite the original;
    #store the first state (time 0) in result.
    #复制输入的道路状态，防止直接修改原始数组。
    #将初始状态（时间 t=0）保存到结果列表中。
    road = road_in.copy()
    result = [road.copy()]
    # Start t from 1 because the initial state (t=0) is already stored before the loop.
    # The loop handles only the updates for steps 1..num_steps.(the reason why end up in num_steps + 1)
    #从 t=1 开始循环，因为 t=0 的状态已保存；循环范围是 1..num_steps。
    for t in range(1, num_steps + 1):
        #We use t - 1 to align the simulation step with the signal cycle,
        #because the signal starts its red phase at time t=0 while our loop starts from t=1.
        #eg 第一次循环：t=1 → t-1=0 → 红灯刚开始
        signals = make_signals(road, sig_loc, sig_timing, t - 1)

        road = accelerate(road, v_max)
        road = decelerate(road, signals)
        road = move(road)

        result.append(road.copy())
        
    # Convert the list of road states into a NumPy 2D array.
    # This allows easy numeric operations and ensures consistent data type.
    return np.array(result)


import numpy as np
from matplotlib.pyplot import *

def plot_speed(road_in, v_max, sig_loc, sig_timing, num_steps):


    """Runs the simulation for a specified number of steps, calculates mean speed
for the initial road and for the road at each subsequent time step,
and plots mean speed (km/h) vs time since start of simulation (s).
Parameters:
-----------
road_in : ndarry[int]
The initial state of the road, with vehicle speeds.
v_max: int
The maximum speed a vehicle can reach.
sig_loc: ndarry[int]
Cell numbers where traffic signals are located
sig_timing: tuple(int):
Tuple of signal timing (red_duration, cycle_time) s
n_step: int
Number of steps in the iteration
Returns:
ndarray[float]:
1d array of mean road speed, km/h
ndarray[float]:
1d array of time since start of simulation

"""

    # 运行模拟：得到形状 (num_steps+1, len(road_in)) 的数组
    sim = simulate(road_in, v_max, sig_loc, sig_timing, num_steps)

   
    # Create an empty NumPy array to store mean speed values for each time step.
    # Initialized with zeros for efficiency.
    #创建一个数组保存每个时间步的平均速度，初始值全为0。
    mean_speeds = np.zeros(num_steps + 1)

    for i in range(num_steps + 1):
        # get the statement of the road when i (times)
        #eg 1st i = 0 [2, -1, 3, -1] the initial statement of the road
        #获取该时间步下的道路状态（车辆速度分布）
        current = sim[i]
        # get all the vehicle speed except no speed
        # 取出非空格（有车）的速度值
        speeds = current[current != -1]
        # If there are cars on the road at this time step, compute mean speed.
        #如果此时道路上有车，计算平均速度
        if len(speeds) > 0:
            # Convert from cells/step to km/h using 1 cell/step = 18 km/h.
            #将单位从格/步转换为 km/h（1 格/步 = 18 km/h）
            mean_speeds[i] = np.mean(speeds) * 18
        # If no cars are present (empty array), set mean speed to 0.
        # 若此时道路上没有车，平均速度设为 0
        else:
            mean_speeds[i] = 0

    #np.arange(start, stop, step)
    #“Each timestep = 2 seconds”
    # Each simulation step = 2 seconds, and we have (num_steps + 1) total states
    time = np.arange(0, (num_steps + 1) * 2, 2)

    # plot
    # label='Mean Speed' gives the plotted line a label that will appear in the legend.
    plot(time, mean_speeds, 'b-o', label='Mean Speed')
    title("Mean vehicle speed over time")
    xlabel("Time, s")
    ylabel("Mean speed, km/h")
    # Display legend to identify the plotted data.
    #显示图例
    legend()
    # Enable grid for better readability.
    # 显示网格
    grid(True)
    # Display the final plot window.
    show()

    #for testing or further analysis.
    return mean_speeds, time

#Task 6: Create the Vehicle class

import numpy as np


class Vehicle:
    # Initialize vehicle position and speed.
    # 初始化车辆的位置和速度。
    # self represents the current object instance.
    # self 表示当前对象自身的实例。
    # eg car1 = Vehicle(3, 2) car1._position == 3 car1._speed == 2
    # 例如 car1 = Vehicle(3, 2) 表示该车的位置是 3，速度是 2。
    def __init__(self, position: int, speed: int):
        

        self._position = position
        self._speed = speed
        # Store the trajectory of the vehicle (list of positions over time).
        # 存储车辆的运动轨迹（记录每一步的位置的列表）。
        self._trajectory = [position]
        
    # The getter methods provide controlled access to private attributes like position, speed, and trajectory
    # can only read without making changes
    # getter 方法提供对私有属性（位置、速度、轨迹）的受控访问。
    # 只能读取而不能修改。
    def get_position(self) -> int:
        return self._position
    
    def get_speed(self) -> int:
        return self._speed
    
    def get_trajectory(self) -> list:
        return self._trajectory

    #-> None means the function doesn’t return anything — it just changes the car’s internal state.
    def accelerate(self, v_max: int) -> None:
        
        """
        Increases the speed of the vehicle by 1, up to a maximum value.
        Rule: v_i = min(v_i + 1, v_max)
        """
        
        # Increase current speed by 1, limited by the maximum allowed speed.
        self._speed = min(self._speed + 1, v_max)

    def decelerate(self, gap: int) -> None:
        """
        Reduces the speed of the vehicle if it exceeds the available gap ahead.
        Rule: v_i = min(v_i, gap)
        """
        # If speed > gap ahead, reduce speed to match the gap.
        self._speed = min(self._speed, gap)
    
    def randomise(self, p: float) -> None:
        """
        Randomly reduces the speed of the vehicle by 1 with probability p.
        """
        if self._speed > 0:
            #生成一个 0 到 1 之间的随机浮点数（包含 0，不包含 1）。
            #Generates a random number between 0 and 1 using NumPy’s random generator.
            random_num = np.random.random()
            #If the generated random number is smaller than p, it means the random slowing event occurs.
            # 如果生成的随机数小于 p，则发生随机减速事件。
            if random_num < p:
                self._speed -= 1
    
    def move(self, road_length: int) -> None:
        """
        Updates the position of the vehicle based on its speed.
        """
        # update the position according to the speed
        # 根据当前速度更新车辆位置。
        self._position = (self._position + self._speed) % road_length
        # add the new position into trajectory list
        # 将新的位置添加进轨迹列表中。
        self._trajectory.append(self._position)




# Task 7 Complete Road class
class Road:
    #Initialises a new road with a given length. Initially, it has no vehicles and no traffic signals.
    # 初始化一个给定长度的道路。最开始没有车辆也没有交通信号灯。
    def __init__(self, length: int):
        self._length = length
        self._vehicles = []
        self._time = 0
        self._signal_position = None
        self._red_duration = None
        self._cycle_length = None
    
    def get_length(self) -> int:
        return self._length
    
    def get_vehicles(self) -> list:
        return self._vehicles

    # Add a vehicle object to the road's vehicle list.
    # 将一个车辆对象添加到道路的车辆列表中。
    def add_vehicle(self, vehicle) -> None:
        self._vehicles.append(vehicle)
    
    def set_signal(self, position: int, red_duration: int, cycle_length: int) -> None:
        # Set traffic signal position and timing parameters
        # 设置信号灯的位置和红绿灯周期的参数。
        self._signal_position = position
        self._red_duration = red_duration
        self._cycle_length = cycle_length

    # Set traffic signal position and timing parameters, if not, turn out to be green
    # 判断信号灯当前是否为红灯；如果未设置信号灯，则默认为绿灯。
    def is_signal_red(self) -> bool:
        if self._signal_position is None:
            return False

        #Calculates the current time position within one signal cycle using the modulo (%) operator.
        # 使用取模（%）运算计算当前时间在一个信号周期中的位置。
        #For example, if the cycle length is 8 and current time is 10:
        #10 % 8 = 2 → means we are in the 3rd time step of the current cycle.
        # 例如：如果周期长度是8，当前时间是10：
        #10 % 8 = 2 → means we are in the 3rd time step of the current cycle.
        # 10 % 8 = 2 → 表示处于当前周期的第3个时间步。
        
        time_in_cycle = self._time % self._cycle_length
        return time_in_cycle < self._red_duration
    
    """
if time_in_cycle < self._red_duration:
    return True
else:
    return False
    """
    
    def calculate_gap(self, position: int) -> int:
        
        #This function determines how far a vehicle can move forward before it meets either:
        #another vehicle, or a traffic light.
        #It returns the smaller of the two distances, because that’s the first obstacle the car will encounter.
       
        gap_to_vehicle = self._calculate_gap_to_vehicle(position)
        gap_to_signal = self._calculate_gap_to_signal(position)
        return min(gap_to_vehicle, gap_to_signal)
    
    def _calculate_gap_to_vehicle(self, position: int) -> int:
        # 检查位置是否有车辆
        #Check if any vehicle currently occupies this position
        #for v in self._vehicles loop all the vehicles on the road
        # 该函数计算车辆在遇到障碍（车或红灯）前可以前进的最大距离。返回两者之间较小的一个，因为那是车辆最先遇到的障碍。
        #v.get_position() == position to see if the position of the vehicle equals to the position updated
        # 判断车辆的位置是否与传入的位置相同。
        #any() go back to True when meeting the first True, go back to False if all of them are False
        #any() 函数：遇到第一个 True 就返回 True；如果全是 False，返回 False。
        position_has_vehicle = any(v.get_position() == position for v in self._vehicles)
        
        
        # the gap length equals to the road length
        # 如果道路上没有其他车辆，空格长度等于道路长度。
        if len(self._vehicles) == 0:
            return self._length  
        

        # maximum of the gap length, which is road length - 1
        # 如果只有一辆车且它就在当前位置，空格长度为最大值（道路长度-1）。
        if len(self._vehicles) == 1 and position_has_vehicle:
            return self._length - 1
        
        
        # 创建一个新的列表，找到所有其他车辆的位置
        #Creates a list of all other vehicles on the road, excluding the one currently at the given position.
        #eg 车辆位置: [3, 7, 9]
        #position = 7
        #other_vehicles = [3, 9] 
        other_vehicles = [v for v in self._vehicles if v.get_position() != position]
        
        # 如果没有其他车辆，返回道路长度或道路长度-1
        #If there are no other cars, return the full road length (if empty) or one less than that (if this car exists).
        if not other_vehicles:
            return self._length - 1 if position_has_vehicle else self._length
        
        # Initialize the minimum gap to the largest possible value — the full road length.
        # Since haven't started compare, the maximum can be a good starting point
        min_gap = self._length

       #Loop through each of the other vehicles on the road, count the distance between them and the current vehicle one by one
       #遍历所有其他车辆，逐一计算与当前位置车辆的距离。
        for vehicle in other_vehicles:
            
            # Get that vehicle’s position.
            # 获取另一辆车的位置。
            v_pos = vehicle.get_position()
            
            #If the other car is ahead in the array (normal case):
            #Example: current = 2, other = 7 → 7 - 2 - 1 = 4 (four empty cells in between)
            # 如果另一辆车在前方（正常情况）
            # 示例：当前位置2，另一车在7 → 7-2-1=4（中间有4个空格）
            
            if v_pos > position:
                distance = v_pos - position - 1

            #If the other car is behind in index (wrap-around case):
            #→ add the road length first, to simulate looping.
            #Example: road length = 10, current = 8, other = 2 →
            #(2 + 10) - 8 - 1 = 3 (three empty cells after wrapping around).
            # 如果另一辆车在后面（环形道路绕回情况）：
            # → 加上道路长度以实现首尾相连。
            
            else:
                distance = (v_pos + self._length) - position - 1
            
            # 只保留有效的正距离，并在发现更小值时更新 min_gap。
            #Only keep valid positive distances, and update min_gap when a smaller one is found.
            if 0 <= distance < min_gap:
                min_gap = distance
        
        return min_gap


    #This helper method calculates how far the next traffic signal (if red) is from the current vehicle.
    #If the light is green or no signal exists, it simply returns the maximum possible gap (the full road length).
    # 辅助函数：计算当前车辆距离红灯的距离（如果红灯存在）。
    # 如果是绿灯或未设置信号灯，则返回最大空格（整条道路长度）。
    def _calculate_gap_to_signal(self, position: int) -> int:
        # if it is not red or no signal installed at all, there is no red light to stop for.
        # 若当前信号灯不是红色，或道路没有信号灯，就不需停车。
        if not self.is_signal_red() or self._signal_position is None:
            
            # 检查位置是否有车辆
            # eg: there are 3 cars in position[2,5,8] position = 5 position_has_vehicle = any(v.get_position() == 5 for v in self._vehicles)
            # there is one True , so come back to True
            
            position_has_vehicle = any(v.get_position() == position for v in self._vehicles)

            #If there are no cars at all, return the full road length.
            #Otherwise, the maximum possible space in front is road length - 1.
            # 如果完全没有车，返回道路长度。
            # 否则返回道路长度 - 1（车辆最大可行空间）。
            return self._length if len(self._vehicles) == 0 else self._length - 1
        
        #get the position of the traffic signal on the road.
        # 获取信号灯在道路上的位置。
        signal_pos = self._signal_position
        
        # 计算到信号灯的距离(the same as the way used in vehicle)
        # 计算距离的方法与车辆之间距离相同。
        if signal_pos > position:
            distance = signal_pos - position - 1
        else:
            distance = (signal_pos + self._length) - position - 1
        
        return distance

# Task 8 simulate
    def simulate(self, num_steps: int, v_max: int, p: float) -> None:
        """
        Run the cellular automaton traffic simulation on the given road.
        
        Parameters:
        num_steps (int): Total number of simulation time steps
        v_max (int): Maximum allowed speed for vehicles
        p (float): Probability of random deceleration
        """
        for step in range(num_steps):
            # Step 1: Acceleration
            #For each car on the road, increase its speed by 1 unit if it’s below v_max.
            # 每辆车都尝试将速度加1，但不能超过最大速度 v_max。
            for vehicle in self._vehicles:
                vehicle.accelerate(v_max)
            
            # Step 2: Deceleration (based on gap ahead)
            #Each car checks the number of empty cells ahead (gap).
            #If its current speed is greater than that gap, it slows down to match it, ensuring no collision.
            # 对每辆车计算它与下一个障碍物（车或红灯）之间的空格数量。
            for vehicle in self._vehicles:
                position = vehicle.get_position()
                gap = self.calculate_gap(position)
                vehicle.decelerate(gap)
            
            # Step 3: Randomization
            #With probability p, a vehicle randomly slows down by 1
            # 每辆车以概率 p 随机减速1个单位
            for vehicle in self._vehicles:
                vehicle.randomise(p)
            
            # Step 4: Movement
            #Update each vehicle’s position based on its new speed.
            #If it reaches the end of the road, wrap around (circular road).
            # 使用取模运算 (%) 实现环形道路（越过尽头自动回到起点）。
            for vehicle in self._vehicles:
                vehicle.move(self._length)
            
            # Update time
            #Increase the internal time counter by 1 after completing all vehicle updates.
            # 道路对象的时间步自增1，用于信号灯周期判断。
            self._time += 1
    
    def get_trajectories(self) -> list:
        # Collect the trajectory (path history) of every vehicle on the road
        # 收集道路上每辆车的运动轨迹（行驶路径的历史记录）。
        return [vehicle.get_trajectory() for vehicle in self._vehicles]
    
    def get_speeds(self) -> list:
        # Collect the current speed of every vehicle
        # 收集道路上每辆车的当前速度。
        return [vehicle.get_speed() for vehicle in self._vehicles]




#Task 9: Plot trajectories

import numpy as np
import matplotlib.pyplot as plt

def plot_trajectories(road):
    """
    Plots the trajectories of all vehicles on the road over time.

    Parameters:
    road (Road): The Road object containing vehicles whose trajectories have been recorded.

    Returns:
    None
    """

    #Get all recorded trajectories from the Road object.
    # 从 Road 对象中获取所有车辆的历史轨迹（位置随时间的变化）。
    #Get the total road length (used later to set y-axis limits)
    # 获取道路总长度，用于设定纵轴范围。
    
    trajectories = road.get_trajectories()
    road_length = road.get_length()
    
    #Create a figure with a fixed size (10×6 inches).
    # 创建一个固定尺寸的绘图窗口（10×6 英寸）。
    plt.figure(figsize=(10, 6))

    # Loop through all vehicle trajectories with their index
    # 遍历所有车辆的轨迹，并获取索引（i 是编号，trajectory 是该车轨迹）。
    #If a car has fewer than 2 recorded positions, skip it (nothing meaningful to plot).
    # 如果车辆轨迹点少于2个，跳过（无法形成有效曲线）。
    for i, trajectory in enumerate(trajectories):

        #If the trajectory list has length 1 or less, skip this iteration of the loop.
        #That means the vehicle has no real movement to plot.
        # 若该车轨迹长度小于等于1，说明未移动，跳过此次循环。
        if len(trajectory) <= 1:
            continue

        # np.arange(n) creates a sequence of integers from 0 to n−1.（横轴）
        # np.arange(n) 创建 0 到 n−1 的整数序列（横坐标代表时间步）。
        # Convert the trajectory list into a NumPy array for easier mathematical operations and plotting.
        # 将轨迹列表转换为 NumPy 数组，便于计算和绘图。
        time = np.arange(len(trajectory))
        positions = np.array(trajectory)

        # 检测车辆绕回位置
        # Detect wrap-around points where vehicle returns to start of circular road
        wrap_points = np.where(np.diff(positions) < 0)[0] + 1

        # 分段绘制，避免跨线
        # Split positions and time arrays at wrap points to avoid long connecting lines
        pos_segments = np.split(positions, wrap_points)
        time_segments = np.split(time, wrap_points)

        for t_seg, p_seg in zip(time_segments, pos_segments):
            t_seg = np.asarray(t_seg)
            p_seg = np.asarray(p_seg)
            plt.plot(t_seg, p_seg, color='blue', marker='o', linestyle='-', linewidth=1.5, markersize=2)

  
    # 横轴：时间步
    plt.xlabel("Time (steps)")
    # 纵轴：道路位置
    plt.ylabel("Position on Road")
    #Use f-string to show number of vehicles and road length.
    # 标题中使用 f-string 展示车辆数量与道路长度
    plt.title(f"Traffic Simulation\nVehicles: {len(road.get_vehicles())}, Road Length: {road_length}")
    #Add light background grid.
    # 添加浅色背景网格，便于阅读。
    plt.grid(True, alpha=0.3)
    #Keep y-axis (position) within road range.
    # 保持纵轴范围与道路长度一致。
    plt.ylim(0, road_length)
    #Automatically adjusts spacing.
    # 自动调整边距以防止标签被遮挡。
    plt.tight_layout()
    plt.show()





# Task 10: Run experiments 

def run_experiments(road_length: int, cell_size: float, signal_pos: int,
                    cycle_length: int, initial_positions: list,
                    initial_speeds: list, v_max: int, num_steps: int,
                    p: float, red_range) -> list:

    """Run traffic simulations with varying red signal durations and record
the total distance travelled by all vehicles.
Parameters:
road_length (int): Number of cells on the road.
cell_size (float): Length of each cell in meters.
signal_pos (int): Position of the traffic signal on the road.
cycle_length (int): Total signal cycle length (red + green time).
initial_positions (list[int]): Starting positions of vehicles.
initial_speeds (list[int]): Initial speeds of vehicles.
num_steps (int): Number of time steps to simulate.
v_max (int): Maximum allowed vehicle speed.
p (float): Probability of a random slowdown.
red_range (iterable[int]): Range of red times to test.
Returns:
list[dict]: A list of results, where each dictionary contains:
- "red_time" (int): Tested red signal duration.
- "total_distance" (int): Total distance travelled by all vehicles in
,
→ meters.
"""

    #Prepare a list to collect the result for each red time tested.
    results = []

    for red_time in red_range:
        # Build road and set signal
        road = Road(road_length)
        road.set_signal(signal_pos, red_time, cycle_length)

        # For each initial (position, speed) pair, create a Vehicle and add it to the road.
        # 逐个把“初始位置+初始速度”的车辆创建并加入道路。
        for pos, spd in zip(initial_positions, initial_speeds):
            road.add_vehicle(Vehicle(pos, spd))

        # Run the NaSch update loop for num_steps with max speed v_max and random slowdown prob p.
        # 运行 num_steps 个时间步，最大车速 v_max，随机减速概率 p。
        road.simulate(num_steps, v_max, p)

        # Compute total distance (sum of movements for all vehicles)
        # 统计器：累加所有车辆在所有时间步中移动的格数。
        total_cells = 0

        #For each vehicle, get its full trajectory (positions at t=0..num_steps).
        #逐车读取轨迹；长度通常是 num_steps + 1（含初始时刻）。
        for v in road.get_vehicles():
            traj = v.get_trajectory()# Vehicle’s full position history，长度应为 num_steps + 1

            #Look at consecutive positions to compute per-step movement.
            #查看相邻两时刻的位置，计算该步的位移。
            for i in range(1, len(traj)):
                prev_pos = traj[i - 1]
                curr_pos = traj[i]
                # If car moved normally → curr_pos >= prev_pos
                # else car wrapped around → add road_length
                step = curr_pos - prev_pos if curr_pos >= prev_pos else (curr_pos + road_length)- prev_pos
                # Add to total distance
                total_cells += step

        #Convert from cells to meters and record results
        #用每格长度 cell_size 把总格数换算为米数。
        total_distance_m = int(total_cells * float(cell_size))
        results.append({
            "red_time": int(red_time),
            "total_distance": int(total_distance_m)
        })

    # Return all experiment results
    return results


