from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, VivadoProgrammer

_io = [
    # U11F
    ("clk50", 0, Pins("L19"), IOStandard("LVCMOS33")),

    ("user_led", 0, Pins("G22"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("H22")), # MCU_RX
        Subsignal("rx", Pins("J22")), # MCU_TX
        IOStandard("LVCMOS33"),
    ),

    ("ddram", 0,
        Subsignal("a", Pins(
            "AB2 AB3 AB1 AA1 V3 U3 Y1 W1 Y2",
            "W2 V2 U2 U1 T1"),
            IOStandard("SSTL15")),
        Subsignal("ba", Pins("AA5 AA3 Y3"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("AB5"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("Y4"), IOStandard("SSTL15")),
        Subsignal("we_n", Pins("AA4"), IOStandard("SSTL15")),
        Subsignal("dm", Pins("B1 K1 M3 N4"), IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "A1 C2 B2 E2 D2 G1 F1 F3 "
            "J1 H2 G2 J5 H5 H3 G3 H4 "
            "K4 J4 L3 K3 M2 K6 J6 L5 "
            "R1 P1 P2 N2 M6 M5 P6 N5 "
            ),
            IOStandard("SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_p", Pins("E1 K2 M1 P5"), IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("D1 J2 L1 P4"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("R3"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("R2"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke", Pins("W6"), IOStandard("SSTL15")),
        Subsignal("odt", Pins("W5"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("G4"), IOStandard("LVCMOS15")),
        Subsignal("cs_n", Pins("V4"), IOStandard("SSTL15")),
        Misc("SLEW=FAST"),
    ),

    ("hdmi_in", 0,
        Subsignal("clk_p", Pins("Y18"), IOStandard("TMDS_33")),
        Subsignal("clk_n", Pins("Y19"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("AB21"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("AB22"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("AA19"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("AB20"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("AA18"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("AB18"), IOStandard("TMDS_33")),
        Subsignal("scl", Pins("L20"), IOStandard("LVCMOS33")), 
        Subsignal("sda", Pins("H20"), IOStandard("LVCMOS33")), 
    ),

    ("hdmi_ov", 0,
        Subsignal("clk_p", Pins("J20"), IOStandard("TMDS_33")),
        Subsignal("clk_n", Pins("J21"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("K21"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("K22"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("M21"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("L21"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("N22"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("M22"), IOStandard("TMDS_33")),
        Subsignal("scl", Pins("G17"), IOStandard("LVCMOS33")), 
        Subsignal("sda", Pins("H17"), IOStandard("LVCMOS33")), 
    ),

    ("hdmi_out", 0,
        Subsignal("clk_p", Pins("W19"), IOStandard("TMDS_33")),
        Subsignal("clk_n", Pins("W20"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("T21"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("U21"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("U22"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("V22"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("W21"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("W22"), IOStandard("TMDS_33")),
        IOStandard("TMDS_33")
    ),

    ("hdmi_sda_over_up", 0, Pins("G20"), IOStandard("LVCMOS33")),
    ("hdmi_sda_over_dn", 0, Pins("H20"), IOStandard("LVCMOS33")),
    ("hdmi_hdp_over", 0, Pins("H22"), IOStandard("LVCMOS33")),

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
        XilinxPlatform.__init__(self, "xc7a15t-fgg484-2", _io,
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
