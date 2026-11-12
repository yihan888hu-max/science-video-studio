"""Create a review sheet from frames decoded from the delivered MP4."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
times = [0.7, 15.133, 22.267, 25.133, 39, 49, 61.8, 68.633,
         79.767, 82, 89.17, 98, 104.33, 109.7, 111.9, 119.4]
w, h, margin, label = 324, 576, 14, 30
sheet = Image.new('RGB', (4*w+5*margin, 4*(h+label)+5*margin), '#081015')
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
for i, t in enumerate(times):
    frame = ROOT / f'out/pingtan-v3-final_{t:.3f}s.png'
    image = Image.open(frame).convert('RGB').resize((w, h), Image.Resampling.LANCZOS)
    x, y = margin+(i%4)*(w+margin), margin+(i//4)*(h+label+margin)
    sheet.paste(image, (x, y))
    draw.text((x+4, y+h+5), f'{t:07.3f} s', font=font, fill='#b8e2e4')
sheet.save(ROOT/'out/pingtan-v3-final-contact.jpg', quality=94)
print('16 final-MP4 frames assembled')
