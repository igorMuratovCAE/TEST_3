import requests
import pandas as pd

# Функция для получения данных с CoinMarketCap
def fetch_cmc_data():
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=3500&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false"
    response = requests.get(url)
    return response.json()

# Функция для получения данных с SimpleSwap
def fetch_ss_data():
    url = "https://simpleswap.io/api/v3/currencies?fixed=false&includeDisabled=false"
    response = requests.get(url)
    return response.json()

# Функция для извлечения информации о монетах с CMC и их объема торгов за 24 часа
def extract_cmc_coins(cmc_data):
    cmc_coins = {
        coin["symbol"].upper(): next((q["volume24h"] for q in coin.get("quotes", []) if q.get("name") == "USD"), 0)
        for coin in cmc_data["data"]["cryptoCurrencyList"]
    }
    return cmc_coins

# Функция для извлечения списка монет с SimpleSwap
def extract_ss_coins(ss_data):
    ss_coins = {coin["ticker"].upper() for coin in ss_data}
    return ss_coins

# Функция для поиска отсутствующих на SimpleSwap монет
def find_missing_coins(cmc_coins, ss_coins):
    missing_coins = set(cmc_coins.keys()) - ss_coins
    return [(coin, cmc_coins[coin]) for coin in missing_coins if coin in cmc_coins]

# Функция для сохранения данных в Excel-файл
def save_to_excel(data, filename='Missing_coin_1000.xlsx'):
    df = pd.DataFrame(data, columns=["Coin", "Volume_24h"])
    df = df.sort_values(by='Volume_24h', ascending=False).head(1000)
    df.to_excel(filename, index=False)

# Основная функция для запуска всех этапов сбора, обработки и сохранения данных
def main():
    cmc_data = fetch_cmc_data()
    ss_data = fetch_ss_data()
    cmc_coins = extract_cmc_coins(cmc_data)
    ss_coins = extract_ss_coins(ss_data)
    missing_coin_data = find_missing_coins(cmc_coins, ss_coins)
    save_to_excel(missing_coin_data)

if __name__ == "__main__":
    main()
