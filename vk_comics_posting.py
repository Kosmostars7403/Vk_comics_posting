import requests
import os
import random
from dotenv import load_dotenv


def check_response_for_errors(response):
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])

def download_random_comic():
    comic_number = get_random_number_of_comic()
    url = 'https://xkcd.com/{}/info.0.json'.format(comic_number)
    response = requests.get(url)
    response.raise_for_status()
    comic_information = response.json()
    image_url = comic_information['img']
    comment = comic_information['alt']
    image = requests.get(image_url)
    with open('random_comic.png', 'wb') as file:
        file.write(image.content)
    return comment


def get_random_number_of_comic():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_number = random.randint(1, response.json()['num'])
    return comic_number


def get_wall_upload_server():
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payrole = {
        'access_token': vk_user_token,
        'v': api_version,
        'group_id': group_id
    }
    response = requests.get(url, params=payrole).json()
    check_response_for_errors(response)
    upload_url = response['response']['upload_url']
    return upload_url


def upload_on_vk_server(upload_url):
    with open('random_comic.png', 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files).json()
        check_response_for_errors(response)
    response_server = response['server']
    response_photo = response['photo']
    response_hash = response['hash']
    return response_server, response_photo, response_hash


def save_photo_to_album(upload_data):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payrole = {
        'access_token': vk_user_token,
        'v': api_version,
        'group_id': group_id,
        'server': upload_data[0],
        'photo': upload_data[1],
        'hash': upload_data[2]
    }

    response = requests.post(url, params=payrole).json()
    check_response_for_errors(response)
    owner_id = response['response'][0]['owner_id']
    media_id = response['response'][0]['id']
    return owner_id, media_id


def post_to_group_wall(photo_id):
    url = 'https://api.vk.com/method/wall.post'
    payrole = {
        'access_token': vk_user_token,
        'v': api_version,
        'owner_id': ('-' + group_id),
        'from_group': group_id,
        'attachments': 'photo{}_{}'.format(photo_id[0], photo_id[1]),
        'message': comment
    }

    response = requests.post(url, params=payrole).json()
    check_response_for_errors(response)


if __name__ == '__main__':
    load_dotenv()
    vk_user_token = os.getenv('VK_USER_TOKEN')
    api_version = os.getenv('API_VERSION')
    group_id = os.getenv('GROUP_ID')

    try:
        comment = download_random_comic()
        upload_url = get_wall_upload_server()
        upload_data = upload_on_vk_server(upload_url)
        photo_id = save_photo_to_album(upload_data)
        post_to_group_wall(photo_id)
    finally:
        os.remove('random_comic.png')
