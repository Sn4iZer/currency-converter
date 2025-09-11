import os
import requests # type: ignore
import json
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv # type: ignore

# ---------- environment ----------
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not found in environment")

BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"   # space removed

# ---------- client ----------
class ExchangeClient:
    """Thin wrapper with 1-hour local-file cache."""
    CACHE_FILE = Path(__file__).parent / "rates_cache.json"
    CACHE_TTL  = timedelta(hours=1)

    # --------------------
    def _download_all_rates(self, base: str = "USD") -> dict:
        resp = requests.get(f"{BASE_URL}/latest/{base}", timeout=10)
        resp.raise_for_status()
        return resp.json()["conversion_rates"]

    # --------------------
    def get_rates(self, base: str = "USD") -> dict:
        now = datetime.utcnow()
        if self.CACHE_FILE.exists():
            cached = json.loads(self.CACHE_FILE.read_text())
            stamp = datetime.fromisoformat(cached["time"])
            if now - stamp < self.CACHE_TTL:
                return cached["rates"]

        # download & cache
        rates = self._download_all_rates(base)
        self.CACHE_FILE.write_text(
            json.dumps({"time": now.isoformat(), "rates": rates})
        )
        return rates

    # --------------------
    def convert(self, from_cur: str, to_cur: str, amount: float) -> float:
        rates = self.get_rates()
        try:
            if from_cur != "USD":
                amount = amount / rates[from_cur]   # → USD
            return round(amount * rates[to_cur], 4)
        except KeyError as e:
            raise ValueError(f"Unsupported currency: {e}") from None

# ---------- convenience helper ----------
def last_fetch_time() -> datetime:
    """Return the timestamp stored in the cache file (or datetime.min)."""
    if ExchangeClient.CACHE_FILE.exists():
        cached = json.loads(ExchangeClient.CACHE_FILE.read_text())
        return datetime.fromisoformat(cached["time"])
    return datetime.min