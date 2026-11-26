// Box.asm: Renders a black box at row K=45, height 20, width 32 pixels (2 words)
// Row 45 start address: SCREEN + 32*45 = 16384 + 1440 = 17824

    @17824
    D=A
    @addr
    M=D        // addr = 17824

    @20
    D=A
    @r
    M=D        // r = 20 rows

(ROW_LOOP)
    // Draw 2 consecutive words (32 pixels) on current row
    @addr
    A=M
    M=-1       // Word 0
    A=A+1
    M=-1       // Word 1

    // Move addr to next row: addr = addr + 32
    @32
    D=A
    @addr
    M=D+M

    // Decrement row counter: r = r - 1
    @r
    MD=M-1
    @ROW_LOOP
    D;JGT      // Repeat while r > 0

(HALT)
    @HALT
    0;JMP
