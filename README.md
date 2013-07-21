# ![Grappling hook](icon.png) Git Hooks [![Build Status](https://travis-ci.org/whiskeysierra/git-hooks-dispatcher.png?branch=master,develop)](http://travis-ci.org/whiskeysierra/git-hooks-dispatcher)

The Git Hooks Dispatcher is a small dispatcher scripts for your git hooks. 
It runs them for you and allows you to track your hooks together with 
your source code in your repository under a special directory (`git-hooks`).
Everything a new contributor needs to do after a `git clone` is:

    git-hooks-dispatcher/manage install

## Requirements

- Python 2.6 or 2.7
 
To install the required python libraries run:
    
    sudo pip install -r requirements.txt

## Installation
Add the repository as a subtree in your existing repository:

    git subtree add -P git-hooks-dispatcher git@github.com:whiskeysierra/git-hooks-dispatcher.git
    
Install the dispatcher

    git-hooks-dispatcher/manage install

Your output should look something like this:

    $ git-hooks-dispatcher/manage install
    Linking dispatcher to ../.git/hooks/applypatch-msg [done]
    Linking dispatcher to ../.git/hooks/pre-applypatch [done]
    Linking dispatcher to ../.git/hooks/post-applypatch [done]
    Linking dispatcher to ../.git/hooks/pre-commit [done]
    Linking dispatcher to ../.git/hooks/prepare-commit-msg [done]
    Linking dispatcher to ../.git/hooks/commit-msg [done]
    Linking dispatcher to ../.git/hooks/post-commit [done]
    Linking dispatcher to ../.git/hooks/pre-rebase [done]
    Linking dispatcher to ../.git/hooks/post-checkout [done]
    Linking dispatcher to ../.git/hooks/post-merge [done]
    Linking dispatcher to ../.git/hooks/pre-receive [done]
    Linking dispatcher to ../.git/hooks/update [done]
    Linking dispatcher to ../.git/hooks/post-receive [done]
    Linking dispatcher to ../.git/hooks/post-update [done]
    Linking dispatcher to ../.git/hooks/pre-auto-gc [done]
    Linking dispatcher to ../.git/hooks/post-rewrite [done]
    
The dispatcher is now installed and fully operational. But we didn't create any hooks yet.

    mkdir -p git-hooks/pre-commit.d
    echo '#!/bin/sh
    branch=$(git rev-parse --abbrev-ref HEAD)
        
    if [ ${branch} == "master" ]; then
        echo "You must not commit directly on the master branch." 1>&2
        echo "Stash your changes and apply them to another branch" 1>&2
        echo "git stash" 1>&2
        echo "git checkout <feature-xyz>" 1>&2
        echo "git stash pop" 1>&2
        exit 1
    fi' > git-hooks/pre-commit.d/enforce-feature-branch.sh
   
We just created a `pre-commit` hook which enforces feature branches by suppressing commits
on the `master` branch.
   
Basically, you'll need a directory `git-hooks` which contains one directory for each hook type
(empty directories can be omitted). Please note the `.d` at the end!

       |-git-hooks
       |---commit-msg.d
       |---post-merge.d
       |---pre-commit.d
       |---prepare-commit-msg.d
       
You may put one or more hooks into each directory, which will then be executed in sequence by the
dispatcher. To enforce a special ordering, name your scripts e.g. 
`001-enfore-feature.sh`, `002-check-permissions.sh`, etc.

If you want to pull the latest changes to the dispatcher, run:

    git subtree pull --prefix git-hooks-dispatcher git@github.com:whiskeysierra/git-hooks-dispatcher.git

Feel free to add a handy git alias for the last command to your `.git/config` or `~/.gitconfig` if you
find the command to noisy. I sure do ;)

    git config --global alias.update-dispatcher 'subtree pull -P git-hooks-dispatcher git@github.com:whiskeysierra/git-hooks-dispatcher.git master'
    git config --global alias.install-dispatcher 'subtree add -P git-hooks-dispatcher git@github.com:whiskeysierra/git-hooks-dispatcher.git master'

You can now install and update the dispatcher in any of your projects with:

    git install-dispatcher
    git update-dispatcher

## Uninstall

To uninstall the dispatcher, use:

    git-hooks-dispatcher/manage uninstall
    
Which will remove all symlinks created by the dispatcher. Existing files or old symlinks will be left as-is.
You can now remove the subtree and commit the changes to your repository.

    git rm -r git-hooks-dispatcher
    git commit -m "Removed Git Hooks Dispatcher"

## Contributing

The easiest way to contribute is use the dispatcher in your project and if you see the need to fix a bug
or add a feature, you can just do so and commit patches to the subtree in your repository. To push the 
changes back you'll need a fork and replace the origin url in the `git subtree` command with your own:

    git subtree push --prefix git-hooks-dispatcher git@github.com:username/git-hooks-dispatcher.git
    
You can than just open a pull-request, which will be highly appreciated.

## Attributions/Links
The Grappling Hook icon was found on [http://ztreasureisle.wikia.com/](http://ztreasureisle.wikia.com/wiki/File:NinjaGear_Grappling_Hook-icon.png).

A good tutorial on the `git subtree` command can be found 
[here](http://blogs.atlassian.com/2013/05/alternatives-to-git-submodule-git-subtree/).

