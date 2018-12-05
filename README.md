## grst ##

> Get status information showing the local git repository.

#### Usage ####

```
Usage: grst [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  add     Add the repository.
  remove  Remove the repository from grst.
  status  Check the status of the repository.
```

#### Output ####

The output format of grst is:

```
status_prefix path (branch)
```

Among them, the possible values of `status_prefix` indicate:

```
S(Green) - The work tree is clean and synchronized with the tracked branch.
C(Blue)  - The work tree is clean but not synchronized with the tracked branch.
M(Red)   - Uncommitted changes in the work tree.
```

In particular, if the local branch is to track remote branches, then `C` will be upgraded to `S`.

For local branches that do not track remote branches, you can make them track remote branches by the following command:

```
git branch -u remote branch
```

#### Install ####

Install by downloading the source code.

```
$ git clone https://github.com/rgb-24bit/grst.git
$ cd grst
$ python setup.py install
```

#### User file ####

Grst will use a file to record the location of the local repository, which is located on a different system:

- **Windows**: `%USERPROFILE%/.gitrepositories`
- **Unix/Linux/Mac**: `$HOME/.gitrepositories`

