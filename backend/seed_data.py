from backend.database import SessionLocal, engine, Base
from backend.models import User, Component, DamageReport, RepairGuide, Product, ServiceCenter, ChatHistory, Notification
from datetime import datetime

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Component).first():
            print("Database already seeded.")
            return

        print("Seeding initial database...")

        # 1. Users
        demo_user = User(
            full_name="Karthik R.",
            email="karthik@example.com",
            password_hash="pbkdf2_sha256_mock_hash",
            phone="+91 98765 43210",
            location="Chennai, Tamil Nadu",
            avatar_url="/assets/avatars/user.jpg",
            role="Senior Electronics Technician"
        )
        db.add(demo_user)

        # 2. Components
        c1 = Component(
            name="Voltage Regulator IC",
            part_number="LM7805",
            category="IC",
            purpose="Regulates input voltage and maintains a constant 5V DC output for microcontrollers and digital logic.",
            working_principle="Linear voltage regulator that drops excess input voltage across an internal series transistor as heat.",
            specifications={
                "Input Voltage": "7V - 25V DC",
                "Output Voltage": "5V DC (±4%)",
                "Output Current": "1.5A Max",
                "Package": "TO-220 / DPAK",
                "Thermal Shutdown": "150°C",
                "Pin Count": 3
            },
            pin_diagram=[
                {"pin": 1, "name": "Input (VI)", "desc": "Unregulated DC Input (7-25V)"},
                {"pin": 2, "name": "Ground (GND)", "desc": "Common Ground Connection"},
                {"pin": 3, "name": "Output (VO)", "desc": "Regulated 5V DC Output"}
            ],
            datasheet_url="https://www.ti.com/lit/ds/symlink/lm7805.pdf",
            common_failures=[
                "Thermal Overheating due to insufficient heatsink",
                "Short circuit output leading to internal pass transistor failure",
                "Output voltage drop or noise ripple caused by degraded input capacitors"
            ],
            replacement_procedure="1. Discharge all circuit capacitors.\n2. Desolder the 3 pins using solder wick and desoldering pump at 350°C.\n3. Remove heat sink screw if present.\n4. Apply thermal paste on new LM7805 backing plate.\n5. Align and solder new IC into position.\n6. Inspect joints with magnifying loupe.",
            safety_notes="Ensure power supply is disconnected before desoldering. Thermal paste contains silicone metal oxide.",
            package_type="TO-220",
            image_url="/assets/components/lm7805.png"
        )

        c2 = Component(
            name="Electrolytic Capacitor 10uF 25V",
            part_number="ECE-A1EV100",
            category="Capacitor",
            purpose="Filtering power supply ripples and decoupling noise in high-frequency power rails.",
            working_principle="Stores electrical energy electrostatically between aluminum foil plates insulated by electrolyte paper.",
            specifications={
                "Capacitance": "10 µF",
                "Voltage Rating": "25V DC",
                "Tolerance": "±20%",
                "Max Temp": "105°C",
                "ESR": "1.2 Ω",
                "Type": "Radial Aluminum Electrolytic"
            },
            pin_diagram=[
                {"pin": 1, "name": "Positive (+)", "desc": "Longer Anode Pin"},
                {"pin": 2, "name": "Negative (-)", "desc": "Shorter Cathode Pin (Striped Marking)"}
            ],
            datasheet_url="https://industrial.panasonic.com/cdbs/www-data/pdf/ABA0000/ABA0000C1032.pdf",
            common_failures=[
                "Top vent bulging or electrolyte leakage",
                "High Equivalent Series Resistance (ESR) due to dried electrolyte",
                "Dielectric breakdown causing direct short circuit"
            ],
            replacement_procedure="1. Observe polarity marking on PCB before removal.\n2. Apply flux and desolder negative and positive leads.\n3. Insert replacement capacitor respecting polarity (+ longer lead).\n4. Solder leads securely and trim excess with flush cutters.",
            safety_notes="Reversing polarity will cause internal gas build-up and explosive venting!",
            package_type="Radial Through-Hole",
            image_url="/assets/components/capacitor.png"
        )

        c3 = Component(
            name="N-Channel Power MOSFET",
            part_number="IRFZ44N",
            category="MOSFET",
            purpose="High-speed switching and power management in motor drivers, inverter stages, and DC-DC converters.",
            working_principle="Voltage-controlled semiconductor where gate voltage modulates channel conductivity between Drain and Source.",
            specifications={
                "Vds (Drain-Source)": "55V",
                "Id (Continuous Drain Current)": "49A",
                "Rds(on)": "17.5 mΩ",
                "Gate Threshold Voltage": "2.0V - 4.0V",
                "Package": "TO-220AB"
            },
            pin_diagram=[
                {"pin": 1, "name": "Gate (G)", "desc": "Control Voltage Input"},
                {"pin": 2, "name": "Drain (D)", "desc": "High Current Output / Tab"},
                {"pin": 3, "name": "Source (S)", "desc": "Ground / Current Sense Connection"}
            ],
            datasheet_url="https://www.infineon.com/dgdl/irfz44n.pdf",
            common_failures=[
                "Gate-to-Source oxide breakdown from ESD spike",
                "Drain-Source short circuit from overcurrent overload",
                "Thermal runaway and charred casing"
            ],
            replacement_procedure="1. Use ESD wrist strap before handling replacement MOSFET.\n2. Desolder Gate, Drain, and Source pins.\n3. Clean pads with isopropyl alcohol (IPA).\n4. Solder new MOSFET ensuring no bridging between Gate and Drain.",
            safety_notes="Always wear ESD protection. Static discharge above 20V can rupture gate oxide.",
            package_type="TO-220AB",
            image_url="/assets/components/mosfet.png"
        )

        c4 = Component(
            name="Fast Switching Schottky Diode",
            part_number="1N5819",
            category="Diode",
            purpose="Flyback diode protection, reverse polarity protection, and high-efficiency rectification.",
            working_principle="Metal-semiconductor junction with very low forward voltage drop (~0.3V) and ultra-fast reverse recovery time.",
            specifications={
                "Forward Current": "1.0 A",
                "Reverse Repetitive Voltage": "40 V",
                "Forward Voltage Drop": "0.45 V @ 1A",
                "Package": "DO-41 Axial"
            },
            pin_diagram=[
                {"pin": 1, "name": "Anode (A)", "desc": "Positive Lead"},
                {"pin": 2, "name": "Cathode (K)", "desc": "Negative Band Banded Lead"}
            ],
            datasheet_url="https://www.diodes.com/assets/Datasheets/ds23001.pdf",
            common_failures=[
                "Thermal overload causing short circuit in both directions",
                "Reverse leakage current increase under temperature"
            ],
            replacement_procedure="1. Note silver cathode band direction on PCB silkscreen.\n2. Desolder component leads.\n3. Form leads on new 1N5819 diode and solder in correct orientation.",
            safety_notes="Incorrect cathode orientation will short out power rails upon power-up.",
            package_type="DO-41 Axial",
            image_url="/assets/components/diode.png"
        )

        db.add_all([c1, c2, c3, c4])
        db.commit()

        # 3. Damage Reports (Sample Scans)
        scan1 = DamageReport(
            user_id=demo_user.id,
            device_name="Smart TV Main Motherboard Rev 4.1",
            component_id=c1.id,
            component_name="Voltage Regulator IC",
            part_number="LM7805",
            image_path="/assets/scans/pcb_sample1.jpg",
            damage_status="Damaged - Thermal Burn",
            confidence_percentage=94.5,
            severity_level="High",
            estimated_repair_cost="$15 - $25 (₹120 - ₹250)",
            estimated_repair_time="30 - 60 mins",
            bounding_boxes=[
                {
                    "id": "box_1",
                    "label": "Voltage Regulator IC (LM7805)",
                    "part_number": "LM7805",
                    "status": "Damaged",
                    "severity": "High",
                    "confidence": 94.5,
                    "x": 38.5,
                    "y": 25.0,
                    "width": 24.0,
                    "height": 28.0,
                    "issue_description": "Severe thermal discoloration and charred package body. Pass transistor short circuit detected."
                },
                {
                    "id": "box_2",
                    "label": "Smoothing Capacitor 10uF",
                    "part_number": "ECE-A1EV100",
                    "status": "Warning",
                    "severity": "Medium",
                    "confidence": 88.2,
                    "x": 68.0,
                    "y": 55.0,
                    "width": 18.0,
                    "height": 22.0,
                    "issue_description": "Slight bulging on top rubber safety vent. ESR degradation suspected due to heat exposure."
                },
                {
                    "id": "box_3",
                    "label": "Flyback Diode (1N5819)",
                    "part_number": "1N5819",
                    "status": "Healthy",
                    "severity": "Low",
                    "confidence": 97.1,
                    "x": 18.0,
                    "y": 62.0,
                    "width": 15.0,
                    "height": 16.0,
                    "issue_description": "Normal visual condition. No charring or thermal cracking present."
                }
            ],
            damage_cause="Prolonged thermal overload without adequate heatsink cooling, leading to junction temperature exceedance above 150°C.",
            repair_steps_summary=[
                "Power down unit and discharge high-voltage primary filter capacitors.",
                "Desolder the damaged LM7805 IC using hot air rework station or desoldering wick.",
                "Clean PCB solder pads thoroughly with Isopropyl Alcohol (IPA > 99%).",
                "Apply fresh high-grade thermal paste to replacement TO-220 backplate.",
                "Solder new LM7805 IC, inspect for solder bridges, and test 5V output rail under load."
            ],
            datasheet_url="https://www.ti.com/lit/ds/symlink/lm7805.pdf"
        )
        db.add(scan1)

        # 4. Repair Guides
        rg1 = RepairGuide(
            title="How to Replace Damaged LM7805 Voltage Regulator IC",
            component_id=c1.id,
            difficulty="Intermediate",
            repair_time="30 - 60 mins",
            required_tools=[
                {"name": "Temperature Controlled Soldering Iron (350°C)", "icon": "fa-fire"},
                {"name": "Desoldering Vacuum Pump / Solder Wick", "icon": "fa-wind"},
                {"name": "Digital Multimeter with Diode Mode", "icon": "fa-bolt"},
                {"name": "Thermal Compound / Heatsink Paste", "icon": "fa-fill-drip"},
                {"name": "Isopropyl Alcohol (IPA 99%) & ESD Brush", "icon": "fa-pump-soap"}
            ],
            safety_precautions=[
                "Always unplug the device from mains AC before starting work.",
                "Wear ESD anti-static wrist strap to protect surrounding microchips.",
                "Use safety eye protection goggles while desoldering.",
                "Do not overheat PCB pads above 380°C to avoid copper trace lifting.",
                "Ensure proper room ventilation when working with solder flux fumes."
            ],
            steps=[
                {
                    "step_number": 1,
                    "title": "Discharge Power Supply Capacitors",
                    "detail": "Disconnect all power cords. Connect a 1kΩ 5W power resistor across the main 400V bulk capacitor leads to discharge residual electrical charge safely.",
                    "tip": "Measure voltage across capacitor with multimeter DC range to confirm 0V before proceeding."
                },
                {
                    "step_number": 2,
                    "title": "Desolder Damaged LM7805 IC",
                    "detail": "Apply flux to all 3 pins. Heat each joint with soldering iron set to 350°C and use desoldering pump or copper braid wick to remove all solder from pad holes.",
                    "tip": "Gently wiggle the pins with tweezers to verify they are completely freed from the PCB barrel."
                },
                {
                    "step_number": 3,
                    "title": "Clean PCB Pads & Inspect Traces",
                    "detail": "Saturate ESD brush with 99% Isopropyl Alcohol and scrub away burnt flux residue and carbonized material around the regulator footprints.",
                    "tip": "Inspect trace continuity with multimeter beep mode to check if any copper pads pulled up."
                },
                {
                    "step_number": 4,
                    "title": "Prepare & Install Replacement IC",
                    "detail": "Bend replacement LM7805 leads to fit pad pitch precisely. Coat the back metal tab with a thin uniform layer of thermal grease.",
                    "tip": "Tighten heatsink screw firmly before soldering pins to avoid mechanical strain on solder joints."
                },
                {
                    "step_number": 5,
                    "title": "Solder Joints & Perform Power-On Verification",
                    "detail": "Solder Input, Ground, and Output leads. Trim excess lead length. Apply DC input power and measure Output pin to confirm steady 5.00V ± 0.05V DC.",
                    "tip": "If output is under 4.5V or oscillating, check input bypass capacitor."
                }
            ],
            video_url="https://www.youtube.com/embed/demo_soldering_guide"
        )
        db.add(rg1)

        # 5. Marketplace Products
        p1 = Product(
            component_id=c1.id,
            name="LM7805 Voltage Regulator IC (5V 1.5A)",
            part_number="LM7805-TO220",
            category="ICs",
            price=0.25,
            price_formatted="$0.25 / ₹20",
            stock_status="In Stock",
            stock_quantity=450,
            compatibility_info="Universal replacement for all 5V linear power supply circuits.",
            rating=4.9,
            image_url="/assets/products/lm7805_part.jpg"
        )

        p2 = Product(
            component_id=c2.id,
            name="10uF 25V Radial Electrolytic Capacitor (High Temp 105°C)",
            part_number="ECE-10UF25V",
            category="Capacitors",
            price=0.10,
            price_formatted="$0.10 / ₹8",
            stock_status="In Stock",
            stock_quantity=1200,
            compatibility_info="Ideal low-ESR bypass capacitor for power rail filtering.",
            rating=4.8,
            image_url="/assets/products/capacitor_part.jpg"
        )

        p3 = Product(
            component_id=c3.id,
            name="IRFZ44N N-Channel Power MOSFET (55V 49A)",
            part_number="IRFZ44N-TO220",
            category="MOSFETs",
            price=0.45,
            price_formatted="$0.45 / ₹35",
            stock_status="In Stock",
            stock_quantity=320,
            compatibility_info="Compatible with inverter stages, motor drives, and SMPS power supplies.",
            rating=4.9,
            image_url="/assets/products/mosfet_part.jpg"
        )

        p4 = Product(
            component_id=c4.id,
            name="1N5819 Schottky Barrier Diode (40V 1A)",
            part_number="1N5819-DO41",
            category="Diodes",
            price=0.05,
            price_formatted="$0.05 / ₹4",
            stock_status="In Stock",
            stock_quantity=2000,
            compatibility_info="Fast switching flyback protection diode.",
            rating=4.7,
            image_url="/assets/products/diode_part.jpg"
        )

        db.add_all([p1, p2, p3, p4])

        # 6. Service Centers
        sc1 = ServiceCenter(
            store_name="Master Electronics Repair Service",
            address="124 Anna Salai, T. Nagar",
            city="Chennai",
            state="Tamil Nadu",
            phone="+91 44 2434 8899",
            opening_hours="09:30 AM - 08:30 PM",
            rating=4.9,
            review_count=342,
            lat=13.0418,
            lng=80.2341,
            distance_km=1.2,
            is_authorized=True,
            image_url="/assets/stores/store1.jpg"
        )

        sc2 = ServiceCenter(
            store_name="Sri Venkateshwara Electronics & Micro-Soldering",
            address="45 Arcot Road, Kodambakkam",
            city="Chennai",
            state="Tamil Nadu",
            phone="+91 44 2481 1122",
            opening_hours="10:00 AM - 09:00 PM",
            rating=4.8,
            review_count=189,
            lat=13.0512,
            lng=80.2205,
            distance_km=2.8,
            is_authorized=True,
            image_url="/assets/stores/store2.jpg"
        )

        sc3 = ServiceCenter(
            store_name="Raj Electronics Repair Hub",
            address="88 L.B. Road, Adyar",
            city="Chennai",
            state="Tamil Nadu",
            phone="+91 44 2441 5566",
            opening_hours="09:00 AM - 08:00 PM",
            rating=4.7,
            review_count=115,
            lat=13.0012,
            lng=80.2565,
            distance_km=4.5,
            is_authorized=False,
            image_url="/assets/stores/store3.jpg"
        )

        sc4 = ServiceCenter(
            store_name="Smart Care Chip-Level Service Center",
            address="12 100 Feet Road, Velachery",
            city="Chennai",
            state="Tamil Nadu",
            phone="+91 44 2243 7788",
            opening_hours="10:00 AM - 08:00 PM",
            rating=4.8,
            review_count=210,
            lat=12.9815,
            lng=80.2180,
            distance_km=6.1,
            is_authorized=True,
            image_url="/assets/stores/store4.jpg"
        )

        db.add_all([sc1, sc2, sc3, sc4])

        # 7. Notifications
        n1 = Notification(
            user_id=demo_user.id,
            title="Scan Complete: Smart TV Board",
            message="AI Scanner identified 1 Damaged IC (LM7805) and 1 Warning Capacitor.",
            type="warning"
        )
        n2 = Notification(
            user_id=demo_user.id,
            title="Repair Guide Ready",
            message="Step-by-step replacement procedure generated for LM7805 IC.",
            type="info"
        )
        db.add_all([n1, n2])

        db.commit()
        print("Database seeding completed successfully.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
