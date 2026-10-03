import argparse

from .agent import agent_init


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()
    agent_init(args.p)


if __name__ == "__main__":
    main()
