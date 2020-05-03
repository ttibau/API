[![GitHub issues](https://img.shields.io/github/issues/ModuleLIFT/API)](https://github.com/ModuleLIFT/API/issues)
[![GitHub license](https://img.shields.io/github/license/ModuleLIFT/API)](https://github.com/ModuleLIFT/API/blob/master/LICENSE)
[![Actions Status](https://github.com/ModuleLIFT/API/workflows/Python%20application/badge.svg)](https://github.com/ModuleLIFT/API/actions)

```
  __  __           _       _      _      _____ ______ _______            _____ _____ 
 |  \/  |         | |     | |    | |    |_   _|  ____|__   __|     /\   |  __ \_   _|
 | \  / | ___   __| |_   _| | ___| |      | | | |__     | |       /  \  | |__) || |  
 | |\/| |/ _ \ / _` | | | | |/ _ \ |      | | |  __|    | |      / /\ \ |  ___/ | |  
 | |  | | (_) | (_| | |_| | |  __/ |____ _| |_| |       | |     / ____ \| |    _| |_ 
 |_|  |_|\___/ \__,_|\__,_|_|\___|______|_____|_|       |_|    /_/    \_\_|   |_____|
```
#### This project is NOT considered production ready.

# Index
- [Documentation](/DOC.md)
- [Roadmap](/ROADMAP.md)
- [About](#about)
- [Why use ModuleLIFT API?](#why-use-modulelift-api)
- [Deploying](#deploying)
- [Contributions](#contributions)
- [Credits](#credits)

# About
ModuleLIFT was 1st created back in 2018 as a proof of concept for a new type of pugging system. Recently I've decided to open source the project in hope to get support from other developers in the communitity.

The idea behind ModuleLIFT is to create a powerful API for creating & monitoring PUGs. Currently ModuleLIFT is just a REST API but Graphql integration is planned.

# Why use ModuleLIFT API?
- We provide support for multiple server hosts, including [Pterodactyl](https://pterodactyl.io/) (self hosting), [Dathost](https://dathost.net/) & [Pacifices Cloud](https://www.pacifices.cloud/).
- CDN support for both [s3](https://aws.amazon.com/s3/) (this includes something like [spaces](https://www.digitalocean.com/products/spaces/)) and [b2](https://www.backblaze.com/b2/cloud-storage.html).
- Full-featured API, want to write your own completely custom PUG / Tournament system? Well, ModuleLIFT won't limit you.
- Region support, make it easy to write a system what supports players from different regions.
- League support, own multiple communities or want to use ModuleLIFT API for your Business? Well, you don't have to bother setting up multiple instances of this script.
- API Key permissions, grant & deny different API Keys different access levels to routes and leagues.
- Discord & Steam integration, Discord based PUGGing systems can easily be implemented using this system. 
- Alt detection, When users login there IP is compared to already existing users & also uses [proxycheck.io](https://proxycheck.io/) to block VPNs.
- Advanced ban system, ModuleLIFT assigns a reputation value to each player, the more they get banned the worse there "rep" becomes resulting in longer bans, staff can also decide the severity of the ban what causes more rep loss.
- Scalable, ModuleLIFT is written in Python Starlette with good coding practices what ensure this application scales well.
- Elo system, measure how skillful players are.
- Statistics & Match recording.

## Deploying
1st install the needed modules ``pip install -r /path/to/requirements.txt``

Edit ``settings.py``

### Production
I recommend deploying [Starlette](https://www.starlette.io/) using [Uvicorn](http://www.uvicorn.org/) in a containerized environment with [Nginx](https://www.nginx.com/) acting as a reverse proxy, then using [pm2](https://pm2.keymetrics.io/) to manage running processes.

[Uvicorn](http://www.uvicorn.org/) will interact with [Nginx](https://www.nginx.com/) using a UNIX domain socket what can be set like this ``uvicorn.run(app, uds="path/to/uds")`` in ``run.py`` or can be done via the [Uvicorn Command Line](http://www.uvicorn.org/#command-line-options).

I like to use [Certbot](https://certbot.eff.org/) for automatizing [LetsEncrypt](https://letsencrypt.org/) certificates.

Make sure to run ``run.py`` with python 3 using [pm2](https://pm2.keymetrics.io/) before wondering why it isn't responding.

Heaps of online resources can help you with each one of these steps.

### Development / Testing
You can adjust the host & port in ``run.py``

Run ``run.py`` with python 3.

## Contributions
### Code Style
This project adheres to the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) with 80 character line limits.

I recommend installing [cornflakes linter](https://marketplace.visualstudio.com/items?itemName=kevinglasson.cornflakes-linter) if you use VS Code.

### Branches
Create a branch if you're working on an issue with the issue number and name like so: `100_Title-Separated-By-Dashes`.

## Credits
All the amazing developers who made the libraries this project is built on.
- [WardPearce](https://github.com/WardPearce) - Lead developer & maintainer.
