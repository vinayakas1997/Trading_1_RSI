# Here all the functions wilkl be saved in functions.py

import Imports 



def get_data(symbol:str, start_date, end_date, api_key:str, candle_bar_multiplier:int, candle_bar_timespan:str)->Imports.pd.DataFrame:
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
    client = Imports.RESTClient(api_key)
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
 
    df = Imports.pd.DataFrame(response)
    if df.empty:
        print("Dataframe is empty")
        exit()
    #print(df.columns)
    # Convert the timestamp to a readable date format
    df['timestamp'] = Imports.pd.to_datetime(df['timestamp'], unit='ms')
    df['Date']= df['timestamp'].dt.strftime('%Y-%m-%d')
    df['Time']= df['timestamp'].dt.strftime('%H:%M:%S')
    # # Rename columns for convenience
    df = standardize_column_names(df)
    
    # # Set the timestamp as the index
    if candle_bar_timespan in ['day','week','month']:
        df.set_index('Date', inplace=True)
        print("The data is set with Date as index")
    else:
        df.set_index('Time', inplace=True)
        print("The data is set with Time as index")
    df_modified = df.drop(columns=['timestamp'])
    return df_modified

def standardize_column_names(df:Imports.pd.DataFrame)->Imports.pd.DataFrame:
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




def to_save_file_with_proper_details(df:Imports.pd.DataFrame,symbol:str,start_date,end_date,cnadle_bartime:int,candles_timespan:str)->None:
    """_summary_
    Args:
        df (pd.DataFrame): data to be stored in csv
        symbol (str): Actual symbol of the stocks 
        start_date (_type_): it can be string or datetime.datetime format 
        end_date (_type_): it can be string or datetime.datetime format
        cnadle_bartime (_type_): integer 
        candles_timespan (_type_): string
    """
    df.to_csv(f'{symbol}_{start_date.date()}_{end_date.date()}_{cnadle_bartime}_{candles_timespan}.csv')
    print(f"Data is saved in {symbol}_{start_date.date()}_{end_date.date()}_{cnadle_bartime}_{candles_timespan}.csv")
    
    
def to_confirm_ticker_polygon(symbol_to_check:str)->bool:
    """_summary_
    I have downloaded the ticker of date (YYYY-MM-DD)->2023-01-13 
    from polygon.io   
    Args:
        symbol_to_check (str): here teh user will input the synbol to confirm.
    Returns:
        bool: True if the symbol is present in the list of tickers
    """
    tickers =  Imports.pd.read_csv("Ticker_list.csv")
    print(tickers.head())
    return False 
    # if symbol_to_check in ti:

def any_empty_data_check(df:Imports.pd.DataFrame)->Imports.pd.DataFrame:
    """_summary_
    This function will check if there is any empty data in the dataframe
    Args:
        df (pd.DataFrame): _description_

    Returns:
        _pd.DataFrame_: _description_
    """
    locations = df[df.High==df.Low].index.tolist()
    return locations 
    
if __name__ == "__main__":
    symbol = "AAPL"
    if to_confirm_ticker_polygon(symbol):
        print(f"{symbol} is present in the list of tickers")
    else:
        print(f"{symbol} is not present in the list of tickers")