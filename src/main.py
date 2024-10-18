# Library imports
from vex import *

THRESHOLD = 3

# Brain should be defined by default
brain = Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)

left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)
drive_left = MotorGroup(left_motor_a, left_motor_b)

right_motor_a = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
right_motor_b = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
drive_right = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(drive_left, drive_right, 339.1, 350, 230, MM)


intake = Motor(Ports.PORT14)
intake.set_velocity(90, VelocityUnits.PERCENT)

grabber1 = DigitalOut(brain.three_wire_port.a)
grabber2 = DigitalOut(brain.three_wire_port.b)
isGrabbing = False
grabber1.set(isGrabbing)
grabber2.set(isGrabbing)

conveyor = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
conveyor.set_velocity(90,VelocityUnits.PERCENT)
conveyorOn = False

wait(30, MSEC)

# define variables used for controlling motors based on controller inputs
left_to_be_stopped = False
right_to_be_stopped = False
intake_is_stopped = False


def remote_control():
    
    global left_to_be_stopped, right_to_be_stopped, intake_is_stopped, conveyorOn, isGrabbing
    while True:

        drivetrain_left_speed = controller_1.axis4.position() * 0.75 - controller_1.axis2.position()
        drivetrain_right_speed = controller_1.axis4.position() * 0.75 + controller_1.axis2.position()


        if drivetrain_left_speed < THRESHOLD and drivetrain_left_speed > -THRESHOLD:
                # check if the left motor has already been stopped
                if left_to_be_stopped:
                    # stop the left drive motor
                    drive_left.stop()
                    # tell the code that the left motor has been stopped
                    left_to_be_stopped = False
                else:
                    # reset the toggle so that the deadband code knows to stop the left motor next
                    # time the input is in the deadband range
                    left_to_be_stopped = True

        if drivetrain_right_speed < THRESHOLD and drivetrain_right_speed > -THRESHOLD:
                # check if the right motor has already been stopped
                if right_to_be_stopped:
                    # stop the right drive motor
                    drive_left.stop()
                    # tell the code that the right motor has been stopped
                    right_to_be_stopped = False
                else:
                    # reset the toggle so that the deadband code knows to stop the right motor next
                    # time the input is in the deadband range
                    right_to_be_stopped = True

        # only tell the left drive motor to spin if the values are not in the deadband range
        if left_to_be_stopped:
            drive_left.set_velocity(drivetrain_left_speed, PERCENT)
            drive_left.spin(FORWARD)
        # only tell the right drive motor to spin if the values are not in the deadband range
        if right_to_be_stopped:
            drive_right.set_velocity(drivetrain_right_speed, PERCENT)
            drive_right.spin(FORWARD)

        # if controller_1.buttonR1.pressing():
        #     intake.spin(FORWARD)
        #     intake_is_stopped = False
        # elif controller_1.buttonR2.pressing():
        #     intake.spin(REVERSE)
        #     intake_is_stopped = False
        # elif not intake_is_stopped:
        #     intake.stop()
        #     # set the toggle so that we don't constantly tell the motor to stop when
        #     # the buttons are released
        #     intake_is_stopped = True


            
        if controller_1.buttonR2.pressing() :
             
            intake_is_stopped = not intake_is_stopped
            while controller_1.buttonR2.pressing() :
                pass

        if intake_is_stopped :
            intake.spin(REVERSE)
        else: 
            intake.stop()

        if conveyorOn :
            conveyor.spin(FORWARD)
        else :
            conveyor.stop()
        if controller_1.buttonL2.pressing() :
             
            conveyorOn = not conveyorOn
            while controller_1.buttonL2.pressing() :
                pass

        if conveyorOn :
            conveyor.spin(FORWARD)
        else :
            conveyor.stop()

        if controller_1.buttonA.pressing():
        # Toggle the piston state
            isGrabbing = not isGrabbing
            grabber1.set(isGrabbing)
            grabber2.set(isGrabbing)
        
        # Wait for the button to be released to avoid rapid toggling
            while controller_1.buttonA.pressing():
                pass
       
        

rc_auto_loop = Thread(remote_control)

def auton() :
    global drivetrain
    drivetrain.drive(FORWARD,400, VelocityUnits.RPM)
    wait(2,TimeUnits.SECONDS)
    drivetrain.stop
    

# def startup_brain():
#     skills = [20 + 130 + 170 + 20, 170, 100, 50]
#     brain.screen.set_font(FontType.MONO30)
#     brain.screen.set_fill_color(Color.WHITE)
#     brain.screen.draw_rectangle(0, 0, 480, 272)
#     brain.screen.set_pen_color(Color.BLUE)
#     #brain.screen.draw_rectangle(10, 10, 460, 74, Color.BLACK)
#     brain.screen.set_cursor(1,9)
#     brain.screen.print("THE VEX VILLAINS")

#     # Replace with photo of field
#     # brain.screen.draw_image_from_file('field.bmp', 155, 46)

#     brain.screen.set_pen_color(Color.BLACK)

#     # Create Skills button
#     brain.screen.set_fill_color(Color.YELLOW)
#     brain.screen.draw_rectangle(skills[0], skills[1], skills[2], skills[3])
#     brain.screen.set_cursor(11,24)
#     brain.screen.print("Skills")

#     while brain.screen.pressing() == False:
#         wait(5, MSEC)


# def pneumatic_on():
#     grabber.set(True)

# def pneumatic_off():
#     grabber.set(False)


# controller_1.buttonUp.pressed(pneumatic_on)
# controller_1.buttonDown.pressed(pneumatic_off)

# pneumatic_off()
# startup_brain()