from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import string
import pandas as pd
import re
import emoji


def basic_stats(curr_user, df):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    msg_size = df.shape[0]
    words = []
    urls = []
    media = 0
    extractor = URLExtract()
    for m in df.message:
        if m == "<Media omitted>":
            media += 1
            continue
        words.extend(m.split())
        urls.extend(extractor.find_urls(m))

    return msg_size, len(words), media, urls


def most_busy_users(df):
    return df.user.value_counts().head()


def busy_percentage(df):
    X = round(df.user.value_counts() * (100 / df.shape[0]), 2).reset_index().rename(
        columns={"index": "user", "user": "percent"})
    # X.user = [x.split()[0] for x in X.user]
    X.percent = X.percent.apply(lambda x: str(x) + '%')
    return X


def word_cloud(df, curr_user, excl):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    df = df[df.user != "group_notification"]
    df = df[df.message != "<Media omitted>"]
    text = ""
    for m in df.message:
        text += " " + m
    text = emoji.replace_emoji(text)
    words = [w for w in text.split() if w not in excl and len(w) > 2]
    text = " ".join(words)
    return WordCloud(min_font_size=10, max_font_size=230, width=1200, height=600,
                     background_color="black").generate(text)


def most_common_words(df, curr_user, excl):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    text = ""
    for m in df.message:
        if m == "<Media omitted>":
            continue
        m = re.sub('\d', "", m)
        for p in string.punctuation:
            if p != " ":
                m = m.replace(p, " ")
        text += m + " "
    text = emoji.replace_emoji(text)
    words = [w for w in text.split() if w not in excl and len(w) > 3]
    res = pd.DataFrame(Counter(words).most_common(20), columns=["Common Words", "Percent"])
    res.Percent = round((res.Percent / len(words)) * 100, 2)
    return res


def get_emojis(df, curr_user):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    emojis = []
    for m in df.message:
        emojis.extend([c for c in m if c in emoji.EMOJI_DATA])
    data = pd.DataFrame(Counter(emojis).most_common(len(emojis)), columns=["emoji", "count"])
    other_sum = sum(data["count"][10:])
    data = data[:10]
    data.loc[len(data)] = ["Other", other_sum]
    return data


def monthly_timeline(df, curr_user):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    A = df.groupby(["year", "month"]).count()["message"].reset_index()
    A["timeline"] = [f'{A.month[i]}-{str(A.year[i])}' for i in range(len(A.year))]
    return A


def daily_timeline(df, curr_user):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    A = df.groupby(["year", "month", "date"]).count()["message"].reset_index()
    A["timeline"] = [f'{str(A.date[i])}-{str(A.month[i])[:3]}-{str(A.year[i])[2:]}' for i in range(len(A.date))]
    return A


def yearly_timeline(df, curr_user):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    A = df.groupby(["year"]).count()["message"].reset_index()
    A.year = A.year.astype(str)
    return A


def hour_timeline(df, curr_user):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    A = df.groupby(["hour"]).count()["message"].reset_index()
    for i in range(24):
        if i not in A.hour.to_list():
            A.loc[len(A.hour)] = [i, 0]
    A = A.sort_values("hour")
    A.hour = A.hour.astype(str)
    return A


def activity_map(df, curr_user):
    if curr_user != "Overall":
        df = df[df.user == curr_user]
    week_dict = {"Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6, "Sunday":7}
    month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8,
                  'September':9, 'October':10, 'November':11, 'December':12}
    m = df.groupby(['month']).count()['message'].reset_index()
    w = df.groupby(['day']).count()['message'].reset_index()
    m= m.sort_values('month', key = lambda x : x.apply (lambda x : month_dict[x]))
    w = w.sort_values('day', key = lambda x : x.apply (lambda x : week_dict[x]))
    return m, w
