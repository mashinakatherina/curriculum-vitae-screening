import pandas as pd
import sys


def process_csv(filename):
    df = pd.read_csv(filename)
    print(df.head())


if __name__ == "__main__":
    process_csv(sys.argv[1])
