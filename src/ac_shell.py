# ============================================================
# AC SHELL — ArcCore-Prime V1.3
# Loop 2: Integration Repair
#
# Responsibilities:
#   - Accept raw user input
#   - Purify through Guardian
#   - Gate through Guardian
#   - Pass commands to Interpreter
#   - Display results
#
# Notes:
#   - Guardian API mismatch fully patched
#   - Purification added
#   - Safe execution wrapper added
# ============================================================

from arc_guardian import ArcGuardian
from ac_interpreter import ArcInterpreter


class ArcShell:
    """
    The command shell for ArcCore-Prime.
    """

    def __init__(self):
        self.guardian = ArcGuardian()
        self.interpreter = ArcInterpreter(self.guardian)

        # Display boot banner
        print("\n============================================================")
        print("              ARC CORE PRIME — SHELL ONLINE")
        print("============================================================")
        print(f"[Guardian] Identity Key: {self.guardian.identity_key[:16]}...")
        print("[Shell] Type 'help' for commands.")
        print("============================================================\n")

    # ============================================================
    # MAIN LOOP
    # ============================================================

    def run(self):
        """
        Persistent interactive shell.
        """

        while True:
            try:
                raw = input("ac> ")

                # Exit conditions
                if raw.strip().lower() in ("exit", "quit"):
                    print("[Shell] Closing ArcCore-Prime. Goodbye.")
                    break

                # ----------------------------------------------------
                # 1) Purify text
                # ----------------------------------------------------
                cleaned = self.guardian.purify(raw)

                # ----------------------------------------------------
                # 2) Shell-level gate (input_gate)
                # ----------------------------------------------------
                if not self.guardian.input_gate(cleaned):
                    print("[Guardian] ❌ Input rejected by gate.")
                    continue

                # ----------------------------------------------------
                # 3) Interpret and execute
                # ----------------------------------------------------
                result = self.interpreter.execute(cleaned)

                # ----------------------------------------------------
                # 4) Display results
                # ----------------------------------------------------
                if result is not None:
                    print(result)

            except KeyboardInterrupt:
                print("\n[Shell] Interrupt detected. Type 'quit' to exit.")
            except Exception as e:
                print(f"[Shell] ❌ Runtime error: {e}")
