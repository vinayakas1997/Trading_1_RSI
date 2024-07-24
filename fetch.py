import functions as fn             
import Imports
from polygon import RESTClient

if __name__ == "__main__":
    api_key = "xP7p1WfWdpaQqjFzFW6eOQfjMga2t4Pl"
    symbol = "C:EURUSD"
    start_date = Imports.datetime.datetime(2003, 5, 5)
    end_date = Imports.datetime.datetime(2023, 10, 16)
    # start_date = "2003-05-05"
    # end_date= "2023-10-16"
    candle_bartime = 4
    candle_timespan = "hour"
    
    from_=start_date.strftime("%Y-%m-%d")
    to=end_date.strftime("%Y-%m-%d")
    
    print(f"Startdate: {from_} Enddate: {to}")
    
    client = RESTClient(api_key=api_key,trace=True)
    ticker = "AAPL"

# List Aggregates (Bars)
    aggs = []
    for a in client.list_aggs(ticker=ticker, multiplier=5, timespan="minute", from_="2003-05-05", to="2024-7-16", limit=50000):
        aggs.append(a)


    #print(aggs)
    df = Imports.pd.DataFrame(aggs)
    print(len(df))
    df['timestamp'] = Imports.pd.to_datetime(df['timestamp'], unit='ms')
    df['Date']= df['timestamp'].dt.strftime('%Y-%m-%d')
    df.to_csv("EURUSD_2003-05-05_2023-10-16_4_minute.csv",index=False)
    #print(f"Startdate: {start_date} Enddate: {end_date}")
    # df = fn.get_data(symbol, start_date, end_date, api_key, candle_bartime, candle_timespan)
    
    # if df.empty:
    #     print("Dataframe is empty check the data or the date range is not correct")
    #     exit()
    # else:
    #     print(df.head())  # Print the first few rows of the dataframe to verify the data
    #     fn.to_save_file_with_proper_details(df,symbol,start_date,end_date,candle_bartime,candle_timespan)


    # import requests  # Assuming requests is used to make API calls

    # response = requests.get("https://api.polygon.io/v2/aggs/ticker/C:EURUSD/range/{}/{}/{}/{}?apiKey={}".format(
    #     candle_bartime, candle_timespan, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), api_key
    # ))
    # print(response.url)
    # print(response.json())  # This prints the API response in JSON format
