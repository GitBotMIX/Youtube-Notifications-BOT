# from Youtube database table
YOUTUBE_TABLE = 'youtube'
YOUTUBE_ROWS = {'CHANNEL_NAME': 'channel_name', 'URL': 'channel_url',
                'VIDEO': 'current_video', 'STREAM': 'stream_current_id', 'USER': 'user_id'}
# from User database table
USER_TABLE = 'user'
USER_ROWS = {'STATUS': 'status', 'LANGUAGE': 'language', 'TIMEZONE': 'timezone', 'USER': 'user_id'}
# from remind database table
REMIND_TABLE = 'remind'
REMIND_ROWS = {'VIDEO_URL': 'video_url', 'JOB_TIME': 'job_time', 'USER': 'user_id'}
# from youtube handler
MAX_NUMBER_ON_CHANNEL = 8
