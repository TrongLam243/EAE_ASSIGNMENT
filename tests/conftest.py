"""Pytest configuration and fixtures for PySpark tests."""

import pytest
from pyspark.sql import SparkSession


# scope="session" parameter ensures SparkSession is created ONLY ONCE
# for the entire test run
@pytest.fixture(scope="session")
def spark():
    """Initialize Local SparkSession shared across all tests."""
    spark_session = (
        SparkSession.builder.master("local[1]")
        .appName("pytest-pyspark-local-testing")
        .getOrCreate()
    )

    # yield keyword returns session for test functions to use
    yield spark_session

    # This block will automatically run to clean up memory
    # after all tests have completed
    spark_session.stop()
