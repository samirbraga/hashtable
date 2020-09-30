from typing import List, Tuple
from commands import Cmd
import numpy as np


def output_writer(track: List[Tuple[Cmd, np.int64]], output_file: str) -> None:
    result = ""
    for log in track:
        if log is None:
            result += '\n\n'
        elif type(log) is tuple:
            if isinstance(log[0], Cmd):
                result += "%s:%d\n" % log
            else:
                result += "%s %d\n" % log

    with open(output_file, "w+") as output:
        output.write(result)
