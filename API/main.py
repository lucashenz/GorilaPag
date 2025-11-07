from fastapi import FastAPI
from web3 import Web3
import json, os

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

with open("abi.json") as f:
    ABI = json.load(f)

CONTRACT_ADDRESS = "0x123..."
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

PRIVATE_KEY = os.getenv("PLATFORM_KEY")
platform = w3.eth.account.from_key(PRIVATE_KEY)

app = FastAPI()

@app.post("/payment/create")
def create_payment(id: int, amount: int, token: str):
    tx = contract.functions.createPayment(id, amount, token).build_transaction({
        "from": platform.address,
        "nonce": w3.eth.get_transaction_count(platform.address),
        "gas": 300000,
        "gasPrice": w3.eth.gas_price
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return {"tx": tx_hash.hex()}
