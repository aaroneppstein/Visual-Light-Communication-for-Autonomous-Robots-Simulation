"""drive_my_robot controller.py"""

# To run this code you need these libraries
# Use python -m pip install [library] to install on local
from controller import Robot
import time
from pandas import DataFrame
import numpy as np

if __name__ == "__main__":

    # create the Robot instance.
    robot = Robot()
    
    # get the time step of the current world.
    timestep = 64
    sample_period = 1000
    wheel_radius = .15 # Fill in wheel size
    linear_velocity = 1 # m/s, constant from our paper
    max_speed = linear_velocity/wheel_radius # angular velocity, rad/s. This drives the wheel motors
    
    
    # Created motor instances (may need to add two more)
    FL_motor = robot.getDevice('FrontMotor_L') # setting up motors. Based on our motor names which idk atm. I made this Front Left
    FR_motor = robot.getDevice('FrontMotor_R') # Front Right
    BL_motor = robot.getDevice('BackMotor_L') # Back Left
    BR_motor = robot.getDevice('BackMotor_R') # Back Right
    SenseLight = robot.getDevice('light_sensor')
    FL_position = robot.getDevice('FrontPosition_L')
    FR_position = robot.getDevice('FrontPosition_R')
    
    FL_motor.setPosition(float('inf')) # This sets motor position to infinity, but I'm not sure why. Comes from tutorial
    FL_motor.setVelocity(0.0) # Sets motor speed to 0.0
    
    FR_motor.setPosition(float('inf'))
    FR_motor.setVelocity(0.0)
    
    BL_motor.setPosition(float('inf'))
    BL_motor.setVelocity(0.0)
    
    BR_motor.setPosition(float('inf'))
    BR_motor.setVelocity(0.0)
    
    #Trying to setup light sensor
    
    class LightSensor:
        def enable(self, samplingPeriod): # Initially powering on sensor. Need to determine a sampling period
            return
        def getValue(self): # Gets light sensor value 
            return   #Right here you are just defining functions, getting the light sensor is later (during robot.step)
        def getSamplingPeriod(self):
            return 
        def disable(self):
            return
        def getLookupTable(self):
            return

    class PositionSensor:
        def enable(self,samplingPeriod):
            return
        def disable(self):
            return
        def getSamplingPeriod(self):
            return
        def getValue(self):
            return
        def getType(self):
            return

    '''def DataCollector(data):        #Over Complicating it cause I suck, just wanted to leave it in
        collected = []
        collected.append(data)
        return collected'''

    def DataExport(collected, position, elapsed):      #Data Export that has not been written yet
        time_elapsed = np.linspace(0,elapsed, num = len(collected))
        df = DataFrame({'Time':time_elapsed, 'Irradiance (Light Sensor)':collected, 'Position (m)':position})
        df.to_csv('data/53.25_cutoff.csv')
        return 

    SenseLight.enable(timestep)
    FL_position.enable(timestep)
    FR_position.enable(timestep)
    Light_Array = []
    Position_Array = []
    t = time.time()
    timestop = 25
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1: # Looks like the robot will just run indefinitely

    #Enabling Light Sensor
    
    Light_Val = SenseLight.getValue()
    print(Light_Val)
    
    Light_Array.append(Light_Val)
    
    PosL_Val = FR_position.getValue()
    PosR_Val = FR_position.getValue()

    Pos_Val = (PosL_Val + PosR_Val) / 2
    
    Position_Array.append(Pos_Val)
    
    # Setting motor speeds 
    FL_speed = 0.5*max_speed
    FR_speed = 0.5*max_speed
    BL_speed = 0.5*max_speed
    BR_speed = 0.5*max_speed

    FL_motor.setVelocity(FL_speed)
    FR_motor.setVelocity(FR_speed)
    BL_motor.setVelocity(BL_speed)
    BR_motor.setVelocity(BR_speed)

# I think we'd need to test the light sensor values under the blue light to determine our threshold for turning around

    if Light_Val >= 800:         #if light value is greater than or equal to some threshold..
        
        # Turn around. Will need to figure out how long a 180° turn takes
        FL_speed = 0
        FR_speed = 0
        BL_speed = 0
        BR_speed = 0

        FL_motor.setVelocity(FL_speed)
        FR_motor.setVelocity(FR_speed)
        BL_motor.setVelocity(BL_speed)
        BR_motor.setVelocity(BR_speed)

        elapsed = time.time() - t
        print('Time of Simulation: ',elapsed)
        DataExport(Light_Array,Position_Array,elapsed)
        break
    
    if time.time()-t > timestop:
        print('Time Exceeded 25s, minimum Light Sensor Value not reached')
        DataExport(Light_Array,Position_Array,timestop)
        break

   
   
    # Enter here exit cleanup code.
    