from polygon import RESTClient
import pandas as pd   
import datetime

# api_key = "xP7p1WfWdpaQqjFzFW6eOQfjMga2t4Pl"
# symbol = "C:EURUSD"

# client = RESTClient(api_key,trace=True)
# response = client.get_aggs(
#     ticker=symbol,
#     multiplier=1,
#     timespan="minute",
#     from_="2022-01-01",
#     to="2024-07-16",
#     limit=50000  # Set a high limit to ensure all data points are fetched
# )

api_key = "xP7p1WfWdpaQqjFzFW6eOQfjMga2t4Pl"
symbol = "C:EURUSD"
start_date = datetime.datetime(2003, 5, 5)
end_date = datetime.datetime(2023, 10, 16)
# start_date = "2003-05-05"
# end_date= "2023-10-16"
candle_bartime = 1
candle_timespan = "minute"

def get_data(symbol:str, start_date, end_date, api_key:str, candle_bar_multiplier:int, candle_bar_timespan:str)->pd.DataFrame:
    """_summary_
    limit is set to 50000 to get all the data points because the default limit is 50000 in free service of polygon.io
    Args:
        symbol (_string_): _description_
        start_date (_datetime.datetime_): _description_
        end_date (_datetime.datetime_): _description_
        api_key (_string_): _description_
        candle_bar_multiplier (_integer_): _description_
        candle_bar_timespan (_string_): _description_

    Returns:
        _Dataframe_: returns dataframe with setting the 'Date' as index depending on the timespan
        while returing the dataframe it will drop the timestamp column
        it will print two lines of information
        1. Modified columns names 
        2. The data is set with Date as index or Time as index
    """
    client = RESTClient(api_key)
    response = client.get_aggs(
        ticker=symbol,
        multiplier=candle_bar_multiplier,
        timespan=candle_bar_timespan,
        from_=start_date.strftime("%Y-%m-%d"),
        to=end_date.strftime("%Y-%m-%d"),
        limit=50000  # Set a high limit to ensure all data points are fetched
    )
    #print(response)
    # Convert response to a DataFrame
 
    df = pd.DataFrame(response)
    if df.empty:
        print("Dataframe is empty")
        exit()
    #print(df.columns)
    # Convert the timestamp to a readable date format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['Date']= df['timestamp'].dt.strftime('%Y-%m-%d')
    df['Time']= df['timestamp'].dt.strftime('%H:%M:%S')
    # # Rename columns for convenience
    df = standardize_column_names(df)
    
    # # # Set the timestamp as the index
    # if candle_bar_timespan in ['day','week','month']:
    #     df.set_index('Date', inplace=True)
    #     print("The data is set with Date as index")
    # else:
    #     df.set_index('Time', inplace=True)
    #     print("The data is set with Time as index")
    # df_modified = df.drop(columns=['timestamp'])
    #  return df_modified
    return df

def standardize_column_names(df:pd.DataFrame)->pd.DataFrame:
        """_summary_
            It standardizes the column names to Open,High,Low,Close,Volume,Transactions 
            for any other variants you can add the requirements in the column_mapping dictionary
        Args:
            df (pd.DataFrame): _description_

        Returns:
            _pd.DataFrame_: _description_
        """
        column_mapping = {
        'Open': ['o', 'OPEN', 'open', 'O'],
        'Close': ['c', 'CLOSE', 'close', 'C'],
        'High': ['h', 'HIGH', 'high', 'H'],
        'Low': ['l', 'LOW', 'low', 'L'],
        'Volume': ['v', 'VOLUME', 'volume', 'V'],
        # Add more mappings if needed
        }
        for standarised_name, variants in column_mapping.items():
            for variant in variants:
                if variant in df.columns:
                    df.rename(columns={variant: standarised_name}, inplace=True)
        print("Columns are standarised-> Open,High,Low,Close,Volume")
        return df

df=get_data(symbol, start_date, end_date, api_key, candle_bartime, candle_timespan)

if df.empty:
    print("Dataframe is empty check the data or the date range is not correct")
    exit()
df.to_csv("EURUSD_1_minute.csv",index=False)