#coding:utf8

from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from app001.models import Book
from app001 import models
from app001 import common
from app001 import html_helper


import logging
from django.db import connection,transaction


from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

import hashlib

import os

from django.contrib import auth

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO 

def validate(request):

    mstream = StringIO.StringIO()
     

    validate_code = create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
     
    request.session['validate'] = validate_code[1]
     
    return HttpResponse(mstream.getvalue(), "image/gif")


def test(requetst):
    return render_to_response('test.html')


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        books = Book.objects.get(title__icontains=q)
        return render_to_response('search_results.html',{'books':books,'query':q})
    else:
        return HttpResponse('Please submit a search term.')



def log(request,pageNumber):
    logger = logging.getLogger('offer')
    ret = {}
    err = ''
    try:
        pageNumber = common.try_int(pageNumber,1)
        pageSize = 5

        start = (pageNumber-1)*pageSize
        end = pageNumber*pageSize

        cursor = connection.cursor()
        count = cursor.execute('select * from app001_host  where hostname like %s',['%'+'nginx'+'%'])
        result = cursor.fetchall()
        print result

        ret = {'data':result,'count':count}

        return  render_to_response('log.html',ret)
    except Exception,e:
        logger.error(e)
        ret['err'] = e
        print e
        return  render_to_response('log.html',ret)






num = 1



def index(request,page):
    if request.session.get('username',None):
        per_item = common.try_int(request.COOKIES.get('pager_num',10),10)
        page = common.try_int(page,1)
    
        '''
        第一种方式用ORM,第二种方式用原生的SQL
        #count = models.Host.objects.all().count()
        #result = models.Host.objects.all()[pageObj.From:pageObj.To]
        '''
    
        sql_count = 'select count(*) from app001_host where hostname like "%s"'
    
        cursor = connection.cursor()
    
        cursor.execute(sql_count%('%nginx-1%'),)
     
        count = cursor.fetchall()[0][0]
    
        pageObj = html_helper.PageInfo(page,count,per_item)
    
        sql_item = 'select HostName,IP,URL from app001_host where 1=1 and id>= (select id from app001_host where hostname like "%s"  order by id limit %d,1)  and hostname like "%s" limit %d'
    
        cursor.execute(sql_item%('%nginx-1%',pageObj.From,'%nginx-1%',per_item))
       
        col_names = [ desc[0] for desc in cursor.description ]
    
        result = [dict(zip(col_names,row)) for row in cursor.fetchall() ]
    
        results = []

        num  =  pageObj.From + 1    
   
        for row in result:
            row['id'] = num
            num += 1 
            results.append(row)

        page_string = html_helper.Custompager('/index',page,pageObj.TotalPage)
 
        username = request.session['username']
        ret = {'data':results,'count':count,'page_number':pageObj.TotalPage,'page':page_string,'username':username}
    
        response = render_to_response('index.html',ret)

        #response.set_cookie('pager_num',per_item)

        return response
    else:
        return  HttpResponseRedirect('/login/')




def login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            username = request.POST.get('username',None)
         
            password = request.POST.get('password',None)
    
            if not username:
         
               return render_to_response('login.html',{'error':'用户名不能为空'},context_instance=RequestContext(request))
        
               if not password:
                    return render_to_response('login.html',{'error':'密码不能为空'},context_instance=RequestContext(request))
    
    
            username_from_db = models.Account.objects.filter(username = username).values('username')
    
            if not username_from_db:
                return render_to_response('login.html',{'error':'用户不存在'},context_instance=RequestContext(request))
    
            username_from_db = username_from_db[0]['username']
    
            password_from_db = models.Account.objects.filter(username = username).values('password')[0]['password']
    
            password = hashlib.sha1(password+username).hexdigest()
    
            if password_from_db != password:
                return render_to_response('login.html',{'error':'密码不匹配'},context_instance=RequestContext(request))
            else:
                request.session['username'] = {'username':username}
                request.session['password'] = {'password':password}
                result = HttpResponseRedirect('/index/')
                result.set_cookie('COOKIE_NAME_FOR_USER','username=%s&password=%s'%(username,password))
                #result.set_cookie('username',username)
                return result
        else:
            return HttpResponse("Please enable cookies and try again.")
    else:
        if request.session.get('username',None):
            print '------------------------------------%s'%request.COOKIES
            print '------------------------------------%s'%request.session
            return HttpResponseRedirect('/index/')
        else:  
            request.session.set_test_cookie()
            return render_to_response('login.html',{'error':''},context_instance=RequestContext(request))


def logout(request):
    if request.session.get('username',None):
        del request.session['username']
        return redirect('/login')
    else:
        return redirect('/login')




def web_console(request,page):
    if request.session.get('user',None):
        per_item = common.try_int(request.COOKIES.get('pager_num',10),10)
        page = common.try_int(page,1)

        '''
        第一种方式用ORM,第二种方式用原生的SQL
        #count = models.Host.objects.all().count()
        #result = models.Host.objects.all()[pageObj.From:pageObj.To]
        '''

        sql_count = 'select count(*) from app001_web_console'

        cursor = connection.cursor()

        cursor.execute(sql_count)

        count = cursor.fetchall()[0][0]

        pageObj = html_helper.PageInfo(page,count,per_item)

        sql_item = 'select HostName,IP,http from app001_web_console where 1=1 and id>= (select id from app001_web_console where 1=1  order by id limit %d,1)   limit %d'

        cursor.execute(sql_item%(pageObj.From,per_item))

        col_names = [ desc[0] for desc in cursor.description ]

        result = [dict(zip(col_names,row)) for row in cursor.fetchall() ]

        results = []

        num  =  pageObj.From + 1

        for row in result:
            row['id'] = num
            num += 1
            results.append(row)

        page_string = html_helper.Custompager('/web_console',page,pageObj.TotalPage)

        username = request.session['user']
        ret = {'data':results,'count':count,'page_number':pageObj.TotalPage,'page':page_string,'username':username}

        response = render_to_response('web_console.html',ret)

        #response.set_cookie('pager_num',per_item)

        return response
    else:
        return  HttpResponseRedirect('/login/')



def upload(request):
    if not request.user.is_superuser:

        str1 = '您不是管理员'

        return HttpResponse(str1.decode('utf8'))

    if request.method == 'POST':

        username = request.POST.get('username',None)

        f = request.FILES.getlist('uploadfile',None)

        l1 = {}
 
        l2 = {}

        l3 = {}

        l4 = []
 
        for ff in f:

            print 'file_name:%s,file_type:%s,file_size:%s'%(ff.name,ff.content_type,ff.size)
    
            if ff.content_type not in ['image/gif','image/jpg','image/jpeg']:
    
                str1 = '文件类型不对'
    
                l1[ff.name]=str1+'<br/>'

    
            elif ff.size > 100*1024*1024:
                
                str1 = '文件太大'

                l2[ff.name]=str1+str(round(ff.size/1024.0/1024,2))+'M'+'<br />'
 
            else:
 
                l4.append(ff)
    

            for fff in l4:

                filename = os.path.join('upload',fff.name)
   
                with open(filename,'a+') as keys:
    
                    for chunk in ff.chunks():
    
                        keys.write(chunk)

                str1 = '上传成功'+'<br />'     

                l3[fff.name]=str1.decode('utf8')

        list1 = {}

        list1['l1'] = l1
        list1['l2'] = l2
        list1['l3'] = l3            

        print list1

        return  render_to_response('upload_ok.html',{'list1':list1})

    return render_to_response('upload.html',context_instance=RequestContext(request))


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponse('ok')
        else:
            return HttpResponse('false')
    else:
        return render_to_response('login_view.html')

'''
def outer(main_func):
    def wrapper(request,*args,**kwargs):
        if not request.session.get('username')
           return main_func(request,*args,**kwargs)
        else:
            return HttpResponse('请登录')
    return wrapper

@outer
def index(request,*arg,**kwargs):
    return HttpResponse('index')

@outer
def show(request,page)
    print page
    return HttpResponse('show')
'''

def Filter(before_func,after_func):
    def outer(main_func):
        def wrapper(request,*args,**kwargs):
            before_result = before_func(request,*args,**kwargs)
            if (before_result != None):
                return before_result

             main_result = main_func(request,*args,**kwargs)
             if (main_result != None):
                 return main_result

             afer_result = after_func(request,*args,**kwargs)
             if (after_result != None):
                 return after_result
        return wrapper
    return outer


def before_index(request):
    print 'before'


def after_index(requetst):
    print 'after'


@Filter(before_index,after_index)
def index(request):
    print 'index'
    return HttpResponse('index')

def show(request,page):
    print page
    return HttpResponse('show')
