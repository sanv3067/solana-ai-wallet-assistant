# Project Details

**Name:** Solana AI Wallet Assistant

**Purpose:** Read-only dashboard for basic public Solana wallet information.

**Data sources:**
- Solana Mainnet JSON-RPC: SOL balance and recent signatures.
- CoinGecko: SOL/USD price.

**Current status:**
- [x] Streamlit dashboard
- [x] Public address input and basic Base58 format validation
- [x] SOL balance lookup
- [x] SOL/USD price lookup
- [x] SOL-only estimated value
- [x] Latest 10 transaction signatures and status
- [x] Rule-based insights
- [ ] SPL token balances
- [ ] Detailed transaction parsing
- [ ] LLM-powered explanations
- [ ] Wallet connection and signed actions
- [ ] Automated tests

**Security:** Never request or store a seed phrase or private key. The app is read-only.
