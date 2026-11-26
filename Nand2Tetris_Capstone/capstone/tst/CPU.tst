load ../hdl/CPU.hdl,
output-file ../CPU.out,
compare-to ../cmp/CPU.cmp,
output-list time%S0.4.0 inM%D1.6.1 instruction%B1.16.1 reset%B2.1.2 outM%D1.6.1 writeM%B2.1.2 addressM%D0.5.1 pc%D0.5.1;

// @12345, D=A, @23456, D=D-A
set inM 0, set reset 0, set instruction %B0011000000111001, tick, tock, output;
set instruction %B1110110000010000, tick, tock, output;
set instruction %B0101101110100000, tick, tock, output;
set instruction %B1110010011010000, tick, tock, output;

// Jump conditions (JGT, JEQ, JGE, JLT, JNE, JLE, JMP)
set instruction %B1110001100000001, tick, tock, output;
set instruction %B1110001100000010, tick, tock, output;
set instruction %B1110001100000011, tick, tock, output;
set instruction %B1110001100000100, tick, tock, output;
set instruction %B1110001100000101, tick, tock, output;
set instruction %B1110001100000110, tick, tock, output;
set instruction %B1110001100000111, tick, tock, output;

// Reset & continue
set reset 1, tick, tock, output;
set reset 0, set instruction %B0000000000000000, tick, tock, output;

// Memory operations: M=D+1, D=D+M
set inM 3000, set instruction %B1110011111001000, tick, tock, output;
set inM 500,  set instruction %B1111000010010000, tick, tock, output;
