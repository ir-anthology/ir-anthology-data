#!/usr/bin/python3
import sys
import scripts.venuecreator as venuecreator

argumentmapper = {}
argumentmapper["--new"] = venuecreator.main

def main(args):
    if args[0] not in argumentmapper.keys():
        raise Exception("asd")
    argumentmapper[args[0]](args[1:])
        

main(sys.argv[1:])