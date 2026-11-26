// Official ComputerMax test script for Nand to Tetris Hardware Simulator
load ../hdl/Computer.hdl,
output-file ../ComputerMax.out,
compare-to ../cmp/ComputerMax.cmp,
output-list time%S0.4.0 reset%B2.1.2 ARegister[0]%D1.7.1 DRegister[0]%D1.7.1 PC[]%D0.4.1 RAM16K[0]%D1.7.1 RAM16K[1]%D1.7.1 RAM16K[2]%D1.7.1;

// Load Max.hack into ROM32K
ROM32K load ../hack/Max.hack,

// First run: test max(3, 5)
set RAM16K[0] 3,
set RAM16K[1] 5,
set reset 1,
tick, tock, output;

set reset 0,
repeat 14 {
    tick, tock, output;
}

// Second run: test max(23456, 12345)
set RAM16K[0] 23456,
set RAM16K[1] 12345,
set reset 1,
tick, tock, output;

set reset 0,
repeat 14 {
    tick, tock, output;
}
