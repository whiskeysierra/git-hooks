#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

from __future__ import print_function, unicode_literals

import argcomplete
import argparse
import git
import os
import sys

from clint.textui.colored import green, red, yellow


# TODO usage/help/description
def parse():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers()

    alias = commands.add_parser('alias')
    alias.set_defaults(command='alias')

    state = commands.add_parser('state')
    state.set_defaults(command='state')

    unalias = commands.add_parser('unalias')
    unalias.set_defaults(command='unalias')

    link = commands.add_parser('link')
    link.set_defaults(command='link')

    unlink = commands.add_parser('unlink')
    unlink.set_defaults(command='unlink')

    argcomplete.autocomplete(parser)
    return parser.parse_args()


args = parse()

repo = git.Repo()
root = repo.working_dir

hooks_directory = os.path.join(root, '.git', 'hooks')

current = os.path.dirname(os.path.realpath(__file__))
dispatcher = os.path.join(current, 'dispatcher.py')

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
    return os.path.relpath(path, root)


def alias():
    config = repo.config_writer(config_level='repository')

    if not config.has_section('alias'):
        config.add_section('alias')

    if not config.has_option('alias', 'hooks'):
        config.set('alias', 'hooks', '!%s' % relativize(__file__))


def state():
    config = repo.config_writer(config_level='repository')

    if not config.has_section('alias'):
        sys.exit(1)

    if not config.has_option('alias', 'hooks'):
        sys.exit(1)


def unalias():
    config = repo.config_writer(config_level='repository')

    if config.has_option('alias', 'hooks'):
        config.remove_option('alias', 'hooks')


def link():
    for hook in hooks:
        target = os.path.join(hooks_directory, hook)

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
        target = os.path.join(hooks_directory, hook)

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


actions = {
    'alias': alias,
    'state': state,
    'unalias': unalias,
    'link': link,
    'unlink': unlink,
}


def unknown():
    raise RuntimeError("Unknown command '%s'" % args.command)


def on_error(message):
    sys.stderr.write(str(message) + '\n')


# see http://www.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3
try:
    action = actions.get(args.command, unknown)
    action()
except git.exc.GitCommandError, e:
    on_error(e.stderr)
    sys.exit(64)
except Exception, e:
    on_error(e)
    sys.exit(70)