#!/usr/bin/env bash
sudo sh -c 'echo "nameserver 8.8.8.8">/etc/resolv.conf'
sudo sh -c 'echo "nameserver 8.8.4.4">>/etc/resolv.conf'
