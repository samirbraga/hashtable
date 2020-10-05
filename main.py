import time
import getopt, sys
from logger import Logger
from hashtable import Hashtable
from input_parser import parse_input

argument_list = sys.argv[1:]

# Options
options = "i:o:s:d:h:"

# Long options
long_options = ["input=", "output=", "table-size=", "doubling-threshold=", "halving-threshold="]


def main():
    input_file = "./input.txt"
    output_file = "./output.txt"
    table_size = 4
    doubling_threshold = 0.75
    halving_threshold = 0.25
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-i", "--input"):
                input_file = currentValue
            elif currentArgument in ("-o", "--output"):
                output_file = currentValue
            elif currentArgument in ("-s", "--table-size"):
                table_size = int(currentValue)
            elif currentArgument in ("-d", "--doubling-threshold"):
                doubling_threshold = float(currentValue)
            elif currentArgument in ("-h", "--halving-threshold"):
                halving_threshold = float(currentValue)
    except getopt.error as err:
        print(str(err))

    inputs = parse_input(input_file)
    logger = Logger()
    hashtable = Hashtable(table_size,
                          logger,
                          grow_threshold=doubling_threshold,
                          shrink_threshold=halving_threshold)

    for ipt in inputs:
        cmd, value = ipt
        hashtable.apply(cmd, value)

    logger.write(output_file)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Tempo de execução: %.3f segundos." % (time.time() - start_time))