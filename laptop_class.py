from tabulate import tabulate
from fpdf import FPDF


class Laptop:
    def __init__(self, brand, ram, storage, processor, graphics, price):
        self.brand = brand
        self.ram = ram
        self.storage = storage
        self.processor = processor
        self.graphics = graphics
        self.price = float(price.replace("₱", "").replace(",", "").strip())
        self.category = Laptop.set_category(self.price)

    @staticmethod
    def set_category(price):
        if price <= 30000:
            return "Budget"
        elif price <= 60000:
            return "Mid-Range"
        else:
            return "High-End"

    @staticmethod
    def get_prices(laptops):
        return [
            laptop.price for laptop in laptops if laptop and laptop.price is not None
        ]

    @staticmethod
    def avg_price(laptops):
        prices = Laptop.get_prices(laptops)
        return sum(prices) / len(prices) if prices else 0

    @staticmethod
    def min_price(laptops):
        prices = Laptop.get_prices(laptops)
        return min(prices) if prices else 0

    @staticmethod
    def max_price(laptops):
        prices = Laptop.get_prices(laptops)
        return max(prices) if prices else 0

    # Core Insights
    @staticmethod
    def group_and_analyze(laptops, key):
        data = {}

        for l in laptops:
            if l and l.price is not None:
                k = getattr(l, key)
                data.setdefault(k, []).append(l.price)

        result = []
        for k, prices in data.items():
            result.append(
                [
                    k,
                    f"{len(prices)} units",
                    sum(prices) / len(prices),
                    max(prices),
                    min(prices),
                ]
            )

        result.sort(key=lambda x: x[2], reverse=True)

        formatted = [
            [
                row[0],
                row[1],
                f"₱{row[2]:,.2f}",
                f"₱{row[3]:,.2f}",
                f"₱{row[4]:,.2f}",
            ]
            for row in result
        ]

        return formatted

    # Market Segmentation
    @staticmethod
    def group_by_category(laptops):
        category_data = {}

        for laptop in laptops:
            if laptop and laptop.price is not None:
                if laptop.category not in category_data:
                    category_data[laptop.category] = {
                        "Processor": {},
                        "Graphics": {},
                        "Price": [],
                    }

                gpu_counts = category_data[laptop.category]["Graphics"]
                if laptop.graphics not in gpu_counts:
                    gpu_counts[laptop.graphics] = 1
                else:
                    gpu_counts[laptop.graphics] += 1

                processor_counts = category_data[laptop.category]["Processor"]
                if laptop.processor not in processor_counts:
                    processor_counts[laptop.processor] = 1
                else:
                    processor_counts[laptop.processor] += 1

                category_data[laptop.category]["Price"].append(laptop.price)

        final_category_data = []
        for items, values in category_data.items():
            processors = values["Processor"]
            gpus = values["Graphics"]
            avg_price = float(sum(values["Price"]) / len(values["Price"]))

            max_processor = max(processors, key=processors.get)
            max_gpus = max(gpus, key=gpus.get)

            final_category_data.append(
                [
                    items,
                    max_processor,
                    max_gpus,
                    f"{sum(processors.values())} units",
                    avg_price,
                ]
            )
        final_category_data.sort(key=lambda x: x[4], reverse=True)
        formatted = [
            [
                row[0],
                row[1],
                row[2],
                row[3],
                f"₱{row[4]:,.2f}",
            ]
            for row in final_category_data
        ]

        return formatted

    @staticmethod
    def best_value_category(laptops):
        category_prices = {}

        for l in laptops:
            if l and l.price is not None:
                category_prices.setdefault(l.category, []).append(l.price)

        best_category = None
        best_avg = float("inf")

        for category, prices in category_prices.items():
            avg = sum(prices) / len(prices)
            if avg < best_avg:
                best_avg = avg
                best_category = category

        return best_category, best_avg

    @staticmethod
    def display(title, data, headers):
        print(f"\n{title}")
        print(tabulate(data, headers=headers, tablefmt="rounded_grid"))

    @staticmethod
    def analyze(laptops):
        print("\nOVERALL PRICE STATS")
        print(f"Average Price: ₱{Laptop.avg_price(laptops):,.2f}")
        print(f"Min Price: ₱{Laptop.min_price(laptops):,.2f}")
        print(f"Max Price: ₱{Laptop.max_price(laptops):,.2f}")

        Laptop.display(
            "Price by Processor",
            Laptop.group_and_analyze(laptops, "processor"),
            ["Processor", "Total Units", "Avg Price", "Max Price", "Min Price"],
        )

        Laptop.display(
            "Price by Graphics",
            Laptop.group_and_analyze(laptops, "graphics"),
            ["Graphics", "Total Units", "Avg Price", "Max Price", "Min Price"],
        )

        Laptop.display(
            "Price by RAM",
            Laptop.group_and_analyze(laptops, "ram"),
            ["RAM", "Total Units", "Avg Price", "Max Price", "Min Price"],
        )

        Laptop.display(
            "Brand Analysis",
            Laptop.group_and_analyze(laptops, "brand"),
            ["Brand", "Total Units", "Avg Price", "Max Price", "Min Price"],
        )

        Laptop.display(
            "Market Segmentation",
            Laptop.group_by_category(laptops),
            ["Category", "Top Processor", "Top GPU", "Total Units", "Avg Price"],
        )

    @staticmethod
    def convert_to_pdf(filename, laptops):
        pdf = FPDF()
        pdf.add_page()

        def clean_val(val):
            return str(val).replace("₱", "P")

        pdf.set_font("helvetica", "B", 18)
        pdf.cell(0, 15, "Comprehensive Laptop Market Report", ln=True, align="C")
        pdf.ln(5)

        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, "Overall Price Statistics", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(
            0, 7, f"Average Market Price: P{Laptop.avg_price(laptops):,.2f}", ln=True
        )
        pdf.cell(
            0, 7, f"Cheapest Unit Found: P{Laptop.min_price(laptops):,.2f}", ln=True
        )
        pdf.cell(
            0, 7, f"Most Expensive Unit: P{Laptop.max_price(laptops):,.2f}", ln=True
        )
        pdf.ln(10)

        analyses = [
            (
                "Market Segmentation",
                "category",
                ["Category", "Top CPU", "Top GPU", "Units", "Avg Price"],
            ),
            (
                "Price by Processor",
                "processor",
                ["Processor", "Total Units", "Avg Price", "Max Price", "Min Price"],
            ),
            (
                "Price by Graphics",
                "graphics",
                ["Graphics", "Total Units", "Avg Price", "Max Price", "Min Price"],
            ),
            (
                "Price by RAM",
                "ram",
                ["RAM", "Total Units", "Avg Price", "Max Price", "Min Price"],
            ),
            (
                "Brand Analysis",
                "brand",
                ["Brand", "Total Units", "Avg Price", "Max Price", "Min Price"],
            ),
        ]

        for title, key, headers in analyses:
            if pdf.get_y() > 230:
                pdf.add_page()

            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 10, title, ln=True)
            pdf.set_font("helvetica", "", 9)

            if key == "category":
                data = Laptop.group_by_category(laptops)
            else:
                data = Laptop.group_and_analyze(laptops, key)

            with pdf.table(text_align="CENTER", width=190) as table:
                header_row = table.row()
                for h in headers:
                    header_row.cell(h)

                for row in data:
                    pdf_row = table.row()
                    for item in row:
                        pdf_row.cell(clean_val(item))
            pdf.ln(10)

        pdf.output(filename)
        print(f"\nPDF Report saved as: {filename}")
