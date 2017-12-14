from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, VivadoProgrammer

_io = [
    # U11F
    ("clk50", 0, Pins("J19"), IOStandard("LVCMOS33")),

    ("user_led", 0, Pins("M21"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("E14")), # MCU_RX
        Subsignal("rx", Pins("E13")), # MCU_TX
        IOStandard("LVCMOS33"),
    ),

    ("ddram", 0,
        Subsignal("a", Pins(
            "U6 V4 W5 V5 AA1 Y2 AB1 AB3 AB2 Y3 W6 Y1 V2 AA3"
            ),
            IOStandard("SSTL15")),
        Subsignal("ba", Pins("U5 W4 V7"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("Y9"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("Y7"), IOStandard("SSTL15")),
        Subsignal("we_n", Pins("V8"), IOStandard("SSTL15")),
        Subsignal("dm", Pins("G1 H4 M5 L3"), IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "C2 F1 B1 F3 A1 D2 B2 E2 "
            "J5 H3 K1 H2 J1 G2 H5 G3 "
            "N2 M6 P1 N5 P2 N4 R1 P6 "
            "K3 M2 K4 M3 J6 L5 J4 K6 "
            ),
            IOStandard("SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_p", Pins("E1 K2 P5 M1"), IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("D1 J2 P4 L1"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("R3"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("R2"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke", Pins("Y8"), IOStandard("SSTL15")),
        Subsignal("odt", Pins("W9"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("AB5"), IOStandard("LVCMOS15")),
        Subsignal("cs_n", Pins("V9"), IOStandard("SSTL15")),
        Misc("SLEW=FAST"),
    ),

    ("hdmi_in", 0,
        Subsignal("clk_p", Pins("L19"), IOStandard("TMDS_33")),
        Subsignal("clk_n", Pins("L20"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("K21"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("K22"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("J20"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("J21"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("J22"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("H22"), IOStandard("TMDS_33")),
        Subsignal("scl", Pins("T18"), IOStandard("LVCMOS33")), 
        Subsignal("sda", Pins("V18"), IOStandard("LVCMOS33")), 
    ),

    ("hdmi_ov", 0,
        Subsignal("clk_p", Pins("Y18"), IOStandard("TMDS_33")),
        Subsignal("clk_n", Pins("Y19"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("AA18"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("AB18"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("AA19"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("AB20"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("AB21"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("AB22"), IOStandard("TMDS_33")),
        Subsignal("scl", Pins("W17"), IOStandard("LVCMOS33")), 
        Subsignal("sda", Pins("R17"), IOStandard("LVCMOS33")), 
    ),

# TX0
    ("hdmi_out", 0,
        Subsignal("clk_p", Pins("W19"), IOStandard("TMDS_33")),
        Subsignal("clk_n", Pins("W20"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("W21"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("W22"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("U20"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("V20"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("T21"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("U21"), IOStandard("TMDS_33")),
        IOStandard("TMDS_33")
    ),

# TX1
#    ("hdmi_out", 0,
#        Subsignal("clk_p", Pins("G21"), IOStandard("TMDS_33")),
#        Subsignal("clk_n", Pins("G22"), IOStandard("TMDS_33")),
#        Subsignal("data0_p", Pins("E22"), IOStandard("TMDS_33")),
#        Subsignal("data0_n", Pins("D22"), IOStandard("TMDS_33")),
#        Subsignal("data1_p", Pins("C22"), IOStandard("TMDS_33")),
#        Subsignal("data1_n", Pins("B22"), IOStandard("TMDS_33")),
#        Subsignal("data2_p", Pins("B21"), IOStandard("TMDS_33")),
#        Subsignal("data2_n", Pins("A21"), IOStandard("TMDS_33")),
#        IOStandard("TMDS_33")
#    ),

    ("hdmi_sda_over_up", 0, Pins("G20"), IOStandard("LVCMOS33")),
    ("hdmi_sda_over_dn", 0, Pins("F20"), IOStandard("LVCMOS33")),
    ("hdmi_hdp_over", 0, Pins("M22"), IOStandard("LVCMOS33")),

]


class Platform(XilinxPlatform):
    name = "netv2"
    default_clk_name = "clk50"
    default_clk_period = 20.0

    # From https://www.xilinx.com/support/documentation/user_guides/ug470_7Series_Config.pdf
    # 17536096 bits == 2192012 == 0x21728c -- Therefore 0x220000
    gateware_size = 0x220000

    # ???
    # FIXME: Create a "spi flash module" object in the same way we have SDRAM
    # module objects.
    spiflash_read_dummy_bits = 10
    spiflash_clock_div = 4
    spiflash_total_size = int((256/8)*1024*1024) # 256Mbit
    spiflash_page_size = 256
    spiflash_sector_size = 0x10000
    spiflash_model = "n25q128"

    def __init__(self, toolchain="vivado", programmer="vivado"):
        XilinxPlatform.__init__(self, "xc7a35t-fgg484-2", _io,
                                toolchain=toolchain)

        self.add_platform_command(
            "set_property CONFIG_VOLTAGE 1.5 [current_design]")
        self.add_platform_command(
            "set_property CFGBVS GND [current_design]")
        self.add_platform_command(
            "set_property BITSTREAM.CONFIG.CONFIGRATE 22 [current_design]")
        self.add_platform_command(
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 1 [current_design]")
        self.toolchain.bitstream_commands = [
            "set_property CONFIG_VOLTAGE 1.5 [current_design]",
            "set_property CFGBVS GND [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 22 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 1 [current_design]",
        ]
        self.toolchain.additional_commands = \
            ["write_cfgmem -verbose -force -format bin -interface spix1 -size 64 "
             "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]
        self.programmer = programmer

        self.add_platform_command("""
create_clock -name pcie_phy_clk -period 10.0 [get_pins {{pcie_phy/pcie_support_i/pcie_i/inst/inst/gt_top_i/pipe_wrapper_i/pipe_lane[0].gt_wrapper_i/gtp_channel.gtpe2_channel_i/TXOUTCLK}}]
""")

    def create_programmer(self):
        if self.programmer == "vivado":
            return VivadoProgrammer(flash_part="n25q128-3.3v-spi-x1_x2_x4")
        else:
            raise ValueError("{} programmer is not supported"
                             .format(self.programmer))

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
