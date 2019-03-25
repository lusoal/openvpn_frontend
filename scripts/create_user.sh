#!/bin/bash -x

CA_CRT_PATH=/etc/openvpn/keys/ca.crt
TA_KEY_PATH=/etc/openvpn/keys/ta.key
KEY_DIR=/etc/openvpn/user_configs/keys
OUTPUT_DIR=/etc/openvpn/user_configs/files
BASE_CONFIG=/etc/openvpn/user_configs/my_base.conf
EASY_RSA=/usr/share/easy-rsa/3/easyrsa

# #Variaveis para configurar as outras chaves
source vars
#Common Name of User
export EASYRSA_REQ_CN=$1

#Generate Key
(echo -en "\n\n\n\n\n\n\n\n") | ${EASY_RSA} gen-req $1 nopass
cp keys/private/$1.key ${KEY_DIR}

#Generate CRT
(echo -en "yes") | ${EASY_RSA} sign-req client $1
cp keys/issued/$1.crt ${KEY_DIR}

#Create .ovpn file for user with credentials
cat ${BASE_CONFIG} \
    <(echo -e '<ca>') \
    ${CA_CRT_PATH} \
    <(echo -e '</ca>\n<cert>') \
    ${KEY_DIR}/${1}.crt \
    <(echo -e '</cert>\n<key>') \
    ${KEY_DIR}/${1}.key \
    <(echo -e '</key>\n<tls-auth>') \
    ${TA_KEY_PATH} \
    <(echo -e '</tls-auth>') \
    > ${OUTPUT_DIR}/${1}.ovpn