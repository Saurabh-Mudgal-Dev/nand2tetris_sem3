// Official CPU test script for Nand to Tetris Hardware Simulator
load ../hdl/CPU.hdl,
output-file ../CPU.out,
compare-to ../cmp/CPU.cmp,
output-list time%S0.4.0 inM%D1.6.1 instruction%B1.16.1 reset%B2.1.2 outM%D1.6.1 writeM%B2.1.2 addressM%D0.5.1 pc%D0.5.1;

// A-instruction: @12345
set inM 0,
set reset 0,
set instruction %B0011000000111001,
tick, tock, output;

// C-instruction: D=A
set instruction %B1110110000010000,
tick, tock, output;

// A-instruction: @23456
set instruction %B0101101110100000,
tick, tock, output;

// C-instruction: D=D-A
set instruction %B1110010011010000,
tick, tock, output;

// C-instruction: JGT
set instruction %B1110001100000001,
tick, tock, output;

// C-instruction: JEQ
set instruction %B1110001100000010,
tick, tock, output;

// C-instruction: JGE
set instruction %B1110001100000011,
tick, tock, output;

// C-instruction: JLT
set instruction %B1110001100000100,
tick, tock, output;

// C-instruction: JNE
set instruction %B1110001100000101,
tick, tock, output;

// C-instruction: JLE
set instruction %B1110001100000110,
tick, tock, output;

// C-instruction: JMP
set instruction %B1110001100000111,
tick, tock, output;

// Reset
set reset 1,
tick, tock, output;

// Continue after reset
set reset 0,
set instruction %B0000000000000000,
tick, tock, output;

// Test writeM and outM: M=D+1
set inM 3000,
set instruction %B1110011111001000,
tick, tock, output;

// Test inM with a-bit: D=D+M
set inM 500,
set instruction %B1111000010010000,
tick, tock, output;
