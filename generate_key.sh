#!/bin/bash
openssl genpkey -out $1 -algorithm RSA -pkeyopt rsa_keygen_bits:1024
openssl pkey -in $1 -pubout -out $2
