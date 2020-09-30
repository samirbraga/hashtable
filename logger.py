from commands import Cmd
from output_writer import output_writer


class Logger:
    """
    Mantém um registro em memória dos comandos aplicados a uma estrutura de dados.
    """
    def __init__(self):
        self.logs = []

    def input(self, input: (Cmd, int), hash_result: int, operation_position: int) -> None:
        self.logs.extend([
            input,
            (hash_result, operation_position),
            None
        ])

    def cmd(self, cmd: Cmd, value: int) -> None:
        self.logs.extend([
            (cmd, value),
            None
        ])

    def write(self, output_file: str) -> None:
        output_writer(self.logs, output_file)
