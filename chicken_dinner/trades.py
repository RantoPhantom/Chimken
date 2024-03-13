from flask import (Blueprint, render_template, redirect, flash, request, url_for, g)
import json
from web3 import Web3, HTTPProvider

bp = Blueprint('trades', __name__, url_prefix='/trades')

# connect to local ethereum node
web3 = Web3(HTTPProvider('http://127.0.0.1:9545'))
web3.eth.default_account = web3.eth.accounts[0]

# getting compiled contract
compiled_contract_path = 'build/contracts/EthExchange.json'
contract_address = '0x7eF5B70AFB8dB7138fb6082727C89fAD5C19eA7B'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address=contract_address, abi=contract_abi)


@bp.route('/<int:item_id>', methods=["GET"])
def index(item_id):
    sql = "SELECT ItemID, NFT_Item.Name, Users.Name, Price FROM NFT_Item INNER JOIN Users ON NFT_Item.UserID = Users.UserID WHERE ItemID = %s"
    g.cursor.execute(sql, (item_id))
    item = g.cursor.fetchone()

    sql = "SELECT * FROM NFT_Item WHERE UserID = %s"
    g.cursor.execute(sql, (g.user["UserID"]))
    itemArray = g.cursor.fetchall()

    return render_template('trades/trades.html', item=item, itemArray=itemArray)


@bp.route('/<int:item_id>', methods=('GET', 'POST'))
def get_data(item_id):
    if request.method == 'POST':
        tradeList = request.form.getlist('trades-item')
        if len(tradeList) > 2:
            flash("More than two NFTs selected", "limit")
            return redirect(url_for('trades.index', item_id=item_id))
        elif len(tradeList) == 0:
            flash("No NFT selected", "limit")
            return redirect(url_for('trades.index', item_id=item_id))

        addEth = request.form['add-eth']
        reqEth = request.form['req-eth']

        global contract
        contract.functions.Deposit(web3.eth.accounts[2], 2).call()
        contract.functions.ExchangeETH(
                web3.eth.accounts[2],
                web3.eth.accounts[4],
                2
                ).call()

        print(web3.eth.get_balance(web3.eth.accounts[2]))

    return redirect(url_for('market.index'))
