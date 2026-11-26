#!/usr/bin/env python3
"""Benchmark test suite for Hack Assembler (Commit 8 validation)."""

import os
import sys

# Add capstone directory to python path
capstone_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, capstone_dir)

from assembler import assemble

def run_benchmarks():
    asm_dir = os.path.join(capstone_dir, "asm")
    hack_dir = os.path.join(capstone_dir, "hack")

    test_cases = [
        ("Add.asm", "Add.hack"),
        ("Max.asm", "Max.hack"),
        ("Rect.asm", "Rect.hack"),
    ]

    print("========================================")
    print("Running Hack Assembler Benchmark Suite")
    print("========================================")

    all_passed = True

    # 1. Official comparison benchmarks
    for asm_name, ref_name in test_cases:
        asm_path = os.path.join(asm_dir, asm_name)
        ref_path = os.path.join(hack_dir, ref_name)

        out_path, sym_path, symbols, binary = assemble(asm_path)

        with open(ref_path, "r") as f:
            ref_lines = [line.strip() for line in f if line.strip()]

        if binary == ref_lines:
            print(f"[PASS] {asm_name:<10} -> {len(binary):4d} lines match official {ref_name}")
        else:
            print(f"[FAIL] {asm_name:<10} -> mismatch with {ref_name}!")
            all_passed = False

    # 2. Large benchmark: Pong.asm (27,000+ lines)
    pong_asm = os.path.join(asm_dir, "Pong.asm")
    if os.path.exists(pong_asm):
        print(f"\nAssembling stress benchmark: {pong_asm}...")
        out_path, sym_path, symbols, binary = assemble(pong_asm)
        assert len(binary) > 20000, f"Expected >20000 lines, got {len(binary)}"
        assert all(len(line) == 16 and set(line).issubset({"0", "1"}) for line in binary), "Invalid binary line found!"
        print(f"[PASS] Pong.asm   -> {len(binary):4d} instructions assembled cleanly.")
    else:
        print("[WARN] Pong.asm not found in asm directory.")

    print("========================================")
    if all_passed:
        print("ALL BENCHMARKS PASSED SUCCESSFULLY!")
    else:
        print("SOME BENCHMARKS FAILED.")
    print("========================================")
    return all_passed

if __name__ == "__main__":
    success = run_benchmarks()
    sys.exit(0 if success else 1)
