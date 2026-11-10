import hashlib
import json
from typing import Dict, Any

class BlockHasher:
    @staticmethod
    def canonical_json(data: Dict[str, Any]) -> str:
        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    @staticmethod
    def compute_hash(index: int, timestamp: float, actor: str, action: str, resource: str, metadata: Dict[str, Any], prev_hash: str) -> str:
        payload = {
            "index": index,
            "timestamp": timestamp,
            "actor": actor,
            "action": action,
            "resource": resource,
            "metadata": metadata,
            "prev_hash": prev_hash
        }
        canonical_str = BlockHasher.canonical_json(payload)
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()
