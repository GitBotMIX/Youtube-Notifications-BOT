from data_base.sqlite_db import Youtube, User
from create_bot import bot
from functions import youtube_url
from middlewares.i18m_language import get_user_locale
from create_bot import _
from aiogram.utils.exceptions import ChatNotFound
from keyboards.markups import get_youtube_add_method_kb
from keyboards.remind_inline import get_youtube_remind_preview_kb

legacy_link_cleaner = {}


async def remove_repeated_user_id(all_user_id: list[tuple]) -> list:
    updated_user_id_list = []
    for i in all_user_id:
        if i not in updated_user_id_list:
            updated_user_id_list.append(i)
    return updated_user_id_list


async def delete_user(user_id):
    await User.delete(user_id)
    await Youtube.delete(user_id)


async def listen():
    all_user_id = await User.Id.get_all()
    for user_id in all_user_id:
        youtube_channel_name_and_url_list = await Youtube.Channel.get_all_rows_related(user_id)
        for user_channel_data in youtube_channel_name_and_url_list:

            user_lang = await get_user_locale(user_id)
            channel_name_old = user_channel_data[0]
            channel_url = user_channel_data[1]
            channel_last_video_id_old = user_channel_data[2]
            channel_last_stream_id_old = user_channel_data[3]
            try:
                channel_name = await youtube_url.get_channel_title(channel_url)
                channel_last_video_id = await youtube_url.parse_videos(channel_url)
                is_stream, channel_last_stream_id = await youtube_url.parse_stream(channel_url, check_is_stream=True)
                channel_last_video_url = await youtube_url.get_video_url_by_id(channel_last_video_id)
                channel_stream_url = await youtube_url.get_video_url_by_id(channel_last_stream_id)
                try:
                    if channel_last_stream_id != channel_last_stream_id_old and is_stream:
                        await Youtube.Channel.StreamId.update(channel_last_stream_id, channel_last_stream_id_old,
                                                              user_id)
                        await bot.send_message(user_id, _('🔔Прямая трансляция на канале '
                                                          '"{}"\n{}', locale=user_lang).format(channel_name_old,
                                                                                               channel_stream_url))

                    if channel_name != channel_name_old:
                        await Youtube.Channel.Name.update(channel_name, channel_name_old, user_id)
                        await bot.send_message(user_id, _('🔔На канале "{}" поменялось название на "{}"',
                                                          locale=user_lang).format(channel_name_old, channel_name))

                    if channel_last_video_id != channel_last_video_id_old:
                        await Youtube.Channel.VideoId.update(channel_last_video_id, channel_last_video_id_old, user_id)
                        button_text = _('Установить напоминание', locale=user_lang)
                        await bot.send_message(user_id, _('🔔На канале "{}" новое видео!\n{}',
                                                          locale=user_lang).format(channel_name,
                                                                                   channel_last_video_url),
                                               reply_markup=await get_youtube_remind_preview_kb(user_id, button_text,
                                                                                                user_lang))
                except ChatNotFound:
                    await delete_user(user_id)
            except:
                try:
                    legacy_link_count = legacy_link_cleaner[channel_url]
                except KeyError:
                    legacy_link_count = 0
                    legacy_link_cleaner[channel_url] = legacy_link_count + 1
                if legacy_link_count == 5:
                    all_user_id_with_channel_url = await Youtube.Channel.Url.get_all_rows_related_reverse(channel_url)
                    for user_id_with_channel_url in all_user_id_with_channel_url:
                        user_id_with_channel_url = user_id_with_channel_url[0]
                        await Youtube.Channel.Url.delete(channel_url, user_id)
                        try:
                            await bot.send_message(user_id_with_channel_url, _('❌Ссылка на канал "{}" больше не '
                                                                               'актуальна, информация о канале удалена, '
                                                                               'попробуй заново добавить канал\n\n'
                                                                               'Устаревшая ссылка - {}',
                                                                               locale=user_lang).format(
                                channel_name_old,
                                channel_url),
                                                   parse_mode='Markdown',
                                                   reply_markup=await get_youtube_add_method_kb(user_id, user_lang))
                        except ChatNotFound:
                            await delete_user(user_id_with_channel_url)
                    legacy_link_cleaner[channel_url] = 0
                else:
                    legacy_link_cleaner[channel_url] = legacy_link_count + 1
