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
7. `python manage.py collectstatic`
8. Configure your webserver to:

   * Reverse proxy `http://ecn.pptik.id/` to `http://localhost:8000/`
      * Exclude `/static/*` (in IIS, use Condition - `{REQUEST_URI}` does not match pattern `^static/`)

   * Serve `/static/` from `ecnweb/static` folder

   * Forward HTTP `Host` header

   * Bonus: Set/Forward HTTP `X-Forwarded-Proto` header

   * Bonus: Support SSL (see https://community.letsencrypt.org/t/how-to-generate-a-ssl-certificate-for-iis-7-0-or-7-5/29467)

9. Linux: Use `gunicorn`:

        pip install --upgrade gunicorn
        gunicorn ecnweb.wsgi

   Windows - Easy way: Use waitress:

        pip install --upgrade waitress
        waitress-serve --listen=*:8000 ecnweb.wsgi:application

   Windows - Hard way: https://medium.com/@bilalbayasut/deploying-python-web-app-flask-in-windows-server-iis-using-fastcgi-6c1873ae0ad8
   You need to install Web Platform Installer in IIS Manager.

### Autostart Script (Windows Server)

    E:
    cd \ecnweb
    call setenv
    set PATH=E:\ecnweb\venv\Scripts;%PATH%
    waitress-serve --listen=*:8000 ecnweb.wsgi:application
