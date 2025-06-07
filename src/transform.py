def clean_data(df):
    # Example transformation: drop nulls and sort by date
    df_clean = df.dropna()
    if 'date' in df_clean.columns:
        df_clean = df_clean.sort_values(by='date')
    print("Data cleaned and sorted")
    return df_clean