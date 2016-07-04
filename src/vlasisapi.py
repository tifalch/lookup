import urllib.request
import re

p_aff = "-</span>(.*?)<"
p_typ = "<span class=\"type\">(.*?)</span>"
p_des = "<p class=\"definition\">(.*?)</p>"
p_noe = "<p class=\"notes\">(.*?)</p>"
p_ans = "<div id=\"definition\">(.*?)</div>"
p_an1 = "<dt>\s*<a href=\".*?\">(.*?)</a>\s*</dt>"
p_an2 = "<dd>(.*?)</dd>"

def furl(search):
    return "http://vlasisku.lojban.org/vlasisku/{}".format(search)

class Vlasisku:
    def __init__(self, search):
        self.search = search

    def uplink(self):
        res = urllib.request.urlopen(furl(self.search))
        if res.code != 200:
            raise ValueError('Could not connect to Vlasisku')
        body = str(res.read())
        res.close()
        try:
            self.definition = re.sub("<.*?>", "", re.search(p_des, body).group(1))
        except:
            intr = re.search(p_ans, body, re.DOTALL & re.MULTILINE)
            s = intr.group(1)
            self.type = "search"
            self.definition = [re.sub("<.*?>", "",x) for x in re.findall(p_an2, s, re.DOTALL & re.MULTILINE)]
            self.finding = re.findall(p_an1, s)
            self.num = len(self.finding)
            return
        try:
            self.rafsi = re.findall(p_aff, body)[:-1]
        except:
            self.rafsi = []
        self.type = re.search(p_typ, body).group(1)
        try:
            self.notes = re.sub("<.*?>", "", re.search(p_noe, body).group(1))
        except:
            self.notes = "<None>"

    def debug(self):
        if self.type == "search":
            for x in range(self.num):
                print("\n{}:\n{}".format(self.finding[x], self.definition[x]))
        else:
            print(self.search, end=" | ")
            for x in self.rafsi:
                print(x, end=" ")
            print("|",self.type)
            print(self.definition)

def get(search):
    v = Vlasisku(search)
    v.uplink()
    return v

if __name__ == '__main__':
    import sys
    v = Vlasisku(sys.argv[1])
    v.uplink()
    v.debug()