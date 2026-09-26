# 《Rust语言圣经》电子书与打印版自动构建工作流

本分支在官方仓库的基础上，构建了专为 **Kindle（特别是 Kindle Oasis 与 6 寸墨水屏）** 和 **纸质打印装订（A4 PDF）** 定制的高质量排版与自动化编译系统。

---

## 🚀 快速上手

### 1. 同步上游更新并重新生成全套文件
当原作者仓库（`https://github.com/sunface/rust-course`）有内容更新时，只需运行：

**Windows (PowerShell):**
```powershell
./scripts/sync_and_build.ps1
```
或者使用 Python：
```bash
python scripts/sync_and_build.py
```
> **工作机制：**
> 1. 自动检查并添加 `upstream` 远程仓库；
> 2. 执行 `git fetch upstream` 抓取最新代码；
> 3. 将 `upstream/main` 的内容更新 merge 到当前分支；
> 4. 自动调用编译引擎，重新生成所有格式的最新电子书到 `dist/` 目录。
> 
> *注：如果上游暂无新提交，但您想强制重新编译，可传入 `-Force` 或 `--force` 参数。*

---

### 2. 仅重新编译（不检查上游更新）
如果只想根据当前内容重新生成部分或全部文件：

```bash
# 生成所有格式（Oasis AZW3、标准 Kindle AZW3、MOBI、A4 打印版 PDF、EPUB）
python scripts/build_ebooks.py

# 仅生成 Kindle Oasis 版和打印版 PDF
python scripts/build_ebooks.py --targets oasis pdf

# 仅重新打包 EPUB 电子书
python scripts/build_ebooks.py --targets epub
```

---

## 📦 输出文件说明 (`dist/` 目录)

编译完成后，文件统一输出在 `dist/` 文件夹中：

| 文件名 | 格式 | 适用场景 |
| :--- | :--- | :--- |
| `Rust-Course-Oasis.azw3` | AZW3 (KF8) | **首选**：专为 **Kindle Oasis**（300 PPI）深度优化，高分辨率插图 |
| `Rust-Course-Kindle.azw3`| AZW3 (KF8) | 适用于 6 寸 Kindle Paperwhite / Basic 系列 |
| `Rust-Course-Kindle.mobi`| MOBI (双引擎) | 兼容全部旧款 Kindle 机型及 Send to Kindle 邮箱推送 |
| `Rust-Course-Printable.pdf` | 高清 A4 PDF | 打印装订专用：1000+ 页完整大册，含动态页眉章节、页脚页码、带页码目录与矢量书签 |
| `Rust-Course.epub` | EPUB 3 | 适用于 iPad、手机各类阅读器 |

---

## 🛠️ 核心排版定制项

1. **Kindle 墨水屏专属样式 (`theme/kindle.css`)**：
   - **代码换行保全**：设置 `white-space: pre-wrap !important; word-wrap: break-word !important;`，彻底避免 Rust 长行代码横向溢出屏幕边界。
   - **墨水屏高对比度底色**：浅灰底色（`#f6f7f9`）+ 纯黑字符 + 细致边框，避免网页版暗色背景在墨水屏上造成的严重残影与对比度不足。
   - **版面节奏与物理按键翻页配合**：大章节（H1）强制从新页面起排，小标题（H2/H3）严格避免孤行。
2. **专属高清竖版封面 (`assets/kindle_cover.jpg`)**：
   - 1600 × 2400 高分辨率，完美贴合 Kindle 锁屏与书架比例。
   - 可通过 `python scripts/generate_cover.py` 随时重新生成。
3. **可打印 A4 PDF 引擎**：
   - 标准 A4 版型与 50 pt（约 17.6 mm）装订线安全边距；
   - 动态提取章节名作为双侧页眉，底部居中显示规范页码；
   - 自动生成带实体页码的印刷目录与 PDF 矢量书签。

---

## 🔧 依赖环境

- **Python 3.8+**（需安装 `Pillow` 用于封面渲染：`pip install pillow`）
- **mdBook** 与 **mdbook-epub**（位于 `~/.cargo/bin`）
- **Calibre**（包含 `ebook-convert` 命令行工具）
