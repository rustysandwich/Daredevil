/*
 * Copyright (c) 2026
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (0=input, 1=output)
    input  wire       ena,      // Module enable pin
    input  wire       clk,      // Clock signal
    input  wire       rst_n     // Reset pin (active low)
);

  // =========================================================================
  // 1. EXPLICIT SIGNAL BREAKOUT (These names will now appear in GTKWave)
  // =========================================================================
  wire [3:0] INP = ui_in[3:0];  // 4-bit Write Data
  wire [2:0] RD  = ui_in[6:4];  // 3-bit Write Register Address (DEMUX select)
  wire [2:0] RA  = uio_in[2:0]; // 3-bit Read Address Port A (MUX A select)
  wire [2:0] RB  = uio_in[5:3]; // 3-bit Read Address Port B (MUX B select)

  wire [3:0] A;                 // 4-bit Output Port A
  wire [3:0] B;                 // 4-bit Output Port B

  // Map internal outputs to Tiny Tapeout output bus
  assign uo_out[3:0] = A;
  assign uo_out[7:4] = B;

  // Set unused IO pins
  assign uio_out = 8'b00000000;
  assign uio_oe  = 8'b00000000;

  // =========================================================================
  // 2. REGISTER FILE CORE (DEMUX + 8 REGISTERS + MUX A + MUX B)
  // =========================================================================
  reg [3:0] registers [0:7];
  integer i;

  // DEMUX & Synchronous Write Logic
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      for (i = 0; i < 8; i = i + 1) begin
        registers[i] <= 4'b0000;
      end
    end else if (ena) begin
      registers[RD] <= INP;     // Route write to register[RD]
    end
  end

  // MUX Read Logic (Combinational / Instant)
  assign A = registers[RA];     // MUX A routes register[RA] to output A
  assign B = registers[RB];     // MUX B routes register[RB] to output B

  // Prevent linter warnings for unused bus bits
  wire _unused = &{ui_in[7], uio_in[7:6], 1'b0};

endmodule