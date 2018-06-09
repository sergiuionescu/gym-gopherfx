import pandas as pd
import os

source = 'rates/'
target = 'potential/'

points = 100
spread = 0.013
wait = 3
duration_limit = 5

for rates_file in os.listdir(source):
    potential = []
    total_profit = 0
    total_loss = 0
    rolls = 0

    df = pd.read_csv(
        'rates/' + rates_file, names=['date', 'rate'])

    total = len(df.index)


    def get_profit(start_rate, end_rate):
        profit = (end_rate - (start_rate + spread)) * points
        return profit


    def search_potential(start, end):
        global total_profit, total_loss, rolls, potential
        start_rate = df['rate'][start]
        start_date = df['date'][start]
        end_rate = df['rate'][end]
        end_date = df['date'][end]

        profit = get_profit(start_rate, end_rate)

        rolls += points
        duration = end - start
        if duration < duration_limit:
            if profit > 0:
                    total_profit += profit
                    print("Profit: " + str(profit) + ". Buy " + str(points) + " at " + str(start_rate) + "(" + str(
                        start_date) + "), Sell at " + str(end_rate) + "(" + str(end_date) + "), Open for " + str(
                        duration) + " minutes")
            else:
                total_loss += profit
                print("Loss: " + str(profit) + ". Buy " + str(points) + " at " + str(start_rate) + "(" + str(
                    start_date) + "), Sell at " + str(end_rate) + "(" + str(end_date) + "), Open for " + str(
                    duration) + " minutes")

            potential.append(
                str(start_date) + ", " + str(end_date) + ", " + str(profit) + ", " + str(start_rate) + ", " + str(
                    end_rate) + ", " + str(duration))

        if duration > wait:
            mid = int((duration) / 2)
            search_potential(start, start + mid)
            search_potential(end - mid, end)


    search_potential(0, total - 1)

    print("\nTotal profit " + str(total_profit) + ", total loss " + str(total_loss) + ", risk " + str(rolls))

    with open(target + rates_file, 'wb') as file:
        for line in potential:
            file.write(line + '\n')

    key_date = pd.to_datetime(df['date'][0]).strftime('%Y-%m-%d')
    with open(target + rates_file + '.total', 'wb') as file:
        file.write(key_date + ',' + str(total_profit) + ',' +  str(total_loss) + ',' + str(rolls) + "\n")
