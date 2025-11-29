# ============================================================
# AC Sigil Engine — Prismatic Weighting System
# ArcCore-Prime V1.4
# ============================================================

class SigilEngine:
    """
    Computes symbolic priority of memory nodes.
    """

    SIGIL_WEIGHTS = {
        "💠": 3,
        "✨": 2,
        "•": 1
    }

    def evaluate(self, text: str) -> int:
        if not isinstance(text, str):
            return 0

        score = 0
        for sigil, weight in self.SIGIL_WEIGHTS.items():
            score += text.count(sigil) * weight

        return score
