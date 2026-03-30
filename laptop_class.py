from tabulate import tabulate


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
        return [laptop.price for laptop in laptops if laptop is not None]

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
    def avg_price_processor(laptops):
        data = {}

        for laptop in laptops:
            if laptop is not None:
                if laptop.processor not in data:
                    data[laptop.processor] = []
                data[laptop.processor].append(laptop.price)

        price_data = []
        for processor, prices in data.items():
            count = len(prices)
            avg = sum(prices) / count
            price_data.append(
                [
                    processor,
                    f"{count} units",
                    f"₱{avg:,.2f}",
                    f"₱{max(prices):,.2f}",
                    f"₱{min(prices):,.2f}",
                ]
            )
        print(
            tabulate(
                price_data,
                headers=[
                    "Processor",
                    "Total Units",
                    "Average Price",
                    "Max Price",
                    "Min Price",
                ],
                tablefmt="rounded_grid",
            )
        )

    @staticmethod
    def avg_price_graphics(laptops):
        data = {}

        for laptop in laptops:
            if laptop is not None:
                if laptop.graphics not in data:
                    data[laptop.graphics] = []
                data[laptop.graphics].append(laptop.price)

        price_data = []
        for graphics, prices in data.items():
            count = len(prices)
            avg = sum(prices) / count
            price_data.append(
                [
                    graphics,
                    f"{count} units",
                    f"₱{avg:,.2f}",
                    f"₱{max(prices):,.2f}",
                    f"₱{min(prices):,.2f}",
                ]
            )
        print(
            tabulate(
                price_data,
                headers=[
                    "Graphics",
                    "Total Units",
                    "Average Price",
                    "Max Price",
                    "Min Price",
                ],
                tablefmt="rounded_grid",
            )
        )

    # Market Segmentation
    @staticmethod
    def group_by_category(laptops):
        category_data = {}

        for laptop in laptops:
            if laptop is not None:
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
                {
                    "Category": items,
                    "Most Common Processor": max_processor,
                    "Most Common GPU": max_gpus,
                    "Total Units": f"{sum(processors.values())} Units",
                    "Average Price": f"₱{avg_price:,.2f}",
                }
            )

        print(
            tabulate(
                final_category_data,
                headers="keys",
                tablefmt="rounded_grid",
            )
        )

    @staticmethod
    def avg_price_ram(laptops):
        data = {}

        for laptop in laptops:
            if laptop is not None:
                if laptop.ram not in data:
                    data[laptop.ram] = []
                data[laptop.ram].append(laptop.price)

        price_data = []
        for ram, prices in data.items():
            count = len(prices)
            avg = sum(prices) / count
            price_data.append(
                [
                    ram,
                    f"{count} units",
                    f"₱{avg:,.2f}",
                    f"₱{max(prices):,.2f}",
                    f"₱{min(prices):,.2f}",
                ]
            )
        print(
            tabulate(
                price_data,
                headers=[
                    "RAM",
                    "Total Units",
                    "Average Price",
                    "Max Price",
                    "Min Price",
                ],
                tablefmt="rounded_grid",
            )
        )

    @staticmethod
    def brand_analysis(laptops):
        brand_data = {}

        for laptop in laptops:
            if laptop is not None:
                if laptop.brand not in brand_data:
                    brand_data[laptop.brand] = []
                brand_data[laptop.brand].append(laptop.price)

        final_brand_data = []
        for brand, prices in brand_data.items():
            count = len(prices)
            avg = sum(prices) / count
            final_brand_data.append(
                [
                    brand,
                    f"{count} units",
                    f"₱{avg:,.2f}",
                    f"₱{max(prices):,.2f}",
                    f"₱{min(prices):,.2f}",
                ]
            )
        print(
            tabulate(
                final_brand_data,
                headers=[
                    "Brand",
                    "Total Units",
                    "Average Price",
                    "Max Price",
                    "Min Price",
                ],
                tablefmt="rounded_grid",
            )
        )
