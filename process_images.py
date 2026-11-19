#!/usr/bin/env python3
"""
Simple Batch Image Processor for Web & Social Media (WordPress, Instagram, Facebook).
Resizes by pixel (preserving aspect ratio) and/or compresses images in a folder.
"""

import argparse
from pathlib import Path
from PIL import Image, ImageOps

# Prevent Pillow decompression errors on massive high-res images
Image.MAX_IMAGE_PIXELS = None

VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def resize_image(img: Image.Image, max_px: int) -> Image.Image:
    """Resize image so its longest edge is max_px while strictly preserving scale."""
    w, h = img.size
    if max(w, h) <= max_px:
        return img
    scale = max_px / max(w, h)
    new_w = max(1, round(w * scale))
    new_h = max(1, round(h * scale))
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)


def main():
    parser = argparse.ArgumentParser(
        description="Resize by pixel and/or compress images for WordPress, Instagram, and Facebook."
    )
    parser.add_argument("input_folder", help="Path to folder containing images.")
    parser.add_argument("-o", "--output", help="Output folder (default: <input_folder>_processed).")
    parser.add_argument("-r", "--resize", action="store_true", help="Resize images to max pixel dimension.")
    parser.add_argument("-c", "--compress", action="store_true", help="Compress images for smaller file size.")
    parser.add_argument(
        "-p", "--pixels", type=int, default=1920,
        help="Max pixel dimension for the longest edge when resizing (default: 1920, keeps same scale)."
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=80,
        help="Compression quality from 1 to 100 for JPEG/WebP (default: 80)."
    )
    parser.add_argument(
        "--to-jpg", action="store_true",
        help="Convert output images to JPG (recommended for massive PNGs uploading to web/social)."
    )

    args = parser.parse_args()

    if not args.resize and not args.compress:
        parser.error("Please specify at least one mode: --resize (-r), --compress (-c), or both (-r -c).")

    in_dir = Path(args.input_folder).resolve()
    if not in_dir.is_dir():
        parser.error(f"Input directory '{in_dir}' does not exist.")

    out_dir = Path(args.output).resolve() if args.output else in_dir.parent / f"{in_dir.name}_processed"
    out_dir.mkdir(parents=True, exist_ok=True)

    images = [f for f in sorted(in_dir.iterdir()) if f.is_file() and f.suffix.lower() in VALID_EXTS]
    if not images:
        print(f"No valid images found in {in_dir}")
        return

    print(f"\nProcessing {len(images)} images: {in_dir.name} -> {out_dir.name}")
    print(f"Settings: Resize={args.resize} (max {args.pixels}px, scale preserved) | Compress={args.compress} (quality {args.quality})\n")

    total_orig_bytes, total_new_bytes = 0, 0

    for i, file in enumerate(images, 1):
        try:
            with Image.open(file) as img:
                img = ImageOps.exif_transpose(img)  # Auto-correct camera orientation
                orig_dim = img.size
                orig_bytes = file.stat().st_size
                total_orig_bytes += orig_bytes

                orig_fmt = img.format or ("PNG" if file.suffix.lower() == ".png" else "JPEG")

                # 1. Resize (preserves aspect ratio)
                if args.resize:
                    img = resize_image(img, args.pixels)

                # 2. Output format & extension
                if args.to_jpg:
                    fmt = "JPEG"
                    ext = ".jpg"
                else:
                    fmt = "JPEG" if orig_fmt.upper() in ("JPG", "JPEG") else orig_fmt.upper()
                    ext = file.suffix.lower()
                out_file = out_dir / f"{file.stem}{ext}"

                # 3. Compress & Save
                save_opts = {}
                if args.compress:
                    save_opts["optimize"] = True
                    if fmt in ("JPEG", "WEBP"):
                        save_opts["quality"] = args.quality
                    elif fmt == "PNG":
                        save_opts["compress_level"] = 9

                if fmt == "JPEG" and img.mode in ("RGBA", "P"):
                    # Flatten transparency to clean white background for JPG
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    alpha_mask = img.split()[-1] if img.mode == "RGBA" else None
                    bg.paste(img.convert("RGB"), mask=alpha_mask)
                    img = bg
                elif fmt != "JPEG" and img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA" if "A" in img.mode else "RGB")

                img.save(out_file, format=fmt, **save_opts)
                new_bytes = out_file.stat().st_size
                total_new_bytes += new_bytes

                orig_mb = orig_bytes / (1024 * 1024)
                new_mb = new_bytes / (1024 * 1024)
                diff_pct = ((orig_bytes - new_bytes) / orig_bytes * 100) if orig_bytes else 0
                sign = "-" if diff_pct >= 0 else "+"

                print(f"[{i}/{len(images)}] {file.name}")
                print(f"      {orig_dim[0]}x{orig_dim[1]} ({orig_mb:.1f}MB) -> {img.size[0]}x{img.size[1]} ({new_mb:.2f}MB) [{sign}{abs(diff_pct):.1f}%]")

        except Exception as err:
            print(f"[{i}/{len(images)}] Error on {file.name}: {err}")

    saved_mb = (total_orig_bytes - total_new_bytes) / (1024 * 1024)
    total_orig_mb = total_orig_bytes / (1024 * 1024)
    total_new_mb = total_new_bytes / (1024 * 1024)
    total_reduction = (1 - (total_new_bytes / total_orig_bytes)) * 100 if total_orig_bytes else 0

    print("\n" + "=" * 55)
    print(f"Finished! Total size: {total_orig_mb:.1f}MB -> {total_new_mb:.1f}MB")
    print(f"Space Saved : {saved_mb:.1f}MB (-{total_reduction:.1f}%)")
    print(f"Output saved in: {out_dir}")
    print("=" * 55)


if __name__ == "__main__":
    main()
