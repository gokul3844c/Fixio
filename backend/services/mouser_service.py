import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("fixio.mouser")

class MouserService:
    """
    Mouser Electronics Search API Service.
    Queries Mouser API for electronic component specifications, datasheets, and availability
    when MOUSER_API_KEY is configured in environment variables.
    """

    @staticmethod
    def is_configured() -> bool:
        return bool(os.getenv("MOUSER_API_KEY"))

    @staticmethod
    def search_part(part_number: str) -> Optional[Dict[str, Any]]:
        api_key = os.getenv("MOUSER_API_KEY")
        if not api_key:
            logger.info("[FIXIO MOUSER] MOUSER_API_KEY not set. Skipping Mouser live lookup.")
            return None

        clean_part = part_number.strip()
        if not clean_part:
            return None

        try:
            import urllib.request
            import json

            url = f"https://api.mouser.com/api/v1/search/partnumber?apiKey={api_key}"
            payload = {
                "SearchByPartRequest": {
                    "mouserPartNumber": clean_part,
                    "partSearchOptions": "Exact"
                }
            }
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                res_json = json.loads(resp.read().decode("utf-8"))
                parts = res_json.get("SearchResults", {}).get("Parts", [])
                if parts:
                    part = parts[0]
                    return {
                        "part_number": part.get("MouserPartNumber") or part.get("ManufacturerPartNumber") or clean_part,
                        "manufacturer": part.get("Manufacturer", "OEM Semiconductor"),
                        "description": part.get("Description", ""),
                        "datasheet_url": part.get("DataSheetUrl", ""),
                        "category": part.get("Category", "Electronic Component"),
                        "package": part.get("PackageHousing", "Standard"),
                        "availability": part.get("Availability", "Available"),
                        "specifications": {
                            "Manufacturer": part.get("Manufacturer", "OEM Semiconductor"),
                            "Mouser Part #": part.get("MouserPartNumber", clean_part),
                            "Factory Stock": str(part.get("FactoryStock", "N/A")),
                            "Lifecycle Status": part.get("LifecycleStatus", "Active")
                        }
                    }
        except Exception as e:
            logger.error(f"[FIXIO MOUSER] Error querying Mouser API for '{clean_part}': {e}")

        return None
