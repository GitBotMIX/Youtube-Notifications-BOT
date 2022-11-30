from data_base.sqlite_db import Youtube, User
from create_bot import bot
from functions import youtube_url
from middlewares.i18m_language import get_user_locale
from create_bot import _


async def remove_repeated_user_id(all_user_id: list[tuple]) -> list:
    updated_user_id_list = []
    for i in all_user_id:
        if i not in updated_user_id_list:
            updated_user_id_list.append(i)
    return updated_user_id_list


async def listen():
    all_user_id = await User.Id.get_all()
    for user_id in all_user_id:
        youtube_channel_name_and_url_list = await Youtube.Channel.get_all_rows_related_id(user_id)
        for user_channel_data in youtube_channel_name_and_url_list:
            channel_name_old = user_channel_data[0]
            channel_url = user_channel_data[1]
            channel_last_video_id_old = user_channel_data[2]
            try:
                channel_name = await youtube_url.get_channel_title(channel_url)
                channel_last_video_id = await youtube_url.parse_videos(channel_url)
                channel_last_video_url = await youtube_url.get_video_url_by_id(channel_last_video_id)
                if channel_name != channel_name_old:
                    await Youtube.Channel.Name.update(channel_name, channel_name_old, user_id)
                    await bot.send_message(user_id, _('🔔На канале "{}" поменялось название на "{}"',
                                                      locale=await get_user_locale(user_id)).format(channel_name_old,
                                                                                                    channel_name))
                if channel_last_video_id != channel_last_video_id_old:
                    await Youtube.Channel.VideoId.update(channel_last_video_id, channel_last_video_id_old, user_id)
                    await bot.send_message(user_id, _('🔔На канале "*{}*" новое видео!\n{}',
                                                      locale=await get_user_locale(user_id)).format(channel_name,
                                                                                                    channel_last_video_url),
                                           parse_mode='Markdown')
            except:
                await Youtube.Channel.Url.delete(channel_url, user_id)
                await bot.send_message(user_id, _('❌Ссылка на канал "{}" больше не актуальна, '
                                                  'информация о канале удалена, попробуй заново добавить канал\n\n'
                                                  'Устаревшая ссылка - {}',
                                                  locale=await get_user_locale(user_id)).format(channel_name_old,
                                                                                                channel_url),
                                       parse_mode='Markdown')