import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


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


def max_return_drawdown(results, leverage=1, verbose=True):
    results = pd.Series(results)
    results -= 1
    results *= leverage
    results += 1
    results = results.values
    max_dd = 1
    max_gain = 0
    for i in range(len(results)):
        gain = np.product(results[: i + 1])
        if gain > max_gain:
            max_gain = gain
        elif gain / max_gain < max_dd:
            max_dd = gain / max_gain
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


def sharpe(returns, leverage=1, annual_risk_free_rate=0.01737, verbose=True):
    daily_rfr = annual_risk_free_rate / 252
    returns = pd.Series(returns)
    returns -= 1
    returns *= leverage
    returns = returns.values
    returns = np.array(returns)
    sharpe = ((np.mean(returns) - daily_rfr) / np.std(returns)) * (252 ** 0.5)
    if verbose:
        print('Annualized Sharpe:', round(sharpe, 4))
    return sharpe
