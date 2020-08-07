import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import logging
from typing import Union


def basic(results):
    print('\n_______________________________________________________________________________________________________\n')
    if len(results) == 0:
        print('NO TRADES!')
        return
    winners = []
    losers = []
    for item in results:
        if item > 1:
            winners.append(item)
        else:
            losers.append(item)
    if losers:
        avg_loss = np.mean(losers)
    else:
        avg_loss = np.nan
    if not winners:
        print('\nAccuracy:\t' + str(round(100 * len(winners) / (len(winners) + len(losers)), 2)) + '%',
              '\nTotal:\t\t' + str(len(results)))
        print('No wins')
        print('Avg Loss:\t' + str(round(100 * (1 - avg_loss), 2)) + '%\tMax Loss:\t' +
              str(round(100 * (1 - np.min(losers)), 2)) + '%')
        ta100 = avg_loss ** 100
        print('Avg Trade:\t' + str(100 * ((ta100 ** 0.01) - 1))[:4] + '%')
        print('Outcome:\t' + str(round(ta100, 4)) + 'x')
        print('(100TA)\n') # 100 Trade Average
        return
    avg_win = np.mean(winners)
    if len(losers) != 0:
        ta100 = (avg_win ** (100 * len(winners) / len(results))) * \
            (avg_loss ** (100 * len(losers) / len(results)))
    else:
        ta100 = avg_win ** 100
    print('\nAccuracy:\t' + str(round(100 * len(winners) / (len(winners) + len(losers)), 2)) + '%',
          '\nTotal:\t\t' + str(len(results)))
    print(
        'Avg Win:\t' + str(round(100 * (avg_win - 1), 2)) +
        '%\tMax Win:\t' + str(round(100 * (np.max(winners) - 1), 2)) + '%')
    if len(losers) != 0:
        print('Avg Loss:\t' + str(round(100 * (1 - avg_loss), 2)) + '%\tMax Loss:\t' +
              str(round(100 * (1 - np.min(losers)), 2)) + '%')
    else:
        print('No losses')
    print('Avg Trade:\t' + str(100 * ((ta100 ** 0.01) - 1))[:4] + '%')
    print('Outcome:\t' + str(round(ta100, 4)) + 'x')
    print('(100TA)\n')  # 100 Trade Average


def max_return_drawdown(results: Union[pd.Series, np.ndarray, list], leverage=1, verbose=True) -> float:
    """
    Get the maximum drawdown for strategy returns

    :param results: strategy returns
    :param leverage: amount of leverage to apply to returns, default=1
    :param verbose: print drawdown at the end of calculation
    :return: maximum drawdown in returns
    """
    if not isinstance(results, pd.Series):
        results = pd.Series(results)
    results -= 1
    results *= leverage
    results += 1
    results = results.cumprod()
    max_dd = 1
    high = 0
    for i in range(len(results)):
        if results.at[i] > high:
            # new high
            high = results.at[i]
        else:
            # in drawdown period
            max_dd = min(max_dd, results.at[i]/high)
    if verbose:
        print('Max Drawdown:', round(1 - max_dd, 4))
    return 1 - max_dd


def simulate(results, acct, commission, leverage):
    print('\n_______________________________________________________________________________________________________\n')
    print('SIMULATION')
    print('Starting acct val:\t', "{:,}".format(round(acct, 2)))
    for i in range(len(results)):
        acct += ((acct * results[i]) - acct) * leverage
        acct -= commission
    print('FINAL BALANCE:\t\t', "{:,}".format(round(acct, 2)))


def chart_results(results, leverage):
    plt.clf()
    results = pd.Series(results)
    results -= 1
    results *= leverage
    results += 1
    temp = []
    for i in range(len(results)):
        temp.append(np.product(results[:i+1]))
    temp = pd.Series(temp)
    temp.plot()
    print('\nRETURN:', str(round(temp.iloc[-1], 4)) + 'x')
    plt.show()


def sharpe(result: Union[pd.Series, list, np.ndarray], leverage=1,
           annual_risk_free_rate=0.01737, verbose=True) -> float:
    """
    Get the annualized daily sharpe ratio for strategy returns
    https://en.wikipedia.org/wiki/Sharpe_ratio

    :param result: daily strategy returns
    :param leverage: amount of leverage to apply to returns, default=1
    :param annual_risk_free_rate: typically 10 year treasury bond yield, default=0.01737
    :param verbose: print sharpe ratio at the end of calculation
    :return: annualized sharpe ratio
    """
    if not isinstance(result, pd.Series):
        result = pd.Series(result)
    daily_rfr = annual_risk_free_rate / 252
    result -= 1
    result *= leverage
    st_dev = result.std()
    if st_dev != 0:
        sharpe = ((result.mean() - daily_rfr) / st_dev) * (252 ** 0.5)
    else:
        logging.warning("Sharpe Error: Return STDEV=0")
        sharpe = 0
    if verbose:
        print('Annualized Sharpe:', round(sharpe, 4))
    return sharpe


def sharpe_monthly(result, leverage=1, annual_risk_free_rate=0.01737, verbose=True):
    daily_rfr = annual_risk_free_rate / 12
    returns = pd.Series(result)
    returns -= 1
    returns *= leverage
    returns = returns.values
    returns = np.array(returns)
    sharpe = ((np.mean(returns) - daily_rfr) / np.std(returns)) * (12 ** 0.5)
    if verbose:
        print('Annualized Sharpe:', round(sharpe, 4))
    return sharpe


def consolidate_monthly_result(data):
    monthly = {}
    for date, gain in data.items():
        if not gain:
            continue
        if date[:7] not in monthly.keys():
            monthly[date[:7]] = []
        monthly[date[:7]].append(gain)
    result = []
    for val in monthly.values():
        result.append(np.product(val))
    return result



def sortino(result, leverage=1, annual_risk_free_rate=0.01737, verbose=True):
    daily_rfr = annual_risk_free_rate / 252
    returns = pd.Series(result)
    returns -= 1
    returns *= leverage
    returns = returns.values
    downside = []
    for i in range(len(returns)):
        if (returns[i] - daily_rfr) < 0:
            downside.append((returns[i] - daily_rfr) ** 2)
        else:
            downside.append(0)
    downside_risk = np.mean(downside) ** 0.5
    sortino = ((np.mean(returns) - daily_rfr) / downside_risk) * (252 ** 0.5)
    if verbose:
        print('Annualized Sortino:', round(sortino, 4))
    return sortino


def vix_f(data: pd.DataFrame) -> pd.Series:
    """
    VIXf

    :param data: pd.DataFrame with at least close and low cols
    :return: VIXf
    """
    highs = data['close'].rolling(20).max()
    return 100 * (highs-data['low'])/highs
