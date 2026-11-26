// Official ComputerRect test script for Nand to Tetris Hardware Simulator
load ../hdl/Computer.hdl,
output-file ../ComputerRect.out,
compare-to ../cmp/ComputerRect.cmp,
output-list time%S0.4.0 reset%B2.1.2 ARegister[0]%D1.7.1 DRegister[0]%D1.7.1 PC[]%D0.4.1 RAM16K[0]%D1.7.1 RAM16K[16]%D1.7.1 RAM16K[17]%D1.7.1;

// Load Rect.hack into ROM32K
ROM32K load ../hack/Rect.hack,

set RAM16K[0] 4,
set reset 1,
tick, tock, output;

set reset 0,
repeat 64 {
    tick, tock, output;
}
