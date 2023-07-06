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
    #"Betting Systems and Promotions Page": "betting_and_promotions"
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
        df_placeholder.dataframe(filtered_data.reset_index().drop(columns=['League']).set_index(['Home Team', 'Away Team']))
    else:
        df_placeholder.dataframe(limited_data_display.reset_index().drop(columns=['League']).set_index(['Home Team', 'Away Team']))

    # Button to display all rows
    if st.button("View All"):
        df_placeholder.dataframe(full_data_display.reset_index().drop(columns=['League']).set_index(['Home Team', 'Away Team']))

    # Trigger download
    st.write('')
    st.write('')




def today_matches_page():
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

    # Filter the data for today's matches
    today = datetime.today().strftime('%Y-%m-%d')
    today_matches = data[data['Date'] == today]
    today_matches_filtered = today_matches[today_matches['Games Played'] >= 8]

    # Display the country, league, and today's matches
    st.header(f"{country_selection} {league_selection}")
    st.subheader("Today's Matches")

    if today_matches_filtered.empty:
        st.write("No matches found for today.")
    else:
        st.write(today_matches_filtered)

    # Get the top 5 statistical selections for each column
    st.subheader("Today's Best Statistical Selections")

    for column in today_matches_filtered.columns:
        if column != 'Date' and column != 'Games Played':
            top_selections = today_matches_filtered.nlargest(5, column)
            st.write(f"Top 5 in {column}:")
            st.write(top_selections)
            st.write("---")



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
    


if __name__ == "__main__":
    main()
