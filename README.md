#gym-gopherfx

A gym environment for reinforcement training on forex historical data.

Historical data is no way a predictor of future behaviour in forex, but can be used as challenging science experiment :).

##How to run
Clone the repo
```bash
docker-compose up -d
```

Access [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to access the dashboard.


To start a random agent and see live evolutions:
```bash
python random_agent.py
```

##About the environment

The available actions are:
* 0 - wait
* 1 - buy
* 2 - sell

Reward:
* 0 - for waiting/buying
* trade_result - for selling
* -1 - when depleting the budget

The episodes ends when the trading day is over or the budget is depleted.