#coding:utf8
from django.db import models
import hashlib

# Create your models here.



class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'publisher'

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    def __unicode__(self):
        return self.first_name+self.last_name

    class Meta:
        db_table = 'author'

class Book(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'书的名字' )
    authors = models.ManyToManyField(Author,verbose_name=u'作者')
    publisher = models.ForeignKey(Publisher,verbose_name='出版社')
    publication_date = models.DateField('出版日期')

    def __unicode__(self):
        return self.title


    class Meta:
        db_table = 'book'
        verbose_name = '书名'
        verbose_name_plural = '书集'


class Host(models.Model):
    HostName = models.CharField(max_length=100)
    IP = models.GenericIPAddressField()
    URL = models.URLField(max_length=1000)


    def __unicode__(self):
        return self.HostName

class Web_Console(models.Model):
    HostName = models.CharField(max_length=100)
    IP = models.GenericIPAddressField()
    http = models.URLField(max_length=1000)

    def __unicode(self):
        return self.HostName

    class Meta:
        verbose_name = '远程控制'  
        verbose_name_plural = '远程控制' 

class Account(models.Model):
    username = models.CharField(max_length=100,verbose_name='用户名')
    password = models.CharField(max_length=100,verbose_name='密码')


    def __unicode__(self):
        return self.username



    def save(self,*args,**kwargs):
        self.password = hashlib.sha1(self.password+self.username).hexdigest()
        super(Account,self).save(*args,**kwargs)
    class Meta:
        verbose_name = '账号'
        verbose_name_plural = '账号'
