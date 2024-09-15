import numpy as np


def Medal(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal['total'] = medal['Gold'] + medal['Silver'] + medal['Bronze']

    medal['Gold'] = medal['Gold'].astype(int)
    medal['Silver'] = medal['Silver'].astype(int)
    medal['Bronze'] = medal['Bronze'].astype(int)
    medal['total'] = medal['total'].astype(int)

    return medal


def country_year_list(df_merge):
    years = df_merge.Year.unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df_merge['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def fetch_year_country(df_merge, year, country):
    medal_df = df_merge.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year != 'Overall' and country != 'Overall':
        # Correct usage with parentheses
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['total'] = x['total'].astype(int)

    return x


def Data_Over_Time(df_merge, col):

    nations_Over_Time = df_merge.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(
        'Year')
    nations_Over_Time.rename(columns={'Year' : 'Edition', 'count' : col}, inplace=True)
    return nations_Over_Time


def top_Performance(df, sport):
    # Filter out rows where the 'Medal' column is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if a specific sport is requested
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Calculate the medal count for each athlete
    top_performers = temp_df['Name'].value_counts().reset_index()
    top_performers.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge to get additional information (Sport and Region)
    merged_df = top_performers.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates(
        subset=['Name'])

    return merged_df.head(25)

def YearWise_medal_Tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_Heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_country(df, country):
    # Filter out rows where the 'Medal' column is NaN
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Calculate the medal count for each athlete
    top_performers = temp_df['Name'].value_counts().reset_index()
    top_performers.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge to get additional information (Sport and Region)
    merged_df = top_performers.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates(
        subset=['Name']).head(10)

    return merged_df


def Weight_vs_Height(df, Sport):
    athlete_df = df.drop_duplicates(subset=['Name'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if Sport != 'Overall':
        tempp = athlete_df[athlete_df["Sport"] == Sport]
        return tempp
    else:
        return athlete_df


def mens_vs_womens(df):
    athlete_df = df.drop_duplicates(subset=['Name'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')

    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
