"""Test suite for window_range function."""

import pytest
from pyspark.sql import Window
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, StructField, StructType
from pyspark.sql.utils import AnalysisException

from src.min_max import window_range


# 1. Normal Case: Default parameters
def test_window_range_default(spark):
    """Test window_range with default parameters."""
    df = spark.createDataFrame([(1, 10), (2, 50), (3, 20)], ["id", "value"])
    # Coverage: Branch when window is None
    result = window_range(df, "value")
    assert "window_range" in result.columns
    assert result.filter(F.col("id") == 1).collect()[0]["window_range"] == 40


# 2. Normal Case: Custom window & Custom output
def test_window_range_custom(spark):
    """Test window_range with custom window and output column."""
    df = spark.createDataFrame([("A", 10), ("A", 20)], ["group", "value"])
    w = Window.partitionBy("group")
    # Coverage: Using custom window parameter
    result = window_range(df, "value", window=w, output_col="diff")
    assert "diff" in result.columns
    assert result.collect()[0]["diff"] == 10


# 3. Abnormal Case: Null Values
def test_window_range_nulls(spark):
    """Test window_range handles null values correctly."""
    df = spark.createDataFrame([(1, 10), (2, None)], ["id", "value"])
    result = window_range(df, "value")
    # Spark handles Null in max/min by ignoring them
    # -> result is still 0 (10-10)
    assert result.filter(F.col("id") == 1).collect()[0]["window_range"] == 0


# 4. Abnormal Case: Empty DataFrame
def test_window_range_empty(spark):
    """Test window_range handles empty DataFrame correctly."""
    schema = StructType([StructField("value", IntegerType())])
    df = spark.createDataFrame([], schema)
    result = window_range(df, "value")
    assert result.count() == 0
    assert "window_range" in result.columns


# 5. Abnormal Case: Missing Column (Failure mode)
def test_window_range_missing_col(spark):
    """Test window_range raises error for missing column."""
    df = spark.createDataFrame([(1, 10)], ["id"])
    with pytest.raises(AnalysisException):
        window_range(df, "wrong_col").collect()


# 6. Abnormal Case: Wrong Data Type (Failure mode)
def test_window_range_wrong_type(spark):
    """Test window_range handles incompatible data types gracefully."""
    df = spark.createDataFrame([(1, "string_val")], ["id", "value"])
    result = window_range(df, "value")
    assert result.collect()[0]["window_range"] is None
