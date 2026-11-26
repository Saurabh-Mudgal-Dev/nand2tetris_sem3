// Official ComputerAdd test script for Nand to Tetris Hardware Simulator
load ../hdl/Computer.hdl,
output-file ../ComputerAdd.out,
compare-to ../cmp/ComputerAdd.cmp,
output-list time%S0.4.0 reset%B2.1.2 ARegister[0]%D1.7.1 DRegister[0]%D1.7.1 PC[]%D0.4.1 RAM16K[0]%D1.7.1 RAM16K[1]%D1.7.1 RAM16K[2]%D1.7.1;

// Load Add.hack into ROM32K
ROM32K load ../hack/Add.hack,

// First run: compute 2 + 3
set reset 1,
tick, tock, output;

set reset 0,
repeat 14 {
    tick, tock, output;
}
