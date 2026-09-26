import subprocess
import sys

tag = "v1.0.0-kindle"
title = "Rust 语言圣经 (Rust Course) - Kindle Oasis/6寸 & 打印版"
notes = """## 《Rust 语言圣经 (Rust Course)》电子书优化版与高清打印版

针对 **Kindle Oasis**、**Kindle 6寸墨水屏** 以及 **实体纸质打印装订需求** 进行了深度定制与排版优化。

### 📦 包含的文件资产 (Assets)

1. **`Rust-Course-Oasis.azw3`** (6.4 MB)
   * **首选推荐**：专为 **Kindle Oasis**（300 PPI 高分辨率屏幕）深度定制；
   * 代码块自动折行（`white-space: pre-wrap`），彻底避免横向溢出；
   * 浅灰底纯黑字高对比度排版，消除墨水屏残影；
   * 大章节强制分页，小标题防孤行，适配 Oasis 物理按键与触屏翻页。

2. **`Rust-Course-Kindle.azw3`** (6.4 MB)
   * 适用于 6 寸 Kindle Paperwhite 3/4/5 及 Basic 标准墨水屏。

3. **`Rust-Course-Kindle.mobi`** (7.2 MB)
   * 双引擎 MOBI（内嵌 KF8 与 KF7），兼容所有版本 Kindle 设备及 Send to Kindle 邮箱推送。

4. **`Rust-Course-Printable.pdf`** (24.6 MB)
   * **打印装订专用**：1,071 页完整大册，标准 A4 规格，预留 50pt 安全边距；
   * 动态双侧页眉（书名 + 当前章节名）、居中页脚页码；
   * 带实体页码的印刷目录与 PDF 矢量书签；
   * 内嵌高清矢量微软雅黑与 Consolas 字体。

5. **`Rust-Course.epub`** (5.0 MB)
   * 标准 EPUB 3 格式，适用于 iPad、手机各类阅读器。
"""

files = [
    r"dist\Rust-Course-Oasis.azw3",
    r"dist\Rust-Course-Kindle.azw3",
    r"dist\Rust-Course-Kindle.mobi",
    r"dist\Rust-Course-Printable.pdf",
    r"dist\Rust-Course.epub"
]

cmd = [
    "gh", "release", "create", tag,
    "--repo", "ysy/rust-course",
    "--title", title,
    "--notes", notes
] + files

print("Creating release and uploading assets via gh...")
res = subprocess.run(cmd)
sys.exit(res.returncode)
