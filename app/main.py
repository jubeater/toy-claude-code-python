import argparse

from .agent import agent_loop


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()
    agent_loop(args.p)


if __name__ == "__main__":
    main()
