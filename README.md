# Gemini 4K Image Reconstruction

A Python script that uses **Google Gemini's image generation API** to reconstruct low-resolution or compressed artwork at up to **4K resolution** — not by naively upscaling pixels, but by intelligently regenerating the artwork with fine detail while preserving the original characters, composition, colors, and style.

Ideal for restoring animated artwork, illustrations, and stylized images that suffer from pixelation, blur, or JPEG compression artifacts.

---

## How It Works

Traditional upscalers (bicubic, Lanczos, even many AI super-resolution models) interpolate existing pixels, which often produces soft or artificial-looking results. This script takes a different approach:

1. It sends your image to the `gemini-3-pro-image` model along with a carefully engineered reconstruction prompt.
2. The prompt instructs the model to treat your image as the **authoritative reference** and re-render it as if it had been natively created at extremely high resolution.
3. Strict constraints in the prompt prevent the model from redesigning, reinterpreting, adding, or removing anything — the goal is **fidelity first**, detail second.
4. The response image is saved locally with the correct file extension automatically detected from the returned MIME type (`.png`, `.jpg`, or `.webp`).

The reconstruction prompt explicitly targets:

- Clean, professional linework and smooth edges
- Fine hair, facial, clothing, and fabric detail
- Accurate shading, highlights, and material textures
- Removal of pixelation, blur, compression artifacts, jagged edges, ringing, and digital noise

---

## Features

- 🖼️ **True reconstruction, not interpolation** — regenerates detail rather than stretching pixels
- 🎯 **Identity-preserving prompt** — explicit constraints to keep faces, expressions, poses, proportions, colors, and composition unchanged
- 📐 **Up to 4K output** — configurable via a single setting
- 🧠 **Powered by `gemini-3-pro-image`**
- 💾 **Smart output handling** — file extension is chosen automatically based on the actual image format Gemini returns
- ⏱️ **Long-request friendly** — generous HTTP timeout for large generations, with elapsed-time reporting
- 🛡️ **Robust error handling** — clear messages for missing API keys, missing input files, unreadable images, API errors, and empty responses
- ⌨️ **Graceful cancellation** — clean exit on `Ctrl+C`

---

## Requirements

- Python 3.9+
- A Google AI Studio API key with access to Gemini image generation
- The following Python packages:

| Package | Purpose |
|---|---|
| `google-genai` | Official Google Gen AI SDK |
| `python-dotenv` | Loads the API key from a `.env` file |
| `Pillow` | Opens and inspects the input image |

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install google-genai python-dotenv Pillow
```

**4. Set up your API key**

Create a file named `.env` in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

You can get an API key from [Google AI Studio](https://aistudio.google.com/).

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`:
>
> ```gitignore
> .env
> ```

---

## Usage

1. Place the image you want to reconstruct in the project root and name it `original.png` (or change `INPUT_FILE` in the script).

2. Run the script:

```bash
python prompt.py
```

3. Watch the console output:

```
API key loaded.
Input image: original.png
Input dimensions: 1024 x 576
Input format: PNG
Input mode: RGB
Gemini client created.

============================================================
STARTING GEMINI IMAGE RECONSTRUCTION
============================================================
Model:      gemini-3-pro-image
Resolution: 4K

Sending image to Gemini...
This may take several minutes.
```

4. On success, the reconstructed image is saved as `reconstructed_4k.png` (or `.jpg` / `.webp` depending on what the API returns):

```
============================================================
SUCCESS
============================================================
Output file: reconstructed_4k.png
Image type:  image/png
File size:   14.32 MB
```

---

## Configuration

All settings live at the top of the script:

| Setting | Default | Description |
|---|---|---|
| `INPUT_FILE` | `original.png` | Path to the source image |
| `OUTPUT_FILE` | `reconstructed_4k.png` | Base name for the output (extension is auto-corrected to match the returned format) |
| `MODEL` | `gemini-3-pro-image` | Gemini model used for generation |
| `RESOLUTION` | `4K` | Target output resolution (`1K`, `2K`, or `4K`) |
| `TIMEOUT` | `6000_000` ms | HTTP client timeout in milliseconds |

### Customizing the prompt

The reconstruction prompt is defined in the `prompt` variable. It is intentionally strict and repetitive — image models respond well to explicit, enumerated constraints. If you want to allow slight stylistic enhancement (or lock things down even further), edit the `PRESERVE`, `DO NOT`, and `RECONSTRUCT` sections.

---

## Example Workflow

```
original.png  (720p screenshot, JPEG artifacts, soft edges)
        │
        ▼
   prompt.py  ──►  Gemini (gemini-3-pro-image, 4K)
        │
        ▼
reconstructed_4k.png  (crisp linework, restored detail, clean edges)
```

---

## Troubleshooting

**`ERROR: GEMINI_API_KEY not found.`**
Your `.env` file is missing or doesn't contain `GEMINI_API_KEY`. Make sure the file is in the same directory you run the script from.

**`ERROR: original.png not found.`**
The input image isn't in the working directory, or `INPUT_FILE` doesn't match its filename.

**Request times out**
Large 4K generations can take a while. Increase `TIMEOUT` (value is in **milliseconds**).

**`NO IMAGE WAS SAVED` and the raw response is printed**
The model returned no image part — usually because the request was blocked by safety filters or the model responded with text only. The full response object is printed so you can inspect the reason. Try adjusting the prompt or using a different input image.

**API / quota errors**
Check that your API key has access to the image generation model and that you haven't exceeded your quota or rate limits.

---

## Limitations & Notes

- **This is generative reconstruction, not lossless upscaling.** The model re-renders the image, so microscopic details may differ from the original even though identity, composition, and style are preserved. For pixel-exact enlargement, use a conventional upscaler instead.
- Results vary by input: clean stylized artwork (anime, illustrations, renders) reconstructs best; heavily degraded or very busy photos may reconstruct less faithfully.
- Only use this on images you own or have the right to modify.
- API usage is billed by Google according to your plan — 4K image generation consumes more quota than lower resolutions.

---

## Project Structure

```
.
├── prompt.py        # Main script
├── original.png     # Your input image (not committed)
├── .env             # Your API key (not committed)
└── README.md
```

---

## License

MIT — feel free to use, modify, and share.
