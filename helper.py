from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract() # Creating a Object for urlextract


def fetch_stats(selected_user, df):

    if selected_user != "overall": # if overall is chosen, then df will remain as it is, if a selected user is
# chosen then df will change
        df = df[df["user"] == selected_user] # this lets you choose a specific user

        num_messages = df.shape[0] # here we are fetching number of messages
        words = []
        for message in df["message"]: # With this we will be able to fetch number of words
            words.extend(message.split())

    # fetch the number of media messages
    num_media_messages = df[df["message"] == "<Media omitted>\n"].shape[0]

    # fetch the number links shared

    links = []
    for message in df["message"]:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df): # giving our dataframe to the function
    x = df["user"].value_counts().head()
    df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={"index": "Name", "user":"percentage"})

    return x, df

def create_wordcloud(selected_user, df):

    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != "group_notification"] # this removes the group notification in the process of word_cloud
    temp = temp[temp["message"] != "<Media omitted>\n"] # removed media omitted messages

    def remove_stop_words(message): # This removes all the hinglish stop words from the wordcloud
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white") # configuring WordCloud
    temp["message"] = temp["message"].apply(remove_stop_words) #
    df_wc = wc.generate(temp["message"].str.cat(sep=" ")) # generate function generates world cloud as an image
    # wordcloud will generate from the message column of df
    return df_wc

def most_common_words(selected_user, df):

    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]

    words = []
    for message in temp["message"]:
        for word in message.lower().split():  # converting every word in lower case
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))
    timeline["time"] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user] # This code is used for filtering

    daily_timeline = df.groupby("only_date").count()["message"].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    return df["day_name"].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

        return df["month"].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    user_heatmap = df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0)

    return user_heatmap

