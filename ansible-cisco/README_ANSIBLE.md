Ansible for SSH mellom rutere og switcher

## Beskrivelse ##

Denne delen av prosjektet benytter Ansible for å automatisere administrasjon og konfigurasjon av Cisco-rutere og Cisco-switcher via SSH

SSH blir først satt opp ved hjelp av Python-skriptene fra Del 1. Deretter brukes Ansible for administrasjon av nettverksutstyret.


## Nettverksdesign ##

VLAN 99 - Management

Brukes til:

- SSH
- Ansible
- Administrasjon av nettverksutstyr

Nett:

192.168.99.0 /24

Gateway:

192.168.99.1


# VLAN 20 - Klientnett #

192.168.20.0 /24

Gateway:
192.168.20.1


# IP-plan #

Multilayer Switch (MLS)
192.168.99.1

Router5
192.168.99.5

Router6
192.168.99.6

Switch3
192.168.99.13

Switch4
192.168.99.14

Management-PC
192.168.99.100


## Forutsetninger ##

Før Ansible brukes så må du:

-Konfigurere SSH på alle enheter
-Enhetene må ha management-IP
-SSH-tilkobling burde være testet

Eksempel:
ssh admin@192.168.99.5


## Installasjon ##

# Installer Ansible #

sudo apt update
sudo apt install ansible -y

# Installer Cisco Collection #

ansible-galaxy collection install cisco.ios

# Installer Netcommon Collection #

ansible-galaxy collection install ansible.netcommon


# Inventory #

Eksempel på inventory.ini

[routers]
Router5 ansible_host=192.168.99.5
Router6 ansible_host=192.168.99.6

[switches]
MLS ansible_host=192.168.99.1
Switch3 ansible_host=192.168.99.13
Switch4 ansible_host=192.168.99.14

[all:vars]
ansible_user=admin
ansible_password=Cisco123
ansible_connection=network_cli
ansible_network_os=cisco.ios.ios

# Variabler #

Variabler lagres i:
group_vars/all.yml

Eksempel:
domain_name: skole.local

vlan_user: 20
vlan_user_name: USERS

vlan_mgmt: 99
vlan_mgmt_name: MGMT


## Playbooks ##

# Kommandoer #
For å konfigurere hostname på enhetene:
ansible-playbook -i inventory.ini playbooks/hostname.yml


For å opprette VLAN og konfigurere VLAN-relaterte innstillinger:
ansible-playbook -i inventory.ini playbooks/vlan.yml


For å opprette DHCP-pool for VLAN20:
ansible-playbook -i inventory.ini playbooks/dhcp.yml


For å konfigurere EtherChannel forbindelser:
ansible-playbook -i inventory.ini playbooks/etherchannel.yml


# Testing av ansible #

Bruk kommandoen under for å teste ansible:
ansible all -i inventory.ini -m cisco.ios.ios_command -a "commands='show version'"

Får du tilbake denne informasjonen så funker disse funksjonene:
- SSH
- Inventory
- Cisco Collection
- Ansible


## DHCP-plan ##

Router5 funker som DHCP-server for VLAN20
192.168.20.21 - 192.168.20.254

Gateway: 
192.168.20.1

DNS:
8.8.8.8


## Vedlikehold ##

Hvis du skal legge til nye enheter:

1. Gi enheten management-IP
2. Aktiver SSH
3. Legg enheten inn i inventory.ini
4. Kjør ønsket playbook.


Hvis du endrer på VLAN eller andre konfigurasjoner som ikke er nevnt så må du oppdatere følgende:

group_vars/all.yml

da slipper du å endre på playbookene.


## Forfatter ##

August Stenbrenden
Nettverk 2 - Arbeidskrav 2