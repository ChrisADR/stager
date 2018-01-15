#Copyright (C) Christopher Díaz Riveros <chrisadr@gentoo.org>
#
#main.py is part of installer.
#
#Installer is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License v2 as published by
#the Free Software Foundation, either version 2 of the License, or
#(at your option) any later version.
#
#Installer is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License v2 for more details.
#
#You should have received a copy of the GNU General Public License v2
#along with Installer.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import os

def main():
    try:
        check_permission()

        parser = argparse.ArgumentParser(
                description="Installer is designed to aid users to install Gentoo Linux",
                epilog="If you find this useful or find a bug please contact to chrisadr@gentoo.org")

        parser.add_argument("-t", "--tui",
                action="store_true",
                help="launch Terminal User Interface")

        parser.add_argument("-v", "--version",
                action="version",
                version="%(prog)s 0.1.0dev")
        
        subparsers = parser.add_subparsers(
                title="available subcommands",
                description="Installer implements two ways of installing Gentoo Linux,\
                from scratch and from an existing system.",
                help="for specific info use installer <command> --help",
                metavar="<command>",
                dest="action")

        beginner_parser = subparsers.add_parser("beginner",
                help="begin a new Gentoo Linux installation")

        beginner_parser.add_argument("-s", "--step",
                metavar="N",
                default=0,
                choices=[1,2,3,4,5,6,7,8,9,10,11],
                type=int,
                help="begin on a specific step of installation")

        generate_parser = subparsers.add_parser("generate",
                help="generate a stageX tarball from current system")

        generate_parser.add_argument("-k","--include-kernel",
                action='store_true',
                dest='kernel',
                help="include /usr/src/ directory in stageX")

        args = parser.parse_args()

        if args.action=="beginner":
            import pym.installer.beginner as beginner
            beginner.init(args)
        elif args.action=="generate":
            import pym.installer.generate as generate
            generate.init(args)
        else:
            raise ValueError()

    except ValueError:
        print("You need to provide an action, see installer --help or -h for more info")
    except PermissionError:
        print("You need to be root for using installer")
        
def check_permission():
    if os.geteuid() != 0:
        raise PermissionError()