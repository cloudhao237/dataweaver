# ⚡ DataWeaver

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green?style=for-the-badge" alt="Platforms">
  <img src="https://img.shields.io/badge/License-MIT-orange?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Privacy-100%25%20Offline-emerald?style=for-the-badge" alt="100% Offline">
</p>

<p align="center">
  <b>Fast, local, and privacy-first batch data merger, cleaner, and entity extractor.</b><br>
  Built for developers, data analysts, marketers, and researchers who deal with messy unformatted tables and dumps.
</p>

---

## 🚀 Instant Download (For Non-Programmers)

If you don't want to install Python or use the command line:

[![Download on Gumroad](https://img.shields.io/badge/Gumroad-Download%20Desktop%20App%20($4.99)-ff90e8?style=for-the-badge&logo=gumroad&logoColor=black)](https://cloudhaven12.gumroad.com/l/python-data-automation)

> **💡 The Pre-built Package includes:**
> - Double-click standalone `.exe` (Windows) & `.dmg / .app` (macOS).
> - High-performance offline GUI studio.
> - Packaged with 100+ production-ready data automation scripts & templates.

---

## ✨ Features

- **📂 Batch File Merger**:
  - Combine tens or hundreds of CSV/TSV files into one consolidated dataset in seconds.
  - Automatic column header alignment (handles disordered or missing columns).
  - Intelligent deduplication and multi-encoding support (`UTF-8`, `UTF-8-SIG`, `GBK/GB18030`, `Latin-1`).
- **🔍 Regex Entity Extractor**:
  - Automatically extract structured information from unformatted log dumps, chat exports, or web copies.
  - Built-in recognition for:
    - 📧 Emails
    - 📞 International & Domestic Phone Numbers
    - 🌐 Web URLs
    - 🖥️ IP Addresses
    - 🆔 Identification Numbers
  - Export structured entities straight into clean, ready-to-use CSV files.
- **💻 Dual Interface**:
  - **Modern Desktop GUI**: Zero-configuration, clean interface with native OS file dialogs.
  - **Command-Line Interface (CLI)**: Perfect for automation pipelines, cron jobs, and terminal power users.
- **🔒 100% Privacy First**:
  - Runs completely offline on your local machine. No external telemetry, no cloud uploads, zero data leakage risks.

---

## 🛠️ Developer Installation

### Method 1: Run via Python CLI

```bash
# Clone the repository
git clone https://github.com/your-username/dataweaver.git
cd dataweaver

# Install as editable package
pip install -e .

# Launch Desktop GUI
dataweaver gui
```

### Method 2: Command Line Usage

#### 1. Batch Merge CSVs
```bash
dataweaver merge -i ./data/sales_jan.csv ./data/sales_feb.csv ./data/sales_mar.csv -o combined_sales.csv
```

#### 2. Extract Entities from Raw Text
```bash
dataweaver extract -i raw_chat_dump.txt -o extracted_leads.csv
```

---

## 🧩 Python API Integration

You can also use DataWeaver as an internal module in your own scripts:

```python
from dataweaver.core import BatchMerger, TextNormalizer

# Merge CSV files programmatically
result = BatchMerger.merge_csv_files(
    file_paths=["report_1.csv", "report_2.csv"],
    output_path="merged_report.csv",
    deduplicate=True
)
print(f"Merged {result['processed_files']} files with {result['total_records']} rows!")

# Extract entities from text
entities = TextNormalizer.extract_entities(
    "Contact us at support@example.com or call +1-800-555-0199 for orders."
)
print(entities)
# Output: {'email': ['support@example.com'], 'phone_intl': ['+1-800-555-0199']}
```

---

## 📦 Building Standalone Binaries

To build a standalone executable locally using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --name "DataWeaver" dataweaver/gui.py
```

The compiled binary will be available in `./dist/DataWeaver/`.

---

## 🤝 Contributing & Sponsorship

Contributions, issue reports, and feature pull requests are welcome!

- Star this repository if you find it helpful! ⭐
- Support development & get exclusive automation blueprints on [CloudHaven Gumroad](https://cloudhaven12.gumroad.com/).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
