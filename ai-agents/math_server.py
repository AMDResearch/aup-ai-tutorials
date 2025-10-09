# Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
# 
# SPDX-License-Identifier: MIT

from mcp.server.fastmcp import FastMCP
from typing import Union

mcp = FastMCP("Math Sever")


@mcp.tool()
def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers
    """
    return a + b


@mcp.tool()
def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Multiply two numbers
    """
    return a * b


@mcp.tool()
def division(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Divide a by b
    """
    return a / b


@mcp.tool()
def square_root(a: Union[int, float]) -> Union[int, float]:
    """
    Compute the square root of a number
    """
    return a ** 0.5


if __name__ == "__main__":
    mcp.run(transport="stdio")
