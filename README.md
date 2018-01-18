# Sansible Scaffold

[![Build Status](https://travis-ci.org/sansible/sansible.svg?branch=scaffold)](https://travis-ci.org/sansible/sansible)  

* [TL;DR](#tldr)
* [Rationale](#rationale)
* [Requirements](#requirements)
* [Creating Your Role](#creating-your-role)
* [Testing Your Role](#testing-your-role)
* [pre-commit Integration](#pre-commit-integration)
* [Travis CI Integration](#travis-ci-integration)


## Rationale

This repository aims to provide an easy-to-use template for the creation of new
[SAnsible roles](https://github.com/sansible).

It uses [molecule](http://molecule.readthedocs.io/) to orchestrate testing, and
[testinfra](https://testinfra.readthedocs.io/) for verification.

The tests described herein provide support for [Ubuntu Long Term Support releases](https://wiki.ubuntu.com/LTS),
currently [Ubuntu 14.04 Trusty Tahr](https://wiki.ubuntu.com/TrustyTahr/ReleaseNotes) (until April 2019) and
[Ubuntu 16.04 Xenial Xerus](https://wiki.ubuntu.com/XenialXerus/ReleaseNotes) (until April 2021), though support
for other distributions can easily be added.

It features a [Makefile](https://www.gnu.org/software/make/) for ease of use, [Travis CI](https://travis-ci.org/)
integration, and an optional, but recommended, [pre-commit](http://pre-commit.com/) configuration for linting and
verification, which can also be installed as a [git pre-commit hook](https://git-scm.com/docs/githooks).

**NOTE:** While this README assumes you are using docker and testinfra for testing, molecule provides drivers for
[a variety of local and cloud
virtualisation technologies](http://molecule.readthedocs.io/en/latest/configuration.html#driver), and also
alternatively supports the [goss testing framework](https://goss.rocks/).  However, providing instructions to that
end are outside the scope of this document.


## Requirements

* [docker](https://www.docker.com/)
* make
* pre-commit (optional, but recommended)
* [python 2.7](https://www.python.org/) (python version 2.6 and older and python 3 is **not** supported)
  * [pip](https://pip.pypa.io/)
  * [virtualenv](https://virtualenv.pypa.io/)

And whatever is required to install the molecule and [docker-py](https://docker-py.readthedocs.io/) python
packages and their dependencies on your machine.


## Creating Your Role

Create a new repository `http://github.com/sansible/<your_repo>` and initialise it with a `master` and `develop`
branch.  Then copy the scaffold repository and point it to your `develop` branch:

```Bash
curl -L https://github.com/sansible/sansible/archive/scaffold.tar.gz | tar xz --strip=1 -
git init
git checkout -b develop
git remote add origin http://github.com/sansible/<your_repo>
git add -A
git commit -m "Original Copy from SAnsible Scaffold"
git push -f -u origin develop
```

You are now ready to work on your role!

Modify `meta/main.yml` to suit your role.  Comments in the file provide basic guidance; further information on Galaxy
meta data can be found [on the Ansible Galaxy website](https://galaxy.ansible.com/intro#meta).

Create your [Ansible role the usual way](http://docs.ansible.com/ansible/latest/playbooks_reuse_roles.html); any valid
role should work with this scaffold.  Use a `sansible_` prefix for your variables, i.e. `sansible_yourrole`.

Should your role require external python packages, add these to `requirements.txt`.  Make sure the `LICENSE` is correct
and modify `README.template` to accurately describe your new role, then delete _this_ file and rename `README.template`
to `README.md`.

After [testing your role](#testing-your-role), enable [enable integration with Travis CI](#travis-ci-integration).
Make sure to [check your role for errors before committing](#pre-commit-integration) your changes!

Once your role has been committed to `development`, follow  the process outlined in the
[main SAnsible repo README](https://github.com/sansible/sansible#merges-and-releases) to release your role.


## Testing Your Role

Testing is [orchestrated by molecule](#molecule-configuration), validation
[handled by testinfra](#testinfra-configuration), both of which and their dependencies are installed into a virtualenv.
Common tasks are made available through simple `make` commands; the virtualenv can be accessed directly by executing
`make activate`.

`make all` is the one-step command to test your role; execute `make clean` to clean up afterwards.

By default, testing will be performed with Ansible 2.2.3.0, but you can force the use of another Ansible version by
setting the `ANSIBLE_INSTALL_VERSION` environment variable to a different version, e.g. `2.4.2.0`.

**CAVEAT:** The version must be available from pip.  You can use the following command to quickly fetch a list of
all Ansible 2.2-2.4 versions available from pip:

```Bash
ANSIBLE_PIP_VERSIONS=`curl -s https://pypi.python.org/pypi/ansible/json`; for I in 2.{2..4}; do echo ${ANSIBLE_PIP_VERSIONS} | jq --arg ver ${I} -r '[.releases | keys | sort[] | select(startswith($ver))][-1]'; done
```


### molecule Configuration

molecule will perform tasks in _scenarios_.  A scenario is simply a subdirectory of the `molecule/` directory
containing a molecule configuration.  At least one scenario needs to be present; the default scenario is aptly named
`default`.

Change **ROLE_NAME** to the name of your new role in the following files:

    * `molecule/default/molecule.yml` (two occurrences)
    * `molecule/default/playbook.yml`

During `make test`, the following tasks will be executed:

* Lint YAML files (see the _lint_ section of `molecule/default/molecule.yml`)
* Resolve role dependencies (see `meta/main.yml` and the _dependency_ section of `molecule/default/molecule.yml`)
* Check Ansible syntax (see the _provisioner_ section of `molecule/default/molecule.yml`)
* Create docker containers (see `molecule/default/create.yml` and the _driver_ and _platforms_ sections of
  `molecule/default/molecule.yml`)
* Prepare docker containers (see `molecule/default/prepare.yml`)
* Apply your role to docker containers (see `molecule/default/playbook.yml` and the _provisioner_ section of
  `molecule/default/molecule.yml`)
* Ensure idempotence
* Inject side effects; this is disabled by default (see
  [the Ansible Provisioner documentation](http://molecule.readthedocs.io/en/latest/configuration.html#provisioner)
  for details
* Verify state of docker containers via testinfra (see `molecule/default/tests/test_default.py` and the _verifier_
  section of `molecule/default/molecule.yml`)

The destruction of docker containers is handled by `molecule/default/destroy.yml`.


### testinfra Configuration

testinfra is a python library inspired by [Test Kitchen](http://kitchen.ci/).  It allows easy testing of common
settings (file permissions, installed packages, open ports, running processes...), but allows the use of python to
extend tests and write entirely new ones.  A simple example can be found in `molecule/default/tests/test_default.py`.

**NOTE**: Only tasks run through the _testinfra_ library are executed on the docker container, all other code is
executed on the host machine.  If you want to use additional python libraries in your tests, add them to
`requirements.txt`.

See [the testinfra documentation](https://testinfra.readthedocs.io/) for reference.


### `make` Commands

#### `make all`

Executes `make deps`, then `make test`

#### `make activate`

Drops you into the virtualenv created by `make deps`.  _Ctrl+d_ to exit.

#### `make clean`

Executes `make destroy`, removes the virtualenv, molecule temp files, and python bytecode (`.pyc`) files.

#### `make deps`

Creates a python virtualenv and installs dependencies required for testing your role.

#### `make destroy`

Destroys all existing docker containers created while testing your role.

#### `make test`

Executes `molecule test` (see above for details)

#### `make watch`

Monitors role directories and molecule files, and executes `make test` on any change.


## pre-commit Integration

pre-commit is an easy way to run one or more linters before committing changes, supporting
[a large variety of hooks](http://pre-commit.com/hooks.html).

It can be installed for the current user via `pip install --user pre-commit` (no root access required).  

Run `pre-commit install` to install pre-commit into your git hooks.  If you want to manually run all pre-commit hooks
on a repository, execute `pre-commit run --all`.

The configuration is read from `.pre-commit-config.yaml`, which has been pre-configured for
[ansible-lint](https://github.com/willthames/ansible-lint) (with exceptions for non-standard Travis CI and molecule
YAML files), [check-json](https://github.com/pre-commit/pre-commit-hooks), [flake8](http://flake8.pycqa.org/),
and [trailing-whitespace](https://github.com/pre-commit/pre-commit-hooks).  More linters can easily be added; see
[the pre-commit website](http://pre-commit.com/) for futher information on this and other pre-commit matters.

**NOTE:** Running a hook for the first time may be slow, since pre-commit will install all dependencies (for example,
if a hook requires node.js, and the machine does not have node.js installed, pre-commit will download and build it;
software installed this way will be re-used across pre-commit installations).


## Travis CI Integration

The section in `.travis.yml` that relevant to testing your role on docker containers is _env_.  This section
contains a list of Ansible versions with which your role will be tested.  Add or remove as many versions as you like
here, but remember that all versions must be available from pip.  Further documentation on availabe options in
`.travis.yml` can be found [on the Travis CI website](https://docs.travis-ci.com/user/customizing-the-build/).

**ToDo:** Add doco as to how enable Travis for a rep.


## TL;DR

1) Clone the _scaffold_ branch of this repository, then change the origin to your repository; work on the `development`
   branch.

2) Add information about your role and any potential Ansible Galaxy dependencies to `meta/main.yml`.

3) Add your role's functionality.  Ensure you use a `sansible_` prefix for your variables, i. e. `sansible_yourrole`.

4) Change **ROLE_NAME** to the name of your new role in the following files:

    * `molecule/default/molecule.yml` (two occurrences)
    * `molecule/default/playbook.yml`

5) Modify `molecule/default/tests/test_default.py` to test your role.

6) Run `make all` to test your new role using Ansible 2.2.3 on Ubuntu Trusty Tahr and Xenial Xerus, or `make deps`,
   then `make watch` to re-run all tests every time a file is changed.  Once you're happy, run `make clean` to destroy
   the docker containers used to test the role and clean up the working directory.

7) Delete _this_ file, rename `README.template` to `README.md` and modify it to describe your new role.

8) Enable Travis CI for your repository, lint the files in your working directory (hint: pre-commit), then commit
   your changes.

9) Follow the process outlined in the
   [main SAnsible repo README](https://github.com/sansible/sansible#merges-and-releases) to release your role.
