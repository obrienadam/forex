import broker, robot, strategy
import chart

def main():
    with open('account.txt') as f:
        ACCOUNT_ID = f.readline().strip()
        ACCESS_TOKEN = f.readline().strip()

    session = broker.API(ACCOUNT_ID, ACCESS_TOKEN)
    strat = strategy.Random(max_capital_risk=3.)
    trader = robot.Robot(session, strat)

    trader.trade()

if __name__ == '__main__':
    main()