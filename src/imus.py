# -*- coding=utf-8 -*-

from db.library import Track, Redis

def main():
    pass

def test():
    r = Redis()
    r.update(Track('test', 'lalal', 'ohoho', 'oops'))
    #print r.lookup('*')
    print 'Lookup results ~ ', r.lookup('test')
    print 'Recreated track ~ ', r.retrieve(r.lookup('test').pop())

if __name__ == '__main__':
    test()
