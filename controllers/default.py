# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    books = db(db.Book_Profile).select(orderby=db.Book_Profile.Title)
    form = FORM(INPUT(_id='keyword',_name='keyword', _onkeyup="ajax('callback', ['keyword'], 'target');"))
    target_div=DIV(_id='target')
    return locals()
    
def search():
    "an ajax wiki search page"
    return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
        _onkeyup="ajax('callback', ['keyword'], 'target');")), target_div=DIV(_id='target'))

def callback():
    "an ajax callback that returns a <ul> of links to wiki pages"
    query = request.vars.keyword
    titleResult = db.Book_Profile.Title.contains(query) 
    authorResult = db.Book_Profile.Author.contains(query)
    results = db(titleResult).select(orderby=db.Book_Profile.Title) | db(authorResult).select(orderby=db.Book_Profile.Title)
    titleLinks = [A(p.Title, _href=URL('book_profile',args=p.id)) for p in results]
    return UL(*titleLinks)
    
#    titlePages = db(titleResult).select(orderby=db.Book_Profile.Title)
#    authorPages = db(authorResult).select(orderby=db.Book_Profile.Title)
#    titleLinks = [A(p.Title, _href=URL('book_profile',args=p.id)) for p in titlePages] or [A(p.Title, _href=URL('book_profile',args=p.id)) for p in authorPages]

@auth.requires_login()
def create_user_bio():
    record = db(db.User_Bio.created_by==auth.user.id).select()
    if (record):
        redirect(URL('update_user_bio', args=auth.user.id))
    form = SQLFORM(db.User_Bio)
    if form.process().accepted:
        session.flash = "Form Accepted"
        redirect(URL('my_profile'))
    else:
        response.flash= "This is completely wrong you weiner..TRY AGAIN!"
    return locals()

@auth.requires_login() 
def update_user_bio():
    record = db.User_Bio(created_by=request.args(0)) or redirect(URL('create_user_bio'))
    if (auth.user.id!=record.created_by):
        session.flash = 'access denied'
        redirect(URL('index'))
    form = SQLFORM(db.User_Bio, record)
    if form.process().accepted:
        session.flash = "Form Accepted"
        redirect(URL('my_profile'))
    else:
        response.flash= "This is completely wrong you weiner..TRY AGAIN!"
    return locals()
      
@auth.requires_login() 
def my_profile():
    profiles = db(db.User_Bio.created_by==auth.user.id).select()
    shelves = db(db.Book_Shelf.created_by==auth.user.id).select()
    return locals()

def profiles_list():
    profiles = db(db.auth_user).select(orderby=db.auth_user.last_name)
    return locals()
    
def user_profile():
    record = db.auth_user(request.args(0)) or redirect (URL('index'))
    if auth.user:
        if (record.id==auth.user.id):
            redirect(URL('my_profile'))
    person = db.User_Bio.created_by==record.id
    profiles = db(person).select(db.User_Bio.ALL)
    shelves = db(db.Book_Shelf.created_by==record.id).select()
    return locals()

@auth.requires_login() 
def create_book_profile():
    form = SQLFORM(db.Book_Profile)
    if form.process().accepted:
        session.flash = "Form Accepted"
        redirect(URL('book_profile'))
    else:
        response.flash= "This is completely wrong you weiner..TRY AGAIN!"
    return locals()
  
@auth.requires_login() 
def update_book_profile():
    record = db.Book_Profile(request.args(0)) or redirect (URL('index'))
    form = SQLFORM(db.Book_Profile, record)
    if form.process().accepted:
        session.flash = "Form Accepted"
        redirect(URL('book_profile', args=record.id))
    else:
        response.flash= "This is completely wrong you weiner..TRY AGAIN!"
    return locals()
      
def book_profile():
    book = db.Book_Profile(request.args(0)) or redirect (URL('index'))
    test = False
    if auth.user:
    	test = True
    	db.comment.Book_Profile_id.default = book.id
    	comment_form = SQLFORM(db.comment).process()  
    	db.Book_Shelf_Items.Book_Profile_id.default=book.id
    	db.Book_Shelf_Items.Book_Profile_id.writable = False
    	db.Book_Shelf_Items.Book_Profile_id.readable = False
    	authBookshelfItems = db.Book_Shelf_Items.created_by==auth.user.id
#    	addItemShelfForm = SQLFORM(db.Book_Shelf_Items.Book_Shelf_id) 
    	addItemShelfForm = SQLFORM(db.Book_Shelf_Items)  
    	if addItemShelfForm.process().accepted:
       		session.flash = "Form Accepted"
        	redirect(URL('book_shelf', args=addItemShelfForm.vars.Book_Shelf_id))
    	else:
        	response.flash= "This is completely wrong you weiner..TRY AGAIN!"
    comments = db(db.comment.Book_Profile_id==book.id).select(orderby =~db.comment.created_on) 
    return locals()

def post_comment():
    if request.env.request_method=='POST':
        db.comment.Book_Profile_id.default = request.args(0)
        db.comment.insert(body=request.vars.comment)   

@auth.requires_login()
def create_book_shelf():
    form = SQLFORM(db.Book_Shelf)
    if form.process().accepted:
        session.flash = "Form Accepted"
        redirect(URL('book_shelf',args=form.vars.id))
    else:
        response.flash = "WRONG!"
    return locals()

@auth.requires_login() 
def update_book_shelf():
    ## add book to book shelf
    record = db.Book_Shelf(request.args(0)) or redirect (URL('index'))
    db.Book_Shelf_Items.Book_Shelf_id.default = record.id
    form = SQLFORM(db.Book_Shelf_Items)  
    if form.process().accepted:
        session.flash = "Form Accepted"
        redirect(URL('book_shelf', args=record.id))
    else:
        response.flash= "This is completely wrong you weiner..TRY AGAIN!"
    return locals()
    
@auth.requires_login()      
def book_shelf():
    shelf = db.Book_Shelf(request.args(0)) or redirect (URL('index'))
    shelfItems = db(db.Book_Shelf_Items.Book_Shelf_id==shelf.id).select()
    books = [db(db.Book_Profile.id==item.Book_Profile_id).select() for item in shelfItems]
    form = FORM(INPUT(_id='keyword',_name='keyword', _onkeyup="ajax('callback', ['keyword'], 'dest');"))
    target_div=DIV(_id='dest')
    return locals()
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
