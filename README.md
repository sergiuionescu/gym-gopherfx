# gym-gopherfx

A gym environment for reinforcement training on forex historical data.

Historical data is no way a predictor of future behaviour in forex, but can be used as challenging science experiment :).

## How to run
Clone the repo
```bash
docker-compose up -d
```

Access [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to access the dashboard.


To start a random agent and see live evolutions:
```bash
python random_agent.py
```

## About the environment

### Gopherfx-v0

Observation:
A tuple of the current datetime and rate

The available actions are:
* 0 - wait
* 1 - buy
* 2 - sell

Reward:
* 0 - for waiting/first buy/first sell
* trade_result - for closing an open position
* -1 - when depleting the budget

The episodes ends when the trading day is over or the budget is depleted.

### Gopherfx-v1

Observation:
- A tuple of Candle rate data representing the market state at the step moment
- The value for the current open position
- The action required to close the current open position

Raw example:
```json
{
  "volume": 45,
  "time": "2018-06-01T00:00:00.000000000Z",
  "bid": {
    "o": "1.16916",
    "h": "1.16929",
    "l": "1.16908",
    "c": "1.16915"
  },
  "ask": {
    "o": "1.16933",
    "h": "1.16946",
    "l": "1.16924",
    "c": "1.16930"
  }
}
```


The available actions are:
* 0 - wait
* 1 - buy
* 2 - sell

Reward:
* 0 - for waiting/first buy/first sell
* trade_result - for closing an open position
* -1 - when depleting the budget

The episode ends when the trading day is over or the budget is depleted.