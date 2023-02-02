from typing import List

import aiohttp
import asyncio
from loguru import logger

from exceptions import MatrixNotSquare, ClientSideErrors, ServerSideErrors

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")


async def get_matrix(url: str) -> List[int]:
    """Основная функция для клиента, которая возвращает финальный List[int]"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            logger.debug(f"Status: {response.status}")
            _handle_errors(response)
            html = await response.text()
            matrix = _get_matrix_list_from_txt(html)
            if not _check_matrix_is_square(matrix):
                logger.error("Была передана не квадратная матрица")
                raise MatrixNotSquare
            final_matrix = _traverse_matrix_to_list(matrix)
            return final_matrix


def _handle_errors(response) -> None:
    """Обработка сетевых/серверный/клиентских ошибок"""
    if 400 <= response.status < 500:
        logger.error(f"Ошибка на стороне клиента. Статус: {response.status}")
        raise ClientSideErrors(f"Ошибка. Статус: {response.status}")
    elif response.status > 500:
        logger.error(f"Ошибка на стороне сервера. Статус: {response.status}")
        raise ServerSideErrors
    return


def _get_matrix_list_from_txt(html: str) -> List[List[int]]:
    """Пасим html, превращаем текст в матрицу формата List[List[int]]"""
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
    """Обходим матрицу по спирали с левого верхнего угла, против часовой стрелки и превращаем в List[int]"""
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
    """Проверяем, что матрица квадратная"""
    len_row = len(matrix[0])
    return len_row == len(matrix)


@logger.catch()
async def main():
    """Функция входа, запускаем в асинхронном режиме"""
    result = await get_matrix("https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt")
    logger.debug(result)


asyncio.run(main())
