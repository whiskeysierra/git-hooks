#!/bin/sh

set -e

branch=$(git rev-parse --abbrev-ref HEAD)

if [ ${branch} == develop ]; then
    echo "You must not commit directly on the develop branch." 1>&2
    echo "Stash your changes and apply them to another branch" 1>&2
    echo "git stash" 1>&2
    echo "git checkout <branch>" 1>&2
    echo "git stash pop" 1>&2
    exit 1
fi