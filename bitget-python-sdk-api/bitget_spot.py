import bitget.v1.mix.order_api as maxOrderApi
import bitget.bitget_api as baseApi 
from bitget.exceptions import BitgetAPIException
import time

# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# import logging
# 获取账户资产
def get_account_assets(baseApiInstance, coin, asset_type="hold_only"):
    try:
        params = {
            "coin": coin,
            "assetType": asset_type
        }
        response = baseApiInstance.get("/api/v2/spot/account/assets", params)
        print("Account assets:", response)
        total = response['data'][0]['available']
        return total
    except BitgetAPIException as e:
        print("Error fetching account assets:", e.message)
        return None

# 获取交易对信息
def get_symbol_info(baseApiInstance, symbol):
    try:
        params = {"symbol": symbol}
        response = baseApiInstance.get("/api/v2/spot/public/symbols", params)
        print("Symbol info:", response)
        quantity_precision = response['data'][0]['quantityPrecision']
        min_trade_usdt = response['data'][0]['minTradeUSDT']
        return quantity_precision, min_trade_usdt
    except BitgetAPIException as e:
        print("Error fetching symbol info:", e.message)
        return None, None

# 下单函数
def place_order(baseApiInstance, symbol, side, order_type, price, size, client_oid):
    try:
        params = {
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "force": "gtc",
            "price": price,
            "size": size,
            "clientOid": client_oid
        }
        response = baseApiInstance.post("/api/v2/spot/trade/place-order", params)
        print("Place order response:", response)
        return response
    except BitgetAPIException as e:
        print("Error placing order:", e.message)
        return None

# 取消订单
def cancel_order(baseApiInstance, symbol, client_oid):
    try:
        params = {
            "symbol": symbol,
            "clientOid": client_oid
        }
        response = baseApiInstance.post("/api/v2/spot/trade/cancel-order", params)
        print("Cancel order response:", response)
        return response
    except BitgetAPIException as e:
        print("Error canceling order:", e.message)
        return None

# 主执行函数
def execute_trading(data , symbol, clientOid,limit , status):
    for key, value in data.items():
        print(f"Config Name: {key}")
        apiKey = value['apiKey']
        secretKey = value['secretKey']
        passphrase = value['passphrase']
        
        # 初始化 API 客户端
        baseApiInstance = baseApi.BitgetApi(apiKey, secretKey, passphrase)
        
        # 获取交易对信息
        symbol = "PEAQUSDT"
        coin = "PEAQ"
        clientOid = 2
        limit = "0.3"
        
        quantityPrecision, minTradeUSDT = get_symbol_info(baseApiInstance, symbol)
        if quantityPrecision is None or minTradeUSDT is None:
            continue
        
        # 获取账户资产
        total = get_account_assets(baseApiInstance, coin)
        if total is None:
            continue
        
        # 修正 total 保留小数点后 quantityPrecision 位
        total = total[:total.find('.') + int(quantityPrecision) + 1]
        
        
        if float(total) > float(minTradeUSDT) and status==1:
            place_order(baseApiInstance, symbol, "sell", "limit", limit, total, clientOid)
        if        status==2:  
            # 取消订单
            cancel_order(baseApiInstance, symbol, clientOid)
        print("-" * 30)  # 分隔符


if __name__ == '__main__':
    data = {
        "account": {
            "apiKey": "",
            "secretKey": "",
            "passphrase": ""
        }
    }
        
    # 获取交易对信息
    symbol = "PEAQUSDT"
    coin = "PEAQ"
    clientOid = 2
    limit = "0.3"
    status=1 # 1 下单， 2 取消订单
    execute_trading(data , symbol, clientOid,limit,status)

    # # 执行交易
    # while True:
    #     execute_trading(data , symbol, clientOid,limit,status)
    #     # 延迟 1.5 小时 (1.5 小时 = 90 分钟 = 5400 秒)
    #     time.sleep(5400)        