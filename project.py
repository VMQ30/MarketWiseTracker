"""Imports"""

import re
import argparse
import csv
from laptop_class import Laptop


def main():
    """
    Parses a text file containing laptop specifications and prints the extracted data.

    This function sets up the command-line interface, accepts a file path via
    the '-n' argument, converts the raw text data into a csv

    Usage:
        python main.py -n <path_to_text_file>
    """
    parser = argparse.ArgumentParser(description="Get information from an html file")
    parser.add_argument(
        "-n", help="the filepath of the text file", type=str, required=True
    )
    args = parser.parse_args()
    laptop_list = extract_data(args.n)

    convert_to_csv(laptop_list)
    laptops = load_from_csv("laptops_info.csv")
    print(f"\nAverage Price: ₱{Laptop.avg_price(laptops):,.2f}")
    print(f"Most Expensive Price: ₱{Laptop.max_price(laptops):,.2f}")
    print(f"Cheapest Price: ₱{Laptop.min_price(laptops):,.2f}\n")
    Laptop.brand_analysis(laptops)
    Laptop.group_by_category(laptops)
    Laptop.avg_price_processor(laptops)
    Laptop.avg_price_graphics(laptops)
    Laptop.avg_price_ram(laptops)


def extract_data(file_path):
    """
    Reads a raw text file and extracts laptop specs using regular expressions.

    Args:
        file_path (str): The path to the text file containing raw laptop listings.

    Returns:
        list: A list of dictionaries, where each dictionary represents
              an extracted laptop (Brand, RAM, SSD, Processor, GPU).
    """

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    details = re.split(r"\n *\n", content.strip())

    laptop_list = []
    for detail in details:
        brand = get_brand(detail)
        processor = get_processor(detail)
        gpu = get_gpu(detail)
        ram, storage_list = get_ram_storage(detail)
        price = get_price(detail)

        laptop_list.append(
            {
                "Brand": brand,
                "RAM": ram,
                "Storage": storage_list,
                "Processor": processor,
                "Graphics": gpu,
                "Price": price,
            }
        )

    return laptop_list


def get_price(detail):
    if price := re.search(
        r"(₱|PHP)\s*([\d\s,]+(?:\.\d{1,2})?)",
        detail,
        re.IGNORECASE,
    ):
        num = price.group(2).replace(",", "")
        num = float(num.replace(" ", ""))

        return f"₱{num:,.2f}"
    return "None"


def get_brand(detail):
    """
    Extracts the laptop brand from a raw string.

    Args:
        detail (str): The raw text or title of a laptop listing.

    Returns:
        str | None: The title-cased brand name if found (e.g., 'Dell'),
            otherwise None.
    """

    if brand := re.search(
        r"(dell|hp|lenovo|asus|acer|msi|macbook)", detail, re.IGNORECASE
    ):
        return brand.group(0).title()
    return "None"


def get_processor(detail):
    """
    Identifies and standardizes the processor type from listing details.

    Handles Intel i-series, AMD Ryzen series, and Apple M-series chips.
    Standardizes 'ryzen5' to 'Ryzen 5' and 'I7' to 'i7'.

    Args:
        detail (str): The raw text of the laptop listing.

    Returns:
        str | None: The formatted processor string (e.g., 'i7', 'Ryzen 5', 'M1'),
            or None if no match is found.
    """

    if processor := re.search(
        r"(i[3579]|(ryzen) *([3579])|m1|m2)", detail, re.IGNORECASE
    ):
        if processor.group(0).lower().startswith("r"):
            processor = f"{processor.group(2)} {processor.group(3)}"
        else:
            processor = processor.group(0)

        if not processor.lower().startswith("i"):
            processor = processor.title()
        else:
            processor = processor.lower()
        return processor
    return "None"


def get_gpu(detail):
    """
    Extracts graphics card information, supporting dedicated and integrated units.

    Specifically targets Nvidia (RTX, GTX, MX), AMD (Vega), and
    Intel (Iris Xe, UHD, Arc) architectures.

    Args:
        detail (str): The raw text of the laptop listing.

    Returns:
        str | None: The uppercase GPU name and brand number (e.g., 'RTX 3050'),
            or None if no match is found.
    """

    if gpu := re.search(
        r"((rtx|gtx|mx)|(iris *xe|vega|integrated|uhd|arc)) *(\d+\w*)?",
        detail,
        re.IGNORECASE,
    ):
        if gpu.group(2):
            return f"{gpu.group(2).upper().strip()} {gpu.group(4).strip()}"
        return gpu.group(0).strip()
    return "None"


def get_ram_storage(detail):
    """
    Parses memory and storage capacity using a heuristic based on size and keywords.

    This function uses regex to find numeric capacities followed by units (GB/TB).
    It differentiates between RAM and Storage by looking for keywords or
    inferring based on common hardware sizes (e.g., <128GB is usually RAM).

    Args:
        detail (str): The raw text of the laptop listing.

    Returns:
        tuple: A tuple containing:
            - ram (str | None): The formatted RAM size (e.g., '16GB').
            - storage_list (list): A list of storage strings (e.g., ['512GB SSD']).
    """

    ram = None
    storage_list = []

    matches = re.findall(
        r"(\d+) *(?=(?:gb|tb|mb|ram|ssd|hdd|storage)) *(gb|tb|mb)? *(ram|ssd|hdd|storage)?",
        detail,
        re.IGNORECASE,
    )

    for size, unit, keyword in matches:
        unit = (unit or "GB").upper()
        size = int(size)

        if "ram" in keyword.lower():
            if not ram:
                ram = f"{size}{unit}"

        elif any(key in keyword for key in ["ssd", "hdd", "storage"]):
            if keyword == "storage":
                keyword = ""
            storage_list.append(
                f"{size}{unit} {keyword.upper() if keyword else ''}".strip()
            )

        else:
            if size < 128 and unit != "TB":
                if not ram:
                    ram = f"{size}{unit}"
            else:
                storage_list.append(f"{size}{unit}")

    if ram is None:
        ram = "None"
    if len(storage_list) == 0:
        storage_list.append("None")
    return ram, storage_list


def convert_to_csv(laptops):
    with open("laptops_info.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["Brand", "RAM", "Storage", "Processor", "Graphics", "Price"],
        )
        writer.writeheader()
        for laptop in laptops:
            storage_value = laptop["Storage"]
            if isinstance(storage_value, list):
                storage_value = " + ".join(storage_value)

            writer.writerow(
                {
                    "Brand": laptop["Brand"],
                    "RAM": laptop["RAM"],
                    "Storage": storage_value,
                    "Processor": laptop["Processor"],
                    "Graphics": laptop["Graphics"],
                    "Price": laptop["Price"],
                }
            )


def load_from_csv(csv_file):
    laptops = []

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            laptop = Laptop(
                brand=row["Brand"],
                ram=row["RAM"],
                storage=row["Storage"].split(" + "),
                processor=row["Processor"],
                graphics=row["Graphics"],
                price=row["Price"],
            )
            laptops.append(laptop)

    return laptops


if __name__ == "__main__":
    main()
