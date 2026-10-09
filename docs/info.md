<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works
 8 different registers, which gather and store information based on the input, then the registers share this info with the output that it is connected to.

## How to test

Give a binary value input; give a value to the demux, which then picks one of the 8 registers; then give the same register number to the demultiplexers to get the different values.
Another way to test is to give one register an input, receive an output, and then do the same with another register with another output.

## External hardware

An output point where you take and check the binary value output for the registers.
