import os
from PIL import Image, ImageDraw, ImageFont

def generate_sample_assets():
    base_dirs = [
        "d:/project/backend/static/assets/scans",
        "d:/project/backend/static/assets/components",
        "d:/project/backend/static/assets/products",
        "d:/project/backend/static/assets/stores",
        "d:/project/frontend/assets/scans",
        "d:/project/frontend/assets/components",
        "d:/project/frontend/assets/products",
        "d:/project/frontend/assets/stores"
    ]

    for d in base_dirs:
        os.makedirs(d, exist_ok=True)

    # 1. Generate Sample PCB Scan Image (800x600 dark green PCB with components & burn mark)
    pcb = Image.new("RGB", (800, 600), color=(10, 35, 20))
    draw = ImageDraw.Draw(pcb)

    # Copper trace lines
    for i in range(0, 800, 40):
        draw.line([(i, 0), (i + 100, 600)], fill=(20, 80, 45), width=3)
        draw.line([(0, i), (800, i + 50)], fill=(20, 80, 45), width=2)

    # PCB Solder pads
    for x in range(50, 750, 60):
        for y in range(50, 550, 60):
            draw.ellipse([x-5, y-5, x+5, y+5], fill=(212, 175, 55))

    # IC LM7805 (Damaged burned area)
    ic_box = [300, 140, 490, 310]
    draw.rectangle(ic_box, fill=(25, 25, 25), outline=(100, 100, 100), width=3)
    # Burn mark overlay
    draw.ellipse([340, 180, 450, 270], fill=(15, 10, 10))
    draw.ellipse([360, 200, 420, 250], fill=(5, 2, 2))

    # Capacitor 10uF (Bulging top)
    cap_box = [540, 320, 680, 470]
    draw.ellipse(cap_box, fill=(30, 60, 120), outline=(200, 200, 200), width=3)
    draw.line([(610, 320), (610, 470)], fill=(220, 220, 220), width=6) # Striped negative bar

    # Flyback Diode
    diode_box = [130, 370, 250, 460]
    draw.rectangle(diode_box, fill=(40, 40, 40), outline=(150, 150, 150), width=2)
    draw.line([(150, 370), (150, 460)], fill=(220, 220, 220), width=8) # Cathode band

    # Text overlays
    draw.text((320, 150), "LM7805 IC", fill=(200, 200, 200))
    draw.text((560, 380), "10uF 25V", fill=(255, 255, 255))
    draw.text((160, 400), "1N5819", fill=(255, 255, 255))

    # Save PCB sample images
    pcb.save("d:/project/backend/static/assets/scans/pcb_sample1.jpg")
    pcb.save("d:/project/frontend/assets/scans/pcb_sample1.jpg")

    print("Sample graphic assets generated successfully!")

if __name__ == "__main__":
    generate_sample_assets()
