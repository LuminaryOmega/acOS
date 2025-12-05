# ============================================================
# ARC CORE — RECONSTRUCTION ENGINE TEST
# Loop 6.D — Structural Reconstruction Verification
# ============================================================

from ac_interpreter import ArcInterpreter
from arc_prime import ArcMemorySystem


def run_test():
    print("\n=== ArcCore Reconstruction Test (Loop 6.D) ===\n")

    interp = ArcInterpreter()
    mem = interp.memory  # direct access for injection

    # ------------------------------------------------------------
    # 1. Inject sample multi-cycle memory
    # ------------------------------------------------------------

    print("[1] Injecting sample interactions...\n")

    mem.ingest_interaction(
        "Cycle 3 insight: 💠 structured descent reveals stability.",
        "Affirmation: Cycle 3 provides grounding.",
        cycle_context=3
    )

    mem.ingest_interaction(
        "Cycle 7 note: recursive clarity is emerging.",
        "Affirmation: Cycle 7 threads strengthen insight.",
        cycle_context=7
    )

    mem.ingest_interaction(
        "Cycle 3 elaboration: deeper patterns appear.",
        "Yes — Cycle 3 forms a harmonic descent pattern.",
        cycle_context=3
    )

    print("[OK] Sample memory injected.\n")

    # ------------------------------------------------------------
    # 2. Full reconstruction
    # ------------------------------------------------------------

    print("[2] FULL TREE RECONSTRUCTION:\n")
    result_full = interp.cmd_reconstruct_full("")
    print(result_full, "\n")

    # ------------------------------------------------------------
    # 3. Cycle-threaded reconstruction
    # ------------------------------------------------------------

    print("[3] THREAD RECONSTRUCTION for cycle 3:\n")
    thread_3 = interp.cmd_reconstruct_thread("3")
    print(thread_3, "\n")

    print("[4] THREAD RECONSTRUCTION for cycle 7:\n")
    thread_7 = interp.cmd_reconstruct_thread("7")
    print(thread_7, "\n")

    # ------------------------------------------------------------
    # 4. Summary (top-level reconstruction)
    # ------------------------------------------------------------

    print("[5] STRUCTURAL SUMMARY:\n")
    summary = interp.cmd_summary("")
    print(summary, "\n")

    print("=== Reconstruction Test COMPLETE ===\n")


if __name__ == "__main__":
    run_test()
