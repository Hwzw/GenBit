"""CoCoPUTs (Codon and Codon Pair Usage Tables) client.

Fetches organism-specific codon usage data from NCBI's CoCoPUTs database.
"""

from app.clients.base_client import BaseClient

COCOPUTS_BASE_URL = "https://dnahive.fda.gov/dna.cgi"


class CoCoPUTsClient(BaseClient):
    def __init__(self):
        super().__init__(base_url=COCOPUTS_BASE_URL, timeout=60.0)

    async def get_codon_usage(self, tax_id: int) -> dict:
        """Fetch codon usage table for an organism by taxonomy ID."""
        response = await self.get(
            "",
            params={"cmd": "codon_usage", "id": str(tax_id), "format": "json"},
        )
        return response.json()


cocoputs_client = CoCoPUTsClient()
