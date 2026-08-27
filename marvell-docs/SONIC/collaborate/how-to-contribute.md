# How to Contribute

Prestera SONiC follows the upstream SONiC community contribution practices.
This page summarizes the [pull request
process](https://github.com/sonic-net/SONiC/wiki/Becoming-a-contributor#pull-request-process)
from the SONiC wiki and adds Marvell-specific guidance for Prestera SONiC
development.

For broader context on joining the SONiC community, legal requirements (ICLA),
and other ways to contribute, see [Becoming a
contributor](https://github.com/sonic-net/SONiC/wiki/Becoming-a-contributor)
on the SONiC wiki.

## Contributing to Prestera SONiC

Most Prestera SONiC changes are made in Marvell-maintained repositories rather
than upstream *sonic-net* repositories. The top-level build repository is
[marvell-sonic-buildimage](https://github.com/MarvellEmbeddedProcessors/marvell-sonic-buildimage).

Raise pull requests against the **release branch** that matches the Prestera
SONiC release you are targeting. See [Details](../releases/details.md) for the
current release branches. For example, changes for release tag
`rls-01.202511.01` are submitted to the `rls-202511.01` branch on
[marvell-sonic-buildimage](https://github.com/MarvellEmbeddedProcessors/marvell-sonic-buildimage/tree/rls-202511.01).

Submodule-specific code changes belong in the corresponding Marvell repository
when one exists. See [Prestera SONiC
Repos](../developers/know-marvell-sonic-repositories.md#prestera-sonic-repos) for
the list of Marvell repositories.

If you do not find a Marvell-specific repository for a particular submodule,
reach out to the **Marvell sales team** for guidance before starting
development.

## Pull Request Process

The steps below follow the upstream SONiC community process for raising a pull
request.

1. **Fork the repository** you want to change. For example, to change
   *marvell-sonic-buildimage*, go to
   [github.com/MarvellEmbeddedProcessors/marvell-sonic-buildimage](https://github.com/MarvellEmbeddedProcessors/marvell-sonic-buildimage)
   and click **Fork**. If you have already forked that repository, rebase your
   fork to sync with the latest upstream, or delete and re-fork if needed.

2. **Clone your fork** and change to the base directory.

   ```bash
   git clone https://github.com/<Your_Username>/marvell-sonic-buildimage.git
   cd marvell-sonic-buildimage
   ```

3. **Create a branch** in your fork. Use a short, meaningful branch name.

   ```bash
   git checkout -b <your_branch_name>
   ```

4. **Make your changes** — add, modify, or delete files as needed. Review and
   test your changes before pushing.

5. **Check what will be committed.**

   ```bash
   git status
   ```

   Confirm that only the intended files are listed.

6. **Stage and commit** your changes.

   ```bash
   git add .
   git commit -m "<brief explanation of the change>"
   ```

7. **Push the branch** to your fork.

   ```bash
   git push --set-upstream origin <your_branch_name>
   ```

8. **Open the pull request** on GitHub. Go to your fork in the browser; GitHub
   shows a **Compare & pull request** option for your recent push. Click it to
   create the PR against the correct release branch on
   *marvell-sonic-buildimage* (or the appropriate Marvell submodule
   repository).

9. **Add labels** for the feature or fix, where applicable.

10. **Fill in the pull request description** with enough detail for reviewers to
    understand the change, how it was tested, and any dependencies on other
    pull requests.

11. **Follow up on review.** Address review comments and work with repository
    maintainers to get the pull request merged.

If your change updates or adds CLI commands, update the [Command
Reference](https://github.com/sonic-net/sonic-utilities/blob/master/doc/Command-Reference.md)
in the appropriate repository as part of the same contribution.

## Upstreaming to SONiC

Marvell plans to upstream Prestera SONiC features to the community SONiC
codebase over time. When a feature is ready for upstream, follow the same pull
request process on the relevant *sonic-net* repository and release branch.
