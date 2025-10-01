# Homeassistant Storj Node statistics

A custom homeassistant integration to read statistics from a storj storage node using json data provided by the node.

## Example card

<img width="500" alt="image" src="https://github.com/user-attachments/assets/e72513fe-89a8-4168-9f55-042df6f35ca6" />

This is somewhat the view I'm using, the graphs should get more interesting over time.

## Setup
### Manual
Copy the "homeassistant_storj_integration" directory into the "custom_components" directory of your homeassistant install.

### HACS
Soon to be possible to install via HACS as well.

### Configuration
After installation, you'll be able to setup your device in the gui like this:

<img width="500" alt="image" src="https://github.com/user-attachments/assets/6cd58485-69c1-4af4-88c3-0f2d9367a1ac" />

Setup is simple and only needs the IP-address (e.g. 192.168.1.123) and the port of your node server.

Default port 14002 provided as a default value.

## Features

This integration only reads data and does not not provide any actionable switches.

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

each sensor uses the first six characters of the Node ID as a prefix to differentiate them and make it so the names are not too generic.

Potential features missing for now:

- Suspension, Audit and Online scores for each satellite
- Total payout history
- Disk space overused
- Time since last contact
- Current period (Current month)

## Backend

This integration uses the api endpoints provided by your storj node, you can find the used json formatted data from the paths below.

Used api paths:
```
http://\<node ip address>:14002/api/sno/
http://\<node ip address>:14002/api/sno/estimated-payout
http://\<node ip address>:14002/api/sno/satellites
```









