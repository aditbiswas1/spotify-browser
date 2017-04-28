import requests


SPOTIFY_ENDPOINT  = 'https://api.spotify.com'
SEARCH_ENDPOINT = '/v1/search'

request_headers = {
                'content-type': "application/json"
            }


def parse_track(item):
    '''
    This function parses an individual track response. The track response is 
    slightly different from the other filters because the images
    of a track are contained in the albums instead images.
    '''
    name = item['name']
    thumbnail_links = item.get('album', {}).get('images')
    smallest_image_width = 640
    image = None
    for thumb in thumbnail_links:
        if not thumb['width'] or not thumb['height']:
            continue
        if thumb['width'] < smallest_image_width and thumb['width'] >= 64 and thumb['height'] >= 64:
            image = thumb['url']
            smallest_image_width = thumb['width']
    return {
        'name': name,
        'image': image,
    }

def parse_other_items(item):
    '''
    This function parses the individual item responses for all the filter types
    except track. 
    '''
    name = item['name']
    image = None
    smallest_image_width = 640
    thumbnail_links = item.get('images', [])
    for thumb in thumbnail_links:
        if not thumb['width'] or not thumb['height']:
            continue
        if thumb['width'] < smallest_image_width and thumb['width'] >= 64 and thumb['height'] >= 64:
            image = thumb['url']
            smallest_image_width = thumb['width']

    return {
        'name': name,
        'image': image
    }


def parse_item(item, item_type):
    '''
    This function returns the parsed item of the specific item_type
    it returns a dictionary
    {
        'name': 'entity_name',
        'image': 'url' or None
    }
    '''
    if item_type == 'track':
        return parse_track(item)
    else:
        return parse_other_items(item)



def get_track_list(search_query, query_filter='track', limit=20, offset=0):
    '''
    This function validates query parameters and calls the spotify webapi if all the validations pass

    NOTE: the spotify webapi has a maximum limit parameter of 100,000 as defined in the doc. while a query
    can have a greater count, spotify will not return results after 100,000

    in case of any failure from the api such as 429 or 500, the function fails gracefully and returns empty results
    '''
    if search_query is None or '':
        return 0, []
    
    if limit < offset:
        return 0, []

    if limit > 100000:
        return 0, []

    valid_query_filters = ['track', 'album', 'playlist', 'artist']
    if query_filter not in valid_query_filters:
        return 0, []

    request_params = {
        'q' : search_query,
        'type' : query_filter,
        'limit': limit,
        'offset': offset,
    }

    api_endpoint = SPOTIFY_ENDPOINT + SEARCH_ENDPOINT
    response = requests.get(api_endpoint, headers=request_headers, params=request_params)

    if response.status_code == requests.codes.ok:
        response_object = response.json()
        key = query_filter + 's'
        count = response_object[key].get('total', 0)
        response_items = response_object[key].get('items')

        items = [parse_item(item, item_type=query_filter) for item in response_items]
        return count, items

    else:
        return 0, []