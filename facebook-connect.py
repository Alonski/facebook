# facebook-connect.py
from pprint import pprint

import facebook
import pymongo

API_KEY = '1893398220887041|20tMykpFDBFjSxavHCZVSm29S08'
PAGE_TEMPLATE = '{}?fields=name,id,fan_count,about'
POSTS_TEMPLATE = '{}/posts?fields=shares,name,message,created_time&limit=50'

PAGE_HTML_TEMPLATE = """
<html>
<title>My Facebook Pages</title>
{}
</html>
"""

pages_posts = []

client = pymongo.MongoClient()

db = client.get_database('socialagg')

pages = db.get_collection('pages')
pages.create_index('id', unique=True)
# pages.drop()
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


def create_pages_info_first():
    for page in pages.find():
        posts = db.get_collection(page['name'])
        # print(posts)
        post = graph.get_object(POSTS_TEMPLATE.format(page['name']))['data']
        posts.create_index('id', unique=True)
        for k in post:
            posts.update({'id': k['id']}, k, upsert=True)
        # print(post)
        # posts.update({'id': post['id']}, post, upsert=True)
        pages_posts.append(posts)


def get_pages_info():
    for page in pages.find():
        posts = db.get_collection(page['name'])
        # print(posts)
        # post = graph.get_object(POSTS_TEMPLATE.format(page['name']))['data']
        # posts.create_index('id', unique=True)
        # for k in post:
        #     posts.update({'id': k['id']}, k, upsert=True)
        # print(post)
        # posts.update({'id': post['id']}, post, upsert=True)
        pages_posts.append(posts)


# def show_pages_info():
#     for page in pages.find():
#         posts = db.get_collection(page['name'])
#         pages_posts.append(posts)
#     for posts in pages_posts:
#         for post in posts.find():
#             pprint(post)

def return_html_page_list():
    html = ""
    for page in pages.find():
        html += "<h1>{}</h1>\n".format(page['name'])
        html += "<h3>About the page: {}</h3>\n".format(page['about'])
        html += "<h3>Fan Count: {}</h3>\n".format(page['fan_count'])
    return html

    # print(page['name'], page['fan_count'], page['about'])


def create_html_all(page_html='', posts_html=''):
    with open('test.html', 'w', encoding='UTF-8') as f:
        html = "<html>\n{}\n</html>".format(page_html + posts_html)
        f.write(html)


def return_html_posts(name=''):
    html = "<html>\n{}\n</html>"
    posts = db.get_collection(name)
    for i, post in enumerate(posts.find()):
        if 'name' not in post.keys():
            post['name'] = ''
        if 'shares' not in post.keys():
            post['shares'] = {'count':'0'}
        if 'message' not in post.keys():
            post['message'] = ''
        print("Post Num: {} - Post Name: {name} - Message: {message} - Shares: {shares[count]}".format(i, **post))
        # print(i, post)
        # f.write(html.format(post))


# add_page('coca-cola')
# add_page('cnn')
# add_page('facebook')
# create_pages_info_first()
get_pages_info()
# show_pages_info()
# create_html()
create_html_all(return_html_page_list(), '')
return_html_posts("CNN")

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
