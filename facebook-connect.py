# facebook-connect.py
from pprint import pprint

import facebook
import pymongo

API_KEY = '1893398220887041|20tMykpFDBFjSxavHCZVSm29S08'
PAGE_TEMPLATE = '{}?fields=name,id,fan_count,about'
POSTS_TEMPLATE = '{}/posts?fields=shares,name,message,created_time'
pages_posts = []

client = pymongo.MongoClient()

db = client.get_database('socialagg')

pages = db.get_collection('pages')
pages.create_index('id', unique=True)

# pages.insert({'id':"1233", 'name':'alon'})

graph = facebook.GraphAPI(access_token='1893398220887041|20tMykpFDBFjSxavHCZVSm29S08', version='2.5')


# print(graph.get_object('cnn/posts'))
# posts = graph.get_object('cnn/posts?fields=shares,name,message,created_time')
# print(posts)
# print(posts['data'])
# pages.insert(posts['data'])

def add_page(page=''):
    page = graph.get_object(PAGE_TEMPLATE.format(return_correct_page(page)))
    pages.update({'id': page['id']}, page, upsert=True)


def return_correct_page(page=''):
    if 'facebook.com' in page:
        page = page.split('/')[1]
        return page
    else:
        return page


def create_pages_info():
    for page in pages.find():
        posts = db.get_collection(page['name'])
        post = graph.get_object(POSTS_TEMPLATE.format(page['name']))['data']
        posts.create_index('id', unique=True)
        for k in post:
            posts.update({'id': k['id']}, k, upsert=True)
        print(post)
        # posts.update({'id': post['id']}, post, upsert=True)
        pages_posts.append(posts)
    for posts in pages_posts:
        for post in posts.find():
            pprint(post)


add_page('buzzfeedtasty')
add_page('cnn')
create_pages_info()

# for k in pages.find():
#     pprint(k)
# print(pages.find())

# for k in posts['data']:
#     if 'name' in k.keys():
#         print("Name: {}".format(k['name']))
#     else:
#         print("Name:")
#     print("Message: {}".format(k['message']))
#     # print("Name: {}".format(k['name']))
#
#     # for i in k.items():
#     #     print(i)

# with open('messages.txt', 'w', encoding='UTF-8') as f:
#     for k in posts['data']:
#         f.write("Message: {}\n".format(k['message']))
#         # for i, info in k.items():
#         #     print(i, info)
# # print(posts['paging'])
