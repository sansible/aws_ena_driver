# aws_ena_driver

Master: [![Build Status](https://travis-ci.org/sansible/aws_ena_driver.svg?branch=master)](https://travis-ci.org/sansible/aws_ena_driver)
Develop: [![Build Status](https://travis-ci.org/sansible/aws_ena_driver.svg?branch=develop)](https://travis-ci.org/sansible/aws_ena_driver)

* [ansible.cfg](#ansible-cfg)
* [Installation and Dependencies](#installation-and-dependencies)
* [Tags](#tags)
* [Examples](#examples)

This role install the AWS ENA driver for (enhanced networking instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking.html).




## ansible.cfg

This role is designed to work with merge "hash_behaviour". Make sure your
ansible.cfg contains these settings

```INI
[defaults]
hash_behaviour = merge
```




## Installation and Dependencies

To install run `ansible-galaxy install sansible.aws_ena_driver` or add this to your
`roles.yml`.

```YAML
- name: sansible.aws_ena_driver
  version: v1.0
```

and run `ansible-galaxy install -p ./roles -r roles.yml`




## Tags

This role uses tags:

* `build` - Installs the driver, will not run if the specified version is already installed




## Examples

Simply include role in your playbook

```YAML
- name: Install and configure aws_ena_driver
  hosts: "somehost"

  roles:
    - role: sansible.aws_ena_driver
      sansible_aws_ena_driver:
        download_checksum: b7ab5621a17e672bee8a1d7c0353a5a4a7a8238a727f8a90734b0f43f80fbad3
        version: 1.5.0
```
