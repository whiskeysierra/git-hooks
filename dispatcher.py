#!/usr/bin/env python

import os
import subprocess
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

hook = os.path.basename(sys.argv[0])
directory = os.path.join(parent, 'git-hooks', hook + '.d')

try:
    if not os.path.exists(directory):
        sys.exit(0)

    if not os.path.isdir(directory):
        sys.exit(0)

    for path, directories, scripts in os.walk(directory, followlinks=True):
        for script in sorted(scripts):
            code = subprocess.call([os.path.join(path, script)])
            if code is not 0:
                sys.exit(code)


except Exception, e:
    sys.stderr.write('%s\n' % e)
    sys.exit(1)