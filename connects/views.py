import random as r
import smtplib

import pyrebase
from django.contrib import messages
from django.shortcuts import render, redirect
import time
from datetime import datetime, timezone
import pytz

# Create your views here.

config = {

    "apiKey": "AIzaSyCztfnYVUT49K8JVDRsL4z1oSxN8lu7V-E",
    "authDomain": "connected-try.firebaseapp.com",
    "databaseURL": "https://connected-try-default-rtdb.firebaseio.com",
    "projectId": "connected-try",
    "storageBucket": "connected-try.appspot.com",
    "messagingSenderId": "1004314390323",
    "appId": "1:1004314390323:web:51d248e16cdf9e15ac5846",
    "measurementId": "G-P0MFRMLT0E",


}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def index(request):
    global otp, email, phn, password, gender,uname, status, fullname

    if request.method == 'POST' and 'signin' in request.POST:


        email = request.POST.get("email")
        psw = request.POST.get("psw")
        # auth.sign_in_with_email_and_password(email, psw)
        print("Sucees")

        people = db.child("Accounts").get()
        for p in people.each():
            x = p.val()
            print(x['e-mail'])

    if request.method == 'POST' and 'signup' in request.POST:
        print("hlomf")
        email = request.POST.get("email")
        uname = request.POST.get("uname")
        request.session['username'] = uname
        p = request.POST.get("phn")
        password = request.POST.get("psw")
        cpassword = request.POST.get("cpsw")

        phn = str(p)
        print(phn)

        if password == cpassword:
            Break = True

            # searching for existing phone number
            try:
                people = db.child("Accounts").get()
                for p in people.each():
                    x = p.val()
                    if x['phone'] == phn or x['e-mail'] == email or x['username'] == uname:
                        Break = False
                        print('innna')
            except:
                pass
            if Break == True:
                try:
                    # OTP Generator
                    x = r.randint(1000, 9999)
                    otp = str(x)
                    print(otp)

                    # Sending email
                    sender = "pollscape10@gmail.com"
                    print(1)
                    reciver = email
                    print(2)
                    psw = "10pollscape"
                    print(3)
                    msg = otp
                    print(4)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    print(5)
                    server.starttls()
                    print(6)
                    server.login(sender, psw)
                    print(7)
                    server.sendmail(sender, reciver, msg)
                    print(8)

                    print("waiting bitch")

                    time.sleep(120)



                except:
                    print("nah...")
            else:
                print("sorry already existing")

    if request.method == 'POST' and 'otp' in request.POST:

        print(otp)

        x1 = request.POST.get('x1')
        x2 = request.POST.get('x2')
        x3 = request.POST.get('x3')
        x4 = request.POST.get('x4')

        x = f"{x1}{x2}{x3}{x4}"

        if x == otp:

            print(email, phn, password)

            data = {
                "e-mail": email,
                "phone": phn,
                "password": password,
                "username": uname

            }

            auth.create_user_with_email_and_password(email, password)
            db.child("Accounts").child(uname).set(data)
            request.session['username'] = uname
            print(request.session['username'],'.......................')
            return redirect("details")
        else:
            print("oops")

    else:
        print("oomb myree")

    return render(request, 'index.html')


def details(request):
    print("glllll")
    uname = request.session['username']
    print("glllll")

    if request.method == 'POST' and 'create' in request.POST:

        r1 = request.POST['choice']
        print(r1)

        r2 = request.POST['choices']
        print(r1)

        def from_dob_to_age(born):
            today = datetime.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        dob = request.POST.get('date')
        dofb = datetime.strptime(dob, '%Y-%m-%d')
        print(dob)
        age = from_dob_to_age(dofb)
        print(age)

        fname = request.POST.get('fname')

        lname = request.POST.get('lname')

        country = request.POST.get('country')
        state = request.POST.get('state')

        fullname = f"{fname} {lname}"
        print('p-----------------------------------p')
        print(fullname)


        data = {

            'uname': uname,
            "age": age,
            "gender": r1,
            "dob": dob,
            "fullname": fullname,
            "fname": fname,
            "lname": lname,
            "status": r2,
            "country": country,
            "state": state,
        }

        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        print(" mili " + str(millis))
        url = request.POST.get('url')
        print(url)

        photo = {
            "url": url,
            "time": millis
        }

        db.child("Accounts").child(uname).child("details").set(data)
        db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(millis).set(photo)
        request.session['yourname'] = uname

        return redirect("home")

    gender = ['Male', 'Female', 'Others']
    status = ['Single', 'Married', 'Not Defined']

    return render(request, "details.html", {'uname': uname, 'gender': gender, 'status': status})


def test(request):
    # people = db.child("Accounts").get()
    # for p in people.each():
    #
    #     x = p.key()
    #     print(x)
    #     z = db.child("Accounts").child(x).get()
    #
    #     for i in z.each():
    #         y = i.val()
    #         print(y)
    people = db.child("Accounts").get()

    for p in people.each():
        x = p.val()
        print(x['username'])

        albin = x['username']

        data = {'alb': albin}
        messages.info(request, data.get('alb'))

    return render(request, "test.html")


def create(request):
    return render(request, 'create.html')


def post_create(request):
    uname = request.session['uname']
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print(" mili " + str(millis))
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    url = request.POST.get('url')
    print(url)

    # idtoken = request.session['jame']
    # a = auth.get_account_info(idtoken)
    # a = a['Accounts']
    # a = a[0]
    # a = a['james']
    # print("info"+str(a))

    data = {
        "work": work,
        'progress': progress,
        'url': url
    }
    print(url)
    db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(millis).set(data)
    return render(request, 'test.html')


def home(request):


    import datetime
    try:

        username = request.session['yourname']
        uname = username
        with open("connected.txt", "a") as f:
            f.write("\n")
            f.write(username)
        del request.session['yourname']

    except:

        with open("connected.txt", "r") as f:
            username = f.readlines()
        uname = username[-1]








    print(uname,"456456453265123645325135")


    # all =  db.child("Accounts").child(uname).get()
    # for a in all.each():
    #     bio = a.val()
    #     print(bio)

    # people = db.child("Accounts").child(uname).child('details').get()
    # for p in people.each():
    #     x = p.val()
    #     print(x)

    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').get().val()

    # print(prot)
    # propic = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').child(prot).child('url').get().val()
    # print(propic)

    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()




    # timestamps = db.child('Accounts').child(uname).child('details').child('images').child('photos').shallow().get().val()
    # lis_time = []
    #
    # for i in timestamps:
    #     lis_time.append(i)
    # lis_time.sort(reverse=True)
    # print(lis_time)
    #
    # des = []
    # urls = []
    # date = []
    #
    # for i in lis_time:
    #     descrip = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
    #         'description').get().val()
    #     des.append(descrip)
    #
    #     pic = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
    #         'url').get().val()
    #     urls.append(pic)
    #
    #     i = float(i)
    #     dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    #     date.append(dat)

    # print(date)
    # print(urls)
    # print(des)

    # urls = []
    # for i in lis_time:
    #     pic = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
    #         'url').get().val()
    #     urls.append(pic)
    # # print(urls)
    #
    # date = []
    # for i in lis_time:
    #     i = float(i)
    #     dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    #     date.append(dat)
    # # print(date)

    # comb_lis = zip(lis_time, date, des, urls)


    names = []
    alluser = db.child('Accounts').get().val()
    print(alluser)
    des = []
    urls = []
    date = []
    lis_time = []


    for l in alluser:

        timestamps = db.child('Accounts').child(l).child('details').child('images').child('photos').shallow().get().val()

        photo = True
        try:

            for i in timestamps:
                lis_time.append(i)

            lis_time.sort(reverse=True)
            # print(lis_time)

        except:

            photo = False

        if photo == True:
            for i in lis_time:
                descrip = db.child('Accounts').child(l).child('details').child('images').child('photos').child(i).child('description').get().val()
                des.append(descrip)

                pic = db.child('Accounts').child(l).child('details').child('images').child('photos').child(i).child('url').get().val()
                urls.append(pic)

                i = float(i)
                dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
                date.append(dat)

                allname = db.child('Accounts').child(l).child('details').child('fullname').get().val()
                names.append(allname)
        else:
            print("no Photos")
            pass
    comb_lis = zip(lis_time, date, des, urls, names)








    if request.method == 'POST' and 'upload-post' in request.POST:

            import time
            from datetime import datetime, timezone
            import pytz
            tz = pytz.timezone('Asia/Kolkata')
            time_now = datetime.now(timezone.utc).astimezone(tz)
            millis = int(time.mktime(time_now.timetuple()))
            print(" mili " + str(millis))
            description = request.POST.get('description')

            url = request.POST.get('url')
            print(url)
            data = {
                'time': millis,
                'description': description,
                'url': url
            }
            print(url)
            db.child('Accounts').child(uname).child('details').child('images').child('photos').child(millis).set(data)
            return redirect('home')
    return render(request, 'home.html', {'name': name,  'list': comb_lis})



def profile(request):
    import datetime

    # uname = request.session['yourname']
    # print(uname)
    uname = 'Ali'




    prot = db.child('Accounts').child(uname).child('details').child('images').child('profilepic').get().val()

    name = db.child('Accounts').child(uname).child('details').child('fullname').get().val()

    timestamps = db.child('Accounts').child(uname).child('details').child('images').child(
        'photos').shallow().get().val()
    lis_time = []

    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    print(lis_time)

    des = []
    urls = []
    date = []

    for i in lis_time:
        descrip = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
            'description').get().val()
        des.append(descrip)

        pic = db.child('Accounts').child(uname).child('details').child('images').child('photos').child(i).child(
            'url').get().val()
        urls.append(pic)

        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    comb_lis = zip(lis_time, date, des, urls)

    for i in comb_lis:
        print(i)

    if request.method == 'POST' and 'upload-post' in request.POST:
        import time
        from datetime import datetime, timezone
        import pytz
        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        print(" mili " + str(millis))
        description = request.POST.get('description')

        url = request.POST.get('url')
        print(url)
        data = {
            'time': millis,
            'description': description,
            'url': url
        }
        print(url)
        db.child('Accounts').child(uname).child('details').child('images').child('photos').child(millis).set(data)
        return render(request, 'profile.html', {'name': name, 'comb_lis': comb_lis})
    return render(request, 'profile.html', {'name': name, 'comb_lis': comb_lis})







def news(request):
    return render(request,'news.html')





# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
#             iiiiiiii
# iiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiii
#
#
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
#
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii
# iiiiiiii
# iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiii                 iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiii                iiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
