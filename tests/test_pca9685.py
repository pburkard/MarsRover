# from marsrovercore.modules.distance_vl53l0x import DistanceSensor
# rename classes to modules
def func(angle):
    from board import SCL, SDA
    import busio
    from adafruit_motor import servo
    from adafruit_pca9685 import PCA9685
    from time import sleep

    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 60
    sample_servo = servo.Servo(pca.channels[5], actuation_range=180, min_pulse=700, max_pulse=2700)
    sample_servo.angle = angle
    sleep(1)
    result = sample_servo.angle
    pca.deinit()
    return result

    

def test_answer():
    test_angle = 180
    precision = 1
    assert (test_angle-precision) <= func(test_angle) <= (test_angle+precision)