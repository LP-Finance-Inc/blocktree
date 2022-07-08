import requests
import time


class BlockTree:
    def __init__(self):
        pass

    # Fetch Price from Jupiter Aggregator
    def get_price(self, token: str):
        price_url = f"https://price.jup.ag/v1/price?id={token}&vsToken=USDC"
        price_data = requests.get(price_url).json()
        price = price_data["data"]["price"]
        return price

    # Fetch Token Holdings of Account from solscan api
    def get_tokens(self, account: str):
        # Request URL
        token_url = "https://public-api.solscan.io/account/tokens?account=EN2CV9nCnH9nBF9GyGYG9B3haNriNBkrPo8jF4c6mzUi"

        # Request
        """
        [
            {
                "tokenAddress": str, // Address of token
                "tokenAmount": {
                    "amount": str, // Amount of token
                    "decimals": int,
                    "uiAmount": int,
                    "uiAmountString": str
                },
            "tokenAccount": str, // User's token account
            "tokenName": str, // Token name
            "tokenIcon": str, // Token img uri
            "rentEpoch": int,
            "lamports": int,
            "tokenSymbol": str // Token symbol
            }
        ]
        """
        tokens = requests.get(token_url).json()

        # Store array of token holding data
        token_data = []
        for token in tokens:
            # If one of token data does not exist, do not add
            try:
                token_address = token["tokenAddress"]
                token_decimal = token["tokenAmount"]["decimals"]
                token_amount = float(token["tokenAmount"]["amount"]) / (
                    10**token_decimal
                )  # str -> decimal
                token_account = token["tokenAccount"]
                token_symbol = token["tokenSymbol"]
                token_img = token["tokenIcon"]
                # Fetch Price and Calculate Token Value
                token_price = self.get_price(token_symbol)
                token_value = token_price * token_amount
                # Only add if token value > 0
                if token_value > 0:
                    sub = {
                        "tokenAddress": token_address,
                        "tokenAmount": token_amount,
                        "tokenAccount": token_account,
                        "tokenSymbol": token_symbol,
                        "tokenImg": token_img,
                        "tokenValue": token_value,
                    }
                    token_data.append(sub)
                else:
                    pass
            except:
                pass
        return token_data

    # Fetch SPL Transctions of Account from solscan api
    def get_spl_tx(self, account: str):
        spl_url = f"https://public-api.solscan.io/account/splTransfers?account={account}&offset=0&limit=100"
        """
        {
            "data": [
                "address": str,
                "changeAmount": int,
                "decimals": int,
                "tokenAddress": str,
                "symbol": str,
                "blockTime": int,
            ]
        }
        """
        spl_tx = requests.get(spl_url).json()

        spl_data = []
        for tx in spl_tx["data"]:
            try:
                address = tx["address"]
                decimal = tx["decimals"]
                amount = tx["changeAmount"] / (10**decimal)
                token_address = tx["tokenAddress"]
                token_symbol = tx["symbol"]
                block_time = tx["blockTime"]
                tx_time = time.ctime(block_time)

                sub = {
                    "address": address,
                    "amount": amount,
                    "tokenAddress": token_address,
                    "tokenSymbol": token_symbol,
                    "time": tx_time,
                    "blockTime": block_time,
                }
                spl_data.append(sub)
            except:
                pass
        return spl_data

    # Fetch SOL Transactions of Account from solscan api
    def get_sol_tx(self, account: str):
        sol_url = f"https://public-api.solscan.io/account/solTransfers?account={account}&offset=0&limit=100"
        """
        {
            "data": [
                "src": str,
                "dst": str,
                "lamport": int,
                "blockTime": int,
                "txHash": str,
                "decimals": int
            ]
        }
        """
        sol_tx = requests.get(sol_url).json()

        sol_data = []
        for tx in sol_tx["data"]:
            try:
                address = tx["dst"]
                decimal = tx["decimals"]
                amount = tx["lamport"] / (10**decimal)
                block_time = tx["blockTime"]
                tx_time = time.ctime(block_time)

                sub = {
                    "address": address,
                    "amount": amount,
                    "tokenAddress": "So11111111111111111111111111111111111111112",
                    "tokenSymbol": "SOL",
                    "time": tx_time,
                    "blockTime": block_time,
                }
                sol_data.append(sub)
            except:
                pass

        return sol_data

    # Merge SOL & SPL Transcations of Account
    def get_total_tx(self, account: str, lim: int):
        spl_tx = self.get_spl_tx(account)
        sol_tx = self.get_sol_tx(account)

        temp = {}
        for i in spl_tx + sol_tx:
            temp[str(i["blockTime"])] = i

        index_temp = [i["blockTime"] for i in spl_tx + sol_tx]
        index_temp.sort()
        index_temp = index_temp[-lim - 1 : -1]

        tx_data = []
        for i in index_temp:
            data = temp[str(i)]
            tx_data.append(data)
        return tx_data
