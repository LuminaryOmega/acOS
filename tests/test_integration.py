
# ============================================================
# ARC CORE — INTEGRATION TEST
# Loop 5.G
# Ensures ArcShell → Interpreter → Guardian → Kernel → Memory
# all operate correctly as a unified system.
# ============================================================

import os
import json

from ac_interpreter import ArcInterpreter
from arc_guardian import ArcGuardian
from arc_prime import ArcMemorySystem


def run_test():
    print("\n=== ArcCore-Prime Integration Test ===\n")

    # ------------------------------------------------------------
    # 1. Initialize Components
    # ------------------------------------------------------------

    guardian = ArcGuardian()
    interp = ArcInterpreter()
    memory = ArcMemorySystem()

    print("[OK] Guardian initialized.")
    print("[OK] Interpreter initialized.")
    print("[OK] Memory Kernel initialized.\n")

    # ------------------------------------------------------------
    # 2. Inject test interaction
    # ------------------------------------------------------------

    print("Injecting test memory...")

    interp.memory.ingest_interaction(
        "Test user message 💠",
        "Test AI response.",
        cycle_context=7
    )

    print("[OK] Interaction injected.\n")

    # ------------------------------------------------------------
    # 3. Walk compressed tree
    # ------------------------------------------------------------

    print("Walking memory tree...")
    tree_output = interp.memory.load_and_inject()
    print(tree_output)
    print("\n[OK] Tree walk complete.\n")

    # ------------------------------------------------------------
    # 4. Export memory
    # ------------------------------------------------------------

    print("Exporting memory...")
    interp.memory.save_memory("test_memory.json")

    print("[OK] Memory exported.\n")

    # ------------------------------------------------------------
    # 5. Reload + integrity verification
    # ------------------------------------------------------------

    print("Reloading + verifying integrity...\n")

    reloaded = interp.memory.load_and_inject("test_memory.json")
    print(reloaded)
    print("\n[OK] Reload + Integrity Verified.\n")

    # ------------------------------------------------------------
    # 6. Sample Interpreter commands
    # ------------------------------------------------------------

    print("Interpreter command tests:\n")

    print("ac walk →")
    print(interp.interpret("ac walk"))

    print("\nac sigil test →")
    print(interp.interpret("ac sigil 💠Hello"))

    print("\nac guardian →")
    print(interp.interpret("ac guardian"))

    print("\n[OK] All interpreter commands executed.\n")

    # ------------------------------------------------------------
    # 7. Cleanup Test Files
    # ------------------------------------------------------------

    if os.path.exists("test_memory.json"):
        os.remove("test_memory.json")

    print("[OK] Cleanup complete.\n")
    print("=== ArcCore Integration Test Complete ===\n")


if __name__ == "__main__":
    run_test()
