import re
import pandas as pd
def preprocess(data):
    pattern = '\\d{1,2}/\\d{1,2}/\\d{2,4},\\s\\d{1,2}:\\d{2}\\s[ap]m\\s-\\s'

    messages = re.split(pattern, data,flags=re.IGNORECASE)[1:]
    dates = re.findall(pattern, data,flags=re.IGNORECASE)
    re_dates = [re.sub(r'\u202f', ' ', date) for date in dates]
    df = pd.DataFrame({'user_message': messages, 'message_date': re_dates})
    # convert message_date type
    # df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M %p - ')
    df['message_date'] = pd.to_datetime(df['message_date'].str.rstrip(' -'), format='%d/%m/%y, %I:%M %p',
                                        errors='coerce')

    df.rename(columns={'message_date': 'date'}, inplace=True)
    # df['am_pm'] = df['date'].dt.hour.apply(lambda x: 'AM' if 0 <= x < 12 else 'PM')
    users = []
    messages = []
    for message in df["user_message"]:
        entry = re.split('([\\w\\W]+?):\\s', message)
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
    df['second'] = df['date'].dt.second
    df['am_pm'] = df['date'].dt.strftime('%p')
    df['month_num']=df['date'].dt.month
    df['date_act']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 24:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period
    return df