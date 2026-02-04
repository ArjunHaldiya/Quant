from dataclasses import dataclass

@dataclass
class Position:
    quantity : int = 0
    avg_price : float = 0.0

class Portfolio:
    def __init__ (self, symbol : str, initial_cash: float = 100_000.0):
        self.symbol = symbol
        self.cash = float(initial_cash)
        self.position = Position()
        self.equity_curve = []
        self.trades = []


        
    def on_fill (self, fill_event):
        qty_signed = fill_event.quantity if fill_event.direction == "BUY" else -fill_event.quantity
        trade_value = qty_signed * fill_event.fill_price

        self.cash -= trade_value
        self.cash -= fill_event.commission

        new_qty = self.position.quantity + qty_signed
        if new_qty == 0:
            self.position.quantity = 0
            self.position.avg_price = 0.0

        else:
            if qty_signed > 0:
                total_cost_existing = self.position.avg_price * self.position.quantity
                total_cost_new = fill_event.fill_price * qty_signed
                self.position.avg_price = (total_cost_existing + total_cost_new) / new_qty

            self.position.quantity = new_qty
        self.trades = ({
            "dt" : fill_event.dt,
            "direction" : fill_event.direction,
            "quantity" : fill_event.quantity,
            "price" : fill_event.fill_price,
            "commission" : fill_event.commission,
            "slippage" : fill_event.slippage,
        })

    def mark_to_market(self, dt, price : float):
        holdings = self.position.quantity * price
        equity = self.cash + holdings
        self.equity_curve.append(
            {"dt" : dt, 
            "equity" : equity,
            "cash" : self.cash,
            "qty" : self.position.quantity, 
            "price" : price}
        )
        return equity
    

    def summary(self):
        return{
            "cash" : self.cash,
            "quantity" : self.position.quantity,
            "avg_price" : self.position.avg_price,
            "equity" : self.cash + self.position.quantity * self.position.avg_price, 
        }