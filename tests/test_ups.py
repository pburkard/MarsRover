from marsrovercore.modules.ups import UPS

def test_ups():
    ups = UPS(i2c_bus_number=1, i2c_address=0x40)
    result = ups.getVoltage()
    assert result > 0.0

