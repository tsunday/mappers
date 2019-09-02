# Development process

Welcome…

## Test suite

Requirements:

- [pyenv](https://github.com/pyenv/pyenv)
- [tox](https://tox.readthedocs.io)
- [vale](https://errata-ai.gitbook.io/vale)
- [node](https://nodejs.org)
- [sed](https://www.gnu.org/software/sed)

Running test suite:

```bash
tox
```

Code coverage…

## Documentation

We use:

- [mkdocs](https://www.mkdocs.org)
- [doctest](https://docs.python.org/3/library/doctest.html)

Running live-reloading server:

```bash
tox -e mkdocs -- serve
```

## Release

We use:

- [semantic-release](https://semantic-release.gitbook.io/semantic-release)
- [conventional-changelog](https://github.com/conventional-changelog/conventional-changelog)

Commit changes:

```bash
npx commit
```
