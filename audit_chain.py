"""Local tamper-evident hash-chain log; this is not a decentralized blockchain."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path("audit_logs/verification_audit.jsonl")
GENESIS_HASH = "0" * 64

def _hash_record(record: dict) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def append_audit_record(text: str, result: dict) -> dict:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    previous_hash = GENESIS_HASH

    if LOG_PATH.exists():
        lines = [line for line in LOG_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            previous = json.loads(lines[-1])
            previous_hash = previous["record_hash"]

    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "prediction": result["prediction"],
        "credibility_score": result["credibility_score"],
        "previous_hash": previous_hash,
    }
    record["record_hash"] = _hash_record(record)

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\n")
    return record
