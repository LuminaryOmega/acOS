# ac_echo.py
# ArcEcho: Signal tracing, loop reflection, memory reverb handler

from datetime import datetime
import hashlib

class ArcEcho:
    def __init__(self):
        self.echo_log = []

    def pulse(self, signal: str, source: str = "manual", intensity: int = 1):
        timestamp = datetime.utcnow().isoformat()
        echo_id = hashlib.sha256(f"{signal}{timestamp}".encode()).hexdigest()[:12]
        echo_entry = {
            "id": echo_id,
            "signal": signal,
            "source": source,
            "intensity": intensity,
            "timestamp": timestamp,
        }
        self.echo_log.append(echo_entry)
        return echo_entry

    def reflect(self, count=5):
        return self.echo_log[-count:]

    def clear(self):
        self.echo_log = []

    def export(self):
        return {
            "echo_count": len(self.echo_log),
            "echoes": self.echo_log,
        }

# Optional: test run
if __name__ == "__main__":
    echo = ArcEcho()
    echo.pulse("Initialization loop")
    echo.pulse("User re-entry", intensity=3)
    print(echo.reflect())
