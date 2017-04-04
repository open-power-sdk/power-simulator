#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (C) 2017 IBM Corporation

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Rafael Peria de Sene <rpsene@br.ibm.com>
'''

import sys
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import pkg_resources
import controller

__all__ = []
__version__ = pkg_resources.require("mambo")[0].version


class CLIError(Exception):
    """Error treatment"""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    """Start Simulator Main Function"""
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_version = "v%s" % __version__
    program_version_message = '%%(prog)s %s ' % (program_version)
    program_shortdesc = '''
    --- IBM POWER Functional Simulator ---
    Configures and starts the IBM POWER8 and POWER9 Functional Simulator
    '''
    try:
        parser = ArgumentParser(description=program_shortdesc,
                                formatter_class=RawTextHelpFormatter)
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-V', '--version',
                           action='version',
                           version=program_version_message)
        group.add_argument('-i', '--install', dest="install",
                           action='store_true',
                           help='install the simulator and its dependencies\n')
        group.add_argument('-s', '--start', dest="start",
                           default=None, choices=['power8', 'power9'],
                           help='start the a selected version of the simulator\n')
        # Process arguments
        args = parser.parse_args()
        if not (args.install or args.start):
            parser.error('no action set, select either -i/--install or -s/--start.\
                        \ne.g: mambo -i/--install\
                        \n     mambo -s/--start [power8 or power9]')
            parser.print_help()
        else:
            controller.run(args)
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
