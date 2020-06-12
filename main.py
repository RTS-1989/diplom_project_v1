import requests, json, time
from time import sleep

token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
user_id = 171691064
##user_id = 'eshmargunov'

def get_groups(user_id):

    groups_list = []
    
    params = {
              'access_token': token,
              'user_id': user_id,
              'v': 5.107,
              'extended': 1,
              'fields': ['id', 'name', 'members_count']
              }

    response = requests.get('https://api.vk.com/method/groups.get', params).json()

    for group in response['response']['items']:
        groups_list.append({'gid': group['id'], 'name': group['name'], 'members_count': group['members_count']})

    return groups_list

##print(get_groups(user_id))

def get_friends(user_id):

    friends_list = []
    
    params = {
              'access_token': token,
              'user_id': user_id,
              'v': 5.107,
##              'count': 50,
              'fields': 'domain'
              }

    response = requests.get('https://api.vk.com/method/friends.get', params)

    for user in response.json()['response']['items']:
        friends_list.append(user['id'])

    return friends_list

friends_list = get_friends(user_id)
user_groups_list = get_groups(user_id)
user_groups_list2 = []

def is_member(user_id, group_id):

    params = {
          'access_token': token,
          'user_id': user_id,
          'v': 5.107,
          'group_id': group_id,
          }

    response = requests.get('https://api.vk.com/method/groups.isMember', params).json()

    return response

def friends_group_checker():
    for friend in friends_list:
        sleep(2)
        for group in user_groups_list:
            group_id = group['gid']
            if is_member(friend, group_id)['response'] == 1:
                user_groups_list2.append(group_id)

    print(f'В данных группах состоит только пользователь id={user_id}:')

    for group in user_groups_list:
        if group['gid'] not in user_groups_list2:
            with open('groups.json', 'a') as write_file:
                json.dump(group, write_file)
            print(group)

friends_group_checker()