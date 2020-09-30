from typing import List, Tuple
from commands import Cmd
import numpy as np


def parse_input(filepath: str) -> List[Tuple[Cmd, np.int64]]:
    cmds = []

    with open(filepath, "r") as file:
        for line in file.readlines():
            cmd, value = line.split(":")
            cmds.append((Cmd.__members__[cmd], np.int64(value)))

    return cmds
