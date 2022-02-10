import datetime
import re

NOW = datetime.datetime.now()
LOCAL_NOW = NOW.astimezone()
LOCAL_TZ = LOCAL_NOW.tzinfo
UTC_TZ = datetime.timezone.utc


def convert_to_lines(text):
    lines = LINE_BREAK.split(text)
    return [line.strip() for line in lines if line not in ['', '\r', '\n']]


def chunks(lst, n=3):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def setup_tz_for_date(dt, tz):
    if tz:
        return dt.replace(tzinfo=tz)
    else:
        return dt


def convert_date(string, formats=None, with_timezone=True, tz=LOCAL_TZ):
    if formats is None:
        formats = (
            '%d.%m.%Y',
            '%m/%d/%Y',
            '%d/%m/%Y'
        )
    for _format in formats:
        try:
            dt = datetime.datetime.strptime(string, _format)
            return setup_tz_for_date(dt, tz) if with_timezone else dt
        except ValueError:
            pass
    print('DON`T CONVERT ', string)


def convert_datetime(string, formats=None, with_timezone=True, tz=LOCAL_TZ):
    if formats is None:
        formats = (
            '%d.%m.%Y %H:%M:%S',
            '%m/%d/%Y %I:%M:%S %p',
        )
    return convert_date(string, formats, with_timezone, tz)


LINE_BREAK = re.compile(r'([\r\n]|\r|\n])')
LINE_TO_DOTS = re.compile(r'[\s]+')
MULTI_SPACE = re.compile(r'[\s]{2,}')


def convert_date_json(date_text, tz=UTC_TZ):
    if date_text:
        text_data = date_text[6:-2]
        timestamp = float(text_data) / 1000
        if timestamp > 0:
            return datetime.datetime.fromtimestamp(timestamp, tz=tz)
