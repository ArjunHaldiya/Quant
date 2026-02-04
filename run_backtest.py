from src.data_handler import CSVDataHandler
from src.backtester import Backtester
from src.strategy import MovingAverageCrossStrategy
from src.execution import SimulatedExecutionHandler
from src.portfolio import Portfolio


def main():
    csv_path = "data/sample.csv"
    symbol = "TEST"
    
    data = CSVDataHandler(csv_path, symbol)
    strat = MovingAverageCrossStrategy(symbol, short_window=2, long_window=4)
    exec_handler = SimulatedExecutionHandler(slippage_bps=2.0, commission=1.0)
    port = Portfolio(symbol, initial_cash=100_000)

    bt = Backtester(data, strat, exec_handler,port,quantity=10)
    bt.run()

if __name__ == "__main__":
    main()