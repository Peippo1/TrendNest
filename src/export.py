def export_to_csv(df, path):
    df.to_csv(path, index=False)
    print(f"Data exported to {path}")