from django.shortcuts import render
import mysql.connector as sql
from random import randint
from multiprocessing import context
fn,ln,s,em,p,='','','','',''
eml,pwd,='',''
dep_amt=0
accno='';ubal=0;money=0
# Create your views here.
def home_page(request):
    return render(request,'home.html')



def signupaction(request):
    global fn,ln,s,em,p,bal
    if request.method=='POST':
        m=sql.connect(host='localhost',user='root',passwd='Yunga@2000',database='BankApp')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=='first_name':
                fn=value
            if key=='last_name':
                ln=value
            if key=='sex':
                s=value
            if key=='email':
                em=value
            if key=='password':
                p=value
        bal=0
        account_no=randint(100000000000000,999999999999999)
        c="insert into users values('{}','{}','{}','{}','{}','{}','{}')".format(fn,ln,s,em,p,account_no,bal)
        cursor.execute(c)
        m.commit()

    return render(request,'signup.html')


def loginaction(request):
    global eml,pwd
    if request.method=='POST':
        ml=sql.connect(host='localhost',user='root',passwd='Yunga@2000',database='BankApp')
        cursor_l=ml.cursor()
        dl=request.POST
        for key,value in dl.items():
            if key=='email':
                eml=value
            if key=='password':
                pwd=value
        cl="select* from users where email='{}' and password='{}'".format(eml,pwd)
        cursor_l.execute(cl)
        tup=tuple(cursor_l.fetchall())
        if tup==():
            return render(request,'login.html')
        else:
            return render(request,"welcome.html")


    return render(request,'login.html')

def deposit_amount(request):
    global dep_amt
    update_bal=0
    deposit_ml=sql.connect(host='localhost',user='root',passwd='Yunga@2000',database='BankApp')
    c3=deposit_ml.cursor()
    c4=deposit_ml.cursor()
    deposit_dl=request.POST
    for key,value in deposit_dl.items():
        if key=='deposit':
            dep_amt=value
    d1="select accountno,balance from users where Email='{}'".format(eml)
    c3.execute(d1)
    l=list(c3.fetchall())
    if len(l)>0:
        update_bal=l[0][1]+int(dep_amt)
    d2="update users set balance={} where Email='{}'".format(update_bal,eml)
    c4.execute(d2)
    deposit_ml.commit()
    dep_amt=0
    return render(request,'deposit_page.html')

def bal_inq(request):
    bal_ml=sql.connect(host='localhost',user='root',passwd='Yunga@2000',database='BankApp')
    c5=bal_ml.cursor()
    query="select fname,lname,accountno,balance from users where Email='{}'".format(eml)
    c5.execute(query)
    l=list(c5.fetchall())
    if len(l)>0:
        context={"first_name":l[0][0],
                "last_name":l[0][1],
                "ano":l[0][2],
                "ba":l[0][3]}
        return render(request,'balance_inquiry.html',context)

def money_transfer(request):
    global accno,ubal,money
    if request.method=="POST":
        if 'first' in request.POST:
            money_ml=sql.connect(host="localhost", user="root", passwd="Yunga@2000", database='BankApp')
            c6=money_ml.cursor()
            money_dl=request.POST
            for key ,value in money_dl.items():
                if key=="acntno":
                    accno=value
            query="select accountno, fname, lname from users where accountno='{}'".format(accno)
            c6.execute(query)
            l=list(c6.fetchall())
            if len(l)==0:
                return render(request,'user_transfer.html')

        if 'transfer' in request.POST:
            money_ml_2=sql.connect(host="localhost", user="root", passwd="Yunga@2000", database='BankApp')
            c7=money_ml_2.cursor()
            query="select accountno, balance from users where Email='{}'".format(eml)
            c7.execute(query)
            print(query)
            li=list(c7.fetchall())
            money_dl_2=request.POST
            for key ,value in money_dl_2.items():
                if key=="transfer_amt":
                    money=value

            if int(money)<=li[0][1]:
                c8=money_ml_2.cursor()
                c9=money_ml_2.cursor()
                c10=money_ml_2.cursor()
                c11=money_ml_2.cursor()
                c12=money_ml_2.cursor()
                query="select balance from users where accountno='{}'".format(accno)
                c8.execute(query)
                l=list(c8.fetchall())
                print(l)
                to_user=int(money)+l[0][0]
                query2="update users set balance='{}' where accountno='{}'".format(to_user,accno)
                c9.execute(query2)
                money_ml_2.commit()

                to_self=int(li[0][1])-int(money)
                query3="update users set balance={} where Email='{}'".format(to_self,eml)
                c10.execute(query3)
                money_ml_2.commit()
                q4="insert into debit_trans values('{}','{}','{}')".format(li[0][0],accno,money)
                q5="insert into credit_trans values('{}','{}','{}')".format(accno,li[0][0],money)
                c11.execute(q4)
                c12.execute(q5)
                money_ml_2.commit()
                return render(request,'money_transfer_page.html')

    return render(request,'money_transfer_page.html')


def m_passbook(request):
    obj=sql.connect(host="localhost", user="root", passwd="Yunga@2000", database='BankApp')
    c13=obj.cursor()
    c14=obj.cursor()

    query="select accountno from users where Email='{}'".format(eml)
    c13.execute(query)
    lu=list(c13.fetchall())
    print(lu)
    la=lu[0][0]
    print(la,'line 162')
    query2="select to_user,cre_amt from credit_trans where from_user='{}'".format(la)
    c14.execute(query2)
    lx=list(c14.fetchall())
    query3="select to_user,deb_amt from debit_trans where from_user='{}'".format(la)
    c14.execute(query3)
    ly=list(c14.fetchall())
    context={
    'data':lx,
    'data2':ly
    }
    return render(request,'passbook.html',context)
