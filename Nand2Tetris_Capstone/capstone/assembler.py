#!/usr/bin/env python3
"""Hack Assembler — Two-pass assembler for the Hack machine language.

Variant feature (K mod 3 == 0):
  After assembly, all resolved symbols (predefined, labels, and user variables)
  are written to symbols.txt alongside their RAM/ROM addresses.
"""

import sys
import os


K = 45                  # Roll: 2501010045 → K = 45
VARIANT = K % 3         # 0 → dump symbol table to symbols.txt


# ---------------------------------------------------------------------------
# Symbol Table
# ---------------------------------------------------------------------------
class SymbolTable:
    """Manages predefined, label, and variable symbols."""
    def __init__(self):
        self.table = {
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
            "SCREEN": 16384, "KBD": 24576,
        }
        for i in range(16):
            self.table[f"R{i}"] = i
        self.labels = set()     # tracks symbols added as labels (Pass 1)

    def add_entry(self, symbol: str, address: int):
        self.table[symbol] = address

    def add_label(self, symbol: str, address: int):
        """Add a label symbol (defined by a (LABEL) pseudo-instruction)."""
        self.table[symbol] = address
        self.labels.add(symbol)

    def contains(self, symbol: str) -> bool:
        return symbol in self.table

    def get_address(self, symbol: str):
        return self.table.get(symbol, None)


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------
class Parser:
    """Parses individual Hack assembly instructions."""
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2

    @staticmethod
    def sanitize(line: str) -> str:
        return "".join(line.split("//")[0].split())

    @classmethod
    def instruction_type(cls, inst: str) -> int:
        if inst.startswith("@"):
            return cls.A_INSTRUCTION
        if inst.startswith("(") and inst.endswith(")"):
            return cls.L_INSTRUCTION
        return cls.C_INSTRUCTION

    @staticmethod
    def symbol(inst: str) -> str:
        if inst.startswith("@"):
            return inst[1:]
        if inst.startswith("(") and inst.endswith(")"):
            return inst[1:-1]
        return ""

    @staticmethod
    def dest(inst: str) -> str:
        return inst.split("=")[0] if "=" in inst else ""

    @staticmethod
    def comp(inst: str) -> str:
        return inst.split("=")[-1].split(";")[0]

    @staticmethod
    def jump(inst: str) -> str:
        return inst.split(";")[1] if ";" in inst else ""


# ---------------------------------------------------------------------------
# Code Generator
# ---------------------------------------------------------------------------
class Code:
    """Translates Hack assembly mnemonics into binary codes."""

    DEST = {
        "":    "000", "M":  "001", "D":  "010", "MD": "011",
        "A":   "100", "AM": "101", "AD": "110", "AMD":"111",
    }

    JUMP = {
        "":    "000", "JGT":"001", "JEQ":"010", "JGE":"011",
        "JLT": "100", "JNE":"101", "JLE":"110", "JMP":"111",
    }

    COMP = {
        # a=0 (use A)
        "0":   "0101010", "1":   "0111111", "-1":  "0111010",
        "D":   "0001100", "A":   "0110000", "!D":  "0001101",
        "!A":  "0110001", "-D":  "0001111", "-A":  "0110011",
        "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
        "A-1": "0110010", "D+A": "0000010", "A+D": "0000010",
        "D-A": "0010011", "A-D": "0000111", "D&A": "0000000",
        "A&D": "0000000", "D|A": "0010101", "A|D": "0010101",
        # a=1 (use M)
        "M":   "1110000", "!M":  "1110001", "-M":  "1110011",
        "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
        "M+D": "1000010", "D-M": "1010011", "M-D": "1000111",
        "D&M": "1000000", "M&D": "1000000", "D|M": "1010101",
        "M|D": "1010101",
    }

    @classmethod
    def dest(cls, mnemonic: str) -> str:
        return cls.DEST.get(mnemonic, "000")

    @classmethod
    def comp(cls, mnemonic: str) -> str:
        return cls.COMP.get(mnemonic, "0000000")

    @classmethod
    def jump(cls, mnemonic: str) -> str:
        return cls.JUMP.get(mnemonic, "000")


# ---------------------------------------------------------------------------
# Pass 1 — Label Resolution
# ---------------------------------------------------------------------------
def first_pass(lines: list, symbols: SymbolTable) -> list:
    """Record all label addresses; return sanitized instruction lines."""
    clean = []
    rom_addr = 0
    for raw in lines:
        line = Parser.sanitize(raw)
        if not line:
            continue
        if Parser.instruction_type(line) == Parser.L_INSTRUCTION:
            symbols.add_label(Parser.symbol(line), rom_addr)
        else:
            clean.append(line)
            rom_addr += 1
    return clean


# ---------------------------------------------------------------------------
# Pass 2 — Binary Code Generation
# ---------------------------------------------------------------------------
def second_pass(instructions: list, symbols: SymbolTable) -> list:
    """Translate each instruction into a 16-bit binary string."""
    binary_lines = []
    next_var_addr = 16   # Variables are allocated from RAM[16] onwards

    for inst in instructions:
        itype = Parser.instruction_type(inst)

        if itype == Parser.A_INSTRUCTION:
            value = Parser.symbol(inst)
            if value.isdigit():
                # Numeric constant
                address = int(value)
            elif symbols.contains(value):
                # Already-known label or predefined symbol
                address = symbols.get_address(value)
            else:
                # New variable — allocate next available RAM address
                symbols.add_entry(value, next_var_addr)
                address = next_var_addr
                next_var_addr += 1
            binary_lines.append(f"0{address:015b}")

        else:  # C_INSTRUCTION
            d = Code.dest(Parser.dest(inst))
            c = Code.comp(Parser.comp(inst))
            j = Code.jump(Parser.jump(inst))
            binary_lines.append(f"111{c}{d}{j}")

    return binary_lines


# ---------------------------------------------------------------------------
# Variant Feature (K mod 3 == 0): Symbol Table Export
# ---------------------------------------------------------------------------
PREDEFINED = {
    "SP", "LCL", "ARG", "THIS", "THAT", "SCREEN", "KBD",
    *[f"R{i}" for i in range(16)]
}

def export_symbols(symbols: SymbolTable, asm_path: str):
    """Write all symbols (predefined, labels, variables) to symbols.txt."""
    # Always place symbols.txt beside the assembler script itself
    sym_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "symbols.txt")

    with open(sym_path, "w") as f:
        f.write("=== Symbol Table Dump ===\n")
        f.write(f"Source file : {os.path.basename(asm_path)}\n")
        f.write(f"K = {K}  |  Variant = K mod 3 = {VARIANT}\n\n")

        f.write("--- Predefined Symbols ---\n")
        for sym in sorted(PREDEFINED, key=lambda s: symbols.get_address(s)):
            f.write(f"  {sym:<12}  addr={symbols.get_address(sym)}\n")

        f.write("\n--- Labels & User Variables ---\n")
        user_syms = {k: v for k, v in symbols.table.items() if k not in PREDEFINED}
        for sym, addr in sorted(user_syms.items(), key=lambda x: (x[1], x[0])):
            mem_type = "ROM" if sym in symbols.labels else "RAM"
            kind = "label   " if sym in symbols.labels else "variable"
            f.write(f"  {sym:<12}  {kind}  {mem_type}[{addr}]\n")

    print(f"[Variant K%3=0] Symbol table written -> {sym_path}")
    return sym_path


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def assemble(asm_path: str):
    with open(asm_path, "r") as f:
        lines = f.readlines()

    symbols = SymbolTable()
    instructions = first_pass(lines, symbols)
    binary = second_pass(instructions, symbols)

    hack_path = os.path.splitext(asm_path)[0] + ".hack"
    with open(hack_path, "w") as f:
        f.write("\n".join(binary) + "\n")

    # Variant feature: dump symbol table if K mod 3 == 0
    sym_path = None
    if VARIANT == 0:
        sym_path = export_symbols(symbols, asm_path)

    return hack_path, sym_path, symbols, binary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)

    out_path, sym_path, sym_table, result = assemble(sys.argv[1])
    print(f"Assembled {len(result)} instructions -> {out_path}")
