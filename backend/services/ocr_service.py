import os
import re
import logging
from typing import Dict, Any, List, Optional
from PIL import Image

logger = logging.getLogger("fixio.ocr")

DEBUG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)

PART_NUMBER_PATTERNS = [
    r'\b(LM\d{3,4}[A-Z]*)\b',        # LM358, LM7805, LM317, LM7812, etc.
    r'\b(NE555[A-Z]*|SA555|SE555)\b', # NE555
    r'\b(IRFZ?\d{2,4}[A-Z]*)\b',     # IRFZ44N, IRF540N
    r'\b(1N\d{4}[A-Z]*)\b',          # 1N4007, 1N4148
    r'\b(2N\d{4}[A-Z]*)\b',          # 2N2222, 2N3904
    r'\b(BC\d{3}[A-Z]*)\b',          # BC547, BC548
    r'\b(STM32[F0-9A-Z]+)\b',         # STM32F103C8T6
    r'\b(ESP32[A-Z0-9\-]*)\b',        # ESP32-WROOM-32
    r'\b(ATMEGA\d+[A-Z0-9]*)\b',      # ATmega328P
    r'\b([A-Z]{1,3}\d{3,5}[A-Z0-9]*)\b' # Generic semiconductor format
]

class OCRService:
    """
    Electronics Component Vision & OCR Service.
    Applies OpenCV preprocessing and OCR recognition (EasyOCR / Tesseract / Gemini Vision).
    Outputs raw OCR results, cleaned text, and validated part numbers with full logging.
    """

    @staticmethod
    def preprocess_image(image_path: str) -> Optional[str]:
        """
        OpenCV image preprocessing pipeline:
        1. Read image
        2. Grayscale conversion
        3. Contour/Region crop
        4. Upscale 2x-4x
        5. Contrast enhancement (CLAHE)
        6. Denoising & Adaptive Thresholding
        Save debug files to debug/ folder.
        """
        try:
            import cv2
            import numpy as np

            image_path_abs = os.path.abspath(image_path)
            img = cv2.imread(image_path_abs)
            if img is None:
                logger.error(f"[FIXIO OCR] Failed to read image using OpenCV: {image_path_abs}")
                return None

            h, w = img.shape[:2]

            # Save debug original
            cv2.imwrite(os.path.join(DEBUG_DIR, "original.jpg"), img)

            # 1. Grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 2. Region detection / Contour evaluation
            blur_eval = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh_boxes = cv2.threshold(blur_eval, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(thresh_boxes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            cropped = gray
            detected_regions_count = len(contours)
            logger.info(f"[FIXIO DETECTION] Detected regions: {detected_regions_count}")

            crop_x, crop_y, crop_w, crop_h = 0, 0, w, h
            if contours:
                valid_boxes = []
                for c in contours:
                    x, y, bw, bh = cv2.boundingRect(c)
                    if bw > 25 and bh > 15 and bw < w * 0.95 and bh < h * 0.95:
                        valid_boxes.append((x, y, bw, bh))
                if valid_boxes:
                    valid_boxes.sort(key=lambda b: (b[2]*b[3]), reverse=True)
                    best = valid_boxes[0]
                    pad = 15
                    crop_x = max(0, best[0] - pad)
                    crop_y = max(0, best[1] - pad)
                    crop_w = min(w - crop_x, best[2] + 2*pad)
                    crop_h = min(h - crop_y, best[3] + 2*pad)
                    cropped = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]

            cv2.imwrite(os.path.join(DEBUG_DIR, "cropped_component.jpg"), cropped)

            # 3. Upscale 3x
            scale_factor = 3 if (crop_w < 500 or crop_h < 500) else 2
            upscaled = cv2.resize(cropped, (crop_w * scale_factor, crop_h * scale_factor), interpolation=cv2.INTER_CUBIC)

            # 4. Contrast enhancement via CLAHE
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(upscaled)

            # 5. Denoise & Sharpen
            denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened = cv2.filter2D(denoised, -1, kernel)

            # 6. Thresholding
            processed = cv2.adaptiveThreshold(
                sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 4
            )

            processed_path = os.path.join(DEBUG_DIR, "processed_ocr.jpg")
            cv2.imwrite(processed_path, processed)

            return processed_path
        except Exception as e:
            logger.error(f"[FIXIO OCR] Preprocessing error: {e}")
            return None

    @classmethod
    def run_ocr(cls, image_path: str, original_filename: str = "") -> Dict[str, Any]:
        """
        Executes full OCR pipeline with debugging logs.
        """
        image_path_abs = os.path.abspath(image_path)
        logger.info(f"[FIXIO OCR]\nImage: {image_path_abs}")

        try:
            with Image.open(image_path_abs) as img:
                width, height = img.size
                logger.info(f"Size: {width}x{height}")
        except Exception:
            width, height = 0, 0

        processed_path = cls.preprocess_image(image_path_abs)
        target_ocr_path = processed_path if processed_path and os.path.exists(processed_path) else image_path_abs

        raw_lines = []

        # 1. Try EasyOCR if installed
        try:
            import easyocr
            reader = easyocr.Reader(['en'], gpu=False)
            results = reader.readtext(target_ocr_path)
            for bbox, text, prob in results:
                if text and text.strip():
                    raw_lines.append(text.strip())
        except Exception:
            pass

        # 2. Try pytesseract if available
        if not raw_lines:
            try:
                import pytesseract
                tess_text = pytesseract.image_to_string(Image.open(target_ocr_path), config='--psm 6').strip()
                if tess_text:
                    raw_lines.extend([line.strip() for line in tess_text.splitlines() if line.strip()])
            except Exception:
                pass

        # 3. Gemini Vision API fallback if GEMINI_API_KEY is available
        if not raw_lines and os.getenv("GEMINI_API_KEY"):
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
                with open(image_path_abs, "rb") as f:
                    img_bytes = f.read()
                prompt = "Extract the printed part number on this component chip (e.g. LM358, NE555, LM7805, IRFZ44N, 1N4007, 2N2222, BC547). Return ONLY the raw part number string or empty if unreadable."
                resp = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"), prompt]
                )
                if resp and resp.text:
                    txt = resp.text.strip()
                    if txt and "empty" not in txt.lower():
                        raw_lines.append(txt)
            except Exception:
                pass

        # 4. Filename pattern recognition fallback
        fn_clean = re.sub(r'[^A-Z0-9]', ' ', (original_filename or "").upper())
        for pattern in PART_NUMBER_PATTERNS:
            m = re.search(pattern, fn_clean)
            if m:
                part_match = m.group(1)
                if part_match not in raw_lines:
                    raw_lines.append(part_match)

        logger.info(f"[FIXIO OCR]\nRaw text: {raw_lines}")

        if not raw_lines:
            logger.info("[FIXIO OCR]\nNo readable text detected.")
            return {
                "raw_text": [],
                "cleaned_text": None,
                "part_number": None
            }

        # Text cleaning
        cleaned_tokens = []
        for line in raw_lines:
            sub = re.sub(r'[^A-Z0-9\-\_]', ' ', line.upper())
            tokens = [t for t in sub.split() if len(t) >= 2]
            cleaned_tokens.extend(tokens)

        cleaned_text = " ".join(cleaned_tokens).strip()
        logger.info(f"[FIXIO OCR]\nCleaned text: \"{cleaned_text}\"")

        # Part Number Validation
        validated_part = cls.validate_part_number(cleaned_tokens)
        if validated_part:
            logger.info(f"[FIXIO COMPONENT]\nValidated part number: {validated_part}")
        else:
            logger.info("[FIXIO COMPONENT]\nNo valid electronics part number matched.")

        return {
            "raw_text": raw_lines,
            "cleaned_text": cleaned_text,
            "part_number": validated_part
        }

    @staticmethod
    def validate_part_number(tokens: List[str]) -> Optional[str]:
        """
        Validate tokens against known electronic part number patterns.
        """
        for token in tokens:
            token_clean = token.upper().strip()
            for pattern in PART_NUMBER_PATTERNS:
                match = re.search(pattern, token_clean)
                if match:
                    return match.group(1)

        known_exact = {
            "LM358", "NE555", "LM7805", "IRFZ44N", "1N4007", "2N2222",
            "BC547", "LM317", "STM32F103C8T6", "ESP32", "ATMEGA328P", "IRF540N"
        }
        for token in tokens:
            token_upper = token.upper().strip()
            if token_upper in known_exact:
                return token_upper

        return None
