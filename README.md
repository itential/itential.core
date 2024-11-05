# Ansible Collection - itential.core

The `itential.core` collection provides a common set of libraries used by
collections running on Itential Automation Gateway  This collection does not
direclty provide any plugins and should only be installed as a dependency for
other `itential.*` collections.

This colleciton is designed to work with Itential Automation Gatewway and
should be installed on a running instance of the server.  It can also be used
outside of Itential Automation Gateway in development environments for
developing Ansible playbooks.

To get started using this collection, it first needs to be installed in either
your local development environment or installed on a running instance of an
Itential Automation Gateway server.

## Installing the collection

The collection can be installed using either the Itential Automation Gateway UI
or the Ansible Galaxy CLI directly or defined as part of a `requirements.yaml`
file.

To install the collection on an server running Itential Automation Gateway,
simply click the "Install a collection" from the main page toolbar.

See the [Itential documentation](https//docs.itential.com) for more details about installing a collection
on an Itential Automation Gateway server.

Alternatively, the Ansible Galaxy CLI can be used to install the collection.
To use the Galaxy CLI, run the following command in your development
environment or on the Itential Automation Gateway server.

```bash
ansible-galaxy collection install itential.core
```

The collection can also be installed by adding it to an Ansible Galaxy
`requirements.yaml` file as shown below.

```yaml
---
collections:
  - name: itential.core
```

Once installed, the collection is available for use.

## Using this collection

The `itential.core` colleciton provides the following plugins that can be used
in Ansible playbooks.

### Modules

| Name                         | Description                                       |
|------------------------------|---------------------------------------------------|
| `itential.core.include_vars` | Include variables from one or more files into one |


## Contributing

Contributions to this collection are welcomed.  This includes new features,
enhancements, bug fixes as well as updates to the documentation.  If you
encounter any problems using this collection, please open an issue
[here](https://github.com/itential/itential.core/issues) or open a pull request with your proposed changes [here](https://github.com/itential/itential.core/pulls).

For additional details please consult the Itential Community Guide found
[here](CONTRIBUTING.md)

## Code of Conduct

This project is managed by the Itential community and sponsered by Itential and
goverened by a Code of Conduuct.  Please familarize yourself with our Code of
Conduct available [here](CODE_OF_CONDUCT.md)

## Release Notes

The release notes provide a quick glance with regards to new and/or changed
features and bug fixes available in each release.  The release notes are
updated for each release and can be found [here](CHANGELOG.md)

## More Information

Additional information about Itential Automation Gateway can be found at
http://itential.com.


# License

GNU General Public License v3.0 or later.

See [LICENSE](LICENSE) to see the full text.
