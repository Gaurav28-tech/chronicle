from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class AuditBlock:
    index: int
    timestamp: float
    actor: str
    action: str
    resource: str
    metadata: Dict[str, Any]
    prev_hash: str
    hash: str = ""
