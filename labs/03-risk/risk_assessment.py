"""Educational qualitative risk matrix; not a production risk engine."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Risk:
    scenario: str
    likelihood: int
    impact: int

    def __post_init__(self):
        if not (1 <= self.likelihood <= 5 and 1 <= self.impact <= 5):
            raise ValueError("likelihood and impact must be 1..5")

    @property
    def score(self):
        return self.likelihood * self.impact

    @property
    def tier(self):
        if self.score >= 20:
            return "critical"
        if self.score >= 12:
            return "high"
        if self.score >= 5:
            return "medium"
        return "low"


def annualized_loss(single_loss: float, annual_rate: float) -> float:
    if single_loss < 0 or annual_rate < 0:
        raise ValueError("loss and rate cannot be negative")
    return single_loss * annual_rate


if __name__ == "__main__":
    items = [
        Risk("unauthorized order data access (hypothesis)", 3, 5),
        Risk("checkout outage (hypothesis)", 3, 4),
        Risk("forgotten test service (hypothesis)", 2, 2),
    ]
    for row in sorted(items, key=lambda x: x.score, reverse=True):
        print(f"{row.scenario}: {row.score}/25 ({row.tier})")
    print("Synthetic ALE:", annualized_loss(180_000, 0.4), "THB/year")
