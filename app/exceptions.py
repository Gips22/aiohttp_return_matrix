"""Кастомные исключения, генерируемые приложением"""


class MatrixNotSquare(Exception):
    """Исключение отрабатывающее если матрица не квадратная"""
    pass

class ClientSideErrors(Exception):
    """Обработка ошибок сервера и сетевых ошибок"""
    pass

class ServerSideErrors(Exception):
    """Обработка ошибок сервера и сетевых ошибок"""
    pass
