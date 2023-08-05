import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import numpy as np

# Constants for column names
PERCENTAGE_COLUMNS = ['Home Win %', 'Draw %', 'Away Win %', 'BTTS %', 'BTTS Home Win %', 'BTTS Away Win %',
                      'BTTS Draw %', 'BTTS No Draw %', 'Over 0.5 Goals %', 'Over 1.5 Goals %', 'Over 2.5 Goals %',
                      'Over 3.5 Goals %', 'Over 4.5 Goals %']
AVERAGE_COLUMNS = ['Average Goals For Home', 'Average Goals For Away']


def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.copy()
        object_to_download.reset_index(
            inplace=True)  # Reset the index to include "Home Team" and "Away Team" as columns
        object_to_download = object_to_download.to_csv(index=False)
    b64 = base64.b64encode(object_to_download.encode()).decode()
    href = f'data:file/csv;base64,{b64}'
    return f'<a href="{href}" download="{download_filename}">{download_link_text}</a>'


def prepare_data(data, percentage_columns, average_columns):
    for column in percentage_columns:
        if column in data.columns:
            if data[column].dtype == 'object':
                data.loc[:, column] = (data[column].str.rstrip('%').astype(float)).round(2).astype(str) + '%'
            else:
                data.loc[:, column] = (data[column] * 100).round(2).astype(str) + '%'
    for column in average_columns:
        if column in data.columns:
            data.loc[:, column] = data[column].apply(lambda x: '{:.2f}'.format(x))
    return data


# File paths and data loading
data_files = {
    "Belgium": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Belgium.csv",
    "England": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/England.csv",
    "France": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/France.csv",
    "Germany": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Germany.csv",
    "Holland": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Holland.csv",
    "Italy": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Italy.csv",
    "Portugal": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Portugal.csv",
    "Scotland": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Scotland.csv",
    "Spain": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Spain.csv",
    "Turkey": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Turkey.csv",
}

data = {k: pd.read_csv(v) for k, v in data_files.items()}

# Configuration for the data processing
config = {
    "Belgium": {
        "league_order": ['Belgian Pro League'],
        "data": data["Belgium"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "England": {
        "league_order": ['Premiership', 'Championship', 'League One', 'League Two'],
        "data": data["England"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "France": {
        "league_order": ['France Ligue One', 'France Ligue Two'],
        "data": data["France"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Germany": {
        "league_order": ['German Bundesliga', 'German Bundesliga Two'],
        "data": data["Germany"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Holland": {
        "league_order": ['Netherlands Ersdvisle'],
        "data": data["Holland"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Italy": {
        "league_order": ['Italy Serie A', 'Italy Serie B'],
        "data": data["Italy"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Portugal": {
        "league_order": ['Portugal Primerira Liga'],
        "data": data["Portugal"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Scotland": {
        "league_order": ['Scottish Premiership', 'Scottish Division One', 'Scottish Division Two'],
        "data": data["Scotland"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Spain": {
        "league_order": ['La Liga', 'Spanish Secunda'],
        "data": data["Spain"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Turkey": {
        "league_order": ['Turkey Super Lig'],
        "data": data["Turkey"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    }
}

PAGES = {
    "Home": "home_page",
    "Stats and Leagues": "stats_and_leagues_page",
    "Today's Matches": "todays_matches_page",
    "Top 5 Statistics": "top_5_stats_page"
    # "Betting Systems and Promotions Page": "betting_and_promotions"
}


def home_page():
    st.title("Both Teams to Score and Goals Scored Percentages")
    st.write("Welcome to Both Teams to Score and Goals Scored Percentages!")
    st.write(
        "This website provides comprehensive statistics on both teams to score (BTTS) and the percentage of goals scored in football matches. The data is based on historic meetings between two teams, covering the 2023/2024 football season across various European leagues.")
    st.write(
        "Our extensive database includes statistics from over 20 seasons, offering valuable insights into the performance of teams when playing at home or away. You can access information such as win, draw, and loss percentages, BTTS percentages, average goals per team, and the percentage of matches with over 0.5 goals to over 4.5 goals.")
    st.write(
        "All the data presented on this website can be downloaded in CSV format, allowing you to analyze and explore the statistics further. We offer downloads for all the leagues available, providing a comprehensive dataset for your analysis.")
    st.write(
        "Additionally, we provide a convenient 'Today's Matches' button that generates a CSV file containing the matches scheduled for today. This allows you to stay up-to-date with the latest matches and access real-time data for your analysis.")
    st.write(
        "Feel free to explore the sidebar to select a country and league of interest. Once selected, you can view and download the corresponding data. We hope that these statistics enhance your understanding of both teams to score and goals scored percentages, empowering you to make informed decisions.")
    st.write(
        "Please note that the statistics provided are based on historical data and should be used for informational purposes only.")


def stats_and_leagues_page():
    # Sidebar for selections
    st.sidebar.title("Selections")

    # Dropdown for country selection
    country_selection = st.sidebar.selectbox("Country", list(config.keys()), 0)

    # Dropdown for league selection
    league_selection = st.sidebar.radio("League", config[country_selection]["league_order"])

    # Read the data for selected country
    data = config[country_selection]["data"]

    # Prepare the data
    data = prepare_data(data, config[country_selection]["percentage_columns"],
                        config[country_selection]["average_columns"])

    # Display the country and league
    st.header(f"{country_selection} {league_selection}")

    # Download link for the limited data
    download_link_text = f'Please download {country_selection} {league_selection} info as a CSV'
    tmp_download_link = download_link(data[data['League'] == league_selection], 'YOUR_DOWNLOADED_DATA.csv',
                                      download_link_text)
    st.markdown(tmp_download_link, unsafe_allow_html=True)

    # Display a limited number of rows by default
    limited_data = data[data['League'] == league_selection].head(10)
    full_data = data[data['League'] == league_selection]

    # Sort 'Home Team' column in alphabetical order
    full_data.sort_values('Home Team', inplace=True)
    limited_data = full_data.head(10)

    # Set 'Home Team' and 'Away Team' as the index
    limited_data_display = limited_data.set_index(['Home Team', 'Away Team'])
    full_data_display = full_data.set_index(['Home Team', 'Away Team'])

    # Create a placeholder for the dataframe
    df_placeholder = st.empty()

    # Select team from a dropdown menu
    teams = sorted(set(full_data_display.index.get_level_values(0)).union(full_data_display.index.get_level_values(1)))
    teams.insert(0, "None")
    selected_team = st.selectbox('Select Team', teams, index=0)

    # Filter DataFrame based on the selected team
    if selected_team != "None":
        home_games = full_data_display[full_data_display.index.get_level_values(0) == selected_team]
        away_games = full_data_display[full_data_display.index.get_level_values(1) == selected_team]

        # Sort opponents in alphabetical order
        home_games.sort_index(level='Away Team', inplace=True)
        away_games.sort_index(level='Home Team', inplace=True)

        filtered_data = pd.concat([home_games, away_games])
        df_placeholder.dataframe(
            filtered_data.reset_index().drop(columns=['League']).set_index(['Home Team', 'Away Team']))
    else:
        df_placeholder.dataframe(
            limited_data_display.reset_index().drop(columns=['League']).set_index(['Home Team', 'Away Team']))

    # Button to display all rows
    if st.button("View All"):
        df_placeholder.dataframe(
            full_data_display.reset_index().drop(columns=['League']).set_index(['Home Team', 'Away Team']))

    # Trigger download
    st.write('')
    st.write('')


def todays_matches_page():
    st.title("Today's Matches")
    st.write(
        "This is a list of the 1st Weekends Premier League Matches. When the Season kicks off then a selection of matches from across europe will be posted daily.")
    st.write(
        "Please download the data as a CSV file (Link at the bottom of the page) to explore it further. In Excel, you can use filters to sort and analyze the data. For example, you can sort columns from largest to smallest to identify interesting patterns or trends.")

    st.write('')
    st.write(
        '**Note:** Please scroll horizontally to view all the stats for today\'s matches, or select a stat from the radio buttons.')
    st.write(
        'These statistics are based on past data and do not guarantee future success. Please gamble responsibly.')

    # Load today's matches data
    todays_matches = pd.read_csv("https://raw.githubusercontent.com/lottiealice18/BTTS/main/fixtures.csv")

    # Initialize an empty list to store today's matches with stats
    todays_data_with_stats = []

    # Loop over each country's data
    for country in config.keys():
        # Load country's data
        country_data = config[country]["data"]

        # Prepare the country's data
        country_data = prepare_data(country_data, config[country]["percentage_columns"],
                                    config[country]["average_columns"])

        # Merge today's matches with this country's data on 'Home Team' and 'Away Team'
        merged_data = pd.merge(todays_matches, country_data, on=['Home Team', 'Away Team'], how='inner')

        # Append this to the overall list
        todays_data_with_stats.append(merged_data)

    # Combine all dataframes
    todays_data_with_stats = pd.concat(todays_data_with_stats)

    # Set 'Home Team' and 'Away Team' as the index
    todays_data_with_stats.set_index(['Home Team', 'Away Team'], inplace=True)

    # Sort by 'League', 'Home Team' and 'Away Team'
    todays_data_with_stats.sort_values(by=['League', 'Home Team', 'Away Team'], inplace=True)

    # Get column names from the filtered DataFrame
    columns = todays_data_with_stats.columns.tolist()

    # Remove unwanted columns
    unwanted_columns = ['Home Team', 'Away Team', 'League']
    columns = [column for column in columns if column not in unwanted_columns]

    # Add "None" option to the column selection
    columns.insert(0, "None")

    # Create a placeholder for the dataframe
    df_placeholder = st.empty()

    # Select columns using radio buttons
    selected_column = st.radio("Select Columns", columns, index=0)

    if selected_column != "None":
        # Filtered DataFrame based on the selected column
        filtered_data = todays_data_with_stats[[selected_column]]
        # Display the filtered data
        df_placeholder.dataframe(filtered_data)
    else:
        # Display the original DataFrame
        df_placeholder.dataframe(todays_data_with_stats.drop(columns=['League']))


    # Download link for the data
    download_link_text = "Click here to download today's matches as a CSV"
    tmp_download_link = download_link(todays_data_with_stats.drop(columns=['League']), 'todays_matches.csv',
                                      download_link_text)
    st.markdown(tmp_download_link, unsafe_allow_html=True)


def top_5_stats_page():
    import pandas as pd

    # Load today's matches data
    todays_matches = pd.read_csv("https://raw.githubusercontent.com/lottiealice18/BTTS/main/Todays%20Matches.csv")

    # Initialize an empty list to store today's matches with stats
    todays_data_with_stats = []

    # Loop over each country's data
    for country in config.keys():
        # Load country's data
        country_data = config[country]["data"]

        # Prepare the country's data
        country_data = prepare_data(country_data, config[country]["percentage_columns"],
                                    config[country]["average_columns"])

        # Merge today's matches with this country's data on 'Home Team' and 'Away Team'
        merged_data = pd.merge(todays_matches, country_data, on=['Home Team', 'Away Team'], how='inner')

        # Append this to the overall list
        todays_data_with_stats.append(merged_data)

    # Combine all dataframes
    todays_data_with_stats = pd.concat(todays_data_with_stats)

    # Columns to sort by for top 5 statistical selections
    columns_to_sort = ['Total Games', 'Average Goals For Home', 'Average Goals For Away', 'Home Win %', 'Draw %',
                       'Away Win %', 'BTTS %', 'BTTS Home Win %', 'BTTS Away Win %', 'BTTS Draw %',
                       'BTTS No Draw %', 'Over 0.5 Goals %', 'Over 1.5 Goals %', 'Over 2.5 Goals %',
                       'Over 3.5 Goals %', 'Over 4.5 Goals %']

    # Add "None" option to the column selection
    columns_to_sort.insert(0, "None")

    # Add a title
    st.title("Top 5 Statistical Selections")

    # Explanation
    st.write("This section displays the top 5 statistical selections based on the chosen category. First, it filters matches that have been played 10 times or more. Then, you can select a category from the drop-down menu. Please note that these statistics are not guaranteed and should be used for informational purposes only.")

    # Create a placeholder for the new dataframe
    new_df_placeholder = st.empty()

    # Dropdown for column selection
    selected_column = st.selectbox('Select Statistic', columns_to_sort, index=0)

    if selected_column != "None":
        # Filter rows where 'Total Games' is less than 10
        filtered_data = todays_data_with_stats[todays_data_with_stats['Total Games'] >= 10]

        # Sort by the selected column and take the top 5
        top_5_data = filtered_data.sort_values(by=selected_column, ascending=False).head(5)

        # Only display 'Home Team', 'Away Team', and the selected column
        top_5_data = top_5_data.reset_index()[['Home Team', 'Away Team', selected_column]]

        # Display the top 5 data
        new_df_placeholder.dataframe(top_5_data)

def main():
    st.markdown("""
        **Note for Mobile Users:** Please click on the arrow at the top left corner to open the selections sidebar.
        """)
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Select a Page", list(PAGES.keys()))
    if selection == "Home":
        home_page()
    elif selection == "Stats and Leagues":
        stats_and_leagues_page()
    elif selection == "Today's Matches":
        todays_matches_page()
    elif selection == "Top 5 Statistics":
        top_5_stats_page()

if __name__ == "__main__":
    main()
