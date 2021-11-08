from datetime import date

import pandas as pd
import requests


def get_ts(
    coin: str = "nexo", vs_currency: str = "eur", days: int = 30
) -> pd.DataFrame:
    """Queries time series data from the coingecko API of a selected coin/token.
    The result will be returned as a pandas DataFrame.

    Parameters
    ----------
    coin : str, optional
        Coin or token e.g. "bitcoin", by default "nexo"
    vs_currency : str, optional
        Currency price is displayed in, by default "eur"
    days : int, optional
        Last x days, by default 30

    Returns
    -------
    pd.DataFrame
        example:

                    prices	    market_caps	    total_volumes
        2019-11-03	0.084479	4.726148e+07	8.724440e+06
        2019-11-04	0.089416	5.003882e+07	9.235387e+06
        2019-11-05	0.093230	5.220886e+07	9.646853e+06
    """

    # https://www.coingecko.com/api/documentations/v3#/coins/get_coins__id__market_chart
    params = {
        "coin": coin,
        "vs_currency": vs_currency,
        "days": days,
        "interval": "daily",  # NOTE: To keep it simple, we'll focus on daily prices only
    }
    base_url = "https://api.coingecko.com/api/v3/coins/"
    param_url = (
        "{coin}/market_chart?vs_currency={vs_currency}&days={days}&interval={interval}"
    )
    url = base_url + param_url.format(**params)
    page = requests.get(url)

    if page.status_code == 200:
        prices = [i[1] for i in page.json()["prices"]]
        market_caps = [i[1] for i in page.json()["market_caps"]]
        total_volumes = [i[1] for i in page.json()["total_volumes"]]
        dates = [date.fromtimestamp(i[0] / 1000) for i in page.json()["prices"]]

        df = pd.DataFrame(
            {
                "prices": prices,
                "market_caps": market_caps,
                "total_volumes": total_volumes,
            },
            index=dates,
        )
        # If last/latest row appears twice, keep only the latest row
        if len(df[df.index == df.index.max()]) > 1:
            df = df[~(df.iloc[:] == df.iloc[-2])].dropna()

        return df
