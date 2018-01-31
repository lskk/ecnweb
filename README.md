# Earthquake Catcher Network Web App

## Local Development

Requires the following environment variables:

    AMQP_USER= (see admin docs)
    AMQP_PASSWORD= (see admin docs)
    MONGODB_URI= (see admin docs)
    AMQP_VHOST= (see admin docs)
    AMQP_HOST= (see admin docs)
    DJANGO_DEBUG=1


## Deployment in Production

1. Install Anaconda with Python 3.6.
   This guide assumes Windows 64bit.

2. Create virtual environment

        python -m venv venv

3. Activate the virtual environment

        venv\Scripts\activate

4. Install dependencies

        pip install -r requirements.txt

5. Edit `setenv.cmd` and ensure configuration (get from Dropbox admin)
6. Run `setenv.cmd`
7. Run `python stationd.py`

