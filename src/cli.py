#!/usr/bin/python
import cmd

class Calc(cmd.Cmd):
    def do_add(self, arg):
        print sum(map(int, arg.split()))

if __name__ == '__main__':
    Calc().cmdloop()

