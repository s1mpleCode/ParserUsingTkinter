import urllib.request
import re
from tkinter import *
from tkinter import ttk

"""Парсинг второстепенных элементов"""
req=urllib.request.urlopen('http://santehzavod.com/')
content=req.read().decode()

categories={}
waterSupply=re.findall('<div class="XDCategoryGroupsBlocks autoSpacing">[\s\S]+?<a href=".+?">Водоснабжение</a></h2>([\s\S]+?)</div>', content)[0]
categories['waterSupply']={'name':'Водоснабжение','itemsList':re.findall('<li><a href="(.+?)">(.+?)</a></li>', waterSupply)}

heating=re.findall('<div class="XDCategoryGroupsBlocks autoSpacing">[\s\S]+?<a href=".+?">Отопление</a></h2>([\s\S]+?)</div>', content)[0]
categories['heating']={'name':'Отопление','itemsList':re.findall('<li><a href="(.+?)">(.+?)</a></li>', heating)}

plumbing=re.findall('<div class="XDCategoryGroupsBlocks autoSpacing">[\s\S]+?<a href=".+?">Сантехника</a></h2>([\s\S]+?)</div>', content)[0]
categories['plumbing']={'name':'Сантехника', 'itemsList':re.findall('<li><a href="(.+?)">(.+?)</a></li>', plumbing)}

stopValves=re.findall('<div class="XDCategoryGroupsBlocks autoSpacing">[\s\S]+?<a href=".+?">Запорная арматура</a></h2>([\s\S]+?)</div>', content)[0]
categories['stopValves']={'name':'Запорная арматура', 'itemsList':re.findall('<li><a href="(.+?)">(.+?)</a></li>', stopValves)}

sewerage=re.findall('<div class="XDCategoryGroupsBlocks autoSpacing">[\s\S]+?<a href=".+?">Канализация</a></h2>([\s\S]+?)</div>', content)[0]
categories['sewerage']={'name':'Канализация','itemsList':re.findall('<li><a href="(.+?)">(.+?)</a></li>', sewerage)}

def parsingProducts(url):
    req = urllib.request.urlopen(url)
    content = req.read().decode()
    flag = re.findall('<input type="hidden" name="product_id"', content)
    if flag:
        result = {}
        result['title'] = re.findall('<title>(.+?)</title>', content)
        result['description'] = re.findall('<meta name="description" content="(.+?)" />', content)
        result['keywords'] = re.findall('<meta name="keywords" content="(.+?)" />', content)
        result['h1'] = re.findall('<h1>(.+?)</h1>', content)
        result['h2'] = re.findall('<h2 id=".+?">(.+?)</h2>', content)
        result['h3'] = re.findall('<h3>(.+?)</h3>', content)
        result['h4'] = re.findall('<h4><.+>(.+?)</h4>', content)
        x = re.compile(r'<.*?>')
        for i in range(len(result['h4'])):
            result['h4'][i] = re.sub('<.*?>', '', result['h4'][i])
        breadcrumb = re.findall(' <div class="breadcrumb">([\s\S]+?)</div>', content)[0]
        result['breadcrumb'] = re.findall('<a href="(.+?)">(.+?)</a>', breadcrumb)
        result['name'] = re.findall('<h1>(.+?)</h1>', content)
        result['manufacturer'] = re.findall('<span>Производитель:</span> <a href=".+?">(.+?)</a>', content)[0]
        result['model'] = re.findall('<span>Модель:</span>(.+?)<br />', content)
        result['price'] = re.findall('price="(.+?)"', content)
        result['determination'] = re.findall('<div id="tab-description" class="tab-content">([\s\S]+?)</div>', content)
        result['mainImg'] = re.findall('<a href="(.+?)" title=".+?" class="colorbox">', content)
        characteristic = re.findall('<div id="tab-attribute" class="tab-content">([\s\S]+?)</div>', content)[0]
        characteristic_re = re.compile('<tr>\s*?<td>(.+?)</td>\s*?<td>(.+?)</td>\s*?</tr>', re.DOTALL)
        result['characteristic'] = re.findall(characteristic_re, characteristic)
        result['additionalImage'] = re.findall('<a href="(.+?)" title=".+?" class="colorbox"><img src=".+?" alt=".+?" /></a>', content)
        tags = re.findall('<div class="tags">([\s\S]+?)</div>', content)[0]
        result['tags'] = re.findall('<a href=(.+?)">(.+?)</a>', tags)
        txt.delete('1.0', END)
        print(url)
        txt.insert(END, url+"\n")
        for key, value in result.items():
            txt.insert(END, key.upper() + ": " + str(value)+"\n")

"""Парсинг списка товаров"""
def parsingListProducts(url):
    req = urllib.request.urlopen(url)
    content = req.read().decode()
    flag=re.findall('<b>На странице:</b>', content)
    if flag:
        products = re.findall('<div class="product-list">([\s\S]+?)<div class="pagination">', content)[0]
        listProducts = re.findall('<div class="name"><a href="(.+?)">(.+?)</a></div>', products)
        for products in listProducts:
            try:
                tree.insert(url, 'end', products[0], text=products[1])
            except BaseException:
                continue
        try:
          link = re.findall('<div class="links">.+?</div>', content)[0]
        except BaseException:
            link=0
        if link:
            pages = re.findall('<a href="(.+?)">\d+?</a>', link)
            for page in pages:
                req = urllib.request.urlopen(page)
                content = req.read().decode()
                products = re.findall('<div class="product-list">([\s\S]+?)<div class="pagination">', content)[0]
                listProducts = re.findall('<div class="name"><a href="(.+?)">(.+?)</a></div>', products)
                for products in listProducts:
                    try:
                      tree.insert(url, 'end', products[0], text=products[1])
                    except BaseException:
                        continue
    else:
        flag = re.findall('<input type="hidden" name="product_id"', content)
        if not flag:
          tree.insert(url, 'end', str('not'+url), text='Товаров нет')


"""Парсинг подкатегорий"""
def searchSubcategory(url):
    req = urllib.request.urlopen(url)
    content = req.read().decode()
    flag = re.findall('<h2>Выберите подкатегорию</h2>', content)
    if flag:
        subcategories = re.findall('<div class="category-list">([\s\S]+?)</div>', content)[0]
        listSubcategories = re.findall('<li><a href="(.+?)"><img src=".+?"><span>(.+?)</a></span></li>', subcategories)
        for subCategory in listSubcategories:
            tree.insert(url,'end',subCategory[0],text=subCategory[1])
        return True


"""Функция выбора элемента"""
def onClick(event):
    item = tree.focus()
    if item:
        try:
            firstStep = searchSubcategory(item)
            if firstStep:
                return
            parsingListProducts(item)
            parsingProducts(item)
        except BaseException:
            return

"""Формирование оконного приложения"""
root = Tk()
root.title('Parser: http://santehzavod.com/')
root.geometry('820x620')
root.resizable(FALSE, FALSE)
tree = ttk.Treeview(root)
tree['show']='tree'
mainList=['waterSupply', 'heating', 'plumbing', 'stopValves', 'sewerage']

for element in mainList:
    tree.insert('', 'end', element, text=categories[element]['name'])
    for value in categories[element]['itemsList']:
        tree.insert(element, 'end', value[0], text=value[1])

tree.place(x=0,y=0, width=300, height=620)
tree.bind('<Double-Button-1>',onClick)
listScrollbar = Scrollbar(root)
listScrollbar.place(x=300, y=0, height=620, width=20)
listScrollbar['command'] = tree.yview
tree['yscrollcommand'] = listScrollbar.set

txtScrollbar=Scrollbar(root)
txtScrollbar.pack(side='right', fill=BOTH)
txt = Text(root,width=53, height=32,font="8",yscrollcommand=txtScrollbar.set)
txt.pack(side='right', fill=BOTH)
txtScrollbar.config(command=txt.yview)

root.mainloop()