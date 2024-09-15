import streamlit as st
import pandas as pd
import Preprocess
import Helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df_merge = Preprocess.preprocess(df, region_df)

# Sidebar content
st.sidebar.title("Olympics Analysis")  # Main title
st.sidebar.markdown("#### By Mohsin Akram")  # Subheading for the author's name
st.sidebar.image("https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png")

user_menu = st.sidebar.radio(
    'Select one option please:',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = Helper.country_year_list(df_merge)

    Selected_Year = st.sidebar.selectbox("Select Year", years)
    Selected_Country = st.sidebar.selectbox("Select Country", country)

    data = Helper.fetch_year_country(df_merge, Selected_Year, Selected_Country)
    if Selected_Year == 'Overall' and Selected_Country == 'Overall':
        st.title("Overall Tally")
    if Selected_Year != 'Overall' and Selected_Country == 'Overall':
        st.title("Overall Tally in " + str(Selected_Year))
    if Selected_Year == 'Overall' and Selected_Country != 'Overall':
        st.title(Selected_Country + " overall performance")
    if Selected_Year != 'Overall' and Selected_Country != 'Overall':
        st.title(Selected_Country + " overall performance in " + str(Selected_Year))
    st.table(data)

if user_menu == 'Overall Analysis':
    edition = df_merge['Year'].unique().shape[0]-1
    cities = df_merge['City'].unique().shape[0]
    sports = df_merge['Sport'].unique().shape[0]
    events = df_merge['Event'].unique().shape[0]
    athletes = df_merge['Name'].unique().shape[0]
    nations = df_merge['region'].unique().shape[0]

    # After displaying statistics, add a separator or organize into columns if needed
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Adding space or a separator to improve layout
    st.markdown("---")

    # Plotting sections
    st.title("Participating nations over the years")
    nations_over_time = Helper.Data_Over_Time(df_merge, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.plotly_chart(fig)

    st.title("Events over the years")
    Events_over_time = Helper.Data_Over_Time(df_merge, 'Event')
    fig = px.line(Events_over_time, x='Edition', y='Event')
    st.plotly_chart(fig)

    st.title("Athletes over the years")
    Athletes_over_time = Helper.Data_Over_Time(df_merge, 'Name')
    fig = px.line(Athletes_over_time, x='Edition', y='Name')
    st.plotly_chart(fig)


    st.title("No. of events every time (every sport)")

    x = df_merge.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)

    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pivot_data, cmap='viridis', cbar=True, ax=ax)

    # Manually add text annotations
    for i in range(pivot_data.shape[0]):
        for j in range(pivot_data.shape[1]):
            ax.text(j + 0.5, i + 0.5, int(pivot_data.iloc[i, j]),
                    ha='center', va='center', color='white', fontsize=10)

    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df_merge['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a sport', sport_list)

    x = Helper.top_Performance(df_merge, selected_sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':
    st.sidebar.title("Country wise Analysis")

    country_list = df_merge['region'].dropna().unique().tolist()
    country_list.sort()
    #country_list.insert(0, 'Overall')

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = Helper.YearWise_medal_Tally(df_merge, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " medal tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excel in the following sports")
    pt = Helper.country_event_Heatmap(df_merge, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = Helper.most_successful_country(df_merge, selected_country)
    st.table(top10_df)


if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df_merge.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age Distribution', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)

    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    sport_list = df_merge['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Height vs Weight")
    selected_sport = st.selectbox('Select a sport', sport_list)
    tempp = Helper.Weight_vs_Height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', data=tempp, hue=tempp['Medal'], style=tempp['Sex'], s=50)

    st.pyplot(fig)

    st.title("Men vs Women participation over the Years.")
    final = Helper.mens_vs_womens(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
