import vk_api
import configparser
import webbrowser as wb


def captcha_handler(captcha):
    wb.open_new_tab(captcha.get_url())
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def parse_ids(group_id, tools):
    ids = tools.get_all('groups.getMembers', 1000, {'group_id': group_id})
    ids = ids['items']
    return ids


def read_groups():
    group_list = []
    with open('groups.txt', 'r', encoding='utf-8') as f:
        for line in f:
            group_list.append(line.strip())
    return group_list


def write_ids(data):
    with open('result.txt', 'w', encoding='utf-8') as f:
        for line in data:
            f.write(str(line) + '\n')


def main():
    parsed = []
    filtered = []

    # Список груп из файла
    group_list = read_groups()

    # Конфиг
    conf = configparser.RawConfigParser()
    conf.read('config.cfg')
    login = conf.get('account', 'login')
    password = conf.get('account', 'password')
    print('Loggin into ' + login)
    vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    tools = vk_api.VkTools(vk_session)

    # Собираем все id с каждой группы
    for group in group_list:
        print('Parsing ' + group)
        parsed = parsed + parse_ids(group, tools)

    # Удаляем дубликаты
    for user in parsed:
        if user not in filtered:
            filtered.append(user)

    # Результат пишем в result.txt
    write_ids(filtered)
    print('Done!')
    input('Press Enter...')
if __name__ == '__main__':
        main()
