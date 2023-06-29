import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

st.text_input("Your name", key="name")
# You can access the value at any point with:
st.session_state.name

# running a basic app
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() # byte is data's stream we will have to convert it to a string
    data = bytes_data.decode("utf-8") # we will be converting it to a UTF-8 string
    df = preprocessor.preprocess(data)

    # st.dataframe(df) # to display a dataframe in streamlit, there is a function called dataframe, we will put df there

# fetching unique users
    user_list = df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort() # sorting the names in ascending order
    user_list.insert(0, "Overall") # putting the overall option at the top (0th position)
# if we have chosen "Overall", then we will show group level analysis

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list) # withthis we can see all the users in the chat

# Stats ares
    if st.sidebar.button("Show Analysis"): # creating a button. If someone clicks on this, then the analysis will start

# stats area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Mothly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"], color = "green")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        # Daily Timeline

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline["message"], color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = "orange")
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        st.title("Weekly Activity Map") # Creating the heatmap
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



# Finding the busiest user in the group(Can be done in Group level)
        if selected_user == "Overall": # This conditions makes sure that this activity works for only for group.
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="green")
                plt.xticks(rotation="vertical") # this makes the heading vertical in the graph as when put horizontally, we couldn't see the names.
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

# Wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df) # This will give the image in return
        fig, ax = plt.subplots()
        ax.imshow(df_wc) # This will display image
        st.pyplot(fig)

# Most common words

        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation="vertical")
        st.title("Emoji Analysis")
        st.pyplot(fig)

        st.dataframe(most_common_df)

# Emoji analysis

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2) # here 2 means that we require 2 columns
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct = "%0.2f") # autopct gives out the percentage in the piechart || head shows the top 5 emojis
            st.pyplot(fig)

