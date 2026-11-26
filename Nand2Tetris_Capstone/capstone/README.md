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
* **Box Height:** $20$ scanlines (spanning row 45 to row 64)
* **Box Width Calculation:**
  $$\text{Width} = 16 \times ((K \bmod 4) + 1) = 16 \times ((45 \bmod 4) + 1) = 16 \times (1 + 1) = 32\text{ pixels}$$
  $$\text{Word Width} = (K \bmod 4) + 1 = 2\text{ words per row}$$
* **Start Memory Address:**
  $$\text{Address} = \text{SCREEN} + 32 \times K = 16384 + 32 \times 45 = 16384 + 1440 = 17824$$
* **Assembler Extra Feature ($K \bmod 3$):**
  $$45 \bmod 3 = 0$$
  **Feature requirement:** Save all labels and variables with their allocated memory addresses in `symbols.txt`.

---

## 2. Deliverables Directory Structure

```
capstone/
├── README.md               # Project overview and parameter specifications
├── REPORT.md               # ZOSIMA 3-4 page report template and viva notes
├── Memory.hdl              # Part A: Memory chip (RAM16K + Screen + Keyboard decoding)
├── CPU.hdl                 # Part A: Hack CPU decode and execution unit
├── Computer.hdl            # Part A: Top-level Hack Computer platform
├── assembler.py            # Part B: Custom 2-pass Python assembler (with K%3=0 feature)
├── Box.asm                 # Part C: Interactive box Hack assembly program
├── Box.hack                # Part C: Binary machine code assembled by assembler.py
├── symbols.txt             # Part B: Exported symbol table dump (ROM & RAM addresses)
│
├── hdl/                    # Hardware Description Files (Part A)
│   ├── Memory.hdl
│   ├── CPU.hdl
│   └── Computer.hdl
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
├── asm/                    # Benchmark Source Programs (.asm)
│   ├── Add.asm
│   ├── Max.asm
│   ├── Rect.asm
│   └── Pong.asm
│
└── tests/                  # Verification and Test Suites
    └── test_assembler.py   # Benchmark validator for Add, Max, Rect, Pong
```

---

## 3. How to Run and Verify Each Part

### Part A: Hardware Tests (Hardware Simulator)
1. Open `HardwareSimulator.bat` (Windows) or `HardwareSimulator.sh` (Mac/Linux).
2. Click `File` $\rightarrow$ `Load Script`.
3. Load and run each script from `capstone/tst/`:
   * `Memory.tst`
   * `CPU.tst`
   * `ComputerAdd.tst`
   * `ComputerMax.tst`
   * `ComputerRect.tst`
4. Confirm **"Comparison ended successfully"** for each test and capture screenshots.

### Part B: Python Assembler Tests
Run the benchmark validation suite:
```bash
python capstone/tests/test_assembler.py
```
This automatically verifies byte-for-byte exact matches for `Add.asm`, `Max.asm`, `Rect.asm`, and assembles `Pong.asm` (27,483 instructions), while generating `symbols.txt`.

### Part C: Interactive Box Program (CPU Emulator)
1. Assemble `Box.asm` using your assembler:
   ```bash
   python capstone/assembler.py capstone/Box.asm
   ```
2. Open `CPUEmulator.bat` (Windows) or `CPUEmulator.sh` (Mac/Linux).
3. Load `capstone/Box.hack` via `File` $\rightarrow$ `Load Program`.
4. Set **Animate** to `No Display` or `Fastest` and click **Run**.
5. Click on the display canvas and press/hold any key:
   * A solid black box appears at row 45 (32 pixels wide, 20 scanlines tall).
   * Release the key $\rightarrow$ box clears back to white.
6. Capture a screenshot with the key pressed for the report.
