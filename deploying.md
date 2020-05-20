# Deploying
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