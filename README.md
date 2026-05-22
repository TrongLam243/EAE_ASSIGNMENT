# PySpark Window Range Calculator

A PySpark utility for computing window range (max - min) operations on DataFrames.

## Overview

This project provides a simple yet efficient function to calculate the range (difference between maximum and minimum values) over a specified window in PySpark DataFrames.

## Features

- **Window-based Range Calculation**: Compute (max - min) over custom or default windows
- **Optimized Performance**: Single-pass window computation for both max and min
- **Flexible Configuration**: Customize window specifications and output column names
- **Production Ready**: Includes comprehensive testing and CI/CD pipeline

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.11+
- PySpark 3.5.0
- Java 11 (required for Spark runtime)

## Usage

```python
from pyspark.sql import SparkSession, Window
from src.min_max import window_range

# Create Spark session
spark = SparkSession.builder.appName("WindowRangeExample").getOrCreate()

# Create sample DataFrame
df = spark.createDataFrame([(1, 10), (2, 20), (3, 15)], ["id", "value"])

# Compute window range with default window (entire dataset)
result = window_range(df, value_col="value", output_col="range")

# Compute window range with custom window
custom_window = Window.orderBy("id").rowsBetween(-1, 1)
result = window_range(df, value_col="value", window=custom_window, output_col="range")
```

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

### Code Quality

```bash
# Run linting
flake8 src/ tests/ --max-line-length=88
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration:

- **Static Analysis**: Flake8 linting on every push and PR
- **Unit Tests**: Automated testing with coverage reporting
- **Python Version**: Tests run on Python 3.11
- **Spark Environment**: Java 11 setup for PySpark compatibility

See [.github/workflows/pr-test.yml](.github/workflows/pr-test.yml) for pipeline details.

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   └── min_max.py          # Main window range function
├── tests/
│   ├── conftest.py         # Pytest configuration
│   └── test_min_max.py     # Test cases
├── .github/
│   └── workflows/
│       └── pr-test.yml     # CI/CD pipeline
├── requirements.txt        # Project dependencies
└── pytest.ini             # Pytest configuration
```

## License

This project is part of an educational assignment (EAE).

## Contributing
Nguyen Trong Lam (MS/EJV6-PS): Lam.NguyenTrong@vn.bosch.com
