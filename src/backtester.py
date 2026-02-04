from collections import deque
from src.events import EventType, OrderEvent
from src.metrics import compute_metrics

class Backtester : 
    def __init__ (self, data_handler, strategy, execution_handler, portfolio, quantity: int = 10):
        self.data = data_handler
        self.strategy = strategy
        self.exec = execution_handler
        self.quantity = quantity
        self.portfolio = portfolio

        self.events = deque()
        self.last_market = None

    def run(self):
        while self.data.has_next() or self.events:
            if not self.events and self.data.has_next():
                me = self.data.stream_next()
                self.last_market = me
                self.events.append(me)

            event = self.events.popleft()

            if event.type == EventType.MARKET:
                print(f"[MARKET] {event.dt} {event.symbol} close = {event.close}")
                
                self.portfolio.mark_to_market(event.dt, event.close)
                sig = self.strategy.on_market(event)
                if sig:
                    self.events.append(sig)
            
            elif event.type == EventType.SIGNAL:
                print(f" [SIGNAL] {event.symbol} -> {event.signal}")

                if event.signal == "LONG":
                    order = OrderEvent(
                        type = EventType.ORDER,
                        symbol=event.symbol,
                        dt = event.dt,
                        order_type="MKT",
                        direction="BUY",
                        quantity=self.quantity,
                    )
                    self.events.append(order)
                
                
                elif event.signal == "EXIT":
                    qty = self.portfolio.position.quantity
                    if qty > 0:
                        order = OrderEvent(
                            type=EventType.ORDER,
                            symbol=event.symbol,
                            dt = event.dt,
                            order_type = "MKT",
                            direction="SELL",
                            quantity= qty,
                        )
                    self.events.append(order)
            
            elif event.type == EventType.ORDER:
                print(f" [ORDER] {event.direction} {event.quantity} {event.symbol} ({event.order_type})")
                fill = self.exec.execute_order(event, self.last_market)
                self.events.append(fill)

            elif event.type == EventType.FILL:
                print(
                    f"      [FILL] {event.direction} {event.quantity} {event.symbol} "
                    f"@ {event.fill_price:.4f} (comm={event.commission}, slip={event.slippage:.4f})"
                )
                self.portfolio.on_fill(event)
        metrics = compute_metrics(self.portfolio.equity_curve)
        print("=== RESULTS ===")
        print(f"Total Results : {metrics['total_return']:.2%}")
        print(f"Max Drawdown : {metrics['max_drawdown']:.2%}")
        print(f"Sharpe :       {metrics['sharpe']:.2f}")


        metrics["equity_df"].to_csv("equity_curve.csv", index = False)
        print("Saved equity_curve.csv")


        summary = self.portfolio.summary()
        print("=== Final Portfolio ===")
        print(f"Cash:       {summary['cash']:.2f}")
        print(f"Quantity:       {summary['quantity']:.2f}")
        print(f"Avg Price:       {summary['avg_price']:.2f}")
        print(f"Equity:       {summary['equity']:.2f}")
        