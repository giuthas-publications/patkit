# PATKIT development guide

## Code conventions

These are guidelines, not a ruleset.

First things first: write in good pythonic style.

- [PEP 8](https://www.python.org/dev/peps/pep-0008/) outlines the general
  style.
  - Most of these guidelines can be followed automatically by using the
    [autopep8](https://pypi.org/project/autopep8/) and Pylint packages to
    format code.
- [PEP 257](https://www.python.org/dev/peps/pep-0257/) talks about conventions
  for docstrings. In addition, we might do the following:
  - Consider what will look good once the docs are compiled.
  - If we are using pdoc, repeating the same thing for a class docstring and
      the constructor is not a good idea. Instead, write general description in
      the class docstring and describe arguments and such in the constructor's
      docstring. This way they'll also make sense when reading the source.
  - Besides docstrings write other comments too.

Also follow the [Zen of Python](https://www.python.org/dev/peps/pep-0020/) with
the following additions:

- Getting it done is better than making it perfect (because getting it perfect
  won't happen).
- A module is the unit of reuse. Ideally, a module should do something that
  gets used time and time again, but it is good enough if it does something
  which has a clear and self-contained purpose. Prefer splitting to smaller
  modules over piles of unrelated code.

## Packages and modules

In Python a module is -- [roughly
speaking](https://docs.python.org/3/reference/import.html#packages) -- any .py
file and a regular package is a directory that contains a `__init__.py` file
and possibly some other `.py` files. In PATKIT `__init__.py` files are used for
two purposes: Defining the public API of the module and running any
initialization that is needed. For an example have a look at
`patkit/__init__.py`.

We'll try to do imports mainly as absolute imports with the exception that
`__init__.py` files will import modules from the local directory with `from
.local_module import functions_to_be_part_of_public_interface`.

## Versioning

We use [SemVer](http://semver.org/) for versioning under the rules as set out
by [PEP 440](https://www.python.org/dev/peps/pep-0440/) with the additional
understanding that releases before 1.0 (i.e. current releases at time of
writing) have not been tested in any way.

For the versions available, see the [tags on this
repository](https://github.com/giuthas/patkit/tags).

## PATKIT's branches

PATKIT uses gitflow as the branching convention (until we have a reason for
doing something else). This means we have the following kinds of branches:

- `main` is the release branch. Any update here after 1.0 will get its own
  version number and be considered a new version of PATKIT. See
  [Versioning](#versioning) above.
- `devel` is the main development branch. New features are added by branching
  from devel, working on the feature branch, and merging back to devel before
  creating a release branch that will be merged in to main to do the actual
  release.
- Feature branches are used to develop a major feature. They may have
  subbranches as needed.
- Release branches are branched from `devel` when all of the features for a
  release have been implemented and merged back to `devel`. After creating the
  release branch, `main` is merged in to the release branch and any problems
  ironed out before creating the actual release by merging into main. If any
  commits need to be made before merging into `main`, a merge back to `devel`
  needs to also be done.
- Hotfix branches can be branched off of any branch, but especially if branched
  from main they need to eventually be merged to both main *and* devel.
  Hotfixes are always small bug fixes never major features.

### Making a release

A release of PATKIT is created as following these steps.

In the fork repository:
1. If planning a major or minor release (first or second version number
   increments), check that all features in the current roadmap are either
   done (implemented and merged to local `devel`, after which you should 
   delete the feature branch: `git push -d <remote_name> <branchname>` and 
   `git branch -d <branchname`)), or that all undone features are
   moved to the next release's roadmap.
   - This applies from version 1.0. Before that the roadmap is for 1.0 and
     minor releases are done when significant parts have been updated without
     fulfilling all of the promises in the roadmap.
   - Check that there are no `# TODO [version number]:` comments (like `TODO 0.11:`) 
     left for the version being released. If you find any either finish them or move 
     them to a later version. Mostly these should be just documentation, but one 
     never knows.
   - This is done in the `devel` branch.
2. Update documentation and bump version number.
   - Version number lives in [pyproject.toml](../pyproject.toml).
     - File version number will be different from program version number after
       1.0 and this is set in constants.py.
   - [Changelog](Changelog.markdown)
   - [Generated documentation](../devel/doc_generation_commands)
3. Send a pull request to the main repo.
4. After the new version has been released there are some housekeeping steps to
   perform in the fork repository. They are listed at the end of these instructions
   below.

In the main repository (done by Pertti or other maintainers):
1. Process the pull request.
2. Create a new release candidate branch named 'vX.Y.Z' e.g. 'v0.7.0' from the
   `devel` branch.
   - You can save a bit of work by keeping this branch only local unless the 
     release does not get done in one working session. 
3. Merge `main` to the release branch (not the other way around).
4. Check that installation works: `uv tool install .`
  - TODO 0.23: This does not actually work because it installs from pypi rather
    than from the local dir.
5. Run tests.
   - These don't exist yet at the time of PATKIT 0.10.0 except as
     'rudimentary_tests.sh'.
6. Fix any bugs that occur, run tests to see that they pass, update the docs.
   - Check if [Changelog](Changelog.markdown) needs any final updates.
     - Check also if any of the old 'known issues' or 'bugs' got fixed.
   - Rerun doc generation if there were any changes.
7. Merge release branch to `main`.
8. Release housekeeping:
   - Delete the now defunct release branch (`git push -d <remote_name>
   <branchname>` and `git branch -d <branchname`)
   - Tag the commit in main with the release title ('vX.Y.Z') and push it to
     remote with `git push --atomic origin main vX.Y.Z`
   - If any commits were made to the release branch, merge `main` into `devel`.
9. Check that the new version shows correctly on GitHub as 'latest' in the
   sidebar.
10. Check that the new version is on PyPi.
11. Announce the release.

In the fork repository:
1. Synch both `main` and `devel` with the main repository.
2. Pull from `main` and `devel` to your local machine.
3. If you have `patkit` installed as a tool, update it.