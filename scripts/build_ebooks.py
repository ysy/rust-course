#!/usr/bin/env python3
"""
Complete Build Script for Rust Course Ebooks
Generates Kindle Oasis AZW3, Kindle 6" AZW3, MOBI, Printable A4 PDF, and EPUB.
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent

def find_tool(tool_name, common_paths=None):
    # 1. PATH check
    path = shutil.which(tool_name)
    if path:
        return path

    # 2. Predefined common paths
    if common_paths:
        for p in common_paths:
            p_expanded = os.path.expandvars(os.path.expanduser(p))
            if os.path.isfile(p_expanded):
                return p_expanded
            if os.path.isdir(p_expanded):
                candidate = os.path.join(p_expanded, tool_name if sys.platform != 'win32' else f"{tool_name}.exe")
                if os.path.isfile(candidate):
                    return candidate

    return None

def get_calibre_converter():
    custom = os.environ.get("CALIBRE_PATH")
    if custom and os.path.isfile(custom):
        return custom

    common_locations = [
        r"C:\PRJS\calibre\Calibre Portable\Calibre\ebook-convert.exe",
        r"C:\Program Files\Calibre2\ebook-convert.exe",
        r"C:\Program Files (x86)\Calibre2\ebook-convert.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Calibre2\ebook-convert.exe"),
        "/Applications/calibre.app/Contents/MacOS/ebook-convert",
        "/usr/bin/ebook-convert",
        "/usr/local/bin/ebook-convert"
    ]
    return find_tool("ebook-convert", common_locations)

def ensure_cover():
    cover_path = ROOT_DIR / "assets" / "kindle_cover.jpg"
    if not cover_path.exists():
        print("[INFO] Generating Kindle Cover image...")
        gen_script = ROOT_DIR / "scripts" / "generate_cover.py"
        if gen_script.exists():
            subprocess.run([sys.executable, str(gen_script)], check=True, cwd=ROOT_DIR)
        else:
            print("[WARN] scripts/generate_cover.py not found!")

def ensure_book_toml():
    book_toml = ROOT_DIR / "book.toml"
    if not book_toml.exists():
        raise FileNotFoundError("book.toml not found in repository root!")

    content = book_toml.read_text(encoding="utf-8")
    if "[output.epub]" not in content:
        print("[INFO] Injecting [output.epub] configuration into book.toml...")
        epub_conf = (
            "\n[output.epub]\n"
            'cover-image = "assets/kindle_cover.jpg"\n'
            'additional-css = ["theme/kindle.css"]\n'
            "use-default-css = false\n"
            "no-section-label = false\n"
            "curly-quotes = true\n"
        )
        book_toml.write_text(content + epub_conf, encoding="utf-8")

def build_mdbook():
    mdbook_bin = find_tool("mdbook", [
        os.path.expanduser(r"~/.cargo/bin"),
        os.path.expandvars(r"%USERPROFILE%\.cargo\bin"),
        r"C:\PRJS\rust-book"
    ])
    if not mdbook_bin:
        raise RuntimeError("mdbook executable not found! Please ensure mdbook is in PATH or ~/.cargo/bin.")

    epub_bin = find_tool("mdbook-epub", [
        os.path.expanduser(r"~/.cargo/bin"),
        os.path.expandvars(r"%USERPROFILE%\.cargo\bin"),
        r"C:\PRJS\rust-book"
    ])
    if not epub_bin:
        raise RuntimeError("mdbook-epub plugin not found! Please install via cargo or place in ~/.cargo/bin.")

    print(f"[INFO] Running mdbook build using: {mdbook_bin} ...")
    res = subprocess.run([mdbook_bin, "build"], cwd=ROOT_DIR)
    if res.returncode != 0:
        raise RuntimeError(f"mdbook build failed with exit code {res.returncode}")

    # Locate generated epub
    epub_dir = ROOT_DIR / "book" / "epub"
    epub_files = list(epub_dir.glob("*.epub"))
    if not epub_files:
        raise FileNotFoundError("No .epub file found in book/epub/ after build!")

    return epub_files[0]

def convert_ebook(calibre_bin, input_epub, output_file, extra_args):
    print(f"\n[INFO] Generating: {output_file.name} ...")
    cmd = [calibre_bin, str(input_epub), str(output_file)] + extra_args
    res = subprocess.run(cmd, cwd=ROOT_DIR)
    if res.returncode != 0:
        print(f"[ERROR] Error generating {output_file.name} (exit code {res.returncode})")
    else:
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"[OK] Generated {output_file.name} ({size_mb:.2f} MB)")

def main():
    parser = argparse.ArgumentParser(description="Build Rust Course Ebooks for Kindle & Print")
    parser.add_argument("--targets", nargs="+", default=["all"],
                        choices=["all", "oasis", "kindle", "mobi", "pdf", "epub"],
                        help="Targets to build (default: all)")
    parser.add_argument("--output-dir", default="dist", help="Output directory (default: dist)")
    parser.add_argument("--skip-mdbook", action="store_true", help="Skip mdbook build step")
    args = parser.parse_args()

    targets = set(args.targets)
    if "all" in targets:
        targets = {"oasis", "kindle", "mobi", "pdf", "epub"}

    out_dir = ROOT_DIR / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Pre-flight checks
    ensure_cover()
    ensure_book_toml()

    # 2. Build EPUB
    epub_path = None
    if not args.skip_mdbook:
        epub_path = build_mdbook()
    else:
        candidates = list((ROOT_DIR / "book" / "epub").glob("*.epub")) + list(out_dir.glob("*.epub"))
        if candidates:
            epub_path = candidates[0]
        else:
            raise FileNotFoundError("No existing EPUB found to convert. Run without --skip-mdbook.")

    # Always deliver standard EPUB to dist/
    dist_epub = out_dir / "Rust-Course.epub"
    if epub_path != dist_epub:
        shutil.copy2(epub_path, dist_epub)
        print(f"📦 EPUB ready at {dist_epub}")

    if targets == {"epub"}:
        print("\n✨ Done! EPUB built successfully.")
        return

    # 3. Find Calibre
    calibre_bin = get_calibre_converter()
    if not calibre_bin:
        print("\n[ERROR] Calibre ebook-convert not found!")
        print("Please install Calibre or set CALIBRE_PATH environment variable.")
        sys.exit(1)

    print(f"[INFO] Using Calibre converter: {calibre_bin}")

    # 4. Generate Targets
    if "oasis" in targets:
        convert_ebook(calibre_bin, dist_epub, out_dir / "Rust-Course-Oasis.azw3", [
            "--output-profile", "kindle_oasis",
            "--prefer-metadata-cover",
            "--linearize-tables"
        ])

    if "kindle" in targets:
        convert_ebook(calibre_bin, dist_epub, out_dir / "Rust-Course-Kindle.azw3", [
            "--output-profile", "kindle_pw3",
            "--prefer-metadata-cover",
            "--linearize-tables"
        ])

    if "mobi" in targets:
        convert_ebook(calibre_bin, dist_epub, out_dir / "Rust-Course-Kindle.mobi", [
            "--output-profile", "kindle_oasis",
            "--mobi-file-type", "both",
            "--prefer-metadata-cover",
            "--linearize-tables"
        ])

    if "pdf" in targets:
        header_template = (
            '<div style="font-size:8.5pt; font-family:\'Microsoft YaHei\', sans-serif; '
            'color:#666; border-bottom:1px solid #ddd; padding-bottom:3px; '
            'display:flex; justify-content:space-between; width:100%;">'
            '<span>Rust 语言圣经 (Rust Course)</span><span>_SECTION_</span></div>'
        )
        footer_template = (
            '<div style="font-size:8.5pt; font-family:\'Microsoft YaHei\', sans-serif; '
            'color:#666; text-align:center; width:100%;">- _PAGENUM_ -</div>'
        )
        convert_ebook(calibre_bin, dist_epub, out_dir / "Rust-Course-Printable.pdf", [
            "--paper-size", "a4",
            "--pdf-page-margin-top", "50",
            "--pdf-page-margin-bottom", "50",
            "--pdf-page-margin-left", "50",
            "--pdf-page-margin-right", "50",
            "--pdf-default-font-size", "11",
            "--pdf-mono-font-size", "9",
            "--pdf-sans-family", "Microsoft YaHei",
            "--pdf-serif-family", "Microsoft YaHei",
            "--pdf-mono-family", "Consolas",
            "--pdf-header-template", header_template,
            "--pdf-footer-template", footer_template,
            "--pdf-add-toc",
            "--preserve-cover-aspect-ratio",
            "--linearize-tables"
        ])

    print("\n[OK] All requested ebooks and printable artifacts have been compiled successfully!")
    print(f"[INFO] Deliverables located in: {out_dir.resolve()}")

if __name__ == "__main__":
    main()
