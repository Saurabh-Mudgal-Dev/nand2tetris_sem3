#!/usr/bin/env python3
"""Hack Assembler - Pass 1: Parser and Symbol Table Label Resolution"""

import sys
import re

class SymbolTable:
    """Manages predefined, label, and variable symbols."""
    def __init__(self):
        # Predefined symbols in Hack architecture
        self.table = {
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
            "SCREEN": 16384, "KBD": 24576
        }
        for i in range(16):
            self.table[f"R{i}"] = i

    def add_entry(self, symbol: str, address: int):
        self.table[symbol] = address

    def contains(self, symbol: str) -> bool:
        return symbol in self.table

    def get_address(self, symbol: str) -> int:
        return self.table.get(symbol, None)


class Parser:
    """Parses Hack assembly instructions and extracts syntax components."""
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2

    @staticmethod
    def sanitize_line(line: str) -> str:
        """Strip comments and surrounding whitespace."""
        line = line.split("//")[0].strip()
        return "".join(line.split())

    @classmethod
    def instruction_type(cls, instruction: str) -> int:
        if instruction.startswith("@"):
            return cls.A_INSTRUCTION
        if instruction.startswith("(") and instruction.endswith(")"):
            return cls.L_INSTRUCTION
        return cls.C_INSTRUCTION

    @staticmethod
    def symbol(instruction: str) -> str:
        """Extract symbol from @symbol or (LABEL)."""
        if instruction.startswith("@"):
            return instruction[1:]
        if instruction.startswith("(") and instruction.endswith(")"):
            return instruction[1:-1]
        return ""

    @staticmethod
    def dest(instruction: str) -> str:
        """Extract destination part of C-instruction."""
        if "=" in instruction:
            return instruction.split("=")[0]
        return ""

    @staticmethod
    def comp(instruction: str) -> str:
        """Extract computation part of C-instruction."""
        inst = instruction.split("=")[-1]
        return inst.split(";")[0]

    @staticmethod
    def jump(instruction: str) -> str:
        """Extract jump part of C-instruction."""
        if ";" in instruction:
            return instruction.split(";")[1]
        return ""


def first_pass(lines: list, symbol_table: SymbolTable) -> list:
    """Scan instructions, record labels in symbol table, and return code lines."""
    clean_instructions = []
    rom_address = 0

    for raw_line in lines:
        line = Parser.sanitize_line(raw_line)
        if not line:
            continue

        inst_type = Parser.instruction_type(line)
        if inst_type == Parser.L_INSTRUCTION:
            label = Parser.symbol(line)
            symbol_table.add_entry(label, rom_address)
        else:
            clean_instructions.append(line)
            rom_address += 1

    return clean_instructions


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)

    asm_filename = sys.argv[1]
    with open(asm_filename, "r") as f:
        asm_lines = f.readlines()

    symbols = SymbolTable()
    instructions = first_pass(asm_lines, symbols)

    print(f"Pass 1 Complete: {len(instructions)} ROM instructions parsed.")
    print("Resolved symbols (labels & predefined):")
    for sym, addr in sorted(symbols.table.items()):
        if not sym.startswith("R") or len(sym) > 3:
            print(f"  {sym:12} -> {addr}")
