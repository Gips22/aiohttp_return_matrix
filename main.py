from typing import List

import aiohttp
import asyncio


async def get_matrix(url: str) -> List[int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)

            html = await response.text()
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
            f = traverse_matrix(matrix)
            print(f)





def traverse_matrix(matrix: List[list[int]], new_matrix: list[int]=None) -> List[int]:
    if not new_matrix:
        new_matrix = []

    if not len(matrix):
        finall_matrix = []
        for i in new_matrix:
            for j in i:
                finall_matrix.append(j)
        print(finall_matrix)
        return finall_matrix

    matrix = list(zip(*matrix[::-1]))
    new_matrix.append(matrix[0][::-1])
    traverse_matrix(matrix[1:], new_matrix)








def check_matrix_is_square(matrix):
    len_row = matrix[0]
    return len_row == len(matrix)




loop = asyncio.get_event_loop()
loop.run_until_complete(
    get_matrix("https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"))
