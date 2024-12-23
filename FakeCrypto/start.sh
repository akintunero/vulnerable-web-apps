#!/bin/bash

echo "🚀 Starting FakeCryptoX -  Crypto Wallet & Exchange"
echo "=============================================================="
exec python -m uvicorn app:app --host 0.0.0.0 --port 8000 