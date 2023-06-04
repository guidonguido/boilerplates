# Ansible oh-my-zsh

## To recreate the roles and inventory

Create inventory file in zsh-playbook/inventory/hosts.ini

```bash
[ubuntu_lab]
192.168.10.10

[all:vars]
ansible_user=guido
```
#
Download existing role - credits gantsign

```bash
ansible-galaxy install gantsign.oh-my-zsh
cp /Users/rguido/.ansible/roles/gantsign.oh-my-zsh ./roles/gantsign.oh-my-zsh
```
#
Define site.yml playbook

#
## Installation guide

[Optional] Test playbook lint 

```bash
ansible-playbook site.yml -i ./inventory/hosts.ini --syntax-check
```

#
[Optional] Dry-run playbook

```bash
ansible-playbook -C site.yml -i inventory/hosts.ini --ask-pass --ask-become-pass
```

#
Run playbook

```bash
ansible-playbook site.yml -i inventory/hosts.ini --ask-pass --ask-become-pass
```