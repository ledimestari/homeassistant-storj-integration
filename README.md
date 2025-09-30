# Homeassistant Storj Node statistics

A custom homeassistant integration to read statistics from a storj storage node.

<img height="700" alt="image" src="https://github.com/user-attachments/assets/6dc164d4-f0e7-4114-806a-df93d9748a3e" />

Uses the api endpoints provided by your storj node. 

Used api paths:
- http://\<node ip address>:14002/api/sno/
- http://\<node ip address>:14002/api/sno/estimated-payout
- http://\<node ip address>:14002/api/sno/satellites

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
