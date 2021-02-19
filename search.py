import os
import requests
import json


def formatrequest(user, channel, hotword):
    # this function will return the usable packet.
    packet = 'https://discord.com/api/v8/guilds/[CHANNEL]/messages/search?author_id=[USER]&content=[HOTWORD]&include_nsfw=true'
    out = packet.replace('[USER]', user)
    out = out.replace('[CHANNEL]', channel)
    out = out.replace('[HOTWORD]', hotword)
    return out


def sendpacket(url):
    # this will send the packet and return the response
    cur_headers = filereader('headers.txt').splitlines()
    dict_headers = {}
    dict_req = {}
    messages = ''
    for header in cur_headers:
        item = header.split(': ')[0]
        content = header.split(': ')[1]
        dict_headers[item] = content
        # format url
    req = requests.get(url, headers=dict_headers, timeout=10)
    if req.ok:
        dict_req = json.loads(req.text)
        del req
    for key, value in dict_req.items():
        if type(value) is list:
            messages = value
    if messages:
        listmessageinfo = []
        for msg in messages:
            # each one of these should be a dict at x[0] amazingly.. idk how tf.
            parse = str(msg[0])
            parse1 = parse.split('\'author')[0]
            # get message id
            msgid1 = parse1.split('\'id\': \'')[1]
            msgid = msgid1.split('\'')[0]
            # get content
            try:
                content1 = parse1.split('\'content\': \'')[1]
                content = content1.split('\'')[0]

                channel1 = parse1.split('\'channel_id\': \'')[1]
                channel = channel1.split('\'')[0]
                listmessageinfo.append(msgid + ': ' + content + ': ' + channel)
            except Exception as e:
                print(e)

        return listmessageinfo


def filereader(filename):
    file_path = os.getcwd() + '/' + filename
    with open(os.getcwd() + '/' + filename) as file:
        filecontents = file.read()
    file.close()
    return filecontents


def filewriter(filename, data):
    with open(os.getcwd() + '/' + filename, 'w') as file:
        file.write(data)
    file.close()
    print('written to: ' + os.getcwd() + filename)


def search(user, channels, hotwords):
    dictcompile = {}  # this will be a list of results.
    htmlstring = ''  # this will be the string for the clickable html page.
    for channel_id in channels:
        for hotword in hotwords:
            url = formatrequest(user, channel_id, hotword)
            # get a list of results
            result = sendpacket(url)
            if type(result) is list and len(result) > 0:
                for result in result:
                    # dictcompile[z.split(': ')[0]] = z.split(': ')(1)
                    m_id = result.split(': ')[0]
                    msg = result.split(': ')[1]
                    channel = result.split(': ')[2]
                    print('got message id: ' + str(m_id) + ' IN: ' + channel_id)
                    # https://discord.com/channels/624505663053103114/731966877743710218/812115988157038632
                    dictcompile['https://discord.com/channels/' + channel_id + '/' + channel + '/' + str(m_id)] = msg
                    htmlstring += '<a href=\'' + 'https://discord.com/channels/' + channel_id + '/' + channel + \
                                  '/' + str(m_id) + '\'>' + str(m_id) + ': ' + msg + '<br>\n'

    out = json.dumps(dictcompile)
    filewriter('results.json', out)
    filewriter('htmlresults.html', htmlstring)
    print("Search Complete!")


def main():
    user = filereader('user.txt')
    channels = filereader('channels.txt').splitlines()
    hotwords = filereader('hotwords.txt').splitlines()
    # print out settings
    print('User to search: ' + user + '\n')
    print('Channel list: \n')
    for channel in channels:
        print(channel + '\n')
    print('Hot words to look for: \n')
    for hotword in hotwords:
        print(hotword + '\n')
    inp = input('Results will be saved in this dir as results.txt\nProceed (y/n)? ').rstrip()
    # proceed with search here which will return true when complete
    # will also print contents of the json database while creating it
    if inp == 'n':
        main()
    if inp == 'y':
        search(user, channels, hotwords)


if __name__ == '__main__':
    main()
