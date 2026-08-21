import struct, zlib, os

SIZE = 512
BG = (255, 153, 0, 255)      # #FF9900 brand orange
FG = (255, 255, 255, 255)    # white bars
LINE = (40, 28, 10, 255)     # dark baseline

# Build RGBA pixel buffer
buf = bytearray()
pixels = [list(BG) for _ in range(SIZE * SIZE)]

def set_px(x, y, c):
    if 0 <= x < SIZE and 0 <= y < SIZE:
        i = y * SIZE + x
        pixels[i] = list(c)

# Three ascending bars (white) sitting on a baseline
baseline = 360
bars = [
    (120, 90, 120),   # x, width, height
    (235, 90, 200),
    (350, 90, 290),
]
for (bx, bw, bh) in bars:
    for y in range(baseline - bh, baseline):
        for x in range(bx, bx + bw):
            set_px(x, y, FG)

# Baseline
for y in range(baseline, baseline + 12):
    for x in range(100, 440):
        set_px(x, y, LINE)

# Add a subtle highlight on top of each bar (lighter orange edge) optional -> skip

# Encode PNG (RGBA, 8-bit)
def chunk(tag, data):
    c = tag + data
    return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

raw = bytearray()
for y in range(SIZE):
    raw.append(0)  # filter type 0
    row = pixels[y * SIZE:(y + 1) * SIZE]
    for (r, g, b, a) in row:
        raw += bytes((r, g, b, a))

png = b"\x89PNG\r\n\x1a\n"
png += chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0))
png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
png += chunk(b"IEND", b"")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build", "icon.png")
out = os.path.abspath(out)
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "wb") as f:
    f.write(png)
print("wrote", out, len(png), "bytes")
