from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt

extractor = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # for fetching number of messages
    num_messages = df.shape[0]

    # for fetching number of words in messages
    words = []
    for message in df['message']:
        words.extend(message.split())

    # for fetching number of media messages
    num_of_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # for fetching number of link shared
    links = []

    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_of_media_messages, len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percentage'})

    return x,df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
