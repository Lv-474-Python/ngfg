# ngfg
new generation form generator

before you make your first migration, export the following environmental variables:
- POSTGRES_USER
- POSTGRES_PASSWORD
- HOST
- PORT
- DB_NAME

###Google auth

To add Google auth you need to export the following environmental variable:
 - GOOGLE_CLIENT_ID
 - GOOGLE_CLIENT_SECRET
 - APP_SECRET_KEY

And export:
- OAUTHLIB_INSECURE_TRANSPORT="1"

for http access.

###Google Sheets
User must share the sheet with ngfg-account@ngfg-268019.iam.gserviceaccount.com
or give link with editing permission