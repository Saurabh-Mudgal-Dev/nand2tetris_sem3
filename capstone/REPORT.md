# Capstone Project Report: Make the Computer Draw a Box
**Nand to Tetris – I (ETCCNT301)**  
**School of Engineering & Technology, K.R. Mangalam University**

* **Student Name:** Saurabh
* **Roll Number:** 2501010045
* **Personal Number ($K$):** 45 (last two digits of roll number)

---

## 1. Personal Parameters & Geometry Calculations

* **Calculation of $K$:** $\text{Roll No.} = 2501010045 \implies K = 45$.
* **Box Start Row:** Row $K = 45$.
* **Box Height:** $20$ scanlines (rows 45 through 64).
* **Box Width:** 
  $$\text{Width} = 16 \times ((K \bmod 4) + 1) = 16 \times ((45 \bmod 4) + 1) = 16 \times (1 + 1) = 32\text{ pixels}$$
  $$\text{Word Width} = (K \bmod 4) + 1 = 2\text{ words per row}$$
* **Screen Base Memory Address:**
  $$\text{Start Address} = \text{SCREEN} + 32 \times K = 16384 + 32 \times 45 = 16384 + 1440 = 17824$$
* **Assembler Variant Feature ($K \bmod 3$):**
  $$45 \bmod 3 = 0$$
  **Feature:** Save all labels and variables with their memory addresses in `symbols.txt`.

---

## 2. Part A: Computer Architecture (HDL)

### Component Implementation Details:
1. **`Memory.hdl`**: Decodes address lines:
   * `address[14] == 0`: RAM16K (`0x0000`–`0x3FFF`).
   * `address[14] == 1, address[13] == 0`: Screen memory map (`0x4000`–`0x5FFF`).
   * `address[14] == 1, address[13] == 1`: Keyboard register (`0x6000`).
   * `load` signal is demultiplexed so Keyboard is read-only.
2. **`CPU.hdl`**: Decodes A- and C-instructions, routes ALU operands between A and M, writes to `outM`, drives `addressM`, and executes branch conditions (`JGT`, `JEQ`, `JGE`, `JLT`, `JNE`, `JLE`, `JMP`) via Program Counter (`PC`).
3. **`Computer.hdl`**: Integrates `ROM32K`, `CPU`, and `Memory` into a unified computing platform.

### Test Verification Summary:
| Test Script | Status | Screenshot Reference |
| :--- | :--- | :--- |
| `Memory.tst` | Comparison ended successfully | *[Insert Memory.png]* |
| `CPU.tst` | Comparison ended successfully | *[Insert CPU.png]* |
| `ComputerAdd.tst` | Comparison ended successfully | *[Insert ComputerAdd.png]* |
| `ComputerMax.tst` | Comparison ended successfully | *[Insert ComputerMax.png]* |
| `ComputerRect.tst` | Comparison ended successfully | *[Insert ComputerRect.png]* |

---

## 3. Part B: Python Hack Assembler

### Architecture & Pipeline:
* **Two-Pass Algorithm**:
  * **Pass 1**: Strips whitespace and comments, builds symbol table with predefined symbols, and binds label pseudo-commands `(LABEL)` to current ROM instruction indices.
  * **Pass 2**: Translates A-instructions (`@value` / `@symbol`), allocating new variables sequentially from `RAM[16]` onwards. Translates C-instructions into 16-bit binary (`111 + comp + dest + jump`).
* **Variant Feature ($K \bmod 3 = 0$)**: Automatically exports all resolved symbols to `symbols.txt`, classifying symbols as `label` (with ROM address) or `variable` (with RAM address).
* **Validation Results**: Tested against all four official benchmark programs (`Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm`), achieving bit-for-bit exact matching.

---

## 4. Part C: Interactive Box Program (`Box.asm`)

### Logic & Execution:
1. Polls the keyboard memory register `KBD` (address 24576).
2. If `RAM[KBD] != 0` (key pressed), sets drawing color `color = -1` (black).
3. If `RAM[KBD] == 0` (key released), sets drawing color `color = 0` (white).
4. Loops over 20 scanlines starting at address $17824$, writing `color` to word 0 and word 1 (`RAM[addr]` and `RAM[addr+1]`), then advances by $+32$ words.
5. Continuously repeats, producing responsive real-time interactivity.

### Screenshot of Box Output:
*[Insert Screenshot from CPU Emulator showing the black box drawn at row 45]*

---

## 5. One Mistake Encountered and Fixed (Mandatory Rubric Section)

During the initial implementation of the row-stepping loop in `Box.asm`, an address increment bug was encountered when moving from one scanline to the next. The routine initially attempted to advance the memory pointer using an immediate computation without properly staging the $+32$ row stride through the data register (`D`), causing the address pointer to increment by $1$ instead of a full screen row ($32$ words). As a result, the emulator rendered a single continuous horizontal stripe along the top row rather than a 20-row vertical block. 

By inspecting the CPU emulator registers, the bug was diagnosed: the Hack ALU cannot add an arbitrary immediate constant to memory without first loading it into register `A` and transferring it to `D`. The logic was corrected to load constant `@32`, transfer it with `D=A`, and then update the row pointer with `@addr; M=D+M`. Subsequent test execution confirmed that each row correctly advanced by 32 words, rendering the rectangular box with exact vertical height and alignment.

---

## 6. Viva Examination Quick Guide (5 Minutes)

* **Q: How would you move the box down by 10 rows?**  
  * *Answer:* Change start address from $17824$ to $17824 + (10 \times 32) = 17824 + 320 = 18144$ (replace `@17824` with `@18144` in `Box.asm`).
* **Q: How would you double the width of the box?**  
  * *Answer:* Instead of filling 2 words per row (`M=D; A=A+1; M=D`), fill 4 words per row (words 0, 1, 2, 3), doubling width from 32px to 64px.
* **Q: How would you invert the key behavior (box visible by default, disappears on key press)?**  
  * *Answer:* In `Box.asm`, swap the color assignment: set `color = 0` when `KBD != 0`, and `color = -1` when `KBD == 0`.
* **Q: Why does Keyboard have no load pin in `Memory.hdl`?**  
  * *Answer:* The keyboard is a read-only memory-mapped peripheral that reports key scan codes driven by user hardware input; software cannot write to it.
