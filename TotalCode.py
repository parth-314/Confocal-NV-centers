import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import re

# -----------------------------
# PARAMETERS
# -----------------------------
NX, NY = 100, 100
DTYPE = np.dtype('<f4')  # float32 little-endian

# -----------------------------
# FIX INTERLEAVED DATA
# -----------------------------
def fix_data(data):
    if data.size == NX * NY:
        return data
    elif data.size == 2 * NX * NY:
        even = data[0::2]
        odd  = data[1::2]
        return odd if np.mean(odd) > np.mean(even) else even
    else:
        raise ValueError(f"Unexpected size: {data.size}")

# -----------------------------
# EXTRACT INDEX FOR SORTING
# -----------------------------
def extract_index(filename):
    nums = re.findall(r'\d+', filename)
    return int(nums[-1]) if nums else 0

# -----------------------------
# MAIN
# -----------------------------
if len(sys.argv) < 2:
    print("Usage: python reconstruct_stack_xz.py <folder>")
    sys.exit(1)

folder = sys.argv[1]

# -----------------------------
# GET FILES
# -----------------------------
files = glob.glob(os.path.join(folder, "*.raw"))

if len(files) == 0:
    print("❌ No .raw files found!")
    sys.exit(1)

# Sort properly based on numbers in filename
files = sorted(files, key=lambda x: extract_index(os.path.basename(x)))

print(f"Found {len(files)} slices")

# -----------------------------
# LOAD + SAVE XY SLICES
# -----------------------------
slices = []

for i, f in enumerate(files):
    print(f"Processing: {os.path.basename(f)}")

    data = np.fromfile(f, dtype=DTYPE)
    data = fix_data(data)

    img = data.reshape((NY, NX))
    slices.append(img)

    # Normalize for display
    if np.max(img) != np.min(img):
        disp = (img - np.min(img)) / (np.max(img) - np.min(img))
    else:
        disp = img

    # Save XY image
    out_path = os.path.join(folder, f"slice_{i:03d}.png")

    plt.figure(figsize=(4,4))
    plt.imshow(disp, cmap='inferno', origin='lower')
    plt.xlabel("X(1 px =  73 nm)")
    plt.ylabel("Y(1 px = 73 nm)")
    plt.colorbar()
    plt.title(f"Z = {i}\n100px*100px")
    plt.savefig(out_path, dpi=200)
    plt.close()

print("✅ All XY slices saved")

# -----------------------------
# BUILD 3D VOLUME
# -----------------------------
volume = np.stack(slices, axis=0)  # (Z, Y, X)

print(f"Volume shape: {volume.shape}")

# -----------------------------
# CENTRAL XZ SLICE
# -----------------------------
x_index = NX // 2

xz = volume[:, :, x_index]  # (Z, Y)
xz = xz.T                   # (Y, Z)

# Normalize
if np.max(xz) != np.min(xz):
    xz_disp = (xz - np.min(xz)) / (np.max(xz) - np.min(xz))
else:
    xz_disp = xz

# -----------------------------
# SAVE XZ IMAGE
# -----------------------------
xz_path = os.path.join(folder, "XZ_central.png")

plt.figure(figsize=(6,4))
plt.imshow(xz_disp, cmap='inferno', aspect='auto', origin='lower')
plt.xlabel("Z(1 px = 2  $\mu m$)")
plt.ylabel("X(1 px = 73 nm)")
plt.title("Central XZ Slice")
plt.colorbar()

plt.tight_layout()
plt.savefig(xz_path, dpi=300)
plt.close()

print(f"✅ Saved: {xz_path}")
print("🚀 Done")