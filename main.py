from datetime import timedelta
import yaml
from utils import collect_prices


def main():
    with open("config.cfg") as f:
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
