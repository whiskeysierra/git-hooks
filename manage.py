#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

from __future__ import print_function, unicode_literals

import argparse
import git
import os
import sys

from clint.textui.colored import yellow, green, red


def parse():
    parser = argparse.ArgumentParser(description='Manages all git hooks for the current repository.')
    commands = parser.add_subparsers(help='commands')

    link = commands.add_parser('link', help='Links the dispatcher to all available git hooks.')
    link.set_defaults(command='link')

    unlink = commands.add_parser('unlink', help='Unlinks the dispatcher from all available git hooks.')
    unlink.set_defaults(command='unlink')

    return parser.parse_args()

args = parse()

repo = git.Repo()
root = repo.working_dir
current = os.path.dirname(os.path.realpath(__file__))

hooks = [
    'applypatch-msg',
    'pre-applypatch',
    'post-applypatch',
    'pre-commit',
    'prepare-commit-msg',
    'commit-msg',
    'post-commit',
    'pre-rebase',
    'post-checkout',
    'post-merge',
    'pre-receive',
    'update',
    'post-receive',
    'post-update',
    'pre-auto-gc',
    'post-rewrite',
]


def relativize(path):
    return os.path.relpath(path, current)


try:
    hook_directory = os.path.join(root, '.git', 'hooks')
    dispatcher = os.path.join(current, 'dispatcher')

    if not os.path.exists(hook_directory):
        raise IOError('%s does not exist' % hook_directory)

    if not os.path.isdir(hook_directory):
        raise IOError('%s is not a directory' % hook_directory)

    def link():
        for hook in hooks:
            target = os.path.join(hook_directory, hook)

            if os.path.islink(target) and os.path.realpath(target) == dispatcher:
                # we can savely assume, we created it in the first place
                os.unlink(target)

            if os.path.exists(target):
                # exists and is not one of our symlinks, leave it alone!
                state = yellow('exists')
            else:
                try:
                    os.symlink(dispatcher, target)
                    state = green('done')
                except OSError:
                    state = red('failed')

            print('Linking %s to %s [%s]' % (relativize(dispatcher), relativize(target), state))

    def unlink():
        for hook in hooks:
            target = os.path.join(hook_directory, hook)

            if os.path.islink(target) and os.path.realpath(target) == dispatcher:
                try:
                    # we can savely assume, we created it in the first place
                    os.unlink(target)
                    state = green('done')
                except OSError:
                    state = red('failed')
            else:
                # exists and is not one of our symlinks, leave it alone!
                state = yellow('skipped')

            print('Unlinking %s [%s]' % (relativize(target), state))

    def unknown():
        raise Exception('Not yet implemented: %s' % args.command)

    mapping = {
        'link': link,
        'unlink': unlink
    }

    action = mapping.get(args.command, unknown)
    action()
except Exception, e:
    sys.stderr.write('%s\n' % e)
    sys.exit(1)