import time
import threading
from typing import List, Dict, Any, Optional
from auditvault.models import AuditBlock
from auditvault.hasher import BlockHasher

class AuditLedger:
    GENESIS_PREV_HASH = "0" * 64

    def __init__(self):
        self.chain: List[AuditBlock] = []
        self.lock = threading.Lock()

    def append(self, actor: str, action: str, resource: str, metadata: Optional[Dict[str, Any]] = None) -> AuditBlock:
        meta = metadata or {}
        with self.lock:
            index = len(self.chain)
            now = time.time()
            prev_hash = self.chain[-1].hash if self.chain else self.GENESIS_PREV_HASH

            block_hash = BlockHasher.compute_hash(
                index=index,
                timestamp=now,
                actor=actor,
                action=action,
                resource=resource,
                metadata=meta,
                prev_hash=prev_hash
            )

            block = AuditBlock(
                index=index,
                timestamp=now,
                actor=actor,
                action=action,
                resource=resource,
                metadata=meta,
                prev_hash=prev_hash,
                hash=block_hash
            )
            self.chain.append(block)
            return block

    def get_chain(self) -> List[AuditBlock]:
        with self.lock:
            return list(self.chain)

    def query(self, actor: Optional[str] = None, action: Optional[str] = None) -> List[AuditBlock]:
        with self.lock:
            results = self.chain
            if actor:
                results = [b for b in results if b.actor == actor]
            if action:
                results = [b for b in results if b.action == action]
            return results
