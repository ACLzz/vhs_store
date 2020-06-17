VHS-store is not real cassettes web-store.
It is practice app for me.<br/>
All variables stored in environment because it is thus easier to configure the web app in real-time on heroku.<br/>
You can checkout this project at: https://vhs-store.herokuapp.com <br/>

### Used technologies:
- Django        : as heart of web-app
- PostgreSQL    : as database
- Scrapy        : as crawler for film info
- Blender3D API : as render engine for cassettes
- Google drive  : as storage for users' avatars and cassettes' covers
- ReCaptcha     : for login and register security
- Heroku        : as hosting

### How to use
Run server with: `gunicorn vhs_store.wsgi --log-file -`<br/>
Crawl for films: `python manage.py crawl`<br/>
Render cassettes: <br/>
`~ $> cd film_constructor/`<br/>
Set COUNT for needed number of cassettes in `render.sh` or leave it for 0 if you need to render all cassettes.<br/>
`~ $> ./render.sh`<br/>
It will render cassettes for films that don't have their own in database.

### Must-have environment variables:
- DATABASE : name of postgresql database
- DB_USER : username for postgresql
- DB_PASS : password for user in postgresql
- DB_HOST : ip address or url of postgresql database
- DB_PORT : Port of postgresql database

- CAPTCHA_SECRET : Server key for recaptcha
- project_id : Google drive project_id 
- private_key_id : Google drive private key id
- client_email : Google drive service account email
- client_id : Google drive client id
- client_x509_cert_url : Google drive client x509 cert url
- private_key : Google drive private key
