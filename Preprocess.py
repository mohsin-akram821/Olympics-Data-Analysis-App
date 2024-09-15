import pandas as pd

def preprocess(df, region_df):

    # Filter for Summer Olympics
    df_with_summer = df[df['Season'] == 'Summer']

    # Merge with custom suffixes
    df_merge = df_with_summer.merge(region_df, on='NOC', how='left')

    # Drop any duplicates
    df_merge.drop_duplicates(inplace=True)

    # One-hot encode the 'Medal' column
    df_concat = pd.concat([df_merge, pd.get_dummies(df_merge['Medal'])], axis=1)

    return df_concat
