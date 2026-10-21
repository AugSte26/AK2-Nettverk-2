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
Kjøre Ansible-playbooks
Alle kommandoene kjøres fra ansible-cisco-mappen i Ubuntu/WSL:

cd /mnt/c/Users/lab/Desktop/AK2-Nettverk-2-main/ansible-cisco

# Kontrollere inventory #
Vis enhetene og gruppene som Ansible har funnet:

ansible-inventory -i inventory.ini --graph

# Teste forbindelsen #
Kjør show version på alle enhetene:

ansible all -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show version'"
Teste bare routerne:

ansible routers -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show version'"
Teste bare switchene:

ansible switches -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show version'"

## Kontrollere syntaksen ##
Før en playbook kjøres, kan syntaksen kontrolleres:

ansible-playbook -i inventory.ini playbooks/hostname.yml --syntax-check
ansible-playbook -i inventory.ini playbooks/vlan.yml --syntax-check
ansible-playbook -i inventory.ini playbooks/dhcp.yml --syntax-check
ansible-playbook -i inventory.ini playbooks/etherchannel.yml --syntax-check


## Hostname-playbook ##
Konfigurerer hostname basert på enhetsnavnet i inventory.ini:

ansible-playbook -i inventory.ini playbooks/hostname.yml
Verifisering:

ansible all -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show running-config | include hostname'"

## VLAN-playbook ##
Oppretter management- og bruker-VLAN på switchene:

ansible-playbook -i inventory.ini playbooks/vlan.yml
Verifisering:

ansible switches -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show vlan brief'"

## DHCP-playbook ##
# Konfigurerer DHCP på routerne: # 

ansible-playbook -i inventory.ini playbooks/dhcp.yml

# Verifiser DHCP-konfigurasjonen: #

ansible routers -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show running-config | section dhcp'"

# Vis DHCP-pool: #

ansible routers -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show ip dhcp pool'"

# Vis tildelte DHCP-adresser: #

ansible routers -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show ip dhcp binding'"

# DHCP-oppsettet bruker følgende nett: #

Nett:             192.168.98.0/24
Gateway:          192.168.98.1
Ekskludert:       192.168.98.1–192.168.98.20
Første klient-IP: 192.168.98.21
DNS:              8.8.8.8
DHCP ble testet med en Windows-klient. Klienten mottok adressen:

192.168.98.21

## EtherChannel-playbook ##
EtherChannel-playbooken skal bare kjøres når begge switchene er koblet sammen med de planlagte kablene:

ansible-playbook -i inventory.ini playbooks/etherchannel.yml
Verifisering:

ansible etherchannel_switches -i inventory.ini \
-m cisco.ios.ios_command \
-a "commands='show etherchannel summary'"

## Test av idempotens ##
En playbook kjøres to ganger for å kontrollere at den er idempotent.

Eksempel:

ansible-playbook -i inventory.ini playbooks/dhcp.yml
Når playbooken kjøres for andre gang, bør resultatet være:

changed=0
failed=0
Dette betyr at Ansible oppdager at ønsket konfigurasjon allerede finnes, og derfor ikke utfører unødvendige endringer.

## Viktig ved testing av DHCP ##
Management-forbindelsen bruker nettverket:

192.168.99.0/24
Klient- og DHCP-nettet bruker:

192.168.98.0/24
Hvis den samme Ethernet-adapteren brukes til begge nettene, vil Ansible miste forbindelsen til routerens management-IP når adapteren endres til DHCP.

Det anbefales derfor å bruke:

Ethernet-adapter 1:
Management-nett
Statisk IP: 192.168.99.100/24

Ethernet-adapter 2:
DHCP-klientnett
Automatisk IP-adresse


## Forfatter ##

August Stenbrenden
Nettverk 2 - Arbeidskrav 2
