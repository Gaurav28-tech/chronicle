from typing import List, Tuple, Optional
from auditvault.models import AuditBlock
from auditvault.hasher import BlockHasher

class ChainVerifier:
    GENESIS_PREV_HASH = "0" * 64

    @classmethod
    def verify(cls, chain: List[AuditBlock]) -> Tuple[bool, Optional[str]]:
        if not chain:
            return True, None

        for i, block in enumerate(chain):
            expected_prev = chain[i - 1].hash if i > 0 else cls.GENESIS_PREV_HASH
            if block.prev_hash != expected_prev:
                return False, f"Broken prev_hash link at index {i}: expected {expected_prev}, got {block.prev_hash}"

            recomputed_hash = BlockHasher.compute_hash(
                index=block.index,
                timestamp=block.timestamp,
                actor=block.actor,
                action=block.action,
                resource=block.resource,
                metadata=block.metadata,
                prev_hash=block.prev_hash
            )

            if block.hash != recomputed_hash:
                return False, f"Tampered data detected at index {i}: hash mismatch"

        return True, None
