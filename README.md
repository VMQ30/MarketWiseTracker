# Laptop Details Analyzer

### Video Demo:

https://youtu.be/xmyeXUBLOks

---

## Description

Laptop Market Analyzer is a command-line data processing and analysis tool designed to extract, structure, and analyze laptop specifications from unstructured text data. The application focuses on transforming messy real-world listings into clean datasets and generating meaningful market insights.

This project was built using Python and emphasizes data parsing, object-oriented design, and analytical reporting. It simulates a real-world data pipeline where raw input is cleaned, stored, processed, and presented in both terminal and PDF formats.

Unlike traditional datasets that are already structured, this project tackles the challenge of **extracting usable data from inconsistent text formats**, making it a strong demonstration of practical data engineering and analysis skills.

---

## 🧠 Core Concept

The application follows a complete data pipeline:

1. **Raw Text Input**
2. **Regex-Based Data Extraction**
3. **CSV Structuring**
4. **Object-Oriented Data Modeling**
5. **Statistical Analysis**
6. **Formatted Output (Terminal + PDF)**

This mirrors how real-world data systems operate — ingest, clean, analyze, and report.

---

## Project Structure and File Descriptions

```id="proj-struct"
.
├── project.py              # Main entry point and pipeline controller
├── laptop_class.py        # Data model and analysis engine
├── laptops_info.csv       # Generated structured dataset
├── laptop_analysis.pdf    # Generated report
├── input.txt              # Raw input data
```

---

## ⚙️ Core Application Logic (`project.py`)

### Command-Line Interface

The program uses `argparse` to accept a file path:

```id="cli-usage"
python project.py -n input.txt
```

This design allows flexibility and simulates real-world script usage.

---

### Data Extraction (`extract_data`)

Raw text is split into blocks and processed individually. Each block represents a laptop entry.

The following attributes are extracted using regular expressions:

- Brand
- Processor (Intel, Ryzen, Apple Silicon)
- Graphics (RTX, GTX, Integrated, etc.)
- RAM and Storage
- Price (converted into standardized format)

This step is critical because it transforms **unstructured data into structured dictionaries**.

---

### CSV Conversion (`convert_to_csv`)

Extracted data is written into a CSV file:

- Ensures consistency
- Allows reuse of data
- Separates extraction from analysis

Storage arrays are normalized into readable strings before saving.

---

### Data Loading (`load_from_csv`)

The CSV is reloaded and converted into `Laptop` objects.

This step introduces **object-oriented design**, allowing each laptop to encapsulate its own data and derived attributes (like category).

---

## Data Model and Analysis (`laptop_class.py`)

### Laptop Class

Each laptop object contains:

- Brand
- RAM
- Storage
- Processor
- Graphics
- Price
- Category (derived from price)

### Category Logic

| Category  | Price Range |
| --------- | ----------- |
| Budget    | ≤ ₱30,000   |
| Mid-Range | ≤ ₱60,000   |
| High-End  | > ₱60,000   |

---

### Statistical Methods

The class provides reusable analytical methods:

- `avg_price()` – average market price
- `min_price()` – lowest price
- `max_price()` – highest price

All methods safely handle missing or invalid data.

---

### Grouped Analysis (`group_and_analyze`)

This function dynamically groups laptops by any attribute:

- Processor
- Graphics
- RAM
- Brand

For each group, it calculates:

- Total units
- Average price
- Maximum price
- Minimum price

Results are sorted by **average price (descending)** before formatting.

---

### Market Segmentation (`group_by_category`)

This method provides deeper insights:

- Most common processor per category
- Most common GPU per category
- Total units per category
- Average price

This helps identify trends like:

- What hardware dominates budget vs high-end markets
- Price distribution across segments

---

### Insight Function (`best_value_category`)

This function determines:

> Which category offers the lowest average price

This simulates a real-world insight useful for consumers or analysts.

---

## Output System

### Terminal Output

Uses `tabulate` to display clean, structured tables for:

- Price distribution
- Hardware analysis
- Brand comparison
- Market segmentation

---

### PDF Report Generation (`convert_to_pdf`)

The application generates a professional report using `FPDF`.

The report includes:

- Market overview
- Statistical summaries
- All grouped analyses
- Structured tables

Special handling ensures compatibility (₱ → P conversion).

---

## Technologies Used

- Python 3
- `re` (Regex parsing)
- `csv` (Data handling)
- `argparse` (CLI interface)
- `tabulate` (Terminal formatting)
- `fpdf` (PDF generation)

---

## Design Decisions

### Why Regex Instead of Structured Input?

Real-world data is often messy. Regex allows flexible parsing of inconsistent formats.

### Why CSV as an Intermediate Step?

Separates extraction from analysis and allows data reuse.

### Why OOP (Laptop Class)?

Encapsulates logic and makes the system scalable and maintainable.

## Future Improvements

Data visualization (Matplotlib / Seaborn)
Web scraping for real-time data
Price-to-performance scoring system
GUI or web dashboard
Export to JSON or Excel
