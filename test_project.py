import pytest
from laptop_class import Laptop  # Replace with your actual filename


@pytest.fixture
def sample_laptops():
    """Fixture to provide a standard set of laptops for testing."""
    return [
        Laptop("Dell", "16GB", "512GB", "i7", "RTX 3050", "₱45,000"),
        Laptop("HP", "8GB", "256GB", "i5", "Integrated", "₱25,000"),
        Laptop("Apple", "16GB", "512GB", "M2", "M2 GPU", "₱75,000"),
    ]


def test_init():
    l1 = Laptop("Brand", "8GB", "256GB", "CPU", "GPU", "₱30,000")
    assert l1.price == 30000
    assert l1.category == "Budget"

    l2 = Laptop("Brand", "8GB", "256GB", "CPU", "GPU", "₱60,000")
    assert l2.category == "Mid-Range"

    l3 = Laptop("Brand", "8GB", "256GB", "CPU", "GPU", "₱60,001")
    assert l3.category == "High-End"


def test_price_calculations(sample_laptops):
    assert Laptop.min_price(sample_laptops) == 25000.0
    assert Laptop.max_price(sample_laptops) == 75000.0

    assert Laptop.avg_price(sample_laptops) == pytest.approx(48333.33, 0.01)


def test_group_and_analyze(sample_laptops):
    analysis = Laptop.group_and_analyze(sample_laptops, "brand")

    assert analysis[0][0] == "Apple"
    assert analysis[0][1] == "1 units"
    assert "₱75,000.00" in analysis[0]


def test_market_segmentation(sample_laptops):
    segments = Laptop.group_by_category(sample_laptops)

    budget_row = next(row for row in segments if row[0] == "Budget")
    assert budget_row[1] == "i5"
    assert budget_row[2] == "Integrated"
    assert "₱25,000.00" in budget_row


def test_best_value(sample_laptops):
    category, price = Laptop.best_value_category(sample_laptops)
    assert category == "Budget"
    assert price == 25000.0


def test_invalid_price():
    with pytest.raises(ValueError):
        Laptop("Brand", "8GB", "256GB", "CPU", "GPU", "Price Unknown")
