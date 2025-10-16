from portfolio_math import returns_to_volatility, max_drawdown, sortino_ratio, sharpe_ratio
from DB_portfolio import add_alert
from mailSending import send_alert, ai_alert


def rule_volatility(returns, threshold=0.5):
    vol = returns_to_volatility(returns)
    if vol > threshold:
        msg = f'Volatility {vol:.2f} above threshold {threshold}'
        add_alert('volatility', msg)
        send_alert(f'Risk Alert: volatility', msg)
        ai_alert('volatility', msg, {'rule': 'volatility'})
        return False, msg
    return True, ''


def rule_sharpe(returns, min_sharpe=0.5):
    s = sharpe_ratio(returns)
    if s < min_sharpe:
        msg = f'Sharpe {s:.2f} below {min_sharpe}'
        add_alert('sharpe', msg)
        send_alert(f'Risk Alert: sharpe', msg)
        ai_alert('sharpe', msg, {'rule': 'sharpe'})
        return False, msg
    return True, ''


def rule_max_drawdown(cum_returns, threshold=-0.2):
    dd = max_drawdown(cum_returns)
    if dd < threshold:
        msg = f'Max Drawdown {dd:.2f} below {threshold}'
        add_alert('max_drawdown', msg)
        send_alert(f'Risk Alert: max_drawdown', msg)
        ai_alert('max_drawdown', msg, {'rule': 'max_drawdown'})
        return False, msg
    return True, ''


def rule_sortino(returns, min_sortino=0.5):
    s = sortino_ratio(returns)
    if s < min_sortino:
        msg = f'Sortino {s:.2f} below {min_sortino}'
        add_alert('sortino', msg)
        send_alert(f'Risk Alert: sortino', msg)
        ai_alert('sortino', msg, {'rule': 'sortino'})
        return False, msg
    return True, ''


def rule_beta():
    return True, ''  # abhi ke liye dummy


def rule_max_asset_weight(weights, max_weight=0.4):
    for sym, w in weights.items():
        if w > max_weight:
            msg = f'Asset {sym} weight {w:.2f} above {max_weight}'
            add_alert('max_asset_weight', msg)
            send_alert(f'Risk Alert: max_asset_weight', msg)
            ai_alert('max_asset_weight', msg, {'rule': 'max_asset_weight', 'asset': sym})
            return False, msg
    return True, ''


def run_all_rules():
    # Dummy test data (tum DB ya real data se replace kar sakte ho)
    returns = [0.01, -0.02, 0.03, 0.04, -0.01]
    cum_returns = [sum(returns[:i+1]) for i in range(len(returns))]
    weights = {"BTC": 0.5, "ETH": 0.3, "ADA": 0.2}

    results = []
    results.append(("Volatility",) + rule_volatility(returns))
    results.append(("Sharpe",) + rule_sharpe(returns))
    results.append(("Max Drawdown",) + rule_max_drawdown(cum_returns))
    results.append(("Sortino",) + rule_sortino(returns))
    results.append(("Beta",) + rule_beta())
    results.append(("Max Asset Weight",) + rule_max_asset_weight(weights))

    return results
