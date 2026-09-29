import os
import json
import uuid
import logging
from typing import Dict, Any, List, Optional
from PIL import Image, ImageStat
from sqlalchemy.orm import Session

from backend.services.ocr_service import OCRService
from backend.services.component_service import ComponentService

logger = logging.getLogger("fixio.ai_engine")

class FixioAIEngine:
    """
    Fixio AI Electronic Component Identification & Analysis Engine.
    Pipeline:
    Uploaded File -> File Validation -> Preprocessing -> OCR Engine -> Part Validation -> Component Database / Mouser Lookup -> Result Object
    """

    @staticmethod
    def inspect_image_quality(image_path: str) -> Dict[str, Any]:
        """
        Inspect basic image metrics: resolution, contrast, brightness.
        """
        try:
            with Image.open(image_path) as img:
                img_rgb = img.convert("RGB")
                w, h = img_rgb.size
                if w < 50 or h < 50:
                    return {"valid": False, "reason": "Image resolution is too low (< 50x50px)."}
                
                stat = ImageStat.Stat(img_rgb)
                std_sum = sum(stat.stddev)
                if std_sum < 10.0:
                    return {"valid": False, "reason": "Image is extremely dark or low-contrast."}

                return {"valid": True, "width": w, "height": h}
        except Exception as e:
            return {"valid": False, "reason": f"Corrupted image payload: {e}"}

    @classmethod
    def analyze_uploaded_image(
        cls,
        image_path: str,
        original_filename: str = "",
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Main Analysis Entrypoint for Electronic Component Scanner.
        """
        scan_id = f"scan_{uuid.uuid4().hex[:10]}"
        rel_image_path = image_path.replace("\\", "/")
        if "static/uploads/" in rel_image_path:
            rel_image_path = "/static/uploads/" + rel_image_path.split("static/uploads/")[-1]

        # 1. Quality inspection
        quality = cls.inspect_image_quality(image_path)
        if not quality["valid"]:
            logger.info(f"[FIXIO AI ENGINE] Quality check failed: {quality.get('reason')}")
            return {
                "success": False,
                "scan_id": scan_id,
                "status": "analysis_failed",
                "message": quality.get("reason", "Unable to process uploaded image."),
                "image_url": rel_image_path,
                "ocr_text": [],
                "components": [],
                "identification": {
                    "status": "unknown",
                    "part_number": None,
                    "component_type": "Unknown",
                    "manufacturer": None,
                    "confidence": None
                },
                "damage_analysis": {
                    "status": "not_available",
                    "findings": []
                }
            }

        # 2. Run OCR Pipeline
        ocr_result = OCRService.run_ocr(image_path, original_filename=original_filename)
        part_number = ocr_result.get("part_number")
        raw_text = ocr_result.get("raw_text", [])
        cleaned_text = ocr_result.get("cleaned_text")

        # 3. Component Data Lookup if Part Number Validated
        if part_number:
            comp_info = ComponentService.lookup_component(part_number, db=db)
            if comp_info.get("found"):
                return {
                    "success": True,
                    "scan_id": scan_id,
                    "status": "confirmed",
                    "image_url": rel_image_path,
                    "mode": "component_datasheet",
                    "identification": {
                        "status": "confirmed",
                        "part_number": comp_info["part_number"],
                        "component_type": comp_info["category"],
                        "manufacturer": comp_info["manufacturer"],
                        "confidence": None  # Evidence-based: no fabricated confidence
                    },
                    "ocr": {
                        "raw_text": raw_text,
                        "cleaned_text": cleaned_text
                    },
                    "component_data": {
                        "name": comp_info["name"],
                        "part_number": comp_info["part_number"],
                        "manufacturer": comp_info["manufacturer"],
                        "category": comp_info["category"],
                        "purpose": comp_info["purpose"],
                        "working_principle": comp_info.get("working_principle", ""),
                        "package": comp_info.get("package_type", "Standard Package"),
                        "specifications": comp_info.get("specifications", {}),
                        "pin_diagram": comp_info.get("pin_diagram", []),
                        "datasheet_url": comp_info.get("datasheet_url"),
                        "replacement_procedure": comp_info.get("replacement_procedure"),
                        "safety_notes": comp_info.get("safety_notes")
                    },
                    "damage_analysis": {
                        "status": "not_available",
                        "message": "Damage analysis requires specialized thermal/electrical testing.",
                        "findings": []
                    },
                    "recommendations": [
                        f"Verify supply voltage rails before installing replacement {comp_info['part_number']}.",
                        "Observe electrostatic discharge (ESD) handling precautions.",
                        "Clean PCB pads with isopropyl alcohol prior to soldering."
                    ]
                }
            else:
                # Part number recognized from OCR, but details not in database
                return {
                    "success": True,
                    "scan_id": scan_id,
                    "status": "confirmed",
                    "image_url": rel_image_path,
                    "mode": "component_datasheet",
                    "identification": {
                        "status": "confirmed",
                        "part_number": part_number,
                        "component_type": "Semiconductor Component",
                        "manufacturer": "OEM Manufacturer",
                        "confidence": None
                    },
                    "ocr": {
                        "raw_text": raw_text,
                        "cleaned_text": cleaned_text
                    },
                    "component_data": {
                        "name": f"Part #{part_number}",
                        "part_number": part_number,
                        "manufacturer": "OEM Manufacturer",
                        "category": "Electronic Component",
                        "purpose": f"Identified part number {part_number} via OCR marking.",
                        "package": "Standard Package",
                        "specifications": {"Part Number": part_number},
                        "datasheet_url": None
                    },
                    "damage_analysis": {
                        "status": "not_available",
                        "findings": []
                    },
                    "recommendations": []
                }

        # 4. If raw text was found but no known part number pattern was validated
        if cleaned_text:
            return {
                "success": True,
                "scan_id": scan_id,
                "status": "possible",
                "image_url": rel_image_path,
                "mode": "component_datasheet",
                "identification": {
                    "status": "possible",
                    "part_number": None,
                    "component_type": "Electronic Component (Marking Unconfirmed)",
                    "manufacturer": None,
                    "confidence": None
                },
                "ocr": {
                    "raw_text": raw_text,
                    "cleaned_text": cleaned_text
                },
                "component_data": {
                    "name": "Electronic Component",
                    "part_number": "UNCONFIRMED",
                    "purpose": f"OCR extracted text \"{cleaned_text}\", but part number pattern could not be automatically validated.",
                    "specifications": {"Extracted Text": cleaned_text}
                },
                "damage_analysis": {
                    "status": "not_available",
                    "findings": []
                },
                "recommendations": [
                    "Re-upload a higher resolution close-up photo of component surface markings.",
                    "Use manual search to query datasheets directly."
                ]
            }

        # 5. No OCR text found - Component unreadable or unidentifiable
        logger.info(f"[FIXIO AI ENGINE] Component text unreadable for image: {image_path}")
        return {
            "success": False,
            "scan_id": scan_id,
            "status": "analysis_failed",
            "message": "Unable to identify component from this image. No readable marking or supported part number detected.",
            "image_url": rel_image_path,
            "ocr_text": [],
            "components": [],
            "identification": {
                "status": "unknown",
                "part_number": None,
                "component_type": "Unknown Electronic Component",
                "manufacturer": None,
                "confidence": None
            },
            "ocr": {
                "raw_text": [],
                "cleaned_text": ""
            },
            "damage_analysis": {
                "status": "not_available",
                "findings": []
            },
            "recommendations": [
                "Ensure image has adequate lighting and sharp focus on component markings.",
                "Search part number manually using the datasheet search bar."
            ]
        }
