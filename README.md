# ERC20 Supply Analyzer
A small Python 3 project with the goal of fetching, parsing and graphing Ethereum ERC20 token supply data.

It uses Python together with Seth from dapp.tools to fetch the ERC20 supply data. And Plotly to generate graphs from the data.

## Getting Started
Make sure you have setup Seth (https://dapp.tools/seth/) with an Ethereum client RPC endpoint, like infura.io or your own local archive node. And make sure `seth` binary is in your PATH.

Run `python erc20-build-supply-data.py --help` to see execution options.

### Prerequisites
```
Seth 
Python 3
Pipenv (if you want automatic dependency install)

Python dependencies:
  Plotly
  Pandas
```

### How to use
* Make sure prerequisites are installed and configured!
* Find the Ethereum address of the token you want to analyze. E.g. Wrapped BTC found by searching Etherscan: https://etherscan.io/token/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599

```
0x2260fac5e5542a773aa44fbcfedf7c193bc2c599
```

* Run erc20-build-supply-data.py to collect and save supply data:

```
python3 erc20-build-supply-data.py 0x2260fac5e5542a773aa44fbcfedf7c193bc2c599
```

This will collect data from currect Ethereum block and as far back as possible, with 5760 block intervals (roughly 24 hour interval). The data will be saved in the file `erc20_supply_data.csv`.

An example with all options:

```
python3 erc20-build-supply-data.py --start 8000000 --end 7000000 --interval 5000 --output wbtc.csv 0x2260fac5e5542a773aa44fbcfedf7c193bc2c599
```

* To create a graph from the supply data run:

```
python3 erc20-draw-supply.py wbtc.csv
```

This will generate a plotly html graph of the supply over time.