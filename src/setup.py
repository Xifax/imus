# -*- coding=utf-8 -*-

import sys

try:
    import pip
except ImportError:
    print 'Please install pip'
    sys.exit(0)

from conf.const import name
from conf.const import packages

def setup_all():
    pip.main(['install'] + packages)

def info():
    if raw_input("Good day! If you've run this without administrative privileges, please, reconsider.\n\
This script will now set up all necessary packages \
and resources to succesfully launch '%s' (at least it will try to) [y/n]: " % name) \
                != ('y' or 'Y'):
        print 'Oh, well, goodbye then.'
        sys.exit(0)

def post_install():
    print "\n'%s' enviroment preparations comlete." % name

if __name__ == '__main__':
    info()
    setup_all()
    post_install()
