import exceptions
import asyncio

import pytest

from app.main import get_matrix, _check_matrix_is_square, _traverse_matrix_to_list, _get_matrix_list_from_txt


SOURCE_URL = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"

TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

ORIGINAL_MATRIX = [[10, 20, 30, 40],
                   [50, 60, 70, 80],
                   [90, 100, 110, 120],
                   [130, 140, 150, 160]]


def test_get_matrix():
    assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL


@pytest.mark.parametrize("expected_exception, url",
                         [(exceptions.ClientSideErrors, "https://vk.com/sfhijsiodsopihdsdf")])
def test_handling_errors(expected_exception, url):
    with pytest.raises(expected_exception):
        asyncio.run(get_matrix(url))


def test_get_matrix_list_from_txt():
    with open("matrix.txt", "r") as file:
        assert _get_matrix_list_from_txt(file.read()) == ORIGINAL_MATRIX
    assert _get_matrix_list_from_txt("") == []


def test_traverse_matrix_to_list():
    new_matrix = []
    assert _traverse_matrix_to_list(ORIGINAL_MATRIX, new_matrix) == TRAVERSAL


def test_check_matrix_is_square():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert _check_matrix_is_square(matrix) == True
    matrix = [[1, 2, 3], [4, 5, 6]]
    assert _check_matrix_is_square(matrix) == False
