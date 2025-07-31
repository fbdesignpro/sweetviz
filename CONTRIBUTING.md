# Contributing to Sweetviz

First off, thank you for considering contributing to Sweetviz! It's people like you that make Sweetviz such a great tool.

## Where do I go from here?

If you've noticed a bug or have a feature request, [make one](https://github.com/fbdesignpro/sweetviz/issues/new)! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

### Fork & create a branch

If this is something you think you can fix, then [fork Sweetviz](https://github.com/fbdesignpro/sweetviz/fork) and create a branch with a descriptive name.

A good branch name would be (where issue #38 is the ticket you're working on):

```sh
git checkout -b 38-add-feature-x
```

### Get the code

```sh
git clone https://github.com/your-username/sweetviz.git
cd sweetviz
git remote add upstream https://github.com/fbdesignpro/sweetviz.git
```

### Create a virtual environment and install dependencies

```sh
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
```

### Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first :smile_cat:

### Make a pull request

At this point, you should switch back to your master branch and make sure it's up to date with Sweetviz's master branch:

```sh
git remote add upstream https://github.com/fbdesignpro/sweetviz.git
git checkout master
git pull upstream master
```

Then update your feature branch from your local copy of master, and push it!

```sh
git checkout 38-add-feature-x
git rebase master
git push --force-with-lease origin 38-add-feature-x
```

Finally, go to GitHub and [make a Pull Request](https://github.com/fbdesignpro/sweetviz/compare)

### Keeping your pull request up to date

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

To learn more about rebasing, check out [this guide](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase).

Once you've rebased your branch, you'll have to force-push to GitHub.

```sh
git push --force-with-lease origin 38-add-feature-x
```

## How to get help

If you're running into problems, please don't hesitate to ask for help in the [issue tracker](https://github.com/fbdesignpro/sweetviz/issues) or in the [discussions](https://github.com/fbdesignpro/sweetviz/discussions).

## Releasing a new version

If you are a maintainer, here's how to release a new version:

1.  Update the version number in `pyproject.toml`.
2.  Create a new entry in `CHANGELOG.md`.
3.  Commit the changes with a message like `Release 2.3.2`.
4.  Tag the commit with the version number: `git tag -a v2.3.2 -m "Version 2.3.2"`.
5.  Push the changes and the tag: `git push && git push --tags`.
6.  Build the package: `python -m build`.
7.  Publish the package to PyPI: `twine upload dist/*`.
