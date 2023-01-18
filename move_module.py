import time
import RPi.GPIO as GPIO

#speed factor
ms = 100
#turning radius factor
radius = 0.6
#motor pins
Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 14
Motor_A_Pin2  = 15
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

def motor_setup():
    
    global pwm_A,pwm_B #PWM for motors
    GPIO.setup(Motor_A_EN,GPIO.OUT)
    GPIO.setup(Motor_B_EN,GPIO.OUT)
    GPIO.setup(Motor_A_Pin1,GPIO.OUT)
    GPIO.setup(Motor_A_Pin2,GPIO.OUT)
    GPIO.setup(Motor_B_Pin1,GPIO.OUT)
    GPIO.setup(Motor_B_Pin2,GPIO.OUT)

    full_stop() #stopping motors at setup
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000) #default PWM 1000 changing speed
        pwm_B = GPIO.PWM(Motor_B_EN, 1000)

    except:
        pass

def full_stop():
    print("move_module.full_stop called")
    GPIO.output(Motor_A_Pin1,GPIO.LOW)
    GPIO.output(Motor_A_Pin2,GPIO.LOW)
    GPIO.output(Motor_B_Pin1,GPIO.LOW)
    GPIO.output(Motor_B_Pin2,GPIO.LOW)
    GPIO.output(Motor_A_EN,GPIO.LOW)
    GPIO.output(Motor_B_EN,GPIO.LOW)

    pwm_A.ChangeDutyCycle(0)
    pwm_B.ChangeDutyCycle(0)
    

def move_right90():
    print("Turning right")
    #direction change will be transferred to gridtest.py
    if(robot_direction == 4):
        robot_direction = 1
    else:
        robot_direction = robot_direction + 1
    #turning the robot 90 degrees to the right
    
    
def move_left90():
    print("Turning left")
    #direction change will be transferred to gridtest.py
    if(robot_direction == 1):
        robot_direction = 4
    else:
        robot_direction = robot_direction - 1
    #turning the robot 90 degrees to the left

def move_motor1(motor1_pwm):
    #motor1_pwm = 100
    print("Motor1 forward")
    GPIO.output(Motor_A_Pin1, GPIO.HIGH)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    pwm_A.start(motor1_pwm)
    pwm_A.ChangeDutyCycle(ms)

def move_motor2(motor2_pwm):
    #motor2_pwm = 100
    print("Motor2 forward")
    GPIO.output(Motor_B_Pin1, GPIO.HIGH)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    pwm_B.start(motor2_pwm)
    pwm_B.ChangeDutyCycle(ms)

def move_forward(a,b):
    move_motor1(a)
    move_motor2(b)

def move_backwards():
    print("Going backwards")


if __name__ == "__main__":
    print("starting main")
    move_forward(70,70)
    time.sleep(15)
    full_stop()