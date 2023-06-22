# Instructions
This is a team project intended for the course Robotics, 2023 Spring, Leiden University.  \
Team: &lt; Pi team &gt; : Siwen Tu, Lin He, Ruilin Ma, Chenyu Shi, Shupei Li\

### Gesture control
#### Hardware environment
- Picar-4wd + RPi Camera v3 (wide)
- A computer with camera

#### Software environment
- picamera2
- opencv-python
- cvzone
- socket

#### Usage
1. Change the variable `host` (Line 5) in `hands_control_pc.py` to "your ip address". Open the port 6666.
2. Change the variable `host_ip` (Line 7) in `hands_control_car.py` to "your ip address".
3. Run `python3 hands_control_pc.py` on the computer.
4. Run `python3 hands_control_car.py` on the car.
5. Use gestures to control the car.

### Autonomous driving
#### Hardware enviornment
- Picar-4wd + RPi Camera v2
- Marking lines (colored tapes)

#### Software environment
- picamera
- opencv-python
- Time
- Picar_4wd


#### Usage
1. Run `python linetrack.py` on the computer.
2. Specify the parameters asked by the program, namely color, task index and threshold, with the following setting.
3. Set `color == orange` or `color == red_2` (orange is recommended.)
4. Set `Task index == 4`
5. Set `Threshold == 10`
6. The above default settings will execute the auto reverse parking of the robot.
