import os
import random
from typing import Dict, Any, List
from PIL import Image

class AIElectronicsEngine:
    """
    AI Engine performing:
    1. Computer Vision simulation & image inspection (YOLO bounding boxes, severity assessment, OCR pin label matching)
    2. Electronics Technical Assistant (AI Q&A reasoning)
    """

    @staticmethod
    def analyze_pcb_image(image_path: str, filename: str) -> Dict[str, Any]:
        """
        Inspect uploaded PCB image, detect components (ICs, capacitors, MOSFETs, diodes),
        assess damage status, and return bounding boxes & diagnostic report.
        """
        # Load image metadata if file exists
        img_width = 800
        img_height = 600
        if os.path.exists(image_path):
            try:
                with Image.open(image_path) as img:
                    img_width, img_height = img.size
            except Exception:
                pass

        # Simulate intelligent vision detection based on file characteristics or random variation
        fn_lower = filename.lower()

        # Preset realistic PCB detection scenarios
        if "tv" in fn_lower or "power" in fn_lower or "1" in fn_lower:
            detected_boxes = [
                {
                    "id": "box_lm7805",
                    "label": "Voltage Regulator IC (LM7805)",
                    "part_number": "LM7805",
                    "category": "IC",
                    "status": "Damaged",
                    "severity": "High",
                    "confidence": 94.8,
                    "x": 38.0,
                    "y": 24.5,
                    "width": 24.0,
                    "height": 28.0,
                    "issue_description": "Severe thermal charring on ceramic package. Pass transistor internal short circuit detected.",
                    "repair_action": "Replace LM7805 IC & apply fresh thermal grease to heatsink tab."
                },
                {
                    "id": "box_cap10uf",
                    "label": "Filter Capacitor (10uF 25V)",
                    "part_number": "ECE-A1EV100",
                    "category": "Capacitor",
                    "status": "Warning",
                    "severity": "Medium",
                    "confidence": 89.2,
                    "x": 68.0,
                    "y": 54.0,
                    "width": 18.0,
                    "height": 22.0,
                    "issue_description": "Slight top rubber vent expansion. Increased ESR suspected from adjacent IC heat.",
                    "repair_action": "Replace with 105°C rated low-ESR electrolytic capacitor."
                },
                {
                    "id": "box_diode1n5819",
                    "label": "Schottky Flyback Diode (1N5819)",
                    "part_number": "1N5819",
                    "category": "Diode",
                    "status": "Healthy",
                    "severity": "Low",
                    "confidence": 97.4,
                    "x": 16.5,
                    "y": 62.0,
                    "width": 15.0,
                    "height": 16.0,
                    "issue_description": "Normal visual condition. Silicon casing intact, no cracking or arc marks.",
                    "repair_action": "No replacement necessary."
                }
            ]
            primary_component = "Voltage Regulator IC"
            primary_part = "LM7805"
            primary_status = "Damaged - Thermal Burn"
            severity = "High"
            cost_est = "$15 - $30 (₹120 - ₹250)"
            time_est = "30 - 60 mins"
            damage_cause = "Prolonged thermal stress exceeding 150°C junction limit due to inadequate heat dissipation."

        elif "gpu" in fn_lower or "motherboard" in fn_lower or "2" in fn_lower:
            detected_boxes = [
                {
                    "id": "box_mosfet",
                    "label": "N-Channel Power MOSFET (IRFZ44N)",
                    "part_number": "IRFZ44N",
                    "category": "MOSFET",
                    "status": "Damaged",
                    "severity": "High",
                    "confidence": 96.2,
                    "x": 42.0,
                    "y": 30.0,
                    "width": 26.0,
                    "height": 32.0,
                    "issue_description": "Cracked epoxy casing with visible gate oxide blowout.",
                    "repair_action": "Desolder MOSFET, inspect gate driver resistor before soldering replacement."
                },
                {
                    "id": "box_fuse",
                    "label": "SMD Fast Acting Fuse (5A 32V)",
                    "part_number": "FUSE-0603-5A",
                    "category": "Fuse",
                    "status": "Damaged",
                    "severity": "High",
                    "confidence": 92.0,
                    "x": 20.0,
                    "y": 45.0,
                    "width": 14.0,
                    "height": 14.0,
                    "issue_description": "Blown internal filament due to MOSFET overcurrent spike.",
                    "repair_action": "Replace SMD 5A fuse after fixing shorted MOSFET."
                }
            ]
            primary_component = "N-Channel Power MOSFET"
            primary_part = "IRFZ44N"
            primary_status = "Damaged - Gate Blowout"
            severity = "High"
            cost_est = "$20 - $40 (₹160 - ₹320)"
            time_est = "45 - 90 mins"
            damage_cause = "Transient overvoltage voltage spike causing gate oxide dielectric breakdown and short circuit current runaway."

        else:
            # Default / Generic component detection
            detected_boxes = [
                {
                    "id": "box_gen_ic",
                    "label": "Voltage Regulator IC (LM7805)",
                    "part_number": "LM7805",
                    "category": "IC",
                    "status": "Damaged",
                    "severity": "High",
                    "confidence": 94.5,
                    "x": 38.5,
                    "y": 25.0,
                    "width": 24.0,
                    "height": 28.0,
                    "issue_description": "Burnt epoxy body with discolored solder contacts.",
                    "repair_action": "Desolder and replace component."
                },
                {
                    "id": "box_gen_cap",
                    "label": "Electrolytic Capacitor 10uF 25V",
                    "part_number": "ECE-A1EV100",
                    "category": "Capacitor",
                    "status": "Warning",
                    "severity": "Medium",
                    "confidence": 88.5,
                    "x": 68.0,
                    "y": 55.0,
                    "width": 18.0,
                    "height": 22.0,
                    "issue_description": "Minor bulge observed at top safety relief vent.",
                    "repair_action": "Replace capacitor."
                }
            ]
            primary_component = "Voltage Regulator IC"
            primary_part = "LM7805"
            primary_status = "Damaged - Overheated"
            severity = "High"
            cost_est = "$15 - $25 (₹120 - ₹250)"
            time_est = "30 - 60 mins"
            damage_cause = "Thermal degradation from high ambient temperature and current overload."

        repair_steps = [
            "Disconnect power supply and discharge bulk capacitors completely.",
            f"Desolder the damaged {primary_part} component using solder wick and temperature-controlled soldering iron.",
            "Clean the circuit board solder pads thoroughly using 99% Isopropyl Alcohol (IPA).",
            "Inspect adjacent components and copper traces for electrical continuity.",
            f"Solder the new replacement {primary_part} component respecting correct orientation and pin alignment.",
            "Perform power-on output voltage verification with a digital multimeter."
        ]

        return {
            "device_name": "Electronics PCB Board",
            "component_name": primary_component,
            "part_number": primary_part,
            "image_path": image_path,
            "damage_status": primary_status,
            "confidence_percentage": detected_boxes[0]["confidence"],
            "severity_level": severity,
            "estimated_repair_cost": cost_est,
            "estimated_repair_time": time_est,
            "bounding_boxes": detected_boxes,
            "damage_cause": damage_cause,
            "repair_steps_summary": repair_steps,
            "datasheet_url": "https://www.ti.com/lit/ds/symlink/lm7805.pdf"
        }

    @staticmethod
    def answer_assistant_query(query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process technical query regarding electronics, failure diagnosis, IC pinouts, and repair procedures.
        """
        q_lower = query.lower()

        if "tv" in q_lower or "not turning on" in q_lower or "power" in q_lower:
            reply = (
                "**Common Reasons Why a TV / Monitor Will Not Turn On:**\n\n"
                "1. **Blown Main Fuse or VARISTOR:** The input AC power surge protector (MOV) or 3.15A glass fuse may have blown.\n"
                "2. **Failed Voltage Regulator IC (LM7805 / SMPS PWM IC):** If the standby 5V rail is missing, the microcontroller won't wake up.\n"
                "3. **Bulging Filter Capacitors:** Secondary output caps on the 12V/24V power supply board often dry out or bulge.\n"
                "4. **Failed Backlight Inverter / LED Driver:** If standby LED blinks but screen stays black, test the LED driver MOSFETs.\n\n"
                "💡 **Recommended Next Step:** Upload a clear photo of your TV power supply PCB in **AI Scanner** so I can highlight damaged components for you!"
            )
            suggested = [
                "How do I test a blown fuse with a multimeter?",
                "How to check standby 5V rail voltage?",
                "Where can I buy replacement capacitors?"
            ]

        elif "ic" in q_lower or "what is" in q_lower or "lm7805" in q_lower:
            reply = (
                "**Component Identification & Function:**\n\n"
                "• **LM7805:** Fixed +5V Positive Linear Voltage Regulator in TO-220 package.\n"
                "• **Pinout:** 1. Input (7-25V DC), 2. Ground (GND), 3. Output (5.0V DC).\n"
                "• **Max Current:** 1.5 Amperes with adequate heat sink.\n\n"
                "If your LM7805 feels extremely hot or outputs 0V / input voltage directly, it is shorted internally and must be replaced immediately to protect downstream microcontrollers!"
            )
            suggested = [
                "Show LM7805 Pin Diagram",
                "How to replace LM7805 IC?",
                "What capacitor values should be used with LM7805?"
            ]

        elif "capacitor" in q_lower or "replace" in q_lower or "bulging" in q_lower:
            reply = (
                "**Testing & Replacing Electrolytic Capacitors:**\n\n"
                "1. **Visual Check:** Look for bulging tops, dark brown electrolyte crust at the base, or cracked sleeves.\n"
                "2. **Multimeter ESR Test:** A good capacitor has low ESR (<1.5Ω). High ESR indicates dried electrolyte.\n"
                "3. **Polarity Check:** ALWAYS match the negative (-) stripe marked on the capacitor sleeve to the shaded/striped side on the PCB silkscreen!\n\n"
                "⚠️ *Warning: Reversing polarity will cause the capacitor to explode under power!*"
            )
            suggested = [
                "Can I substitute a higher voltage capacitor?",
                "How to safely discharge a 400V capacitor?",
                "Show capacitor repair guide"
            ]

        elif "mosfet" in q_lower or "testing" in q_lower or "multimeter" in q_lower:
            reply = (
                "**How to Test an N-Channel MOSFET (e.g., IRFZ44N) with a Multimeter:**\n\n"
                "1. Set multimeter to **Diode Test Mode**.\n"
                "2. Place Red probe on **Source (Pin 3)** and Black probe on **Drain (Pin 2 / Tab)**. You should read ~0.4V to 0.7V (body diode).\n"
                "3. Touch Red probe briefly to **Gate (Pin 1)** while keeping Black on Source to charge the gate.\n"
                "4. Place Red probe back on Drain. The reading should drop near **0.00V** (channel opened!).\n"
                "5. Discharge gate by touching Gate to Source with finger. Reading should return to diode drop."
            )
            suggested = [
                "How to desolder a TO-220 MOSFET?",
                "What causes MOSFET gate blowout?",
                "Find compatible MOSFET replacement"
            ]

        else:
            reply = (
                f"I've analyzed your technical inquiry regarding **\"{query}\"**.\n\n"
                "Here are key diagnostics for electronic hardware repair:\n"
                "1. Always measure DC voltage rails starting from AC input down to secondary regulators.\n"
                "2. Perform cold resistance checks across power rails to GND before applying power.\n"
                "3. Inspect IC pin connections under magnification for micro-cracks or cold solder joints.\n\n"
                "Feel free to upload an image of your circuit board or ask for specific component pinouts!"
            )
            suggested = [
                "How to check for short circuits on motherboard?",
                "What temperature to set for soldering iron?",
                "Show service centers near me"
            ]

        return {
            "reply": reply,
            "suggested_actions": suggested
        }
