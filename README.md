# AutoCertBot

A script and webserver to generate and install Certbot certificates using Nginx reverse proxy

## Installation

### Install requriements

- `pip install -r requirements.txt`

### Configuration

- Make changes to `nginx-config.template` to fit your reverse proxy needs
- Makes changes to `config.json` in webserver folder
  - Change `secret` to a randomly generated secret key
  - Change `path` to the path of the local repo

## Usage

### Certificate Generation

- `USAGE: sudo python3 domain.py sub.domain.tld`
- Generates and installs certificates for the supplied domain.

### Webserver

- I recommend generating a self-signed certificate to enforce TLS on the app.
- `sudo FLASK_APP=index.py flask run -p [port_num] -h 0.0.0.0 --cert=cert.pem --key=key.pem`
- Default credentials: `admin:admin` _Please change password upon first login_
