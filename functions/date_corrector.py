from datetime import datetime, timezone, timedelta


async def get_time_with_timezone(user_timezone_math_sign: str, user_timezone_value: str | int) -> datetime.now():
    utc_date_now = datetime.now(timezone.utc)
    if user_timezone_math_sign == '+':
        user_date_now = utc_date_now + timedelta(hours=int(user_timezone_value))
    else:
        user_date_now = utc_date_now - timedelta(hours=int(user_timezone_value))
    return user_date_now
