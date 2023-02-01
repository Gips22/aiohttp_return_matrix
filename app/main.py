from typing import List

import aiohttp
import asyncio
from loguru import logger

from exeptions import MatrixNotSquare

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")

async def get_matrix(url: str) -> List[int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            logger.debug(f"Status: {response.status}")
            html = await response.text()
            matrix = _get_matrix_list_from_txt(html)
            if not _check_matrix_is_square(matrix):
                logger.error("Была передана не квадратная матрица")
                raise MatrixNotSquare
            final_matrix = _traverse_matrix_to_list(matrix)
            return final_matrix

def _get_matrix_list_from_txt(html):
    matrix = []
    for i in html.split('\n'):
        if i.startswith('+'):
            continue
        else:
            row = []
            for j in i.split():
                if j.isdigit():
                    row.append(int(j))
            if row:
                matrix.append(row)
    return matrix


def _traverse_matrix_to_list(matrix: List[list[int]], new_matrix: list[int] = None) -> List[int]:
    if not new_matrix:
        new_matrix = []

    if not len(matrix):
        result = []
        for i in new_matrix:
            for j in i:
                result.append(j)
        return result

    matrix = list(zip(*matrix[::-1]))
    new_matrix.append(matrix[0][::-1])
    return _traverse_matrix_to_list(matrix[1:], new_matrix)


def _check_matrix_is_square(matrix):
    len_row = len(matrix[0])
    return len_row == len(matrix)


async def main():
    result = await get_matrix("https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt")
    logger.debug(result)

asyncio.run(main())