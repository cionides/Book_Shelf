# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('Book_Profile',
    Field('ISBN', requires=IS_NOT_EMPTY()),
    Field('Title', requires=IS_NOT_EMPTY()),
    Field('Author', requires=IS_NOT_EMPTY()),
    Field('Genre'),
    Field('Publisher'),
    Field('Publication_Date'),
    Field('Picture', 'upload'),
    Field('Details', 'text'),
    auth.signature)

db.define_table('User_Bio',
    Field('Favorite_Book'),
    Field('Bio', 'text'),
    auth.signature)    

db.define_table('Book_Shelf',
    Field('Shelf_Name'),
    auth.signature)   
    
db.define_table('Book_Shelf_Items',
    Field('Book_Shelf_id', db.Book_Shelf),
    Field('Book_Profile_id', db.Book_Profile),
    auth.signature)
    
db.define_table('comment',
    Field('Book_Profile_id', db.Book_Profile),
    Field('body', 'text'),
    auth.signature)
    
db.define_table(
    'assign_shelf',
    Field('bookshelf', 'list:reference Book_Shelf_id'),
    auth.signature)
    
db.Book_Profile.is_active.readable = db.Book_Profile.is_active.writable = False  
db.Book_Profile.ISBN.requires = IS_NOT_IN_DB(db, db.Book_Profile.ISBN) 
db.Book_Profile.id.readable = db.Book_Profile.id.writable = False  
   
db.User_Bio.is_active.readable = db.User_Bio.is_active.writable = False
db.User_Bio.id.readable = db.User_Bio.writable = False

db.Book_Shelf.is_active.readable = db.Book_Shelf.is_active.writable = False

db.Book_Shelf_Items.is_active.readable = db.Book_Shelf_Items.is_active.writable = False
db.Book_Shelf_Items.Book_Shelf_id.writable = db.Book_Shelf_Items.Book_Shelf_id.readable = False

