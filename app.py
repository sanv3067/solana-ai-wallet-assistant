import streamlit as st
import requests
from datetime import datetime

# PAGE CONFIG
st.set_page_config(
    page_title="Solana AI Wallet Assistant",
    page_icon="🚀",
    layout="wide"
)

RPC_URL = "https://api.mainnet-beta.solana.com"

# SOLANA RPC
def solana_rpc(method, params):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }

    response = requests.post(
        RPC_URL,
        json=payload,
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise ValueError(data["error"]["message"])

    return data["result"]


# WALLET VALIDATION
def valid_wallet(address):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    if not 32 <= len(address) <= 44:
        return False

    if any(c not in alphabet for c in address):
        return False

    number = 0

    for char in address:
        number = number * 58 + alphabet.index(char)

    decoded = (
        number.to_bytes((number.bit_length() + 7) // 8, "big")
        if number else b""
    )

    leading = len(address) - len(address.lstrip("1"))
    decoded = b"\x00" * leading + decoded

    return len(decoded) == 32


# SOL PRICE
def get_sol_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    return response.json()["solana"]["usd"]


# CUSTOM DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #080d20;
    color: white;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0756b5, #142d75);
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #287bff;
}

div[data-testid="stMetricValue"] {
    color: white;
}

</style>
""", unsafe_allow_html=True)


# MAIN TITLE
st.title("🚀 Solana AI Wallet Assistant")

st.write("Your simple Solana wallet monitoring dashboard")

st.info(
    "Network: Solana Mainnet | Read-only wallet monitoring"
)


# WALLET INPUT
wallet = st.text_input(
    "Enter Solana Public Wallet Address",
    placeholder="Paste your public wallet address"
)

check = st.button(
    "🔍 Check My Wallet",
    type="primary"
)


# WALLET CHECK
if check:

    wallet = wallet.strip()

    if not valid_wallet(wallet):

        st.error("Please enter a valid Solana public address.")

    else:

        try:

            with st.spinner("Checking your wallet..."):

                # GET BALANCE
                balance_data = solana_rpc(
                    "getBalance",
                    [wallet]
                )

                sol = balance_data["value"] / 1_000_000_000

                # GET PRICE
                try:
                    price = get_sol_price()
                    price_available = True
                except requests.RequestException:
                    price = None
                    price_available = False

                # GET TRANSACTIONS
                transactions = solana_rpc(
                    "getSignaturesForAddress",
                    [wallet, {"limit": 10}]
                )

            st.success("Wallet information retrieved!")

            # WALLET OVERVIEW
            st.subheader("💰 Wallet Overview")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "SOL Balance",
                f"{sol:.6f} SOL"
            )

            if price_available:

                col2.metric(
                    "SOL Price",
                    f"${price:,.2f}"
                )

                col3.metric(
                    "Estimated SOL Value",
                    f"${sol * price:,.2f}"
                )

            else:

                col2.metric("SOL Price", "Unavailable")
                col3.metric("Estimated SOL Value", "Unavailable")

            st.caption(
                "Estimated value includes SOL balance only, not other tokens."
            )

            st.divider()

            # AI WALLET ASSISTANT
            st.subheader("🤖 AI Wallet Assistant")

            if sol == 0:

                st.warning(
                    "Your SOL balance is 0. "
                    "No SOL balance was found."
                )

            elif sol < 0.1:

                st.warning(
                    "Your SOL balance is low. "
                    "Keep some SOL available for transaction fees."
                )

            else:

                st.success(
                    f"Your wallet holds {sol:.6f} SOL."
                )

            # TRANSACTION STATISTICS
            successful = sum(
                1 for tx in transactions
                if tx.get("err") is None
            )

            failed = len(transactions) - successful

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Recent Transactions",
                len(transactions)
            )

            col2.metric(
                "Successful",
                successful
            )

            col3.metric(
                "Failed",
                failed
            )

            if failed == 0:
                st.info(
                    "No failed transactions found in the retrieved recent history."
                )
            else:
                st.warning(
                    f"{failed} failed transaction(s) found."
                )

            st.caption(
                "Insights are rule-based, not AI-generated financial advice."
            )

            st.divider()

            # TRANSACTION HISTORY
            st.subheader("📜 Recent Transaction History")

            if not transactions:

                st.info("No recent transactions found.")

            else:

                for index, tx in enumerate(transactions, 1):

                    signature = tx["signature"]

                    status = (
                        "Success"
                        if tx.get("err") is None
                        else "Failed"
                    )

                    with st.expander(
                        f"Transaction {index} - {status}"
                    ):

                        st.write("Signature:")
                        st.code(signature)

                        block_time = tx.get("blockTime")

                        if block_time:

                            date = datetime.fromtimestamp(
                                block_time
                            )

                            st.write(
                                "Date:",
                                date.strftime("%d-%m-%Y %H:%M:%S")
                            )

                        else:
                            st.write("Date: Not available")

                        st.write("Status:", status)

                        st.markdown(
                            f"[View Transaction on Solscan](https://solscan.io/tx/{signature})"
                        )

            st.divider()

            # WALLET EXPLORER
            st.subheader("🔎 Wallet Explorer")

            st.markdown(
                f"[Open Wallet on Solscan](https://solscan.io/account/{wallet})"
            )

        except requests.RequestException as error:

            st.error(f"Network Error: {error}")

        except (ValueError, KeyError, TypeError) as error:

            st.error(f"Wallet / Data Error: {error}")


# FOOTER
st.divider()

st.caption(
    "🚀 Solana AI Wallet Assistant | Hackathon Project"
)

st.caption(
    "Read-only application. Never enter your seed phrase or private key."
)
