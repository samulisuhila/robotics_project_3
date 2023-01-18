#pip install --upgrade pip /upgrade pip for opencv
#sudo pip3 install numpy

# https://raspberrypi-guide.github.io/programming/install-opencv
#sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev 
# libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev 
# libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y

#pip install numpy --upgrade  /if error 0xe to 0xd
#export PYTHONPATH="${PYTHONPATH}:/file/location/forscripts/here"  https://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath
#sudo pip3 install opencv-contrib-python /4.6.0.66 or 4.5.3.36
#sudo nano /boot/config.txt  /and these to bootconfig start_x=1 & gpu_mem=256

import multiprocessing #for multiple processes at a same time

import testi_mikki #importing voice recognition variable

import camera_module #camera_module file for camera vision
import move_module #move_module file for motor control

#cameratest.py cX / cY linefollowing values

import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685

#pin placements
#linetraking module pins
line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

#servos
camera_servo = 11

#positions
class positions:
    def __init__(pos, current_x,current_y,final_x,final_y):
        pos.current_x = current_x
        pos.current_y = current_y
        pos.final_x = final_x
        pos.final_y = final_y

    def starting_pos():
        print("running positions.starting.pos():")
        positions.current_x = 0
        positions.current_y = 0

    def return_pos():

        positions.final_x = 0
        positions.final_y = 0

    def item1():

        positions.final_x = 2
        positions.final_y = 2

    def item2():

        positions.final_x = 2
        positions.final_y = 1

    def item3():

        positions.final_x = 2
        positions.final_y = 0

robot_direction = 1 #1-4 for north-east-south-west / starting facing north

def setup():
    #setting up GPIO inputs and initial setup
    GPIO.setwarnings(False) #normally this is false, set to true for testing purposes
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)

    GPIO.setup(camera_servo,GPIO.OUT)

def camera_angle():
    #set camera angle to default
    ps = GPIO.PWM(camera_servo, 50) 
    ps.start(0) #servo initialization
    time.sleep(1)
    ps.ChangeDutyCycle(0) #pausing the cycle pulse for servo

def sensor_inputs(): 
    #multiprocessing need for this one
    #GPIO inputs for tracking sensors
    time.sleep(1)

    while(True): #add condition later/ turn off junction detection when picking up item
        sensor_right = GPIO.input(line_pin_right)
        sensor_middle = GPIO.input(line_pin_middle)
        sensor_left = GPIO.input(line_pin_middle)
        print("SL1: ",sensor_left,"SM2:",sensor_middle,"SR3:",sensor_right)
        if(sensor_left == 1 & sensor_middle == 1 & sensor_right ==1):
            print("junction found")
            print("robot direction is %d",robot_direction)
            time.sleep(0.4)
            if(robot_direction == 1): #north
                positions.current_y = positions.current_y + 1
                print("RD1",positions.current_y)
                continue
            elif(robot_direction == 2): #east
                positions.current_x = positions.current_x + 1
                print("RD2",positions.current_x)
                continue
            elif(robot_direction == 3): #south
                positions.current_y = positions.current_y - 1
                print("RD3",positions.current_y)
                continue
            elif(robot_direction == 4): #west
                positions.current_x = positions.current_x - 1
                print("RD4",positions.current_x)
                continue
            #print("Direction is",robot_direction,"so pos is",positions.current_x,positions.current_x)
        else:
            time.sleep(1)
            continue

def voice_command(voice_recognition):
    positions.starting_pos()
    if(voice_recognition == '1'):
        positions.item1

    elif(voice_recognition == '2'):
        positions.item2

    elif(voice_recognition == '3'):
        positions.item3
    else:
        print("voice command not recognised" + voice_recognition)
    return

def GPIO_cleanup():
    print("cleaning up the GPIO") #calling for the cleaning up of the GPIO ports
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    time.sleep(0.1)
    camera_angle()
    microphone_process1 = multiprocessing.Process(name = 'microphone_process1', target=testi_mikki.voice_recog)
    microphone_process1.start() # 1/4 process
    voice_command(testi_mikki.value)
    print("testimikki value %d",testi_mikki.value)
    microphone_process1.join()

    #sensor_inputs()

    positions.starting_pos()
    positions.item1()
    sensor_process1 = multiprocessing.Process(name='sensor_process1',target=sensor_inputs)
    sensor_process1.start() #1/4 processes
    print("starting camera process") #maxium of 4 different processes available / 1 process = 1 CPU core
    
    camera_process1 = multiprocessing.Process(name='camera_process1',target=camera_module.start_camera)
    camera_process1.start() #2/4 processes
    time.sleep(100)
    print("main stop camera")
    camera_process1.terminate() #1/4 processes

    time.sleep(0.1)
    #print(camera_process1, camera_process1.is_alive()) #process termination check
    camera_process2 = multiprocessing.Process(name='camera_process2',target=camera_module.stop_camera)
    camera_process2.start() #2/4 processes
    time.sleep(1)
    camera_process2.terminate() #1/4 processes
    sensor_process1.terminate() #0/4