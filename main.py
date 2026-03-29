import re
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Get information from an html file")
    parser.add_argument(
        "-n", help="the filepath of the html file", type=str, required=True
    )
    args = parser.parse_args()
    laptop_list = convert_to_csv(args.n)

    for laptop in laptop_list:
        print(laptop)


def convert_to_csv(file_path):
    with open(file_path) as file:
        content = file.read()

    details = re.split(r"\n *\n", content.strip())

    laptop_list = []
    for detail in details:
        if model := re.search(
            r"(dell|hp|lenovo|asus|acer|msi|macbook)", detail, re.IGNORECASE
        ):
            model = model.group(0).title()
        else:
            model = None

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
        else:
            processor = None

        if gpu := re.search(
            r"((rtx|gtx|mx)|(iris *xe|vega|integrated|uhd|arc)) *(\d+\w*)?",
            detail,
            re.IGNORECASE,
        ):
            if gpu.group(2):
                gpu = f"{gpu.group(2).upper()} {gpu.group(4)}"
            else:
                gpu = gpu.group(0)

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

        laptop_list.append(
            {
                "Model": model,
                "RAM": ram,
                "Storage": storage_list,
                "Processor": processor,
                "Graphics": gpu,
            }
        )

    return laptop_list


if __name__ == "__main__":
    main()
