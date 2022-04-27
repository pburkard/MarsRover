from marsrovercore.modules.ups import UPS

def test_ups():
    ups = UPS(i2c_bus_number=1, i2c_address=0x40)
    result = ups.getVoltage()
    assert result > 0.0

def test_ups_raw():
    from ina219 import INA219, DeviceRangeError
    SHUNT_OHMS = 0.05
    """Define method to read information from coulometer."""
    ina = INA219(SHUNT_OHMS, busnum=1, address=0x40)
    ina.configure()
    voltage_v = ina.voltage()
    current_mA = ina.current()
    power_mW = ina.power()
    shunt_voltage_mV = ina.shunt_voltage()
    # print("Bus Voltage: %.3f V" % ina.voltage())
    # try:
    #     print("Bus Current: %.3f mA" % ina.current())
    #     print("Power: %.3f mW" % ina.power())
    #     print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    # except DeviceRangeError as e:
    #     print(e)