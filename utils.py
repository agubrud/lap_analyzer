import yaml

def floatsec_to_minsecms(num):
    minutes = num // 60
    seconds = num % 60
    milliseconds = int((seconds % 1) * 1000)
    return f'{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}.{milliseconds}'

def load_config(cfg):
    with open(cfg, 'r') as f:
        return yaml.safe_load(f)