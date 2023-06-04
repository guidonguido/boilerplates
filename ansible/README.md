# Ansible installation

Ansible will be installed only on a single host (control node), which will control managed nodes remotely with SSH.

## MacOS Installation

```bash
brew install ansible

#Install sshpass to execute playbooks with password auth
brew install hudochenkov/sshpass/sshpass
```