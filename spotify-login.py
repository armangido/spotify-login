import datetime
import login5_pb2
import requests
import hashlib
import time
import binascii
ntz8tab = bytes.fromhex(
    "08 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "04 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "05 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "04 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "06 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "04 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "05 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "04 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "07 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "04 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "05 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "04 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "06 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "04 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "05 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
    "04 00 01 00 02 00 01 00 03 00 01 00 02 00 01 00"
)

d = login5_pb2.LoginRequest()
d.client_info.client_id = "9a8d2f0ce77a4e248bb71fefcb557637"
d.password.id = "test@gmail.com"
d.password.password = "test123"
t = d.SerializeToString()

headers = {
    "User-Agent":"Spotify/8.9.30.433 Android/30 (Phone)",
    "Content-Type":"application/x-protobuf",
}
r = requests.post("https://login5.spotify.com/v3/login",

                  data=t)
def TrailingZeros8(x):
    return ntz8tab[x]
def chc(s,leng):
    i = len(s) - 1
    while i >= 0:
        z = TrailingZeros8(s[i])
        if z >= leng:
            return True
        elif z < 8:
            return False
        leng -= 8
        i -= 1
    return False
def ihc(dat, i):
    if dat[i] == 254 and i != 0:
        dat[i] = 0
        return ihc(dat,i-1)
    else:
        dat[i] += 1
    return dat
def shc(lc,pref,hlen):
    lcs = hashlib.sha1(lc).digest()
    suff = bytearray(16)
    suff = lcs[12:20] + suff[0:8]
    h = hashlib.sha1()
    while True:
        h.update(pref)
        h.update(suff)
        s = h.digest()
        if chc(s,hlen):
            return suff
        suff = bytearray(suff)
        suff[0:8] = ihc(suff[0:8],7)
        suff[8:16] = ihc(suff[8:16],7)
        suff = bytes(suff)
e = login5_pb2.LoginResponse()
sol = login5_pb2.ChallengeSolution()
e.ParseFromString(r.content)
hch = e.challenges.challenges[0]
hpref = hch.hashcash.prefix
hlen = hch.hashcash.length
ctx = e.login_context
s = shc(ctx,hpref,hlen)
sol.hashcash.suffix = s
sol.hashcash.duration.nanos = 29900
d.login_context = ctx
d.challenge_solutions.solutions.append(sol)
pass
t = d.SerializeToString()
r = requests.post("https://login5.spotify.com/v3/login",
                  data=t,headers=headers)
e.ParseFromString(r.content)
print(e)
pass