import re
import pandas as pd
from datetime import datetime


def convert24(time):
    t = datetime.strptime(time, '%d/%m/%Y, %I:%M%p')
    return t.strftime('%d/%m/%Y, %H:%M:%S')


"""
    The function preprocesses WhatsApp chat data by extracting relevant information such as date, user,
    and message.
    
    :param data: The input data that contains the WhatsApp chat messages
    :return: a pandas DataFrame with columns for the date, day, date, month, year, hour, minute, user,
    and message. The input data is preprocessed to extract the relevant information and clean the data.
"""


def proprocess(data):
    data = data.replace("\u202f", "")
    data = data[219:]
    pattern1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\w{2}\s-\s'
    msgs = re.split(pattern1, data)[1:]
    date_pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\w{2}"
    dates = re.findall(date_pattern, data)
    df = pd.DataFrame({"Date": dates, "Messages": msgs})
    df.Date = df.Date.apply(convert24)
    df.Date = pd.to_datetime(df.Date, format="%d/%m/%Y, %H:%M:%S")
    df["day"] = df.Date.dt.day_name()
    df["date"] = df.Date.dt.day
    df["month"] = df.Date.dt.month_name()
    df["year"] = df.Date.dt.year
    df["hour"] = df.Date.dt.hour
    df["minute"] = df.Date.dt.minute

    user = []
    message = []
    for m in df.Messages:
        entry = re.split("([\w\W]+?):\s", m)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append("group notification")
            message.append(entry[0])

    df['user'] = user
    df['message'] = message
    df.drop(["Messages", "Date"], axis=1, inplace=True)
    df.message = df.message.str.replace("\n", "")

    return df
