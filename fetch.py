import functions as fn             
import Imports

if __name__ == "__main__":
    api_key = "xP7p1WfWdpaQqjFzFW6eOQfjMga2t4Pl"
    symbol = "C:EURUSD"
    start_date = Imports.datetime.datetime(2003, 5, 5)
    end_date = Imports.datetime.datetime(2024, 10, 16)
    candle_bartime = 4
    candle_timespan = "hour"
    
#     df = fn.get_data(symbol, start_date, end_date, api_key, candle_bartime, candle_timespan)
    
#     if df.empty:
#         print("Dataframe is empty check the data or the date range is not correct")
#         exit()
#     else:
#         print(df.head())  # Print the first few rows of the dataframe to verify the data
#         fn.to_save_file_with_proper_details(df,symbol,start_date,end_date,candle_bartime,candle_timespan)


    import requests  # Assuming requests is used to make API calls

    response = requests.get("https://api.polygon.io/v2/aggs/ticker/C:EURUSD/range/{}/{}/{}/{}?apiKey={}".format(
        candle_bartime, candle_timespan, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), api_key
    ))
    print(response.url)
    print(response.json())  # This prints the API response in JSON format
