```
  __  __           _       _      _      _____ ______ _______            _____ _____ 
 |  \/  |         | |     | |    | |    |_   _|  ____|__   __|     /\   |  __ \_   _|
 | \  / | ___   __| |_   _| | ___| |      | | | |__     | |       /  \  | |__) || |  
 | |\/| |/ _ \ / _` | | | | |/ _ \ |      | | |  __|    | |      / /\ \ |  ___/ | |  
 | |  | | (_) | (_| | |_| | |  __/ |____ _| |_| |       | |     / ____ \| |    _| |_ 
 |_|  |_|\___/ \__,_|\__,_|_|\___|______|_____|_|       |_|    /_/    \_\_|   |_____|
```
##### This project is NOT considered production ready.

# About
ModuleLIFT was 1st created back in 2018 as a proof of concept for a new type of pugging system. Recently I've decided to open source the project in hope to get support from other developers in the communitity.

The idea behind ModuleLIFT is to create a powerful API for creating & monitoring PUGs. Currently ModuleLIFT is just a REST API but Graphql integration is planned.

# Why use ModuleLIFT API?
- We provide support for multiple server hosts, including [Pterodactyl](https://pterodactyl.io/) (self hosting), [Dathost](https://dathost.net/) & [Pacifices Cloud](https://www.pacifices.cloud/).
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

## Index
- [Deploying](#deploying)
- [Planned Features](#planned-features)
- Documentation is planned.

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

## Planned Features
- Example website.
- Example discord bot.
- Setup guide.
- Python API client.
- Documentation.