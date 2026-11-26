// Official Memory test script for Nand to Tetris Hardware Simulator
load Memory.hdl,
output-file Memory.out,
compare-to Memory.cmp,
output-list time%S1.4.1 in%D1.6.1 load%B2.1.2 address%B1.15.1 out%D1.6.1;

// RAM tests
set in -1,
set load 0,
set address 0,
tick,
tock,
output;

set load 1,
tick,
tock,
output;

set in 9999,
set load 0,
set address %X2000,
tick,
tock,
output;

set load 1,
tick,
tock,
output;

set in 0,
set load 0,
set address 0,
tick,
tock,
output;

set address %X2000,
tick,
tock,
output;

// Screen tests
set in 1234,
set address %X4000,
tick,
tock,
output;

set load 1,
tick,
tock,
output;

set in 5678,
set load 0,
set address %X5000,
tick,
tock,
output;

set load 1,
tick,
tock,
output;

set address %X4000,
tick,
tock,
output;

// Keyboard test
set address %X6000,
set load 0,
tick,
tock,
output;
