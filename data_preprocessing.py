import re
import pandas as pd
from dateutil import parser


def preprocess(datas):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w{2}\s-\s'

    messages = re.split(pattern, datas)[1:]
    dates = re.findall(pattern, datas)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = df['message_date'].map(lambda x: x[:-3])
    df['message_date'] = df['message_date'].map(lambda x: x.replace("/", "-"))
    df['message_date'] = df['message_date'].map(lambda x: x.replace(",", ""))
    df['message_date'] = df['message_date'].map(lambda x: parser.parse(x))
    df['message_date'] = pd.to_datetime(df.message_date, format='%Y-%m-%d %H:%M:%S')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
