## Hyperliquid Market Maker (Python)

A clean, extensible async market-making bot scaffold targeting Hyperliquid perps. Includes:

- Paper-trading mode (no external deps) to validate logic locally
- Pluggable live exchange adapter for Hyperliquid SDK
- Config via env vars or CLI
- Quote management (re-quote on mid changes), inventory-aware skewing
- Graceful shutdown and cancel-on-exit

### Quick start (paper mode)

```bash
python3 -m pip install --user --upgrade pip
python3 src/run_maker.py --paper --asset BTC --size 0.001 --spread-bps 10
```

Paper mode runs without the Hyperliquid SDK. It simulates a mid-price that randomly walks and logs orders you would place.

### Live mode (Hyperliquid)

1) Create and activate a virtualenv (recommended):

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

If your system blocks venv creation, install your platform's venv package (e.g., `apt install python3-venv`) or use your preferred environment tool.

2) Set credentials via env vars or a `.env` file (see `.env.example`):

```
HYPERLIQUID_NETWORK=testnet
HL_ACCOUNT_ADDRESS=0xYourPublicKey
HL_PRIVATE_KEY=0xYourPrivateKey
```

3) Run:

```bash
python src/run_maker.py --asset BTC --size 0.001 --spread-bps 10 --update-interval 1.0
```

Notes:
- This repository wires a `HyperliquidExchange` adapter but intentionally keeps the minimal SDK calls guarded to avoid runtime errors if the SDK is missing. You may need to adjust import paths/types to match the SDK’s current version.
- Start on testnet. Understand the risks before using mainnet.

### Configuration

You can configure via CLI flags or environment variables:

- `HYPERLIQUID_NETWORK` (default: `testnet`) – network selection
- `HL_ACCOUNT_ADDRESS` – your public address
- `HL_PRIVATE_KEY` – your private key or API key with order permissions
- `QUOTE_SIZE` – default order size
- `QUOTE_SPREAD_BPS` – quoted half-spread in basis points
- `QUOTE_SKEW_BPS_PER_UNIT` – inventory skew per inventory unit in bps
- `RISK_MAX_POSITION` – absolute max position size (in base units)

See `src/hlmm/config.py` for full details.

### Project structure

```
src/
  hlmm/
    __init__.py
    config.py
    exchange_paper.py
    exchange_hyperliquid.py
    maker.py
    risk.py
    strategy.py
    utils.py
    logging_config.py
  run_maker.py
```

### Disclaimer

This code is a starting point. Market making is risky. You are responsible for testing, monitoring, and complying with exchange rules and local laws. Use at your own risk.

# HL