# performance-analysis
Useful tools for evaluating trading strategy performance

# Dependencies

* Python 3
* Numpy
* Pandas
* Matplotlib

# API
All functions require a list of trading returns in decimal format. A 1% gain would be 1.01, a 1% loss would be 0.99

```python
results = [0.9884, 1.007, 0.9875, 1.0345, 1.0251, 1.0172, 1.0197, 0.9902, 0.9932, 1.0113]
```

The ```basic()``` function reports an assortment of valuable metrics including the average return of 100 trades (100TA)

```python
basic(results=results)
```
```
Accuracy:	60.0% 
Total:		10
Avg Win:	1.91%	Max Win:	3.45%
Avg Loss:	1.02%	Max Loss:	1.25%
Avg Trade:	0.73%
Outcome:	2.0711x
(100TA)
```

The ```simulate()``` function reports the simulated gain with a brokerage account for a given commission, initial balance, 
and leverage

```python
simulate(results=results, acct=250000, commission=10, leverage=2)
```
```
SIMULATION
Starting acct val:	 250,000
FINAL BALANCE:		 288,077.32
```

Other available functions:

```
max_return_drawdown()
chart_results()
sharpe()  [annualized]
sortino() [annualized]

