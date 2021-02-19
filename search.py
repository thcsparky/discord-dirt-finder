import os
import requests
import json
headers = ''

def formatrequest(user, channel, hotword):
    ##this function will return the usable packet.
    packet = 'https://discord.com/api/v8/guilds/[CHANNEL]/messages/search?author_id=[USER]&content=[HOTWORD]&include_nsfw=true'
    out = packet.replace('[USER]', user)
    out = out.replace('[CHANNEL]', channel)
    out = out.replace('[HOTWORD]', hotword)
    return(out)

def sendpacket(url):
    global headers
    ##this will send the packet and return the response
    a = headers.splitlines()
    dictcompile = {} ##this will be all our results, sorted by message ID.
    dictheaders = {}
    dictreq = {}
    messages = ''
    for x in a:
        item = x.split(': ')[0]
        content = x.split(': ')[1]
        dictheaders[item] = content
        ##format url
    req = requests.get(url, headers=dictheaders, timeout=10)
    if req.ok:
        dictreq = json.loads(req.text)
        del req
    for key, value in dictreq.items():
        if type(value) is list:
            messages = value
    if messages:
        listmessageinfo = []
        for x in messages:
            ##each one of these should be a dict at x[0] amazingly.. idk how tf.
            parse = str(x[0])
            parse1 = parse.split('\'author')[0]
            ##get message id
            msgid1 = parse1.split('\'id\': \'')[1]
            msgid = msgid1.split('\'')[0]
            ##get content
            try:
                content1 = parse1.split('\'content\': \'')[1]
                content = content1.split('\'')[0]

                channel1 = parse1.split('\'channel_id\': \'')[1]
                channel = channel1.split('\'')[0]
                listmessageinfo.append(msgid + ': ' + content + ': ' + channel)
            except Exception as e:
                print(e)

        return(listmessageinfo)

def search(user, channels, hotwords):
    global headers
    ##set headers
    dictcompile = {} ##this will be a list of results.
    dictmsglinks = {} ##this will be a list of links ot messages.
    htmlstring = '' ##this will be the string for the clickable html page.
    for x in channels:
        for y in hotwords:
            url = formatrequest(user, x, y)
            ##get a list of results
            result = sendpacket(url)
            if type(result) is list and len(result) > 0:
                for z in result:
                    # dictcompile[z.split(': ')[0]] = z.split(': ')(1)
                    id = z.split(': ')[0]
                    msg = z.split(': ')[1]
                    channel = z.split(': ')[2]
                    print('got message id: ' + str(id) + ' IN: ' + x + '\n')
                    print('\n')
                    ##https://discord.com/channels/624505663053103114/731966877743710218/812115988157038632
                    dictcompile['https://discord.com/channels/' + x + '/' + channel + '/' + str(id)] = msg
                    htmlstring += '<a href=\'' + 'https://discord.com/channels/' + x + '/' + channel + '/' + str(id) + '\'>' + str(id) + ': ' +  msg + '<br>\n'

    out = json.dumps(dictcompile)
    a = open(os.getcwd() + '/results.json', 'w')
    a.write(out)
    a.close()
    print('written to: ' + os.getcwd() + '/results.json')
    ##write html string
    a = open(os.getcwd() + '/htmlresults.html', 'w')
    a.write(htmlstring)
    a.close()
    print('document written to: ' + os.getcwd() + '/htmlresults.html')
def main():
    global headers
    nl = '\n'
    a = open(os.getcwd() + '/user.txt')
    b = a.read()
    a.close()
    user = b
    a = open(os.getcwd() + '/channels.txt')
    b = a.read()
    a.close()
    channels = b.splitlines()
    a = open(os.getcwd() + '/hotwords.txt')
    b = a.read()
    a.close()
    hotwords = b.splitlines()
    a = open(os.getcwd() + '/headers.txt')
    b = a.read()
    a.close()
    headers = b
    ##print out settings
    print('User to search: ' + user + nl)
    print('Channel list: ' + nl)
    for x in channels:
        print(x + nl)
    print('Hot words to look for: ' + nl)
    for x in hotwords:
        print(x + nl)
    inp = input('Proceed? y/n, results will be saved in this dir as results.txt').rstrip()
    ##proceed with search here which will return true when complete. It will also spit out
    ##contents of the jason database while creating it. print()
    if inp == 'n':
        main()
    if inp == 'y':
        search(user, channels, hotwords)


if __name__ == '__main__':
    main()
