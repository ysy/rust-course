#!/usr/bin/env python3
"""
Generate a high-resolution, portrait Kindle cover for Rust Course.
Optimized for 300 PPI E-ink displays (Kindle Oasis, Paperwhite).
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def generate_cover(output_path="assets/kindle_cover.jpg", banner_path="assets/banner.jpg"):
    width, height = 1600, 2400
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    img = Image.new('RGB', (width, height), color='#1e232a')
    draw = ImageDraw.Draw(img)

    # Decorative header bar (Rust orange-red)
    draw.rectangle([0, 0, width, 24], fill='#ce422b')

    # Border framing
    draw.rectangle([60, 60, width - 60, height - 60], outline='#3a424e', width=3)
    draw.rectangle([70, 70, width - 70, height - 70], outline='#ce422b', width=2)

    # Fonts
    def get_font(name, size, fallback="arial.ttf"):
        paths = [
            os.path.join(r"C:\Windows\Fonts", name),
            f"/usr/share/fonts/truetype/{name}",
            f"/Library/Fonts/{name}",
            fallback
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    font_title = get_font("msyhbd.ttc", 110)
    font_sub = get_font("msyh.ttc", 56)
    font_en = get_font("consola.ttf", 52)
    font_author = get_font("msyh.ttc", 48)
    font_tag = get_font("msyh.ttc", 38)
    font_desc = get_font("msyh.ttc", 42)

    # Top badge
    badge_text = 'KINDLE E-INK OPTIMIZED EDITION'
    bbox = draw.textbbox((0, 0), badge_text, font=font_en)
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, 160), badge_text, font=font_en, fill='#a0aec0')

    # Title
    title_text = 'Rust 语言圣经'
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, 280), title_text, font=font_title, fill='#ffffff')

    # Subtitle
    sub_text = 'Rust Course'
    bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, 420), sub_text, font=font_sub, fill='#ce422b')

    # Horizontal divider
    draw.line([(width // 2 - 300, 520), (width // 2 + 300, 520)], fill='#4a5568', width=2)

    # Middle banner artwork
    middle_bottom = 800
    if os.path.exists(banner_path):
        try:
            banner = Image.open(banner_path)
            bw, bh = 1400, int(1400 * (banner.height / banner.width))
            banner_resized = banner.resize((bw, bh), Image.Resampling.LANCZOS)
            img.paste(banner_resized, ((width - bw) // 2, 600))
            middle_bottom = 600 + bh
        except Exception as e:
            print(f"Warning: Failed to load banner image: {e}")

    # Feature highlights
    features = [
        '• 全面深入：从基础语法到并发、异步与底层探秘',
        '• 实践驱动：网络服务、高并发架构与复杂数据结构实战',
        '• 深度剖析：攻克所有权、生命周期与编译报错难点'
    ]
    y_start = middle_bottom + 120
    for feat in features:
        bbox = draw.textbbox((0, 0), feat, font=font_desc)
        w = bbox[2] - bbox[0]
        draw.text(((width - w) // 2, y_start), feat, font=font_desc, fill='#cbd5e0')
        y_start += 90

    # Footer line
    draw.line([(200, height - 360), (width - 200, height - 360)], fill='#4a5568', width=2)

    # Author
    author_text = '作者：sunface & 社区开源贡献者'
    bbox = draw.textbbox((0, 0), author_text, font=font_author)
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, height - 280), author_text, font=font_author, fill='#ffffff')

    # Edition tag
    edition_text = '精心排版 · 专为 6 寸/Oasis 墨水屏深度定制'
    bbox = draw.textbbox((0, 0), edition_text, font=font_tag)
    w = bbox[2] - bbox[0]
    draw.text(((width - w) // 2, height - 190), edition_text, font=font_tag, fill='#a0aec0')

    img.save(output_path, 'JPEG', quality=95)
    print(f"Cover generated successfully at {output_path}")

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/kindle_cover.jpg"
    generate_cover(out)
