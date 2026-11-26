// Box.asm: Interactive box program (K=45)
// Black box appears while any key is pressed; disappears when released
// Start row: 45 (addr = 16384 + 32*45 = 17824), Height: 20, Width: 2 words (32px)

(POLL_KBD)
    @KBD
    D=M
    @PRESSED
    D;JNE

    // Released: color = 0 (white)
    @color
    M=0
    @DRAW
    0;JMP

(PRESSED)
    // Pressed: color = -1 (black)
    @color
    M=-1

(DRAW)
    @17824
    D=A
    @addr
    M=D

    @20
    D=A
    @r
    M=D

(ROW_LOOP)
    @color
    D=M
    @addr
    A=M
    M=D
    A=A+1
    M=D

    // addr += 32
    @32
    D=A
    @addr
    M=D+M

    // r -= 1
    @r
    MD=M-1
    @ROW_LOOP
    D;JGT

    @POLL_KBD
    0;JMP
