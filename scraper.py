import datetime
import requests
import json


def getUserId(username):
    url = 'https://www.instagram.com/{}/?__a=1'.format(username)
    data = requests.get(url).json()
    return data['graphql']['user']['id']


def getUserPosts(userId, query_hash = '56a7068fea504063273cc2120ffd54f3', cursor = None, count = None, start = None, end = None):
    url = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash + '&variables={"id":' + userId + ', "first": "50"'

    if cursor:
        url += ', "after":"' + cursor + '"'
    url += '}'

    data = requests.get(url).json()
    end_cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    nextPage = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
    edges = data['data']['user']['edge_owner_to_timeline_media']['edges']

    quitLoop = False
    resultData = []
    for edge in edges:
        currData = {
            "is_album": False,
            "is_image": False,
            "is_video": False,
            'preview': None,
            "shortcode": None,
            'caption': None,
            "comments": None,
            "likes": None,
            "timestamp": None
        }

        node = edge['node']
        typename = node['__typename']
        if typename == 'GraphSidecar':
            currData['is_album'] = True
        elif typename == 'GraphImage':
            currData['is_image'] = True
        elif typename == 'GraphVideo':
            currData['is_video'] = True
        
        currData['preview'] = node['thumbnail_src']
        currData['shortcode'] = node['shortcode']
        if node['edge_media_to_caption']['edges']:
            currData['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
        currData['comments'] = node['edge_media_to_comment']['count']
        currData['likes'] = node['edge_media_preview_like']['count']
        currData['timestamp'] = node['taken_at_timestamp']
        
        if start:
            if start > datetime.datetime.fromtimestamp(int(currData['timestamp'])):
                quitLoop = True
                break
        
        resultData.append(currData)

    if count:
        while len(resultData) < count and nextPage:
            url = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash + '&variables={"id":' + userId + ', "first": "50"'
            url += ', "after":"' + end_cursor + '"'
            url += '}'

            data = requests.get(url).json()
            end_cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            nextPage = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            edges = data['data']['user']['edge_owner_to_timeline_media']['edges']

            for edge in edges:
                currData = {
                    "is_album": False,
                    "is_image": False,
                    "is_video": False,
                    'preview': None,
                    "shortcode": None,
                    'caption': None,
                    "comments": None,
                    "likes": None,
                    "timestamp": None
                }

                node = edge['node']
                typename = node['__typename']
                if typename == 'GraphSidecar':
                    currData['is_album'] = True
                elif typename == 'GraphImage':
                    currData['is_image'] = True
                elif typename == 'GraphVideo':
                    currData['is_video'] = True
                
                currData['preview'] = node['thumbnail_src']
                currData['shortcode'] = node['shortcode']
                if node['edge_media_to_caption']['edges']:
                    currData['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
                currData['comments'] = node['edge_media_to_comment']['count']
                currData['likes'] = node['edge_media_preview_like']['count']
                currData['timestamp'] = node['taken_at_timestamp']
                
                resultData.append(currData)    
    else:
        if start and len(resultData) >= 50:
            quitLoop = False
            index = 0
            while start < datetime.datetime.fromtimestamp(int(resultData[-1]['timestamp'])) and nextPage and not quitLoop:
                url = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash + '&variables={"id":' + userId + ', "first": "50"'
                url += ', "after":"' + end_cursor + '"'
                url += '}'

                data = requests.get(url).json()
                end_cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                nextPage = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
                edges = data['data']['user']['edge_owner_to_timeline_media']['edges']

                for edge in edges:
                    currData = {
                        "is_album": False,
                        "is_image": False,
                        "is_video": False,
                        'preview': None,
                        "shortcode": None,
                        'caption': None,
                        "comments": None,
                        "likes": None,
                        "timestamp": None
                    }

                    node = edge['node']
                    typename = node['__typename']
                    if typename == 'GraphSidecar':
                        currData['is_album'] = True
                    elif typename == 'GraphImage':
                        currData['is_image'] = True
                    elif typename == 'GraphVideo':
                        currData['is_video'] = True
                    
                    currData['preview'] = node['thumbnail_src']
                    currData['shortcode'] = node['shortcode']
                    currData['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
                    currData['comments'] = node['edge_media_to_comment']['count']
                    currData['likes'] = node['edge_media_preview_like']['count']
                    currData['timestamp'] = node['taken_at_timestamp']

                    if start > datetime.datetime.fromtimestamp(int(currData['timestamp'])):
                        quitLoop = True
                        break

                    resultData.append(currData)
        else:
            while nextPage and len(resultData) > 50:
                url = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash + '&variables={"id":' + userId + ', "first": "50"'
                url += ', "after":"' + end_cursor + '"'
                url += '}'

                data = requests.get(url).json()
                end_cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                nextPage = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
                edges = data['data']['user']['edge_owner_to_timeline_media']['edges']

                for edge in edges:
                    currData = {
                        "is_album": False,
                        "is_image": False,
                        "is_video": False,
                        'preview': None,
                        "shortcode": None,
                        'caption': None,
                        "comments": None,
                        "likes": None,
                        "timestamp": None
                    }

                    node = edge['node']
                    typename = node['__typename']
                    if typename == 'GraphSidecar':
                        currData['is_album'] = True
                    elif typename == 'GraphImage':
                        currData['is_image'] = True
                    elif typename == 'GraphVideo':
                        currData['is_video'] = True
                    
                    currData['preview'] = node['thumbnail_src']
                    currData['shortcode'] = node['shortcode']
                    currData['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
                    currData['comments'] = node['edge_media_to_comment']['count']
                    currData['likes'] = node['edge_media_preview_like']['count']
                    currData['timestamp'] = node['taken_at_timestamp']
                    
                    resultData.append(currData)    

    if end:
        resultDataCopy = resultData
        resultData = []

        for data in resultDataCopy:
            if end > datetime.datetime.fromtimestamp(int(data['timestamp'])):
                resultData.append(data)

    return { "resultData": resultData, "end_cursor": end_cursor }


print((getUserPosts("173560420", start=datetime.datetime(2020, 10, 7), end=datetime.datetime(2020, 10, 11))))