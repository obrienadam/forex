import broker, robot, strategy
import chart

def main():
    with open('account.txt') as f:
        ACCOUNT_ID = f.readline().strip()
        ACCESS_TOKEN = f.readline().strip()

    session = broker.API(ACCOUNT_ID, ACCESS_TOKEN)
    strat = strategy.McGinleyDynamic()
    trader = robot.Robot(session, strat)

    trader.trade('EUR_GBP', 'M1', 14400)

if __name__ == '__main__':
    main()