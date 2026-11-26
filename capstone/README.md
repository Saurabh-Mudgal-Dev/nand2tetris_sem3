# Nand to Tetris I (ETCCNT301) — Capstone Project

**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Subject:** Nand to Tetris – I (ETCCNT301)  
**Student Name:** Saurabh  
**Roll Number:** 2501010045  
**Personal Parameter ($K$):** 45 (last two digits of roll number: 45)

---

## 1. Project Specifications & Parameter Derivations

Based on $K = 45$:
* **Box Start Row:** Row $K = 45$
* **Box Height:** $20$ rows (spanning row 45 to row 64)
* **Box Width Calculation:**
  $$\text{Width} = 16 \times ((K \bmod 4) + 1) = 16 \times ((45 \bmod 4) + 1) = 16 \times (1 + 1) = 32\text{ pixels}$$
  $$\text{Word Width} = (K \bmod 4) + 1 = 2\text{ words per row}$$
* **Assembler Extra Feature ($K \bmod 3$):**
  $$45 \bmod 3 = 0$$
  **Feature requirement:** Save all labels and variables with their allocated memory addresses in `symbols.txt`.

---

## 2. Directory Structure

```
capstone/
├── README.md           # Project documentation and student parameter specifications
├── Memory.hdl          # Part A: Memory chip (RAM16K + Screen + Keyboard decoding)
├── CPU.hdl             # Part A: Hack CPU implementation
├── Computer.hdl        # Part A: Hack Computer top-level chip
├── assembler.py        # Part B: Custom Hack assembler with K mod 3 feature
├── Box.asm             # Part C: Hack assembly source code for interactive box
├── Box.hack            # Part C: Assembled binary machine code
├── tests/              # Verification scripts (.tst, .cmp)
│   ├── Memory.tst
│   └── Memory.cmp
└── symbols.txt         # Part B output: symbol table dump (K mod 3 == 0)
```

---

## 3. Implementation Roadmap

* **Part A — Build the Computer:**
  * Implement `Memory.hdl`, `CPU.hdl`, and `Computer.hdl`.
  * Validate with `CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`.
* **Part B — Python Assembler:**
  * Two-pass assembler (`assembler.py`) translating `.asm` to `.hack`.
  * Passes standard benchmarks: `Add.asm`, `Max.asm`, `Rect.asm`, `Pong.asm`.
  * Implement $K \bmod 3 = 0$ feature: dump symbol table into `symbols.txt`.
* **Part C — Interactive Box Program:**
  * Implement `Box.asm` rendering a 32-pixel wide by 20-row tall black box starting at row 45 while any key is pressed, disappearing when released.
  * Translate using custom `assembler.py` to `Box.hack`.
  * Test in official CPU Emulator.
