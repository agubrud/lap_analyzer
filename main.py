import argparse
from Session import Session
from utils import load_config

def main():
    cfg = load_config(args.config)
    s = Session(cfg)
    s.process_video()
    s.summarize()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=False, help="Configuration YAML file", dest="config", default='cfg.yml')
    args = parser.parse_args()
    main()