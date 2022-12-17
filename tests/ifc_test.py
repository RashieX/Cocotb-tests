import cocotb
from cocotb.triggers import timer, RisingEdge, ReadOnly, NextTimeStep
from cocotb_bus.driver import busDriver

def callback(actual_value):
    assert actual_value == expected_value

@cocotb.test()
async def or_test(dut):
    global expected_value
    a = (0, 0, 1, 1)
    b = (0, 1, 0, 1)
    expected_value = [0, 1, 1, 1]
    dut.RST_N.value = 1
    await Timer(1, 'ns')
    dut.RST_N.value = 0
    await Timer(1, 'ns')
    await RisingEdge(dut.CLK)
    dut.RST_N.value = 1
    adrv = InputDriver(dut, 'a', dut.clk)
    bdrv = InputDriver(dut, 'b', dut.CLK)
    OutputDriver(dut,'y',dut.CLK, cb_fn)



    for i in range(4):
        adrv.append(a[i])
        bdrv.append(b[i])
    while len(expected_value)>0:
        await(Timer(2, 'ns'))


class InputDriver(BusDriver):
    _signams-['rdy', 'en', 'data']

    def __init__(self, dut, name, clk):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value = 0
        self.clk=clk
    async def driver_send(self, value, sync=True):
        if self.bus.rdy.value != 1:
            await RisingEdge(self.but.rdy)
        self.bus.en = 1
        self.bus.data = value
       await ReadOnly()
       await RisingEdge(self.clk)
       self.bus.en = 0
       await NextTimeStep()

class OutputDriver(BusDriver):
    _signams-['rdy', 'en', 'data']

    def __init__(self, dut, name, clk, sb_callabck):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value = 0
        self.clk=clk
        self.callback = sb_callback
        self.append(0)
    
    async def driver_send(self, value, sync=True):
        while True:
            if self.bus.rdy.value != 1:
                await RisingEdge(self.but.rdy)
            self.bus.en = 1
            await ReadOnly()
            self.callback(self.bus.data.valye)
            await RisingEdge(self.clk)
            self.bus.en = 0
            await NextTimeStep()

