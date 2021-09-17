from datetime import timedelta
import sys
import yaml
from utils import collect_prices


def main():
    if len(sys.argv) > 1:
        cfg_file = sys.argv[1]
    else:
        cfg_file = "config.yml"
    print(sys.argv)
    print(cfg_file)
    with open(cfg_file) as f:
        cfg = yaml.load(f, yaml.SafeLoader)

    period = timedelta(**cfg.get("CRAWLING_PERIOD", {"hours": 4}))
    save_interval = timedelta(**cfg.get("SAVE_INTERVAL", {"minutes": 30}))
    pair = cfg.get("PAIR", "BTC/USD")
    log_level = cfg.get("LOG_LEVEL", "ERROR")

    collect_prices(
        for_=period,
        pair=pair,
        save_interval=save_interval,
        log_level=log_level,
    )


if __name__ == "__main__":
    main()
