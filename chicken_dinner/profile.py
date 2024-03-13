from flask import (Blueprint, render_template, request, url_for, g, make_response, redirect)
from .auth import login_required
import json
from web3 import Web3, HTTPProvider

bp = Blueprint('profile', __name__, url_prefix='/profile')

<<<<<<< HEAD

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

itemArray = []

userArray = []

=======
>>>>>>> dea844d16ac7dedcd72f36b35b2d7a4bad0cbab9

def load_items(user_id):
    print("fetching")
    g.cursor.execute("SELECT * FROM NFT_Item WHERE UserID = %s", (user_id,))
    itemArray = g.cursor.fetchall()
    return itemArray


def load_users(user_id):
    g.cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
    userArray = g.cursor.fetchone()
    return userArray


def load_deal(user_id):
    g.cursor.execute("SELECT Deals.*, User_From.Name AS FromName, User_To.Name AS ToName FROM Deals INNER JOIN Users AS User_From ON Deals.FromUserID = User_From.UserID INNER JOIN Users AS User_To ON Deals.ToUserID = User_To.UserID WHERE ToUserID = %s", user_id)
    dealsArray = g.cursor.fetchall()
    return dealsArray


def search_deal_item(idArray):
    if len(idArray) < 2:
        sql = f"SELECT * From NFT_Item WHERE ItemID = {idArray[0]}"
    else:
        sql = f"SELECT * FROM NFT_Item WHERE ItemID = {idArray[0]} OR ItemID = {idArray[1]}"

    g.cursor.execute(sql)
    fromArray = g.cursor.fetchall()

    return fromArray


eth1 = {
        "plus": "+ 2.3ETH"
}

eth2 = {
        "plus": "+ 6.9ETH"
}

eth3 = {
        "plus": "+ 8.12ETH"
}

ethArray = [eth1, eth2, eth3]

trade_info = {
    "hash": "0xdC0b8cA898DB8D46A37517d70E63985ABA1FaF0B",
    "block": "hong biet cai nay =))",
}

trade_infoArray = [trade_info]


@bp.route('/<int:user_id>', methods=["GET"])
@login_required
def index(user_id):
    print(user_id)
    is_own_profile = False
    if user_id == g.user["UserID"]:
        is_own_profile = True

<<<<<<< HEAD
    itemArray = load_items(user_id)
    user = load_users(user_id)
=======
    itemArray = load_items(user_id) 
    print(itemArray)
    user = load_users(user_id)   
>>>>>>> dea844d16ac7dedcd72f36b35b2d7a4bad0cbab9
    dealArray = load_deal(user_id)

    dealArray = deals_handle(dealArray)

    return render_template('profile/profile.html', itemArray=itemArray, user=user, dealArray = dealArray, 
                           ethArray=ethArray, trade_infoArray=trade_infoArray, is_own_profile=is_own_profile)


def deals_handle(dealArray):
    for deal in dealArray:
        deal["FromNFTs"] = deal["FromNFTs"].split(",")
        deal["ToNFTs"] = deal["ToNFTs"].split(",")

        deal["FromNFTs"] = search_deal_item(deal["FromNFTs"])
        deal["ToNFTs"] = search_deal_item(deal["ToNFTs"])

    return dealArray


@bp.route('/redirect/<int:item_id>')
def lol(item_id):
    url = url_for('buy.index', item_id=item_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response


@bp.route("/deal-accept", methods=["POST"])
def deal_accept():
    deal = request.form.get('getDeal')
    print(deal)
    global contract
    contract.functions.Deposit(web3.eth.accounts[2], 2).call()
    contract.functions.ExchangeETH(
            web3.eth.accounts[2],
            web3.eth.accounts[4],
            2
            ).call()

    print(web3.eth.get_balance(web3.eth.accounts[2]))


@bp.route("/deal-decline", methods=["POST"])
def deal_decline():
    deal = request.form.get('getDeal')
    print(deal)
