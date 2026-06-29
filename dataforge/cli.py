"""Command-line entrypoint: dataforge run / export."""

import argparse


def main():
    """
    dataforge run <task.yaml>     # load config, build pipeline, run, print stats
    dataforge export <task.yaml>  # build HF dataset from existing data.jsonl
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
