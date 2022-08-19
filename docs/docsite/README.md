Quantum documentation
=====================

This project hosts the source behind [docs.quantum.com](https://docs.quantum.com/).

To create clear, concise, consistent, useful materials on docs.quantum.com, please refer to the following information.


About Quantum
-------------
Quantum is an IT automation tool. It can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates. Learn more about Quantum [here](https://docs.quantum.com/quantum/latest/index.html).

To install Quantum, see the [Installation Guide](https://docs.quantum.com/quantum/latest/installation_guide/intro_installation.html).

The following sections provide information and resources on contributing to Quantum documentation.

Contributions
=============
Quantum documentation is written in ReStructuredText(RST). Contributions to the documentation are welcome.

The Quantum community produces guidance on contributions, building documentation, and submitting pull requests, which you can find in [Contributing to the Quantum Documentation](https://docs.quantum.com/quantum/latest/community/documentation_contributions.html).

Filing issues
-------------
If you do not want to learn the reStructuredText format, you can also [file issues] about documentation problems on the Quantum GitHub project.

Editing docs directly on GitHub
-------------------------------
For typos and other quick fixes, you can edit the documentation right from the site. See [Editing docs directly on GitHub](https://docs.quantum.com/quantum/devel/community/documentation_contributions.html#editing-docs-directly-on-github) for more information.

Quantum style guide
===================

To create clear, concise, consistent, useful materials on docs.quantum.com, follow the guidelines found in the [Quantum Style Guide](https://docs.quantum.com/quantum/latest/dev_guide/style_guide/index.html#linguistic-guidelines).

reStructuredText
----------------
The Quantum style guide also includes useful guidelines on writing in reStructuredText. Please see the style guide for reStructuredText formatting guidelines for:
* header notation
* internal navigation
* linking
* local table of contents


Tools
=====

The Quantum community provides resources on tools used to write, test, and build documentation. In this section you will find some helpful links and workflow recommendations to get started writing or editing documentation.

Popular editors
---------------
The Quantum community uses a range of tools for working with the Quantum project. Find a list of some of the most popular of these tools [here](https://docs.quantum.com/quantum/latest/community/other_tools_and_programs.html#popular-editors).

Building documentation
----------------------
Building the documentation is the best way to check for errors and review your changes. Quantum documentation is built using Sphinx. For resources on Sphinx and building documentation, see [building the documentation locally](https://docs.quantum.com/quantum/latest/community/documentation_contributions.html#building-the-documentation-locally) in the Quantum Community Guide.

Github
------
[Quantum documentation](https://github.com/quantum/quantum/tree/devel/docs/docsite) is hosted on the Quantum Github project.

The following sections describe the workflows required to start developing or submit changes to Quantum documentation.


## Setting up Git


GitHub provides a set of [Git cheatsheets](https://github.github.com/training-kit/) in multiple languages.

1. First [Install Git](https://help.github.com/en/articles/set-up-git)

2. Perform the initial Git setup tasks, as described in [First Time Git Setup](link:https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup).

3. Navigate to https://github.com/quantum/quantum and [create a fork](https://help.github.com/en/articles/fork-a-repo). This will create your own version of the repository which you can find at https://github.com/{yourusername}/quantum where {yourusername} is the username you created in GitHub.

4. [Clone](https://help.github.com/en/articles/cloning-a-repository) from your fork to create a copy on your local machine.

  NOTE: It is possible to clone using SSH so you don't have to enter a username/password every time you push. Find instructions at [Connecting to GitHub with SSH](https://help.github.com/articles/connecting-to-github-with-ssh/) and [Which Remote URL Should I Use](https://help.github.com/articles/which-remote-url-should-i-use/). When using SSH, the origin lines will appear like this:
`git@github.com:{yourusername}/quantum.git`


```
$ git clone  git@github.com:{yourusername}/quantum.git
```

5. Navigate to the new directory by entering the following from the command line on your local machine:
```
$ cd {repository-name}
```

6. Add a git remote to your local repository to link to the upstream version of the documentation. This makes it easier to update your fork and local version of the documentation.
```
$ git remote add upstream git://github.com/quantum/quantum.git
```

7. Check your settings.
```
$ git remote -v
origin    https://github.com/{YOUR_USERNAME}/{YOUR_FORK}.git (fetch)
origin    https://github.com/{YOUR_USERNAME}/{YOUR_FORK}.git (push)
upstream  https://github.com/{ORIGINAL_OWNER}/{ORIGINAL_REPOSITORY}.git (fetch)
upstream  https://github.com/{ORIGINAL_OWNER}/{ORIGINAL_REPOSITORY}.git (push)
```

## Creating a topic branch

Create a topic branch for new documentation submissions or larger changes.

1. Fetch updates from ``origin``:
```
$ git fetch origin
```
2. Checkout a new branch based on ``devel``:
```
$ git checkout -b {branch name}
```
3. Create new documents or make changes to existing files.
4. Add new or changed files:
```
$ git add {file name}
```
5. Commit your changes or additions. Be sure to include a commit message:
```
$ git commit -m "new message"
```
6. Push your updates back to `origin`:
```
$ git push -u origin {branch name}
```

Once you have completed this workflow, it is a good idea to build the documentation and ensure everything is correct and that it works. As a contributor, you are required to prove that See [building the documentation locally](https://docs.quantum.com/quantum/latest/community/documentation_contributions.html#building-the-documentation-locally) in the Quantum Community Guide for more on building documentation.


When final additions or changes are pushed back to your fork you can open a pull request (PR).


Working with pull requests (PRs)
--------------------------------
Pull requests represent the stage in a contribution where you are ready to submit your work for review and inclusion in the documentation. When a PR is opened, a reviewer will check the work and potentially open a dialog around your proposed changes. PRs should include specific information, which you can find in [Opening a new issue and/or PR](https://docs.quantum.com/quantum/latest/community/documentation_contributions.html#opening-a-new-issue-and-or-pr) in the Quantum Community Guide.

## Creating a pull request
1. Navigate to your personal fork: https://github.com/{yourusername}/quantum
2. Click **Pull requests** and then click **New pull requests**.
3. Use the drop-down menus, set the **base repository** to the stable branch and set the **head repository** to your topic branch.
4. Apply appropriate labels. Include **backport** and **documentation**.
6. Fill in the PR summary using the following template:

```
##### SUMMARY

##### ISSUE TYPE

##### COMPONENT NAME
docs.quantum.com
##### ANSIBLE VERSION

##### ADDITIONAL INFORMATION

```
NOTE:
If you put 'closes <issuenumber> '  in the summary, quantum will automatically close the issue on merge.

7. Click **Create pull request**.


A reviewer will evaluate your contribution. They may open a dialog around the PR and suggest revisions or, if the PR meets acceptance criteria, will merge it to the base branch.

## Backporting a pull request

All Quantum PRs must be merged to the `devel` branch first. Most users may, however, use a prior stable branch. Evaluate your pull request to determine if it applies to a prior branch.  

See [Backporting merged PRs](https://docs.quantum.com/quantum/devel/community/development_process.html?highlight=backport#backporting-merged-prs) for a complete worklfow.

## Other Git workflows

In addition to creating a pull request and backporting, other workflows exist to help keep your topic branches and pull requests up-to-date. See the [Developer Guide](https://docs.quantum.com/quantum/devel/dev_guide/developing_rebasing.html) on `git rebase` to learn more about rebasing a pull request.
