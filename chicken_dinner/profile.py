from flask import (Blueprint, render_template, request, url_for, g, make_response, redirect)
from .auth import login_required
import json
from web3 import Web3, HTTPProvider
import datetime

bp = Blueprint('profile', __name__, url_prefix='/profile')


# connect to local ethereum node
web3 = Web3(HTTPProvider('http://127.0.0.1:9545'))
web3.eth.default_account = web3.eth.accounts[0]

# getting compiled contract
compiled_contract_path = 'build/contracts/EthExchange.json'
contract_address = '0x929fb1240CBB2FF4e4eDf130F95dc2f6D14D4af9'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

itemArray = []

userArray = []


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
    g.cursor.execute("SELECT Deals.*, User_From.Name AS FromName, User_To.Name AS ToName FROM Deals INNER JOIN Users AS User_From ON Deals.FromUserID = User_From.UserID INNER JOIN Users AS User_To ON Deals.ToUserID = User_To.UserID WHERE ToUserID = %s AND Status = 'PENDING'", user_id)
    dealsArray = g.cursor.fetchall()
    return dealsArray


def load_history(user_id):
    g.cursor.execute("SELECT TradeID, Date, Deals.*, User_From.Name AS FromName, User_To.Name AS ToName FROM `TradeHistory` INNER JOIN Deals ON TradeHistory.DealID = Deals.DealID INNER JOIN Users AS User_From ON Deals.FromUserID = User_From.UserID INNER JOIN Users AS User_To ON Deals.ToUserID = User_To.UserID WHERE FromUserID = %s OR ToUserID = %s", (user_id, user_id))
    tradeArray = g.cursor.fetchall()

    print(tradeArray)
    return tradeArray


def search_deal_item(idArray):
    if len(idArray) < 2:
        sql = f"SELECT * From NFT_Item WHERE ItemID = {idArray[0]}"
    else:
        sql = f"SELECT * FROM NFT_Item WHERE ItemID = {idArray[0]} OR ItemID = {idArray[1]}"

    g.cursor.execute(sql)
    fromArray = g.cursor.fetchall()

    return fromArray


@bp.route('/<int:user_id>', methods=["GET"])
@login_required
def index(user_id):
    print(user_id)
    is_own_profile = False
    if user_id == g.user["UserID"]:
        is_own_profile = True

    itemArray = load_items(user_id) 

    user = load_users(user_id)  

    dealArray = load_deal(user_id)
    dealArray = deals_handle(dealArray)

    tradeArray = load_history(user_id)
    tradeArray = deals_handle(tradeArray)

    return render_template('profile/profile.html', itemArray=itemArray, user=user, dealArray = dealArray, 
                            tradeArray=tradeArray, is_own_profile=is_own_profile)


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
    deal_id = request.form.get('getDeal')
    sql = "select * from Deals where DealID={}"
    g.cursor.execute(sql.format(deal_id))
    deal = g.cursor.fetchone()

    sender_id = deal['FromUserID']
    receiver_id = deal['ToUserID']

    sender_nfts = deal['FromNFTs'].split(',')
    receiver_nfts = deal['ToNFTs'].split(',')

    for nft_id in sender_nfts:
        sql = "UPDATE NFT_Item "
        sql += "SET UserID = {} "
        sql += "WHERE ItemID = {};"
        g.cursor.execute(sql.format(receiver_id, nft_id))

    for nft_id in receiver_nfts:
        sql = "UPDATE NFT_Item "
        sql += "SET UserID = {} "
        sql += "WHERE ItemID = {};"
        g.cursor.execute(sql.format(sender_id, nft_id))

    sql = "UPDATE Deals SET Status=(%s) WHERE DealID=(%s)"
    g.cursor.execute(sql, ("COMPLETE", deal["DealID"]))

    sql = "INSERT INTO TradeHistory (DealID, Date) VALUES (%s, %s)"
    g.cursor.execute(sql, (deal["DealID"], datetime.datetime.now()))
    g.conn.commit()

    return ''

    global contract
    contract.functions.Deposit(web3.eth.accounts[7], 3).call()
    contract.functions.ExchangeETH(
            web3.eth.accounts[3],
            web3.eth.accounts[7],
            1
            ).call()
    
    


@bp.route("/deal-decline", methods=["POST"])
def deal_decline():
    deal_id = request.form.get('getDeal')
    sql = "UPDATE Deals "
    sql += "SET Status='ARCHIVED' "
    sql += "WHERE DealID={};"
    g.cursor.execute(sql.format(str(deal_id)))
    g.conn.commit()
    return ''
