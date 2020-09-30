import numpy as np
from commands import Cmd
from hashtable import Hashtable, _split_in_binary_pieces
from logger import Logger
from input_parser import parse_input

INPUT_FILE = "./input.txt"
OUTPUT_FILE = "./output.txt"

if __name__ == "__main__":
    inputs = parse_input(INPUT_FILE)
    logger = Logger()
    hashtable = Hashtable(4, logger)

    for ipt in inputs:
        cmd, value = ipt
        hashtable.apply(cmd, value)

    logger.write(OUTPUT_FILE)
