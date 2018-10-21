import  requests

headers = {
    'Host': 'www.che168.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

content = requests.get(url='https://www.che168.com/china/a0_0msdgscncgpi1lto8csp24exb2x0/', headers=headers).content
content = str(content, encoding='gb2312', errors='ignore')
print(content)
