import os
from datetime import datetime, timedelta
import logging
import time

import pandas as pd
from currencycom.client import Client


def minute_passed(
    last_timestamp: datetime, current_timestamp: datetime
) -> bool:
    return current_timestamp - last_timestamp >= timedelta(minutes=1)


def hour_passed(last_timestamp: float, current_timestamp: datetime) -> bool:
    return current_timestamp - last_timestamp >= timedelta(hours=1)


def delta_passed(
    last_timestamp: float, current_timestamp: datetime, delta: timedelta
) -> bool:
    return current_timestamp - last_timestamp >= delta


def time_up(current_timestamp: datetime, finish_time: datetime) -> bool:
    return finish_time - current_timestamp <= timedelta()


def get_server_time() -> datetime:
    return datetimify(Client.get_server_time()["serverTime"])


def datetimify(time: str) -> datetime:
    return datetime.fromtimestamp(int(time) * 0.001)


def collect_prices(
    for_: timedelta,
    pair: str = "BTC/USD",
    save_interval: timedelta = timedelta(hours=1),
    log_level: str = "ERROR",
) -> None:
    def save_prices():
        time_str = save_time.strftime("%d-%m-%y_%H-%M")
        pair_str = "_".join(pair.split("/"))
        filename = f"data/{pair_str}_{time_str}_prev{save_interval}.csv"
        pd.DataFrame.from_records(prices).drop_duplicates().to_csv(filename)
        logging.info(f"Saved to {filename}.")

    logging.basicConfig(
        filename=f'logs/{time.strftime("%d-%m-%y_%H-%M")}-run.log',
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%d-%m-%y %H:%M:%S",
        level=log_level,
    )

    current_time = save_time = start_time = get_server_time()
    prices = []
    logging.info("Crawling started.")

    while not delta_passed(start_time, current_time, for_):
        try:
            current_time = get_server_time()
            price_change = Client.get_24h_price_change(pair)
            prices.append(
                {
                    "price": float(price_change["lastPrice"]),
                    "time": datetimify(price_change["closeTime"]),
                }
            )

            if delta_passed(save_time, current_time, save_interval):
                logging.debug("Delta passed.")
                save_time = current_time
                save_prices()
                prices = []
        except Exception as e:
            logging.error(e)
        except KeyboardInterrupt:
            logging.error("Manual exit.")
            break

    save_time = current_time
    save_prices()
    logging.info("Crawling finished.")


def load_prices(data_dir="data"):
    series = []
    for f in os.listdir(data_dir):
        if f.endswith("csv"):
            series.append(
                pd.read_csv(
                    os.path.join(data_dir, f),
                    index_col=0,
                    parse_dates=["time"],
                )
            )
    return (
        pd.concat(series)
        .drop_duplicates()
        .sort_values("time")
        .reset_index(drop=True)
    )
