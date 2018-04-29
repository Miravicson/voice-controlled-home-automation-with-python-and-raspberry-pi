import RPi.GPIO as GPIO
import time
import os
import multiprocessing as mp


def ultrasonic(trig, echo, conn, name):
    GPIO.cleanup()
    os.system("sudo chown root.gpio /dev/gpiomem")
    os.system("sudo chmod g+rw /dev/gpiomem")

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    while True:
        GPIO.output(trig, False)  # Set the trig1 to low
        print(">>>>>>>>>>>>")
        time.sleep(1)  # Delay the sensor until it gets ready

        GPIO.output(trig, True)

        time.sleep(0.00001)

        GPIO.output(trig, False)

        pulse_start1 = 0
        pulse_end1 = 0

        while GPIO.input(echo) == 0:
            pulse_start1 = time.time()

        while GPIO.input(echo) == 1:
            pulse_end1 = time.time()

        pulse_duration1 = pulse_end1 - pulse_start1

        distance = pulse_duration1 * 17150

        distance = round(distance, 2)

        if distance > 2 and distance < 400:
            # print("{0}: {1} cm".format(name, distance1 - 0.5))
            conn.send([name, distance])

        else:
            conn.send([name, "Out of Range"])
            # print("{0}: Out of Range".format(name))


if __name__ == "__main__":
    def main():
        parent_conn1, child_conn1 = mp.Pipe()
        parent_conn2, child_conn2 = mp.Pipe()

        first_sensor = mp.Process(target=ultrasonic, args=(17, 22, child_conn1, "ultrasonic1"))
        second_sensor = mp.Process(target=ultrasonic, args=(14, 15, child_conn2, "ultrasonic2"))
        first_sensor.start()
        second_sensor.start()
        while True:
            distance1 = parent_conn1.recv()
            print("{0[0]} : {0[1]}".format(distance1))
            distance2 = parent_conn2.recv()
            print("{0[0]} : {0[1]}".format(distance2))

        first_sensor.join()
        second_sensor.join()

    main()