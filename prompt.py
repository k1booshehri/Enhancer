import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = "original.png"
OUTPUT_FILE = "reconstructed_4k.png"

MODEL = "gemini-3-pro-image"

RESOLUTION = "4K"

TIMEOUT = 6000_000  # 10 minutes


# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    sys.exit(1)

print("API key loaded.")


# ============================================================
# LOAD IMAGE
# ============================================================

input_path = Path(INPUT_FILE)

if not input_path.exists():
    print(f"ERROR: {INPUT_FILE} not found.")
    sys.exit(1)

try:
    image = Image.open(input_path)

    print(f"Input image: {INPUT_FILE}")
    print(f"Input dimensions: {image.width} x {image.height}")
    print(f"Input format: {image.format}")
    print(f"Input mode: {image.mode}")

except Exception as e:
    print(f"ERROR opening image: {e}")
    sys.exit(1)


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=api_key,
    http_options={
        "timeout": TIMEOUT
    }
)

print("Gemini client created.")


# ============================================================
# PROMPT
# ============================================================

prompt = """
Reconstruct this animated artwork at the HIGHEST POSSIBLE QUALITY.

This is a high-resolution image reconstruction task.

Use the supplied image as the authoritative reference.

DO NOT simply enlarge or sharpen the existing pixels.

Instead, intelligently reconstruct missing visual information and recreate
the artwork as if it had originally been rendered at extremely high
resolution.

PRESERVE THE ORIGINAL EXACTLY:

- same characters
- same faces
- same facial identity
- same expressions
- same poses
- same proportions
- same clothing
- same colors
- same objects
- same composition
- same framing
- same camera angle
- same perspective
- same background
- same lighting
- same artistic style

DO NOT redesign the artwork.

DO NOT reinterpret the characters.

DO NOT add anything that is not present.

DO NOT remove anything that is present.

DO NOT change facial identity.

DO NOT change expressions.

DO NOT change proportions.

DO NOT change the composition.

RECONSTRUCT EXTREMELY FINE DETAIL:

- clean professional linework
- perfectly smooth edges
- precise curves
- fine hair detail
- facial detail
- clothing detail
- fabric texture
- small accessories
- subtle shading
- highlights
- shadows
- material texture
- background texture
- fine environmental detail

REMOVE:

- pixelation
- blur
- JPEG artifacts
- compression artifacts
- jagged edges
- blockiness
- ringing
- digital noise
- muddy details

The result should look as though the original artwork was created
natively at extremely high resolution.

Prioritize:

1. Fidelity to the reference
2. Character consistency
3. Original composition
4. Original artistic style
5. Maximum fine detail
6. Clean professional rendering

Generate the image at the maximum available resolution.
"""


# ============================================================
# CONFIGURATION
# ============================================================

config = types.GenerateContentConfig(
    response_modalities=["IMAGE"],

    image_config=types.ImageConfig(
        image_size=RESOLUTION
    )
)


# ============================================================
# GENERATE
# ============================================================

print()
print("=" * 60)
print("STARTING GEMINI IMAGE RECONSTRUCTION")
print("=" * 60)
print(f"Model:      {MODEL}")
print(f"Resolution: {RESOLUTION}")
print()
print("Sending image to Gemini...")
print("This may take several minutes.")
print()


start = time.time()

try:

    response = client.models.generate_content(
        model=MODEL,

        contents=[
            image,
            prompt
        ],

        config=config
    )

except KeyboardInterrupt:

    print("\nRequest cancelled.")
    sys.exit(1)

except Exception as e:

    elapsed = time.time() - start

    print()
    print("=" * 60)
    print("GEMINI ERROR")
    print("=" * 60)
    print(f"Time elapsed: {elapsed:.1f} seconds")
    print()
    print(e)

    sys.exit(1)


elapsed = time.time() - start

print()
print("=" * 60)
print("RESPONSE RECEIVED")
print("=" * 60)
print(f"Generation time: {elapsed:.1f} seconds")
print()


# ============================================================
# SAVE IMAGE
# ============================================================

saved = False

for part in response.parts:

    if part.inline_data:

        try:

            image_data = part.inline_data.data
            mime_type = part.inline_data.mime_type

            # Determine extension from Gemini's response
            if mime_type == "image/png":
                extension = ".png"
            elif mime_type == "image/jpeg":
                extension = ".jpg"
            elif mime_type == "image/webp":
                extension = ".webp"
            else:
                extension = ".img"

            # Automatically use the correct extension
            output_path = Path(
                Path(OUTPUT_FILE).stem + extension
            )

            output_path.write_bytes(image_data)

            saved = True

            file_size = (
                output_path.stat().st_size
                / 1024
                / 1024
            )

            print()
            print("=" * 60)
            print("SUCCESS")
            print("=" * 60)

            print(f"Output file: {output_path}")
            print(f"Image type:  {mime_type}")
            print(f"File size:   {file_size:.2f} MB")

            break

        except Exception as e:

            print("ERROR saving image:")
            print(e)


if not saved:

    print()
    print("=" * 60)
    print("NO IMAGE WAS SAVED")
    print("=" * 60)

    print(response)

