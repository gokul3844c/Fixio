from backend.database import SessionLocal, engine, Base
from backend.models import User, Component, DamageReport, RepairGuide, Product, ServiceCenter, Review, ChatHistory, Notification
from datetime import datetime

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Seed electronic components if empty or missing prompt components
        if db.query(Component).count() < 15:
            components = [
                Component(
                    name="LM317 Adjustable Voltage Regulator",
                    part_number="LM317",
                    manufacturer="Texas Instruments",
                    category="Integrated Circuit / Power Management",
                    purpose="Linear adjustable voltage regulator providing over 1.5A over a 1.2V to 37V output range.",
                    working_principle="Internal bandgap voltage reference maintains 1.25V between Output and Adjust terminals.",
                    specifications={
                        "Manufacturer": "Texas Instruments",
                        "Output Voltage Range": "1.25V to 37V",
                        "Max Output Current": "1.5A",
                        "Input Voltage Max": "40V",
                        "Package Type": "TO-220 / SOT-223",
                        "Operating Temp": "-40°C to 125°C"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "ADJ", "description": "Adjust terminal"},
                        {"pin": 2, "name": "OUTPUT", "description": "Regulated output voltage"},
                        {"pin": 3, "name": "INPUT", "description": "Unregulated input voltage"}
                    ],
                    datasheet_url="https://www.ti.com/lit/ds/symlink/lm317.pdf",
                    common_failures=["Thermal shutdown under high current without heatsink", "Output voltage drift"],
                    replacement_procedure="Desolder TO-220 pins, clean PCB pads, mount heatsink with thermal paste, and solder new IC.",
                    safety_notes="Ensure thermal paste is applied between TO-220 tab and metal heatsink.",
                    package_type="TO-220",
                    image_url="/assets/components/lm317.jpg"
                ),
                Component(
                    name="NE555 Precision Timing Circuit",
                    part_number="NE555",
                    manufacturer="STMicroelectronics",
                    category="Integrated Circuit / Timers",
                    purpose="Monolithic timing circuit capable of producing accurate time delays or oscillation.",
                    working_principle="Dual internal comparators trigger and reset a flip-flop based on RC charge/discharge.",
                    specifications={
                        "Manufacturer": "STMicroelectronics",
                        "Supply Voltage": "4.5V to 16V",
                        "Max Frequency": "500 kHz",
                        "Output Current": "200 mA",
                        "Package Type": "DIP-8 / SOIC-8"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "GND", "description": "Ground (0V)"},
                        {"pin": 2, "name": "TRIG", "description": "Trigger pulse input"},
                        {"pin": 3, "name": "OUT", "description": "Output high/low signal"},
                        {"pin": 4, "name": "RESET", "description": "Active-low reset"},
                        {"pin": 8, "name": "VCC", "description": "Supply voltage (+5V to +15V)"}
                    ],
                    datasheet_url="https://www.ti.com/lit/ds/symlink/ne555.pdf",
                    common_failures=["Latch-up caused by voltage spikes", "Blown output stage"],
                    replacement_procedure="Pop old IC out of DIP-8 socket or desolder SOIC-8 pins using hot air station.",
                    safety_notes="Verify correct VCC polarity before powering.",
                    package_type="DIP-8",
                    image_url="/assets/components/ne555.jpg"
                ),
                Component(
                    name="STM32F103C8T6 ARM Cortex-M3 MCU",
                    part_number="STM32F103C8T6",
                    manufacturer="STMicroelectronics",
                    category="Microcontroller / 32-Bit ARM",
                    purpose="High-performance 32-bit RISC microcontroller operating up to 72 MHz.",
                    working_principle="ARM Cortex-M3 core with embedded Flash memory and nested vector interrupt controller.",
                    specifications={
                        "Manufacturer": "STMicroelectronics",
                        "Core": "ARM Cortex-M3 (32-bit)",
                        "Clock Speed": "72 MHz",
                        "Flash Memory": "64 KB",
                        "SRAM": "20 KB",
                        "Operating Voltage": "2.0V to 3.6V"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "VBAT", "description": "Backup power supply"},
                        {"pin": 9, "name": "VDD", "description": "Digital 3.3V Power"},
                        {"pin": 34, "name": "SWDIO", "description": "Serial Wire Data"},
                        {"pin": 37, "name": "SWCLK", "description": "Serial Wire Clock"}
                    ],
                    datasheet_url="https://www.st.com/resource/en/datasheet/stm32f103c8.pdf",
                    common_failures=["Flash corruption due to brownout", "Damaged GPIO pins from 5V overvoltage"],
                    replacement_procedure="Use SMD hot air rework station at 350°C. Apply flux around LQFP-48 leads.",
                    safety_notes="Use ESD wrist strap when handling bare LQFP chips.",
                    package_type="LQFP-48",
                    image_url="/assets/components/stm32.jpg"
                ),
                Component(
                    name="ESP32-WROOM-32 Wi-Fi & Bluetooth Module",
                    part_number="ESP32-WROOM-32",
                    manufacturer="Espressif Systems",
                    category="Wireless / IoT Microcontroller",
                    purpose="Powerful Wi-Fi + Bluetooth LE MCU module targeting IoT automation and sensor networking.",
                    working_principle="Dual-core Xtensa 32-bit LX6 microprocessors running at up to 240 MHz.",
                    specifications={
                        "Manufacturer": "Espressif Systems",
                        "Processor": "Dual-Core Xtensa 32-bit LX6",
                        "Clock Speed": "240 MHz",
                        "Wi-Fi": "802.11 b/g/n",
                        "Bluetooth": "v4.2 BR/EDR and BLE",
                        "Flash Memory": "4 MB"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "GND", "description": "Ground"},
                        {"pin": 2, "name": "3V3", "description": "3.3V Power Input"},
                        {"pin": 3, "name": "EN", "description": "Enable / Reset"}
                    ],
                    datasheet_url="https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf",
                    common_failures=["Brownout reset on boot due to weak 3.3V power rail"],
                    replacement_procedure="Apply low-temp solder paste on PCB castellated pads, position module, apply hot air reflow.",
                    safety_notes="Ensure decoupling capacitor is placed close to 3V3 pin.",
                    package_type="Castellated Module",
                    image_url="/assets/components/esp32.jpg"
                ),
                Component(
                    name="ATmega328P 8-Bit AVR Microcontroller",
                    part_number="ATmega328P",
                    manufacturer="Microchip Technology",
                    category="Microcontroller / 8-Bit AVR",
                    purpose="High-performance low-power 8-bit AVR RISC microcontroller used on Arduino boards.",
                    working_principle="Executes powerful instructions in a single clock cycle.",
                    specifications={
                        "Manufacturer": "Microchip Technology",
                        "Architecture": "8-bit AVR RISC",
                        "Clock Frequency": "Up to 20 MHz",
                        "Flash Memory": "32 KB",
                        "Operating Voltage": "1.8V to 5.5V"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "RESET", "description": "Active-low reset pin"},
                        {"pin": 7, "name": "VCC", "description": "Digital supply voltage"},
                        {"pin": 8, "name": "GND", "description": "Ground"}
                    ],
                    datasheet_url="https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega48A-PA-88A-PA-168A-PA-328-P-DS-DS40002061B.pdf",
                    common_failures=["Corrupted bootloader", "Blown I/O port pin due to overcurrent"],
                    replacement_procedure="Lever old chip out of DIP-28 socket with IC puller tool. Insert replacement microcontroller.",
                    safety_notes="Never exceed 40mA per I/O pin.",
                    package_type="DIP-28",
                    image_url="/assets/components/atmega328p.jpg"
                ),
                Component(
                    name="IRF540N N-Channel Power MOSFET",
                    part_number="IRF540N",
                    manufacturer="Infineon Technologies",
                    category="Transistor / Power MOSFET",
                    purpose="Advanced HEXFET power MOSFET designed for high-speed switching and heavy DC motor load control.",
                    working_principle="N-channel enhancement mode transistor controlled by gate-to-source electric field.",
                    specifications={
                        "Manufacturer": "Infineon Technologies",
                        "Drain-Source Voltage (Vds)": "100V",
                        "Continuous Drain Current (Id)": "33A",
                        "Rds(on) Max": "44 mOhm",
                        "Package Type": "TO-220AB"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "GATE", "description": "Gate control terminal"},
                        {"pin": 2, "name": "DRAIN", "description": "Drain load terminal"},
                        {"pin": 3, "name": "SOURCE", "description": "Source ground terminal"}
                    ],
                    datasheet_url="https://www.infineon.com/dgdl/Infineon-IRF540N-DataSheet-v01_01-EN.pdf",
                    common_failures=["Gate oxide puncture caused by ESD"],
                    replacement_procedure="Desolder leads from PCB. Screw TO-220 tab onto heatsink, then solder pins.",
                    safety_notes="Connect 10k pull-down resistor between Gate and Source.",
                    package_type="TO-220AB",
                    image_url="/assets/components/irf540n.jpg"
                ),
                Component(
                    name="2N2222 NPN Bipolar Junction Transistor",
                    part_number="2N2222",
                    manufacturer="ON Semiconductor",
                    category="Transistor / BJT",
                    purpose="Ubiquitous NPN general-purpose silicon transistor used for low-power amplification and switching.",
                    working_principle="Base current controls larger Collector-Emitter current.",
                    specifications={
                        "Manufacturer": "ON Semiconductor",
                        "Collector-Emitter Voltage (Vceo)": "40V",
                        "Collector Current (Ic)": "800 mA",
                        "DC Current Gain (hFE)": "100 to 300"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "EMITTER", "description": "Emitter lead"},
                        {"pin": 2, "name": "BASE", "description": "Base control lead"},
                        {"pin": 3, "name": "COLLECTOR", "description": "Collector load lead"}
                    ],
                    datasheet_url="https://www.onsemi.com/pub/Collateral/P2N2222A-D.PDF",
                    common_failures=["Thermal breakdown caused by operation exceeding current limits"],
                    replacement_procedure="Verify pinout, trim leads, solder into place.",
                    safety_notes="Use current limiting resistor on Base pin.",
                    package_type="TO-92",
                    image_url="/assets/components/2n2222.jpg"
                ),
                Component(
                    name="LM358 Dual Operational Amplifier",
                    part_number="LM358",
                    manufacturer="Texas Instruments",
                    category="Integrated Circuit / Operational Amplifier",
                    purpose="Dual high-gain independent operational amplifier suitable for single power supply operation.",
                    working_principle="Internal differential input stage driving push-pull output stage.",
                    specifications={
                        "Manufacturer": "Texas Instruments",
                        "Supply Voltage": "3V to 32V",
                        "Gain Bandwidth": "1 MHz",
                        "Channels": "2 (Dual Op-Amp)",
                        "Package Type": "DIP-8 / SOIC-8"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "OUTPUT A", "description": "Op-Amp A Output"},
                        {"pin": 2, "name": "IN- A", "description": "Op-Amp A Inverting Input"},
                        {"pin": 3, "name": "IN+ A", "description": "Op-Amp A Non-Inverting Input"},
                        {"pin": 4, "name": "GND", "description": "Ground / Negative Supply"},
                        {"pin": 8, "name": "VCC", "description": "Positive Supply Input"}
                    ],
                    datasheet_url="https://www.ti.com/lit/ds/symlink/lm358.pdf",
                    common_failures=["Input overvoltage damage", "Output latch-up"],
                    replacement_procedure="Clean pads, align pin 1 notch, solder carefully using fine-tip iron.",
                    safety_notes="Do not exceed supply voltage maximum of 32V.",
                    package_type="DIP-8",
                    image_url="/assets/components/lm358.jpg"
                ),
                Component(
                    name="LM7805 Linear Voltage Regulator (5V)",
                    part_number="LM7805",
                    manufacturer="Texas Instruments",
                    category="Integrated Circuit / Power Management",
                    purpose="3-terminal positive voltage regulator delivering steady 5.0V output.",
                    working_principle="Internal series pass transistor regulated by bandgap voltage reference.",
                    specifications={
                        "Manufacturer": "Texas Instruments",
                        "Output Voltage": "5.0V DC",
                        "Max Current": "1.5A",
                        "Input Voltage": "7.0V to 25V",
                        "Package Type": "TO-220"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "INPUT", "description": "Unregulated Input Voltage (7V - 25V)"},
                        {"pin": 2, "name": "GND", "description": "Common Ground"},
                        {"pin": 3, "name": "OUTPUT", "description": "Regulated 5.0V Output"}
                    ],
                    datasheet_url="https://www.sparkfun.com/datasheets/Components/LM7805.pdf",
                    common_failures=["Thermal shutdown under high current", "Input short to ground"],
                    replacement_procedure="Apply thermal compound on TO-220 backplate, attach heatsink, solder 3 leads.",
                    safety_notes="Input voltage must be at least 2V higher than 5V output (minimum 7.0V).",
                    package_type="TO-220",
                    image_url="/assets/components/lm7805.jpg"
                ),
                Component(
                    name="IRFZ44N N-Channel Power MOSFET",
                    part_number="IRFZ44N",
                    manufacturer="Infineon Technologies",
                    category="Transistor / Power MOSFET",
                    purpose="High-performance 55V single N-channel HEXFET power MOSFET.",
                    working_principle="N-channel enhancement mode transistor for DC switching.",
                    specifications={
                        "Manufacturer": "Infineon Technologies",
                        "Vds": "55V",
                        "Continuous Id": "49A",
                        "Rds(on)": "17.5 mOhm",
                        "Package Type": "TO-220AB"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "GATE", "description": "Gate input"},
                        {"pin": 2, "name": "DRAIN", "description": "Drain load terminal"},
                        {"pin": 3, "name": "SOURCE", "description": "Source ground terminal"}
                    ],
                    datasheet_url="https://www.infineon.com/dgdl/Infineon-IRFZ44N-DataSheet-v01_01-EN.pdf",
                    common_failures=["Gate oxide breakdown from ESD spike"],
                    replacement_procedure="Mount TO-220 onto heatsink with insulating mica washer, then solder pins.",
                    safety_notes="Always include pull-down resistor on gate terminal.",
                    package_type="TO-220AB",
                    image_url="/assets/components/irfz44n.jpg"
                ),
                Component(
                    name="1N4007 Silicon Power Rectifier Diode",
                    part_number="1N4007",
                    manufacturer="ON Semiconductor",
                    category="Diode / Rectifier",
                    purpose="General-purpose 1A 1000V silicon power rectifier diode.",
                    working_principle="P-N junction diode allowing current flow in cathode direction only.",
                    specifications={
                        "Manufacturer": "ON Semiconductor",
                        "Forward Current": "1.0A",
                        "Repetitive Reverse Voltage": "1000V",
                        "Forward Drop": "1.1V",
                        "Package Type": "DO-41"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "ANODE", "description": "Positive terminal"},
                        {"pin": 2, "name": "CATHODE", "description": "Negative terminal (marked with band)"}
                    ],
                    datasheet_url="https://www.onsemi.com/pub/Collateral/1N4001-D.PDF",
                    common_failures=["Shorted PN junction from overcurrent reverse surge"],
                    replacement_procedure="Observe silver cathode band orientation on PCB silkworm print. Solder leads.",
                    safety_notes="Ensure correct polarity prior to applying AC voltage.",
                    package_type="DO-41",
                    image_url="/assets/components/1n4007.jpg"
                ),
                Component(
                    name="BC547 NPN General Purpose Transistor",
                    part_number="BC547",
                    manufacturer="Fairchild / ON Semi",
                    category="Transistor / BJT",
                    purpose="Low-noise NPN bipolar junction transistor for signal amplification and switching.",
                    working_principle="NPN silicon junction controlled by base current.",
                    specifications={
                        "Manufacturer": "ON Semiconductor",
                        "Vceo": "45V",
                        "Collector Current": "100 mA",
                        "DC Current Gain": "110 to 800",
                        "Package Type": "TO-92"
                    },
                    pin_diagram=[
                        {"pin": 1, "name": "COLLECTOR", "description": "Collector terminal"},
                        {"pin": 2, "name": "BASE", "description": "Base control terminal"},
                        {"pin": 3, "name": "EMITTER", "description": "Emitter ground terminal"}
                    ],
                    datasheet_url="https://www.onsemi.com/pub/Collateral/BC546-D.PDF",
                    common_failures=["Thermal breakdown from excessive base-emitter current"],
                    replacement_procedure="Check TO-92 flat face orientation on PCB silkscreen, trim leads, solder.",
                    safety_notes="Always place base resistor to limit drive current.",
                    package_type="TO-92",
                    image_url="/assets/components/bc547.jpg"
                )
            ]
            db.add_all(components)
            db.commit()

        # Re-seed if no repair guides exist for property damage
        first_guide = db.query(RepairGuide).filter(RepairGuide.category != None).first()
        if first_guide and "Wall" in first_guide.title:
            print("Database already seeded with Fixio data.")
            return

        print("Seeding initial Fixio database...")

        # 1. User
        demo_user = db.query(User).filter(User.email == "karthik@example.com").first()
        if not demo_user:
            demo_user = User(
                full_name="Karthik R.",
                email="karthik@example.com",
                password_hash="pbkdf2_sha256_mock_hash",
                phone="+91 98765 43210",
                location="Chennai, Tamil Nadu",
                avatar_url="/assets/avatars/user.jpg",
                role="user"
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)

        # 2. Service Centers
        sc1 = ServiceCenter(
            store_name="Metro Structural & Masonry Experts",
            category="Masonry & Structural",
            address="124 Anna Salai, T. Nagar",
            city="Chennai",
            state="Tamil Nadu",
            phone="+91 44 2434 8899",
            opening_hours="08:00 AM - 07:00 PM",
            is_open_now=True,
            rating=4.9,
            review_count=48,
            lat=13.0418,
            lng=80.2341,
            distance_km=1.2,
            is_authorized=True,
            image_url="/assets/stores/store1.jpg"
        )

        sc2 = ServiceCenter(
            store_name="AquaShield Waterproofing & Plumbing",
            category="Plumbing & Water",
            address="45 Arcot Road, Kodambakkam",
            city="Chennai",
            state="Tamil Nadu",
            phone="+91 44 2481 1122",
            opening_hours="08:30 AM - 08:00 PM",
            is_open_now=True,
            rating=4.8,
            review_count=36,
            lat=13.0512,
            lng=80.2205,
            distance_km=2.8,
            is_authorized=True,
            image_url="/assets/stores/store2.jpg"
        )

        sc3 = ServiceCenter(
            store_name="Apex Roof & Tile Contracting",
            category="Roofing & Tiles",
            address="88 L.B. Road, Adyar",
            city="Chennai",
            state="Tamil Nadu",
            phone="+91 44 2441 5566",
            opening_hours="09:00 AM - 06:00 PM",
            is_open_now=False,
            rating=4.7,
            review_count=22,
            lat=13.0012,
            lng=80.2565,
            distance_km=4.5,
            is_authorized=False,
            image_url="/assets/stores/store3.jpg"
        )

        sc4 = ServiceCenter(
            store_name="VoltSafe Electrical Services",
            category="Electrical Hazard",
            address="12 100 Feet Road, Velachery",
            city="Chennai",
            state="Tamil Nadu",
            phone="+91 44 2243 7788",
            opening_hours="08:00 AM - 09:00 PM",
            is_open_now=True,
            rating=4.85,
            review_count=54,
            lat=12.9815,
            lng=80.2180,
            distance_km=6.1,
            is_authorized=True,
            image_url="/assets/stores/store4.jpg"
        )

        db.add_all([sc1, sc2, sc3, sc4])
        db.commit()
        db.refresh(sc1)
        db.refresh(sc2)

        # 3. Reviews
        rev1 = Review(
            service_center_id=sc1.id,
            user_id=demo_user.id,
            user_name="Karthik R.",
            rating=5,
            comment="Excellent work on repairing the compound wall crack. Professional team, clean finishing!",
            verified_job=True,
            provider_response="Thank you Karthik! Glad we could help restore your wall safely."
        )

        rev2 = Review(
            service_center_id=sc2.id,
            user_id=demo_user.id,
            user_name="Arun V.",
            rating=4,
            comment="Prompt leak detection service. Solved the concealed pipe seepage issue in 3 hours.",
            verified_job=True,
            provider_response="Thanks Arun!"
        )

        db.add_all([rev1, rev2])

        # 4. Repair Guides for key categories
        guides = [
            RepairGuide(
                title="Repairing Exterior & Interior Wall Cracks",
                category="Wall cracks",
                difficulty="Intermediate",
                repair_time="2 - 4 hours",
                short_explanation="Wall cracks occur due to thermal expansion, foundation settlement, or moisture penetration. Proper filling prevents water seepage and structural degradation.",
                common_causes=[
                    "Thermal movement of cement plaster",
                    "Moisture ingress & freeze-thaw cycles",
                    "Minor foundation setting",
                    "Inadequate curing during construction"
                ],
                signs_to_check=[
                    "Check crack width with a feeler gauge",
                    "Look for peeling paint or white efflorescence near the crack",
                    "Check if the crack extends diagonally across structural columns"
                ],
                safe_diy_actions=[
                    "Scrape away loose plaster & debris",
                    "V-cut hairline cracks slightly for sealant adhesion",
                    "Apply elastomeric masonry sealant or crack-fill putty",
                    "Sand smooth & repaint with exterior weatherproof primer"
                ],
                professional_actions=[
                    "Structural stitching with steel rebar pins for load-bearing cracks",
                    "Polyurethane resin pressure injection for deep structural fractures",
                    "Foundation underpinning"
                ],
                required_tools=[
                    {"name": "Putty Knife & Scraper", "icon": "fa-screwdriver"},
                    {"name": "Stiff Wire Brush", "icon": "fa-brush"},
                    {"name": "Caulking Gun", "icon": "fa-fill-drip"},
                    {"name": "Flexible Crack Filler Compound", "icon": "fa-box"},
                    {"name": "Sandpaper (120 grit)", "icon": "fa-scroll"}
                ],
                safety_precautions=[
                    "Wear safety goggles and dust mask when scraping plaster.",
                    "Use a stable step ladder for upper wall surfaces.",
                    "Never ignore wide expanding diagonal cracks (>5mm)."
                ],
                estimated_cost_range="$30 - $120 (₹2,500 - ₹9,000)",
                when_to_stop="STOP DIY repair if the crack is widening rapidly, spans across support beams, or doors/windows near the wall stick tight.",
                related_service_categories=["Masonry & Structural", "Paints & Plaster"],
                steps=[
                    {
                        "step_number": 1,
                        "title": "Clean & Open the Crack",
                        "detail": "Use a wire brush and scraper to widen the crack slightly into a V-shape. Remove all dust, sand particles, and flaking paint.",
                        "tip": "Wetting the crack with water spray improves adhesion of cementitious fillers."
                    },
                    {
                        "step_number": 2,
                        "title": "Apply Polymer Crack Filler",
                        "detail": "Press elastomeric crack sealant firmly into the cavity using a putty knife. Ensure no air gaps remain.",
                        "tip": "Overfill slightly as filler shrinks slightly as it cures."
                    },
                    {
                        "step_number": 3,
                        "title": "Smooth & Cure",
                        "detail": "Smooth the surface flat with a wet spatula. Allow 24 hours full curing time before sanding.",
                        "tip": "Apply a coat of alkali-resistant primer before final paint coat."
                    }
                ]
            ),
            RepairGuide(
                title="Treating Dampness & Water Leakage in Walls",
                category="Dampness or water leakage",
                difficulty="Advanced",
                repair_time="4 - 8 hours",
                short_explanation="Dampness is caused by plumbing leaks, rainwater seepage, or capillary action from the ground. Treating the root moisture source is essential before surface refinishing.",
                common_causes=[
                    "Concealed pipe joint leakage",
                    "Defective exterior wall waterproofing",
                    "Damaged damp-proof course (DPC)",
                    "Blocked rainwater gutters"
                ],
                signs_to_check=[
                    "Flaking paint & bubbling plaster",
                    "Musty odor and mold growth",
                    "Moisture meter reading above 15%"
                ],
                safe_diy_actions=[
                    "Fix accessible leaking tap washers or external pipe fittings",
                    "Clear blocked roof drainage channels",
                    "Scrape damp plaster and apply anti-fungal solution",
                    "Apply silicone-based damp block primer"
                ],
                professional_actions=[
                    "Thermal imaging leak detection",
                    "Chemical DPC injection at plinth level",
                    "External wall hydrophobic coating installation"
                ],
                required_tools=[
                    {"name": "Moisture Meter", "icon": "fa-gauge"},
                    {"name": "Anti-Fungal Treatment Wash", "icon": "fa-spray-can"},
                    {"name": "Waterproof Damp Block Sealant", "icon": "fa-shield"},
                    {"name": "Scraper & Paint Brush", "icon": "fa-paint-roller"}
                ],
                safety_precautions=[
                    "Keep electrical power turned off near damp electrical switchboards.",
                    "Wear gloves and mask when applying anti-fungal chemical wash."
                ],
                estimated_cost_range="$80 - $250 (₹6,500 - ₹20,000)",
                when_to_stop="STOP DIY if water actively drips from electrical conduits or if water pools near main power panels.",
                related_service_categories=["Plumbing & Water", "Paints & Plaster"],
                steps=[
                    {
                        "step_number": 1,
                        "title": "Isolate Leak Source",
                        "detail": "Check internal plumbing lines and roof rainwater drains to confirm active source.",
                        "tip": "Turn off main stopcock valve to see if meter stops running."
                    },
                    {
                        "step_number": 2,
                        "title": "Strip Damaged Plaster",
                        "detail": "Chisel out hollow damaged plaster 6 inches beyond the damp boundary.",
                        "tip": "Allow raw masonry to dry thoroughly under ventilation for 48 hours."
                    },
                    {
                        "step_number": 3,
                        "title": "Apply Waterproof Barrier & Re-plaster",
                        "detail": "Apply 2 coats of latex waterproofing slurry followed by polymer mortar plaster.",
                        "tip": "Finish with breathable exterior paint."
                    }
                ]
            ),
            RepairGuide(
                title="Replacing Broken Roof & Floor Tiles",
                category="Broken tiles",
                difficulty="Intermediate",
                repair_time="2 - 3 hours",
                short_explanation="Cracked or broken tiles allow water penetration into lower slabs and create tripping hazards.",
                common_causes=["Heavy object impact", "Thermal stress", "Hollow mortar bedding"],
                signs_to_check=["Hollow sound on tapping", "Cracked grout lines"],
                safe_diy_actions=["Chisel out broken tile pieces", "Clean base mortar", "Apply tile adhesive & press new tile", "Grout joints"],
                professional_actions=["Large scale terrace retiling & membrane waterproofing"],
                required_tools=[
                    {"name": "Grout Saw & Chisel", "icon": "fa-hammer"},
                    {"name": "Rubber Mallet", "icon": "fa-gavel"},
                    {"name": "Notched Trowel & Tile Adhesive", "icon": "fa-trowel"}
                ],
                safety_precautions=["Wear eye protection against flying tile chips."],
                estimated_cost_range="$40 - $100 (₹3,000 - ₹8,000)",
                when_to_stop="STOP if terrace slab concrete beneath tile shows heavy corrosion of steel rebar.",
                related_service_categories=["Roofing & Tiles", "Masonry & Structural"],
                steps=[
                    {
                        "step_number": 1,
                        "title": "Remove Damaged Tile",
                        "detail": "Rake out perimeter grout then carefully chisel broken tile from center outward.",
                        "tip": "Avoid damaging adjacent intact tiles."
                    },
                    {
                        "step_number": 2,
                        "title": "Set & Grout Replacement Tile",
                        "detail": "Comb polymer thin-set adhesive onto substrate and set new tile level.",
                        "tip": "Use tile spacers for uniform grout joints."
                    }
                ]
            ),
            RepairGuide(
                title="Safely Managing Electrical Conduit & Wire Hazards",
                category="Electrical hazards",
                difficulty="Advanced / Professional",
                repair_time="1 - 3 hours",
                short_explanation="Exposed wiring or weathered conduit poses severe risk of electrical shock or short-circuit fire.",
                common_causes=["UV deterioration", "Mechanical impact", "Rodent damage"],
                signs_to_check=["Frayed wire insulation", "Sparks", "Burning plastic smell"],
                safe_diy_actions=["Turn OFF main breaker immediately", "Keep area dry & mark hazard"],
                professional_actions=["Replace wiring harness", "Install outdoor IP66 weatherproof junction box"],
                required_tools=[
                    {"name": "Non-Contact Voltage Tester", "icon": "fa-bolt"},
                    {"name": "Insulated Wire Strippers", "icon": "fa-scissors"}
                ],
                safety_precautions=["NEVER TOUCH EXPOSED LIVE WIRES. Always verify zero voltage before touching any conduit."],
                estimated_cost_range="$50 - $180 (₹4,000 - ₹14,000)",
                when_to_stop="URGENT: Call a licensed electrician immediately. Do not attempt DIY on live main lines.",
                related_service_categories=["Electrical Hazard"],
                steps=[
                    {
                        "step_number": 1,
                        "title": "De-energize Circuit",
                        "detail": "Switch off MCB/ELCB breaker at distribution board. Verify zero voltage with tester.",
                        "tip": "Lock out breaker panel so no one switches it back on."
                    }
                ]
            )
        ]

        db.add_all(guides)

        # 5. Products
        products = [
            Product(
                name="Elastomeric Masonry Crack Sealant (1kg)",
                part_number="FIX-CRACK-1KG",
                category="Wall Repair",
                price=12.50,
                price_formatted="$12.50 / ₹950",
                stock_status="In Stock",
                stock_quantity=300,
                compatibility_info="Flexible waterproof acrylic filler for exterior & interior wall cracks.",
                rating=4.9,
                image_url=""
            ),
            Product(
                name="Hydrophobic Wall Waterproofing Slurry (5 Litres)",
                part_number="FIX-HYDRO-5L",
                category="Waterproofing",
                price=34.00,
                price_formatted="$34.00 / ₹2,700",
                stock_status="In Stock",
                stock_quantity=150,
                compatibility_info="Deep penetrating barrier against dampness and salt efflorescence.",
                rating=4.8,
                image_url=""
            ),
            Product(
                name="Polymer Modified Waterproof Tile Adhesive (20kg)",
                part_number="FIX-TILE-ADH-20K",
                category="Roofing & Tiles",
                price=18.00,
                price_formatted="$18.00 / ₹1,400",
                stock_status="In Stock",
                stock_quantity=200,
                compatibility_info="High-bond strength adhesive for outdoor terrace & floor tile repairs.",
                rating=4.85,
                image_url=""
            )
        ]
        db.add_all(products)

        # 6. Notifications
        n1 = Notification(
            user_id=demo_user.id,
            title="Scan Complete: Compound Entrance Wall",
            message="AI Scanner identified 1 Medium Wall Crack. Repair guide generated.",
            type="info"
        )
        db.add(n1)

        db.commit()
        print("Fixio database seeding completed successfully.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
