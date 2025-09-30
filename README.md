# Homeassistant Storj Node statistics

A custom homeassistant integration to read statistics from a storj storage node.

## Example card

<img width="500" alt="image" src="https://github.com/user-attachments/assets/6dc164d4-f0e7-4114-806a-df93d9748a3e" />

## Setup

<img width="500" alt="image" src="https://github.com/user-attachments/assets/6cd58485-69c1-4af4-88c3-0f2d9367a1ac" />

Setup is simple and only needs the IP-address (e.g. 192.168.1.123) and port of your node server.

Default port 14002 provided as a default value.

## Features

This integration only reads data and does not not provide any switches.

Provided sensors:

- Node ID
- Wallet address
- QUIC status
- Uptime
- Version number
- Diskspace Total
- Diskspace Used
- Diskspace Trash
- Diskspace Free
- Average Disk Space Used This Month
- Disk Use Percentage
- Bandwidth used this month
- Bandwidth Egress this month
- Bandwidth Ingress this month
- Estimated earning this month
- Held back this month
- Gross total this month

Features missing for now:

- Suspension, Audit and Online scores for each satellite
- Total payout history
- Disk space overused
- Time since last contact
- Current period (Current month)

## Backend

Uses the api endpoints provided by your storj node. 

Used api paths:
- http://\<node ip address>:14002/api/sno/
- http://\<node ip address>:14002/api/sno/estimated-payout
- http://\<node ip address>:14002/api/sno/satellites  

