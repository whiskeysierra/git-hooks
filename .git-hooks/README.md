# ![Grappling hook](icon.png) Git Hooks [![Build Status](https://travis-ci.org/whiskeysierra/git-hooks-dispatcher.png?branch=master,develop)](http://travis-ci.org/whiskeysierra/git-hooks-dispatcher)

The Git Hooks is a small tool to simplify the work with git hooks. Git Hooks allows you to treat your git hooks
like any other source and track them in your repository. Additionally it supports multiple scripts to run
for the same hook, while plain old git only supports one; this is sometimes referred to as *chaining*.

## Requirements

- Python 2.6 or 2.7
 
To install the required python libraries run:
    
    sudo pip install -r requirements.txt

## Installation
First of all, if you are planning to use Git Hooks on a regular basis, consider installing the corresponding
[`git dispatcher`](https://github.com/whiskeysierra/git-dispatcher) tool. It's a custom git command which 
offers a simpler interface to install and manage git hooks in all of your projects.

To install and activate the Git Hooks dispatcher to one of your projects:

    git dispatcher install
    git dispatcher activate
    
or update

    git dispatcher update
    
or to deactivate and uninstall

    git dispatcher deactivate
    git dispatcher uninstall
    
For more details about the usage, please see the *Manual installation* section.

### Manual installation

Add the repository as a subtree in your existing repository:

    git subtree add --prefix .git-hooks --squash git@github.com:whiskeysierra/git-hooks.git master
    
Optionally, you may add a repository-wide git alias by running:

    .git-hooks/git-hooks.py alias
    
This shortens `.git-hooks/git-hooks.py <command>` to `git hooks <command>`.
    
The next step: Activate the dispatcher:

    git hook link

Your output should look something like this:

    $ git hooks link
    Linking .git-hooks/dispatcher.py to .git/hooks/applypatch-msg [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/pre-applypatch [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/post-applypatch [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/pre-commit [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/prepare-commit-msg [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/commit-msg [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/post-commit [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/pre-rebase [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/post-checkout [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/post-merge [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/pre-receive [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/update [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/post-receive [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/post-update [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/pre-auto-gc [done]
    Linking .git-hooks/dispatcher.py to .git/hooks/post-rewrite [done]
    
The dispatcher is now installed and fully operational. But we didn't create any hooks yet. You can either create
a hook manually:

    mkdir -p git-hooks/pre-commit.d
    vi git-hooks/pre-commit.d/my-hook.sh
   
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
    
Alternatively you may reuse some of the default hooks, shipped with this tool. You can find them in
[`.git-hooks/defaults`](https://github.com/whiskeysierra/git-hooks/tree/master/defaults).

If you want to pull the latest changes to the dispatcher, run:

    git subtree pull --prefix .git-hooks --squash git@github.com:whiskeysierra/git-hooks-dispatcher.git master

## Uninstall

To uninstall the dispatcher, use:

    git hooks unalias
    git hooks unlink
    
Which will remove all symlinks created by the dispatcher. Existing files or old symlinks will be left as-is.
You can now remove the subtree and commit the changes to your repository.

    git rm -r .git-hooks
    git commit -m "Removed Git Hooks"

## Contributing

The easiest way to contribute is use the dispatcher in your project and if you see the need to fix a bug
or add a feature, you can just do so and commit patches to the subtree in your repository. To push the 
changes back you'll need a fork and replace the origin url in the `git subtree` command with your own:

    git subtree push --prefix .git-hooks git@github.com:username/git-hooks.git
    
You can than just open a pull-request, which will be highly appreciated.

## Attributions
![Creative Commons License](http://i.creativecommons.org/l/by-sa/3.0/80x15.png)
Hook shot photo by [Rick Dikeman](http://commons.wikimedia.org/wiki/File:Basketball.jpg) is licensed under a
[Creative Commons (Attribution-ShareAlike 3.0 Unported)](http://creativecommons.org/licenses/by-sa/3.0/).

A good tutorial on the `git subtree` command can be found 
[here](http://blogs.atlassian.com/2013/05/alternatives-to-git-submodule-git-subtree/).

