import simplematrixbotlib as botlib
import sqlite3,re
# keyinfo: id,name,tags,content,todolist
# todolist: id,content
help_strs = ['todo','todo+内容1','todo-id','\n','！黄龙','！黄龙+事项1','！黄龙/替换事项1；事项2','\n','+黄龙','+黄亮【xx的子女】','+黄亮#上海人','+黄亮#上海人【xx的子女】','\n','-黄亮','@黄亮','\n','#上海人','#上海人#浙江大学','#上海人？子女','#上海人？子女','？子女','\n','u黄亮#上海人','u黄亮【信息】','u黄亮#河南信阳人【信息】']
dbname='todokey.db'
config = botlib.Config()
config.encryption_enabled = True
config.emoji_verify = True
config.ignore_unverified_devices = True
creds = botlib.Creds(
    homeserver="xxx",
    username="xxx",
    password="xxx"
    )
bot = botlib.Bot(creds, config)
def create_table_keyinfo(dbname):
    db_table='keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t="""CREATE TABLE "%s" (
        "id"	INTEGER NOT NULL UNIQUE,
	    "name"	TEXT NOT NULL,
	    "tags"	TEXT,
	    "content"	TEXT,
	    "todolist"	TEXT,
	    PRIMARY KEY("id" AUTOINCREMENT))
        ;"""%(db_table)
    cs.execute(t)
    conn.commit()
    conn.close()
    print('建立keyinfo信息表完成')

    db_table1 = 'todolist'
    conn1 = sqlite3.connect(dbname)
    conn1.text_factory = str
    cs1 = conn1.cursor()
    t1 = """CREATE TABLE  "%s" (
            "id"	INTEGER NOT NULL UNIQUE,
    	    "content"	TEXT,
    	    PRIMARY KEY("id" AUTOINCREMENT)
            );""" % (db_table1)
    cs1.execute(t1)
    conn1.commit()
    conn1.close()
    print('建立todolist完成')
# create_table_keyinfo(dbname)
def checkname(name):
    tab_name = []
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    a = "select name from %s;"%(db_table)
    cs.execute(a)
    tab_list = cs.fetchall()
    for i in tab_list:
        tab_name.append(i[0])
    if name in tab_name:
        conn.commit()
        conn.close()
        return 1
    else:
        conn.commit()
        conn.close()
        return 0
def add_name(name):
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    a = "INSERT OR IGNORE INTO keyinfo (name) VALUES ('%s')"%(name)
    cs.execute(a)
    conn.commit()
    conn.close()
def get_names():
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    a = "SELECT name FROM keyinfo;"
    cs.execute(a)
    names=cs.fetchall()
    conn.commit()
    conn.close()
    namelist=''
    for i in names:
        l=i[0]+'，'
        namelist+=l
    return namelist
def add_content(name,content):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """UPDATE %s SET content = '%s' WHERE name='%s';""" % (db_table, content, name)
    # print(t)
    cs.execute(t)
    conn.commit()
    conn.close()
def add_tag(name,tags):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """UPDATE %s SET tags = '%s' WHERE name='%s';""" % (db_table, tags, name)
    # print(t)
    cs.execute(t)
    conn.commit()
    conn.close()
def add_content_tags(name,tags,content):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """UPDATE %s SET tags = '%s', content='%s' WHERE name='%s';""" % (db_table, tags, content,name)
    # print(t)
    cs.execute(t)
    conn.commit()
    conn.close()
def del_name(name):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """DELETE FROM %s WHERE name='%s';""" % (db_table, name)
    cs.execute(t)
    conn.commit()
    conn.close()
def at_name(name):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """SELECT tags,content FROM %s WHERE name='%s';""" % (db_table, name)
    cs.execute(t)
    mes= cs.fetchall()
    conn.commit()
    conn.close()
    tags=mes[0][0]
    content=mes[0][1]
    return tags,content
def sear_3(tag0,tag1,wenhao):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    sql = "SELECT name,tags,content FROM %s WHERE tags LIKE ? AND tags LIKE ? AND content LIKE ?"%(db_table)
    # 定义查询条件
    tag11 = '%'+tag0+'%'
    tag22 = '%'+tag1+'%'
    content = '%'+wenhao+'%'
    cs.execute(sql, (tag11, tag22, content))
    mes= cs.fetchall()
    conn.commit()
    conn.close()
    names=[]
    if len(mes)>0:
        for i in mes:
            name=i[0]
            content=i[2]
            if wenhao in content:
                names.append(name)
    else:
        pass
    print(names)
    return names
def sear_3_1(tag0,wenhao):
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    sql = "SELECT name,tags,content FROM keyinfo WHERE tags LIKE ? AND content LIKE ?"
    # 定义查询条件
    tag11 = '%'+tag0+'%'
    content = '%'+wenhao+'%'
    cs.execute(sql, (tag11, content))
    mes= cs.fetchall()
    conn.commit()
    conn.close()
    names=[]
    if len(mes)>0:
        for i in mes:
            name=i[0]
            content=i[2]
            if wenhao in content:
                names.append(name)
    else:
        pass
    print(names)
    return names
def sear_3_tags(tags):
    n=len(tags)
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    if n==1:
        tag0=tags[0]
        print(tag0)
        sql = "SELECT name,tags,content FROM %s WHERE tags LIKE ?" % (db_table)
        tag = ('%' + tag0 + '%',)
        cs.execute(sql, tag)
    elif n==2:
        tag0 = tags[0]
        tag1 = tags[1]
        sql = "SELECT name,tags,content FROM %s WHERE tags LIKE ? AND tags LIKE ?" % (db_table)
        tag00 = '%' + tag0 + '%'
        tag11 = '%' + tag1 + '%'
        cs.execute(sql, (tag00, tag11))
    elif n==3:
        tag0 = tags[0]
        tag1 = tags[1]
        tag2 = tags[2]
        sql = "SELECT name,tags,content FROM %s WHERE tags LIKE ? AND tags LIKE ? AND tags LIKE ?" % (db_table)
        tag11 = '%' + tag0 + '%'
        tag22 = '%' + tag1 + '%'
        tag33 = '%' + tag2 + '%'
        cs.execute(sql, (tag11, tag22, tag33))
    mes = cs.fetchall()
    conn.commit()
    conn.close()
    names = []
    if len(mes) > 0:
        for i in mes:
            name = i[0]
            names.append(name)
    else:
        pass
    print(names)
    return names
def wenhao_xx(content):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """SELECT name FROM %s WHERE content LIKE ?;""" % (db_table)
    params = ('%' + content + '%',)  # 注意逗号，确保是一个元素的元组
    cs.execute(t, params)
    mes= cs.fetchall()
    conn.commit()
    conn.close()
    names=[]
    if len(mes)>0:
        for i in mes:
            names.append(i[0])
    print(names)
    return names
def u_content(name,content):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """UPDATE %s SET content = '%s' WHERE name='%s';""" % (db_table, content, name)
    cs.execute(t)
    conn.commit()
    conn.close()
    return name
def u_3(name,tags):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """UPDATE %s SET tags = '%s' WHERE name='%s';""" % (db_table, tags, name)
    cs.execute(t)
    conn.commit()
    conn.close()
    return name
def u_3_content(name,tags0,content):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """UPDATE %s SET tags = '%s',content='%s' WHERE name='%s';""" % (db_table, tags0,content, name)
    cs.execute(t)
    conn.commit()
    conn.close()
    return name
def todos(name):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """SELECT todolist FROM %s WHERE name='%s';""" % (db_table, name)
    cs.execute(t)
    mes = cs.fetchall()
    conn.commit()
    conn.close()
    todol=''
    if len(mes)>0:
        todol=mes[0][0]
    return todol
def todo_add(name,todol):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """SELECT todolist FROM %s WHERE name='%s';""" % (db_table, name)
    cs.execute(t)
    mes = cs.fetchall()
    content0=mes[0][0]
    if content0 is None:
        content=todol
    else:
        content=content0+'\n'+todol
    tt = """UPDATE %s SET todolist = '%s' WHERE name='%s';""" % (db_table, content, name)
    cs.execute(tt)
    conn.commit()
    conn.close()
    return name
def todo_repl(name, todol):
    db_table = 'keyinfo'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """UPDATE %s SET todolist = '%s' WHERE name='%s';""" % (db_table, todol, name)
    cs.execute(t)
    conn.commit()
    conn.close()
    return name
def get_list():
    db_table = 'todolist'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """SELECT id,content FROM '%s';""" % (db_table)
    cs.execute(t)
    data = cs.fetchall()
    list_content = '\n'.join([f'{row[0]}. {row[1]}' for row in data])
    print(list_content)
    conn.commit()
    conn.close()
    return list_content
def add_list(content):
    db_table = 'todolist'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = "INSERT OR IGNORE INTO {} ('content') VALUES (?)".format(db_table)
    cs.execute(t,(content,))
    conn.commit()
    conn.close()
def del_list(the_id):
    db_table = 'todolist'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """DELETE FROM %s WHERE id='%s';""" % (db_table, the_id)
    cs.execute(t)
    conn.commit()
    conn.close()
def check_renew_list():
    db_table = 'todolist'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    cs = conn.cursor()
    t = """SELECT content FROM '%s';""" % (db_table)
    cs.execute(t)
    list0=cs.fetchall()
    cs.close()
    conn.close()
    if len(list0)>0:
        return 1
    else:#表格为空
        return 0

def renew_list():
    conn = sqlite3.connect(dbname)
    css = conn.cursor()
    css.execute("delete from sqlite_sequence where name = 'todolist';")
    conn.commit()
    css.close()
    conn.close()
@bot.listener.on_message_event
async def echo(room, event):
    match = botlib.MessageMatch(room, event, bot)
    if match.is_not_from_this_bot() and match.is_from_allowed_user():
        args=event.body
        print(args)
        input_str=args
        # print(input_str)
        if "+" == input_str[0:1]:
            if "【" in input_str and '#' not in input_str:
                name = input_str[1:input_str.index("【")]
                if checkname(name)==1:
                    content = input_str[input_str.index("【") + 1:input_str.index("】")]
                    # print(content)
                    add_content(name, content)
                    tags,content=at_name(name)
                    if tags is None and content is None:
                        message=name+'：'+'空'
                    elif tags is None and content is not None:
                        message=name+'：'+'\n'+'【'+content+'】'
                    elif tags is not None and content is None:
                        message = name + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = name + '：' + '\n' + tags+ '\n' + '【'+content+'】'
                    else:
                        message='+error'
                    await bot.api.send_text_message(room.room_id, message)
                    print('+%s【xxx】 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name'%(name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name'%(name))
            elif "#" in input_str and '【' not in input_str:
                name = input_str[1:input_str.index("#")]
                if checkname(name)==1:
                    tags = input_str[input_str.index("#"):]
                    # print(tags)
                    add_tag(name, tags)
                    tags, content = at_name(name)
                    if tags is None and content is None:
                        message = name + '：' + '空'
                    elif tags is None and content is not None:
                        message = name + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = name + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = name + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = '+error'
                    await bot.api.send_text_message(room.room_id, message)
                    print('+%s#tags 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            elif "#" in input_str and '【' in input_str:
                name = input_str[1:input_str.index("#")]
                if checkname(name)==1:
                    tags = input_str[input_str.index("#"):input_str.index("【")]
                    content = input_str[input_str.index("【") + 1:input_str.index("】")]
                    add_content_tags(name, tags, content)
                    tags, content = at_name(name)
                    if tags is None and content is None:
                        message = name + '：' + '空'
                    elif tags is None and content is not None:
                        message = name + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = name + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = name + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = '+error'
                    await bot.api.send_text_message(room.room_id, message)
                    print('+%s#xxx【xxx】完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            elif all('\u4e00' <= c <= '\u9fff' for c in input_str[1:]):
                name = input_str[1:]
                if checkname(name)==1:
                    message='%s 已存在' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('%s 已存在' % (name))
                else:
                    add_name(name)
                    message = '+%s 完成' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('+%s 完成' % (name))
            else:
                message = '+error'
                await bot.api.send_text_message(room.room_id, message)
                print('+error')
        elif "-" == input_str[0:1]:
            if all('\u4e00' <= c <= '\u9fff' for c in input_str[1:]):
                name = input_str[1:]
                del_name(name)
                message = '-%s 完成' % (name)
                await bot.api.send_text_message(room.room_id, message)
                print('-%s 完成' % (name))
            else:
                message = '-error'
                await bot.api.send_text_message(room.room_id, message)
                print('-error')
        elif "@" == input_str[0:1]:
            if all('\u4e00' <= c <= '\u9fff' for c in input_str[1:]):
                name = input_str[1:]
                if checkname(name)==1:
                    tags, content = at_name(name)
                    if tags is None and content is None:
                        message = name + '：' + '空'
                    elif tags is None and content is not None:
                        message = name + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = name + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = name + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = '@error'
                    await bot.api.send_text_message(room.room_id, message)
                    print('@%s 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            elif '@@'==input_str[0:2]:
                message=get_names()
                await bot.api.send_text_message(room.room_id, message)
                print('@@所有名单')
            else:
                message = '@error'
                await bot.api.send_text_message(room.room_id, message)
                print('@error')
        elif "#" == input_str[0:1]:
            if "？" in input_str and '#' in input_str[1:]:
                tags0 = input_str[1:input_str[1:].index("#") + 1]
                tags1 = input_str[input_str[1:].index("#") + 2:input_str.index("？")]
                wenhao = input_str[input_str.index("？") + 1:]
                names = sear_3(tags0, tags1, wenhao)
                for i in names:
                    tags, content = at_name(i)
                    if tags is None and content is None:
                        message = i + '：' + '空'
                    elif tags is None and content is not None:
                        message = i + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = i + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = i + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = '#tag#tag？xxx error'
                    await bot.api.send_text_message(room.room_id, message)
                print('#tag#tag？xxx 完成')
            elif "？" in input_str and '#' not in input_str[1:]:
                tag0 = input_str[1:input_str.index("？")]
                wenhao = input_str[input_str.index("？") + 1:]
                names = sear_3_1(tag0, wenhao)
                for i in names:
                    tags, content = at_name(i)
                    if tags is None and content is None:
                        message = i + '：' + '空'
                    elif tags is None and content is not None:
                        message = i + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = i + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = i + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = '#tag？xxx error'
                    await bot.api.send_text_message(room.room_id, message)
                print('#tag？xxx 完成')
            else:
                tags = input_str.split("#")[1:]
                names = sear_3_tags(tags)
                for i in names:
                    tags, content = at_name(i)
                    if tags is None and content is None:
                        message = i + '：' + '空'
                    elif tags is None and content is not None:
                        message = i + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = i + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = i + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = '#xxx#xxx#xxx error'
                    await bot.api.send_text_message(room.room_id, message)
                print('#xxx#xxx#xxx 完成')
        elif "？" == input_str[0:1]:
            if all('\u4e00' <= c <= '\u9fff' for c in input_str[1:]):
                content = input_str[1:]
                names = wenhao_xx(content)
                for i in names:
                    tags, content = at_name(i)
                    if tags is None and content is None:
                        message = i + '：' + '空'
                    elif tags is None and content is not None:
                        message = i + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = i + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = i + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = '？xxx error'
                    await bot.api.send_text_message(room.room_id, message)
                print('？xxx 完成')
            else:
                message = '？xxx error end'
                await bot.api.send_text_message(room.room_id, message)
                print('？error end')
        elif "u" == input_str[0:1]:
            if "【" in input_str and '#' not in input_str:
                name = input_str[1:input_str.index('【')]
                content = input_str[input_str.index("【") + 1:input_str.index("】")]
                u_content(name, content)
                if checkname(name)==1:
                    tags, content = at_name(name)
                    if tags is None and content is None:
                        message = name + '：' + '空'
                    elif tags is None and content is not None:
                        message = name + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = name + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = name + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = 'u%s【xxx】 error'
                    await bot.api.send_text_message(room.room_id, message)
                    print('u%s【xxx】 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            elif "#" in input_str and "【" not in input_str:
                name = input_str[1:input_str.index("#")]
                tags0 = input_str[input_str.index("#") + 1:]
                u_3(name, tags0)
                if checkname(name)==1:
                    tags, content = at_name(name)
                    if tags is None and content is None:
                        message = name + '：' + '空'
                    elif tags is None and content is not None:
                        message = name + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = name + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = name + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = 'u%s#xxx#xxx error'
                    await bot.api.send_text_message(room.room_id, message)
                    print('u%s#xxx#xxx 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            elif "#" in input_str and "【" in input_str:
                name = input_str[1:input_str.index('#')]
                tags0 = input_str[input_str.index("#"):input_str.index("【")]
                content = input_str[input_str.index("【") + 1:input_str.index("】")]
                u_3_content(name, tags0, content)
                if checkname(name)==1:
                    tags, content = at_name(name)
                    if tags is None and content is None:
                        message = name + '：' + '空'
                    elif tags is None and content is not None:
                        message = name + '：' + '\n' + '【'+content+'】'
                    elif tags is not None and content is None:
                        message = name + '：' + '\n' + tags
                    elif tags is not None and content is not None:
                        message = name + '：' + '\n' + tags + '\n' + '【'+content+'】'
                    else:
                        message = 'u%s#xxx【xxx】 error'% (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('u%s#xxx【xxx】 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            else:
                message = 'uerror error'
                await bot.api.send_text_message(room.room_id, message)
                print('uerror')
        elif '！' == input_str[0:1]:
            if '+' in input_str:
                name = input_str[1:input_str.index('+')]
                todo0 = input_str[input_str.index('+') + 1:].split("；")
                todo0 = [x for x in todo0 if x != '']
                todol = ''
                if len(todo0) > 1:
                    for i in todo0:
                        todol += i + '\n'
                    todol = todol[0:-1]
                else:
                    todol = todo0[0]
                todo_add(name, todol)
                if checkname(name)==1:
                    message = todos(name)
                    print(message)
                    await bot.api.send_text_message(room.room_id, message)
                    print('！%s+xxx； 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            elif '/' in input_str:
                name = input_str[1:input_str.index('/')]
                todo_r = input_str[input_str.index('/') + 1:].split("；")
                todol = ''
                if len(todo_r) > 1:
                    for i in todo_r:
                        todol += i + '\n'
                    todol = str(todol[0:-1])
                else:
                    todol = todo_r[0]
                todo_repl(name, todol)
                if checkname(name)==1:
                    message = todos(name)
                    print(message)
                    await bot.api.send_text_message(room.room_id, message)
                    print('！%s/xxx；xxx 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            elif all('\u4e00' <= c <= '\u9fff' for c in input_str[1:]):
                name = input_str[1:]
                if checkname(name)==1:
                    todol = todos(name)
                    message = todol
                    print(message)
                    await bot.api.send_text_message(room.room_id, message)
                    print('+%s【xxx】 完成' % (name))
                else:
                    message = '暂无 %s 信息，请新建+name' % (name)
                    await bot.api.send_text_message(room.room_id, message)
                    print('暂无 %s 信息，请新建+name' % (name))
            else:
                print('！error')
        elif 'todo' == input_str[0:4]:
            if 'todo' == input_str:
                message0 = get_list()
                if len(message0) == 0:
                    message = '空'
                else:
                    message = 'Todo：'+'\n'+message0
                print(message)
                await bot.api.send_text_message(room.room_id, message)
                print('todolist')
            elif '+' == input_str[4]:
                thel = input_str[5:]
                add_list(thel)
                message = get_list()
                message='Todo：'+'\n'+message
                print(message)
                await bot.api.send_text_message(room.room_id, message)
                print('list+内容1 完成')
            elif '-' == input_str[4]:
                the_id = input_str[5:]
                if the_id.isdigit():
                    del_list(the_id)
                    if check_renew_list()==0:
                        renew_list()
                    message = get_list()
                    message = 'Todo：' + '\n' + message
                    await bot.api.send_text_message(room.room_id, message)
                    print(message)
                else:
                    message = '输入id错误'
                    message = 'Todo：' + '\n' + message
                    print(message)
                    await bot.api.send_text_message(room.room_id, message)
                print('todo-id 完成')
            else:
                message='todo error'
                await bot.api.send_text_message(room.room_id, message)
                print('todo error')
        elif len(input_str)==1 and 'h'== input_str[0]:
            result = ','.join(help_strs)
            message=result
            await bot.api.send_text_message(room.room_id, message)
        else:
            message = 'error'
            await bot.api.send_text_message(room.room_id, message)
            print('error')
bot.run()
