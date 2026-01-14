import re
from typing import Optional, Tuple

class DataResolver:
    """
    Helper class to resolve stock identifiers (ISIN -> Ticker).
    """
    def __init__(self):
        pass

    def is_isin(self, identifier: str) -> bool:
        """Checks if the identifier looks like an ISIN."""
        # Simple regex: 2 letters, 9 alphanum, 1 digit.
        # Real validation would check checksum, but this is enough for skeleton.
        return bool(re.match(r'^[A-Z]{2}[A-Z0-9]{9}[0-9]$', identifier))

    def resolve(self, identifier: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Returns (Ticker, ISIN).
        If input is Ticker, ISIN is None (unless we fetch it).
        If input is ISIN, Ticker is resolved (if possible).
        """
        identifier = identifier.strip().upper()

        if self.is_isin(identifier):
            # It's an ISIN.
            # Try to resolve to Ticker.
            # Placeholder for future implementation (e.g. OpenFIGI API).
            # For now, we return (None, identifier) so the UI knows to ask for Ticker.
            return None, identifier
        else:
            # Assume it's a Ticker.
            return identifier, None
