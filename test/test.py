# SPDX-FileCopyrightText: © 2026
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


# Helper function to pack Write Address (RD) and Data (INP) onto ui_in
def write_register(dut, rd_addr: int, inp_data: int):
    # ui_in[6:4] = RD, ui_in[3:0] = INP
    dut.ui_in.value = ((rd_addr & 0x7) << 4) | (inp_data & 0xF)


# Helper function to pack Read Addresses (RA, RB) onto uio_in
def set_read_addresses(dut, ra_addr: int, rb_addr: int):
    # uio_in[5:3] = RB, uio_in[2:0] = RA
    dut.uio_in.value = ((rb_addr & 0x7) << 3) | (ra_addr & 0x7)


@cocotb.test()
async def test_register_file(dut):
    dut._log.info("--- Starting Register File Simulation ---")

    # 1. Setup Clock (100 kHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # 2. Reset Phase
    dut._log.info("Asserting Reset...")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 1  # Release reset
    await ClockCycles(dut.clk, 1)

    # 3. Write Phase: Store 0xA (10) into Register 2
    dut._log.info("Writing 0xA into Register 2 (RD=2, INP=0xA)...")
    write_register(dut, rd_addr=2, inp_data=0xA)
    await ClockCycles(dut.clk, 1)  # Trigger posedge clk write

    # 4. Write Phase: Store 0x5 (5) into Register 5
    dut._log.info("Writing 0x5 into Register 5 (RD=5, INP=0x5)...")
    write_register(dut, rd_addr=5, inp_data=0x5)
    await ClockCycles(dut.clk, 1)  # Trigger posedge clk write

    # 5. Read Phase: Read Register 2 on Port A (RA=2) and Register 5 on Port B (RB=5)
    dut._log.info("Reading Register 2 on Port A and Register 5 on Port B...")
    set_read_addresses(dut, ra_addr=2, rb_addr=5)
    await ClockCycles(dut.clk, 1)

    # 6. Verify Outputs
    # Expected Port A = 0xA (10), Port B = 0x5 (5) -> Combined uo_out = 0x5A
    port_a_val = int(dut.uo_out.value) & 0x0F
    port_b_val = (int(dut.uo_out.value) >> 4) & 0x0F

    dut._log.info(
        f"Read Results -> Port A: {hex(port_a_val)}, Port B: {hex(port_b_val)}"
    )

    assert port_a_val == 0xA, f"Port A mismatch! Expected 0xA, got {hex(port_a_val)}"
    assert port_b_val == 0x5, f"Port B mismatch! Expected 0x5, got {hex(port_b_val)}"

    dut._log.info("--- TEST PASSED SUCCESSFULLY ---")