from litex.gen import *

from litevideo.input import HDMIIn
from litevideo.output import VideoOut
from litedram.common import LiteDRAMPort

from gateware import freq_measurement
from gateware import i2c

from targets.utils import csr_map_update, period_ns

#from targets.netv2.pcie import SoC as BaseSoC
from targets.netv2.base import SoC as BaseSoC


class VideoSoC(BaseSoC):
    csr_peripherals = {
        "hdmi_out0",
        "hdmi_in0",
        "hdmi_in0_freq",
        "hdmi_in0_edid_mem",
        "hdmi_in1",
        "hdmi_in1_freq",
        "hdmi_in1_edid_mem",
    }
    csr_map_update(BaseSoC.csr_map, csr_peripherals)
    
    interrupt_map = {
        "hdmi_in0": 3,
        "hdmi_in1": 4,
    }
    interrupt_map.update(BaseSoC.interrupt_map)

    def __init__(self, platform, *args, **kwargs):
        BaseSoC.__init__(self, platform, *args, **kwargs)

        # # #

        # hdmi out 0
        hdmi_out0_pads = platform.request("hdmi_out", 0)

        mode = "ycbcr422"

        if mode == "ycbcr422":
            hdmi_out0_dram_port = self.sdram.crossbar.get_port(mode="read", dw=16, cd="hdmi_out0_pix", reverse=True)
            self.submodules.hdmi_out0 = VideoOut(platform.device,
                                                 hdmi_out0_pads,
                                                 hdmi_out0_dram_port,
                                                 "ycbcr422")
        elif mode == "rgb":
            hdmi_out0_dram_port = self.sdram.crossbar.get_port(mode="read", dw=32, cd="hdmi_out0_pix", reverse=True)
            self.submodules.hdmi_out0 = VideoOut(platform.device,
                                                 hdmi_out0_pads,
                                                 hdmi_out0_dram_port,
                                                 "rgb")

        self.platform.add_period_constraint(self.crg.cd_sys.clk, 10.0)
        self.platform.add_period_constraint(self.hdmi_out0.driver.clocking.cd_pix.clk, 10.0)
        self.platform.add_false_path_constraints(
            self.crg.cd_sys.clk,
            self.hdmi_out0.driver.clocking.cd_pix.clk)

        pix_freq = 148.50e6
        
        # hdmi in 0
        hdmi_in0_pads = platform.request("hdmi_in", 0)

        self.submodules.hdmi_in0 = HDMIIn(
            hdmi_in0_pads,
            self.sdram.crossbar.get_port(mode="write"),
            fifo_depth=512,
            device="xc7")

        self.submodules.hdmi_in0_freq = freq_measurement.FrequencyMeasurement(
            self.hdmi_in0.clocking.clk_input, measure_period=self.clk_freq)

        self.platform.add_period_constraint(self.hdmi_in0.clocking.cd_pix.clk, period_ns(1*pix_freq))
        self.platform.add_period_constraint(self.hdmi_in0.clocking.cd_pix1p25x.clk, period_ns(1.25*pix_freq))
        self.platform.add_period_constraint(self.hdmi_in0.clocking.cd_pix5x.clk, period_ns(5*pix_freq))

        self.platform.add_false_path_constraints(
            self.crg.cd_sys.clk,
            self.hdmi_in0.clocking.cd_pix.clk,
            self.hdmi_in0.clocking.cd_pix1p25x.clk,
            self.hdmi_in0.clocking.cd_pix5x.clk)
        
        # hdmi in 1
        hdmi_in1_pads = platform.request("hdmi_ov", 0)

        self.submodules.hdmi_in1 = HDMIIn(
            hdmi_in1_pads,
            self.sdram.crossbar.get_port(mode="write"),
            fifo_depth=512,
            device="xc7")

        self.submodules.hdmi_in1_freq = freq_measurement.FrequencyMeasurement(
            self.hdmi_in1.clocking.clk_input, measure_period=self.clk_freq)

        self.platform.add_period_constraint(self.hdmi_in1.clocking.cd_pix.clk, period_ns(1*pix_freq))
        self.platform.add_period_constraint(self.hdmi_in1.clocking.cd_pix1p25x.clk, period_ns(1.25*pix_freq))
        self.platform.add_period_constraint(self.hdmi_in1.clocking.cd_pix5x.clk, period_ns(5*pix_freq))

        self.platform.add_false_path_constraints(
            self.crg.cd_sys.clk,
            self.hdmi_in1.clocking.cd_pix.clk,
            self.hdmi_in1.clocking.cd_pix1p25x.clk,
            self.hdmi_in1.clocking.cd_pix5x.clk)
        

        # FIXME: Fix the HDMI out so this can be removed.
        platform.add_platform_command(
            """PIN "hdmi_out_pix_bufg.O" CLOCK_DEDICATED_ROUTE = FALSE;""")
        platform.add_platform_command(
            """PIN "hdmi_out_pix_bufg_1.O" CLOCK_DEDICATED_ROUTE = FALSE;""")
        # We have CDC to go from sys_clk to pixel domain
        platform.add_platform_command(
            """
NET "{pix0_clk}" TNM_NET = "GRPpix0_clk";
""",
                pix0_clk=self.hdmi_out0.driver.clocking.cd_pix.clk,
        )
        self.platform.add_false_path_constraints(
            self.crg.cd_sys.clk,
            self.hdmi_out0.driver.clocking.cd_pix.clk)
        
SoC = VideoSoC
