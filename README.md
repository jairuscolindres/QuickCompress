# QuickCompress

A fast, lightweight batch image processor designed for publishing workflows (WordPress, Facebook, Instagram, and web platforms). It resizes large camera and graphic assets while strictly preserving aspect ratio, compresses files for fast web delivery, and converts heavy PNGs/TIFFs to web-ready JPEGs.

---

## Features

- **Strict Aspect-Ratio Preserving Resizing (`-r`)**: **Guarantees 100% scale and aspect ratio preservation**—images are never stretched, squished, or cropped. Downscales the longest edge to a maximum pixel limit (`-p`, default: `1920px`) via high-quality Lanczos resampling while automatically scaling the opposing edge proportionally. Smaller images remain untouched.
- **Intelligent Compression**:
  - **JPEG / WebP**: Adjustable quality compression (`1`–`100`, default: `80`) with stream optimization enabled.
  - **PNG**: Maximum lossless compression (`compress_level=9`) with optimization.
- **Safe Format Conversion (`--to-jpg`)**: Converts images to JPEG. Automatically flattens alpha transparency channels onto a clean white background.
- **EXIF Auto-Orientation**: Transposes photos automatically using embedded camera metadata so mobile and DSLR uploads are never upside down or sideways.
- **Large Image Protection**: Disables Pillow's decompression bomb limit (`MAX_IMAGE_PIXELS = None`) to safely ingest large raw, scanned, or high-resolution camera media.
- **Non-Destructive Batching**: Preserves original source assets and outputs to a dedicated folder with real-time progress, per-file metrics, and overall space savings statistics.
- **Wide Format Support**: Supports `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`, and `.tif`.

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher

### 1. Clone the Repository
```bash
git clone https://github.com/jairuscolindres/QuickCompress.git
cd QuickCompress
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment if not already present
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Or install Pillow directly: `pip install Pillow`)*

---

## Usage

```bash
python3 process_images.py [OPTIONS] <input_folder>
```

> [!NOTE]
> You must specify at least one mode: `--resize` (`-r`), `--compress` (`-c`), or both (`-r -c`).

> [!IMPORTANT]
> **Aspect Ratio & Proportions are Strictly Preserved:**
> When using `-r` (`--resize`), images are **never stretched, skewed, or cropped**. The script identifies whichever edge is longer (width for landscape, height for portrait/square) and caps it to the `--pixels` (`-p`) value, scaling the other side proportionally with Lanczos resampling. Images already within the limit remain untouched.

### Command-Line Arguments

| Flag | Long Option | Type / Default | Description |
|---|---|---|---|
| `<input_folder>` | *(Positional)* | Path (Required) | Directory containing images to process. |
| `-r` | `--resize` | Flag | **Preserves aspect ratio strictly**. Downscales the longest edge while keeping exact proportions (no distortion or cropping). |
| `-c` | `--compress` | Flag | Enable compression and stream optimization. |
| `-p` | `--pixels` | Integer (Default: `1920`) | Max dimension for the longest edge when `-r` is set (both width and height scale proportionally). |
| `-q` | `--quality` | Integer (Default: `80`) | Compression quality (`1`–`100`) for JPEG/WebP. |
| | `--to-jpg` | Flag | Convert all output files to `.jpg` format (flattens transparency to clean white). |
| `-o` | `--output` | Path (Optional) | Custom output folder (defaults to `<input_folder>_processed`). |
| `-h` | `--help` | Flag | Display help message and options. |

---

## Common Recipes

### 1. Standard Web & Social Media Optimization (Recommended)
Resizes images down to a maximum of 1920px on their longest edge (strictly preserving original scale and aspect ratio) and compresses them at quality 80:
```bash
python3 process_images.py -r -c /path/to/photos
```
*Output will be saved in `/path/to/photos_processed`.*

---

### 2. Convert Heavy Graphic Assets / PNGs to Web-Ready JPGs
Ideal for editorial graphics, Canva exports, or screenshots intended for web articles:
```bash
python3 process_images.py -r -c --to-jpg -p 1600 -q 85 /path/to/graphics
```

---

### 3. Quick Size Compression Only (No Resizing)
Maintains full original pixel resolution while stripping metadata overhead and applying quality compression:
```bash
python3 process_images.py -c -q 75 /path/to/event_photos
```

---

### 4. Custom Output Directory
Specify an exact target destination for the processed files:
```bash
python3 process_images.py -r -c -p 1200 -o ./optimized_media /path/to/raw_uploads
```

---

## Example Console Output

```text
Processing 12 images: raw_coverage -> raw_coverage_processed
Settings: Resize=True (max 1920px, scale preserved) | Compress=True (quality 80)

[1/12] DSC_0042.jpg
      6000x4000 (14.2MB) -> 1920x1280 (0.64MB) [-95.5%]
[2/12] banner_infographic.png
      3840x2160 (8.1MB) -> 1920x1080 (1.12MB) [-86.2%]
...
=======================================================
Finished! Total size: 148.4MB -> 12.8MB
Space Saved : 135.6MB (-91.4%)
Output saved in: ./raw_coverage_processed
=======================================================
```

---

## Project Structure

```text
QuickCompress/
├── process_images.py    # Main CLI script
├── requirements.txt     # Python package requirements (Pillow)
├── README.md            # Documentation and usage guide
└── .gitignore           # Git ignore rules
```
