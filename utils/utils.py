import re

from html.entities import entitydefs


def stringhtml(chaine):
    emap = {}
    for i in range(256):
        emap[chr(i)] = "&%d;" % i

    for entity, char in entitydefs.items():
        if char in emap:
            emap[char] = "&%s;" % entity

    def remplace(m, get=emap.get):
        return "".join(map(get, m.group()))

    return re.sub(r'[&<>\"\x80-\xff]+', remplace, chaine)
