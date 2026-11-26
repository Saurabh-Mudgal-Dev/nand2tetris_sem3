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

The project maintains a dedicated, modular folder hierarchy for maximum readability:

```
capstone/
├── README.md               # Project documentation and specifications
│
├── hdl/                    # Hardware Description Files (Part A)
│   ├── Memory.hdl          # RAM16K + Screen + Keyboard decoding
│   ├── CPU.hdl             # Hack CPU decode and execution unit
│   └── Computer.hdl        # Top-level Hack Computer platform
│
├── tst/                    # Hardware Simulator Test Scripts (.tst)
│   ├── Memory.tst          # Tests Memory address ranges
│   ├── CPU.tst             # Tests A- and C-instructions, ALU, PC jumps
│   ├── ComputerAdd.tst     # Tests Computer execution of Add program
│   ├── ComputerMax.tst     # Tests Computer execution of Max program
│   └── ComputerRect.tst    # Tests Computer execution of Rect program
│
├── cmp/                    # Expected Output Comparison Files (.cmp)
│   ├── Memory.cmp
│   ├── CPU.cmp
│   ├── ComputerAdd.cmp
│   ├── ComputerMax.cmp
│   └── ComputerRect.cmp
│
├── hack/                   # Assembled Benchmark Binaries for Hardware Tests
│   ├── Add.hack            # 2 + 3 calculation
│   ├── Max.hack            # max(R0, R1) calculation
│   └── Rect.hack           # Rectangle drawing on Screen
│
├── assembler.py            # Part B: Custom 2-pass Python assembler (upcoming)
├── Box.asm                 # Part C: Hack assembly source code (upcoming)
├── Box.hack                # Part C: Assembled binary machine code (upcoming)
└── symbols.txt             # Part B output: symbol table dump (K mod 3 == 0)
```

---

## 3. Running Hardware Tests

Open the official **Nand to Tetris Hardware Simulator** (`HardwareSimulator.bat` on Windows or `HardwareSimulator.sh` on Linux/macOS):
1. Go to `File` $\rightarrow$ `Load Script`.
2. Navigate to `capstone/tst/` and select:
   * `Memory.tst` (validates `capstone/hdl/Memory.hdl` against `capstone/cmp/Memory.cmp`)
   * `CPU.tst` (validates `capstone/hdl/CPU.hdl` against `capstone/cmp/CPU.cmp`)
   * `ComputerAdd.tst` (validates `capstone/hdl/Computer.hdl` running `Add.hack`)
   * `ComputerMax.tst` (validates `capstone/hdl/Computer.hdl` running `Max.hack`)
   * `ComputerRect.tst` (validates `capstone/hdl/Computer.hdl` running `Rect.hack`)
3. Click **Run** and verify **"Comparison ended successfully"**. Capture screenshots for your ZOSIMA report.
