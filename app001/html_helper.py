#!/usr/bin/env python
#coding:utf8

#from django.utils.safestring import mark_safe

class PageInfo(object):
    def __init__(self,current,totalItem,peritems=5):
        self.__current = current
        self.__totalItem = totalItem
        self.__peritems = peritems

    @property
    def From(self):
        return (self.__current-1) * self.__peritems

    @property
    def To(self):
        return self.__current * self.__peritems

    @property
    def TotalPage(self): #总页数
        result = divmod(self.__totalItem,self.__peritems)
        if result[1] ==0:
            return result[0]
        else:
            return result[0]+1

def Custompager(baseurl,currentPage,totalpage):
    '''
    baseurl:基础页
    currentPage:当前页
    totalpage:总页数
    #总页数<11
    #0 -- totalpage
    #总页数>11
    #当前页大于5 currentPage-5 -- currentPage+5
    #currentPage+5是否超过总页数,超过总页数，end就是总页数
    #当前页小于5 0 -- 10

    '''

    perPage = 10

    begin = 0
    end = 0
  
    begin_two = 0
    end_two = 0
    

    if totalpage <= 10:
        begin = 0
        end = totalpage
    else:
        if currentPage > 5:
            begin = currentPage - 6
            end = currentPage + 4
            if end > totalpage:
                end = totalpage
        else:
            begin = 0
            end = 10


    if currentPage > 10:
        begin_two = 9
    if currentPage < totalpage - 10:
        end_two = 9

    pager_list = []
 
    if currentPage <= 1:
        first =  "<a href=''>首页</a>"
    else:
        first = "<a href='%s/%d'>首页</a>"%(baseurl,1)
    pager_list.append(first)

    if currentPage <= 1:
        prev = "<a href=''>上一页</a>"
    else:
        prev = "<a href='%s/%d'>上一页</a>"%(baseurl,currentPage-1)
    pager_list.append(prev)


    if begin_two:
        prev_two = "<a href='%s/%d'>...</a>"%(baseurl,currentPage-begin_two)
        pager_list.append(prev_two)


    for i in range(begin+1,end+1):
        if i == currentPage:
            temp = "<a href='%s/%d' class='selected'>%d</a>"%(baseurl,i,i)
        else:
            temp = "<a href='%s/%d'>%d</a>"%(baseurl,i,i)
        pager_list.append(temp)


    if end_two:
        next_two = "<a href='%s/%d'>...</a>"%(baseurl,currentPage + end_two)
        pager_list.append(next_two)


    if currentPage >= totalpage:
        next = "<a href='#'>下一页</a>"
    else:
        next = "<a href='%s/%d'>下一页</a>"%(baseurl,currentPage+1)
    pager_list.append(next)

    if currentPage >= totalpage:
        last = "<a href=''>末页</a>"
    else:
        last = "<a href='%s/%d'>末页</a>"%(baseurl,totalpage)

    pager_list.append(last)
 
    result = ''.join(pager_list)

    #page_string = make_safe(result)

    return result
