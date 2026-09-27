"""V2 research transport: local write-once spool + per-domain consumer (Stage B, D-22).

The envelope itself is ``research_protocol.v2`` (frozen release 2.0.0rc2); this package only moves its bytes
between the CAIN and a domain adapter and never decides anything about a task or a result.
"""

from research_transport.spool import Spool, SpoolConflict

__all__ = ["Spool", "SpoolConflict"]
