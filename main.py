import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('token')
group_id = os.getenv('group_id')
topics = os.getenv('topics')


def topics_iterate():
    for topic_id in topics:
        get_comments(topic_id)


def get_comments(topic_id):
    # Получение комментариев из записей сообщества
    response = requests.post('https://api.vk.com/method/board.getComments?'
                             'group_id=' + str(group_id) + '&'
                             'topic_id=' + str(topic_id) + '&'
                             'count=100&'
                             'sort=asc&'
                             'access_token=' + token + '&'
                             'v=5.124')
    comment_content = json.loads(response.content)
    delete_comments(comment_content, topic_id)


def delete_comments(comment_content, topic_id):
    comments_list = comment_content['response']['items']
    target_time = (int(time.time()) - 691200)
    comments_list.pop(0)
    if comments_list[-1]['date'] >= target_time:
        print('In if ' + str(topic_id))
        for item in comments_list:
            time.sleep(1)
            i = comments_list.index(item)
            if comments_list[i]['date'] <= target_time:
                pass
                # # Удалить комментарий к записи сообщества который старше 8 дней.
                # requests.post('https://api.vk.com/method/board.deleteComment?'
                #               'group_id=' + str(group_id) + '&'
                #               'topic_id=' + str(topic_id) + '&'
                #               'comment_id=' + str(item['id']) + '&'
                #               'access_token=' + token + '&'
                #               'v=5.124')
                return
    elif comments_list[-1]['date'] < target_time:
        print('elif ' + str(topic_id))
        for item in comments_list:
            time.sleep(1)
            i = comments_list.index(item)
            if comments_list[i]['date'] <= target_time:
                # Удалить комментарий к записи сообщества который старше 8 дней.
                # requests.post('https://api.vk.com/method/board.deleteComment?'
                #               'group_id=' + str(group_id) + '&'
                #               'topic_id=' + str(topic_id) + '&'
                #               'comment_id=' + str(item['id']) + '&'
                #               'access_token=' + token + '&'
                #               'v=5.124')
                return get_comments(topic_id)


topics_iterate()
