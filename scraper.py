import datetime
import requests
import json
import re


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
                    if node['edge_media_to_caption']['edges']:
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
                    if node['edge_media_to_caption']['edges']:
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

    return { "resultData": resultData, "end_cursor": end_cursor, "next_page": nextPage }

def getPostData(postShortcode):
    url = 'https://instagram.com/p/{}'.format(postShortcode)

    data = requests.get(url).text
    match = re.search(
        r"<script[^>]*>\s*window._sharedData\s*=\s*((?!<script>).*)\s*;\s*</script>",
        data,
    )
    data = json.loads(match.group(1))['entry_data']['PostPage'][0]['graphql']['shortcode_media']

    currData = {
        "is_album": False,
        "is_image": False,
        "is_video": False,
        "preview": data['display_url'],
        "video_url": None,
        "shortcode": postShortcode,
        "nodes": [],
        'caption': None,
        "comments": None,
        "likes": None,
        "timestamp": None
    }

    typename = data['__typename']
    if typename == 'GraphSidecar':
        currData['is_album'] = True
    elif typename == 'GraphImage':
        currData['is_image'] = True
    elif typename == 'GraphVideo':
        currData['is_video'] = True

    if "edge_media_to_comment" in data:
        currData['comments'] = data["edge_media_to_comment"]["count"]
    else:
        currData['comments'] = data["edge_media_to_parent_comment"]["count"]
    
    currData['likes'] = data['edge_media_preview_like']['count']
    currData['timestamp'] = data['taken_at_timestamp']
    if data['edge_media_to_caption']['edges']:
        currData['caption'] = data['edge_media_to_caption']['edges'][0]['node']['text']    
    
    if currData['is_album']:
        if "edge_sidecar_to_children" in data:
            for edge in data["edge_sidecar_to_children"]["edges"]:
                node = {
                    'shortcode': edge['node']['shortcode'],
                    'id': None,
                    'is_video': None,
                    'video_url': None,
                    'display_url': None,
                    'resources': None
                }
                node['id'] = edge["node"]["id"]
                node['is_video'] = edge["node"]["is_video"]
                if node['is_video'] and "video_url" in edge["node"]:
                    node['video_url'] = edge["node"]["video_url"]
                node['display_url'] = edge["node"]["display_url"]
                if "display_resources" in edge["node"]:
                    node['resources'] = [resource["src"] for resource in edge["node"]["display_resources"]]
                elif "thumbnail_resources" in edge["node"]:
                    node['resources'] = [resource["src"] for resource in edge["node"]["thumbnail_resources"]]

                currData['nodes'].append(node)
    elif currData['is_video']:
        currData['video_url'] = data['video_url']

    return currData