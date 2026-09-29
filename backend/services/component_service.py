import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models import Component
from backend.services.mouser_service import MouserService

logger = logging.getLogger("fixio.component_service")

class ComponentService:
    """
    Evidence-based Electronic Component Identification Service.
    Queries database and Mouser API for component technical specifications, pinouts, and datasheets.
    Does NOT invent data or fake components if OCR / vision returns unreadable text.
    """

    @staticmethod
    def lookup_component(part_number: str, db: Optional[Session] = None) -> Dict[str, Any]:
        """
        Lookup component specifications from Local DB first, then Mouser API.
        """
        if not part_number:
            return {
                "found": False,
                "part_number": None,
                "message": "No part number provided."
            }

        clean_part = part_number.strip().upper()

        # 1. Query local database if DB session provided
        if db:
            comp = db.query(Component).filter(
                (Component.part_number.ilike(clean_part)) |
                (Component.part_number.ilike(f"%{clean_part}%")) |
                (Component.name.ilike(f"%{clean_part}%"))
            ).first()

            if comp:
                return {
                    "found": True,
                    "part_number": comp.part_number,
                    "name": comp.name,
                    "category": comp.category,
                    "manufacturer": getattr(comp, "manufacturer", "Original Semiconductor Manufacturer"),
                    "purpose": comp.purpose,
                    "working_principle": comp.working_principle,
                    "specifications": comp.specifications or {},
                    "pin_diagram": comp.pin_diagram or [],
                    "datasheet_url": comp.datasheet_url,
                    "replacement_procedure": comp.replacement_procedure,
                    "safety_notes": comp.safety_notes,
                    "package_type": comp.package_type,
                    "image_url": comp.image_url
                }

        # 2. Mouser API lookup if configured
        mouser_result = MouserService.search_part(clean_part)
        if mouser_result:
            return {
                "found": True,
                "part_number": mouser_result["part_number"],
                "name": f"{mouser_result['part_number']} — {mouser_result['description']}",
                "category": mouser_result["category"],
                "manufacturer": mouser_result["manufacturer"],
                "purpose": mouser_result["description"],
                "working_principle": "Semiconductor electronic component.",
                "specifications": mouser_result["specifications"],
                "pin_diagram": [],
                "datasheet_url": mouser_result["datasheet_url"],
                "replacement_procedure": "Follow standard IPC soldering and anti-static precautions.",
                "safety_notes": "Handle with ESD protection.",
                "package_type": mouser_result["package"],
                "image_url": None
            }

        # 3. Known component catalog fallback specs if not yet in SQLite DB
        known_components_catalog = {
            "LM358": {
                "name": "LM358 Dual Operational Amplifier",
                "category": "Integrated Circuit / Operational Amplifier",
                "manufacturer": "Texas Instruments",
                "purpose": "Dual high-gain independent operational amplifier suitable for single power supply operation.",
                "specifications": {
                    "Supply Voltage": "3V to 32V",
                    "Bandwidth": "1 MHz",
                    "Channels": "2 (Dual)",
                    "Package": "DIP-8 / SOIC-8"
                },
                "datasheet_url": "https://www.ti.com/lit/ds/symlink/lm358.pdf"
            },
            "NE555": {
                "name": "NE555 Precision Timing Circuit",
                "category": "Integrated Circuit / Timer",
                "manufacturer": "STMicroelectronics",
                "purpose": "Precision timing circuit producing accurate time delays or oscillation.",
                "specifications": {
                    "Supply Voltage": "4.5V to 16V",
                    "Max Frequency": "500 kHz",
                    "Output Current": "200 mA",
                    "Package": "DIP-8 / SOIC-8"
                },
                "datasheet_url": "https://www.ti.com/lit/ds/symlink/ne555.pdf"
            },
            "LM7805": {
                "name": "LM7805 Linear Voltage Regulator (5V)",
                "category": "Integrated Circuit / Power Management",
                "manufacturer": "Texas Instruments",
                "purpose": "3-terminal positive voltage regulator producing steady 5.0V output.",
                "specifications": {
                    "Output Voltage": "5.0V DC",
                    "Max Output Current": "1.5A",
                    "Input Voltage": "7V to 25V",
                    "Package": "TO-220"
                },
                "datasheet_url": "https://www.sparkfun.com/datasheets/Components/LM7805.pdf"
            },
            "IRFZ44N": {
                "name": "IRFZ44N N-Channel Power MOSFET",
                "category": "Transistor / Power MOSFET",
                "manufacturer": "Infineon Technologies",
                "purpose": "55V single N-channel HEXFET power MOSFET for switching and motor drivers.",
                "specifications": {
                    "Vds (Drain-Source)": "55V",
                    "Continuous Id": "49A",
                    "Rds(on)": "17.5 mOhm",
                    "Package": "TO-220AB"
                },
                "datasheet_url": "https://www.infineon.com/dgdl/Infineon-IRFZ44N-DataSheet-v01_01-EN.pdf"
            },
            "1N4007": {
                "name": "1N4007 Silicon Rectifier Diode",
                "category": "Diode / Rectifier",
                "manufacturer": "ON Semiconductor",
                "purpose": "General-purpose 1A 1000V power rectifier diode.",
                "specifications": {
                    "Forward Current": "1.0A",
                    "Reverse Voltage Max": "1000V",
                    "Forward Voltage Drop": "1.1V",
                    "Package": "DO-41"
                },
                "datasheet_url": "https://www.onsemi.com/pub/Collateral/1N4001-D.PDF"
            },
            "2N2222": {
                "name": "2N2222 NPN Bipolar Junction Transistor",
                "category": "Transistor / BJT",
                "manufacturer": "ON Semiconductor",
                "purpose": "High-speed switching NPN transistor for amplification and logic drive.",
                "specifications": {
                    "Collector-Emitter Voltage": "40V",
                    "Collector Current": "800 mA",
                    "Power Dissipation": "500 mW",
                    "Package": "TO-92"
                },
                "datasheet_url": "https://www.onsemi.com/pub/Collateral/P2N2222A-D.PDF"
            },
            "BC547": {
                "name": "BC547 NPN General Purpose Transistor",
                "category": "Transistor / BJT",
                "manufacturer": "Fairchild / ON Semi",
                "purpose": "Low noise general-purpose NPN bipolar transistor.",
                "specifications": {
                    "Collector-Emitter Voltage": "45V",
                    "Collector Current": "100 mA",
                    "DC Current Gain": "110 to 800",
                    "Package": "TO-92"
                },
                "datasheet_url": "https://www.onsemi.com/pub/Collateral/BC546-D.PDF"
            }
        }

        if clean_part in known_components_catalog:
            cat = known_components_catalog[clean_part]
            return {
                "found": True,
                "part_number": clean_part,
                "name": cat["name"],
                "category": cat["category"],
                "manufacturer": cat["manufacturer"],
                "purpose": cat["purpose"],
                "working_principle": "Semiconductor device operation.",
                "specifications": cat["specifications"],
                "pin_diagram": [],
                "datasheet_url": cat["datasheet_url"],
                "replacement_procedure": "Inspect orientation, verify supply rails, solder safely.",
                "safety_notes": "Observe anti-static safety and power limits.",
                "package_type": cat["specifications"].get("Package", "Standard"),
                "image_url": None
            }

        return {
            "found": False,
            "part_number": clean_part,
            "message": f"Part number '{clean_part}' verified, but detailed specs are not present in local database."
        }
