"""Module for computing window range (max - min) on PySpark DataFrames."""

import sys

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def window_range(
    df: DataFrame,
    value_col: str,
    window=None,
    output_col: str = "window_range",
) -> DataFrame:
    """
    Args:
        df: spark dataframe
        value_col: column name to compute range on
        window: calculation window
        output_col:

    Returns:
        spark dataframe with (max - min) computed over the specified window
    """
    if window is None:
        window = Window.rangeBetween(-sys.maxsize, sys.maxsize)

    # single window pass: compute max & min together
    df = df.withColumn(
        "_mm",
        F.struct(
            F.max(F.col(value_col)).over(window).alias("maxv"),
            F.min(F.col(value_col)).over(window).alias("minv"),
        ),
    )

    df = df.withColumn(
        output_col, F.col("_mm.maxv") - F.col("_mm.minv")
    ).drop(  # noqa: E501
        "_mm"
    )
    return df
