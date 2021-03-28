from django.shortcuts import render, redirect
from django.http import Http404
from .models import *
from django.db.models import Q, Min
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    title = "All You will ever need for Education in Azamgarh"
    tutordata = tutor.objects.order_by('-count')[:5]
    colleges = college.objects.order_by('-count')[:5]
    schools = school.objects.order_by('-count')[:5]
    institutes = institute.objects.order_by('-count')[:5]
    minbookdata = books.objects.filter().values_list('bookname','overview').annotate(Min('sellprice')).order_by('sellprice')[0]
    minbook = minbookdata[0]
    minoverview = minbookdata[1]
    minprice = minbookdata[2]
    minspacedata = spaces.objects.filter().values_list('location','equip').annotate(Min('charge')).order_by('charge')[0]
    minlocation = minspacedata[0]
    minequip = minspacedata[1]
    mincharge = minspacedata[2]
    mostviewed = courses.objects.order_by('-count')[:1]
    parms = {
        'title':title,
        'tutordata':tutordata,
        'institutes':institutes,
        'schools':schools,
        'minprice':minprice,
        'minbook':minbook,
        'minoverview':minoverview,
        'minlocation':minlocation,
        'minequip':minequip,
        'mincharge':mincharge,
        'mostviewed':mostviewed,
        'colleges':colleges,
    }
    return render(request, 'index.html',parms)

def reg_tutor(request):
    title = "Register for a tutor and Start Earning!"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_tutor == True:
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                url = fs.url(filename)
                image = url
                name =  request.POST.get('name')
                email = request.POST.get('email')
                mobno = request.POST.get('mobno')
                subject = request.POST.get('subject')
                hours = request.POST.get('hours')
                days = request.POST.get('days')
                price = request.POST.get('price')
                tutor(name=name,email=email,mobno=mobno,subject=subject,hours=hours,days=days,price=price,image=image).save()
                return redirect(success,who=1)
        else:
            messages.info(request,'Register with a tutor account first!')
            return redirect('logout')
    else:
        return redirect('signup')
    return render(request,'register_tutor.html',{'title':title,})
        
def tutorsearch(request):
    title = "Tutors Available in Azamgarh"
    query = request.GET.get('q')
    if query is not None:
        object_list = tutor.objects.filter(
            Q(name__icontains = query) | Q(subject__icontains = query) | Q(price__icontains = query)
        )
        parms = {
            'title':title,
            'object_list':object_list,
        }
    else:
        object_list = tutor.objects.all()
        parms = {
            'title':title,
            'object_list':object_list,
        }
    return render(request, 'tutorsearch.html', parms)

def profiletutor(request, id):
    try:
        obj = tutor.objects.get(pk=id)
    except:
        raise Http404("Tutor Does Not Exist") 
    title = "Hello, "+obj.name
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_tutor==True and user.email == obj.email:
            ownprofile = True
            if request.method == 'POST':
                obj.name =  request.POST.get('name')
                obj.mobno = request.POST.get('mobno')
                obj.subject = request.POST.get('subject')
                obj.hours = request.POST.get('hours')
                obj.days = request.POST.get('days')
                obj.price = request.POST.get('price')
                obj.save()
                return redirect(profiletutor,id)
        else:
            ownprofile= False
    else:
        obj.count+=1
        obj.save()
        ownprofile = False
    parms = {
            'title':title,
            'obj':obj,
            'ownprofile':ownprofile,
        }
    return render(request, 'profiletutor.html', parms)

def reg_school(request):
    title = "Register Your School and Check who's on the top"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_school == True:
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                url = fs.url(filename)
                image = url
                name = request.POST.get('name')
                email = request.POST.get('email')
                mobno = request.POST.get('mobno')
                board = request.POST.get('board')
                website = request.POST.get('website')
                tillclass = request.POST.get('tillclass')
                medium = request.POST.get('medium')
                fees = request.POST.get('fees')
                location = request.POST.get('location')
                school(name=name,email=email,mobno=mobno,board=board,website=website,tillclass=tillclass,medium=medium,fees=fees,location=location,image=image).save()
                return redirect(success,who=2)
        else:
            messages.info(request,'Register with a School account first!')
            return redirect('logout')
    else:
        return redirect('signup')
    return render(request,'reg_school.html',{'title':title,})

def success(request, who):
    if who == 1:
        title = "Register for a Tutor and get listed in Azamgarh Tutor List!"
        message = 'You have been successfully registered as a tutor! Congrats! You will start recieving calls soon!'
    if who == 2:
        title = "Register Your School and Check who's on the top"
        message = "You have been successfully registered as a school on Proxima Care! You will start recieving calls soon!"
    if who == 3:
        title = "Sell your second hand books here in Azamgarh"
        message = "You have successfully submitted your book for selling!"
    if who == 4:
        title = "Register Your Free Space available for teaching and earn some Cash!"
        message = "Your have successfully registered your rooms for Rent!"
    if who == 5:
        title = "Stuck anywhere? Contact us Right Away!"
        message = "Success, We will contact you very soon! Thank you!"
    if who == 6:
        title="Register your Coaching Institute and get listed in Azamgarh!"
        message = "Congrats! You have successdfully registered your Institute!"
    if who == 7:
        title="Enroll Easily with Proxima Edu Care!"
        message = "Congrats! You have successfully taken up a step towards being a better Version of Yourself! We will contact you soon, If we don't respond, feel free to call us at 7007013502"
    if who == 8:
        title="Register Your College and Check who's on the top"
        message="You have been successfully registered as a college on Proxima Care! You will start recieving calls soon!"
    parms = {
        'title':title,
        'message':message,
    }
    return render(request, 'success.html', parms)

def schoolsearch(request):
    title = "Schools Available in Azamgarh"
    user = request.user
    query = request.GET.get('q')
    if query is not None:
        object_list = school.objects.filter(
            Q(name__icontains = query) | Q(location__icontains = query) | Q(medium__icontains = query) | Q(board__icontains = query) | Q(fees__icontains = query)
        )
        parms = {
            'title':title,
            'object_list':object_list,
            'user':user,
        }
    else:
        object_list = school.objects.all()
        parms = {
            'title':title,
            'object_list':object_list,
            'user':user,
        }
    return render(request, 'schoolsearch.html', parms)

def profileschool(request, id):
    try:
        obj = school.objects.get(pk=id)
    except:
        raise Http404("School Does Not Exist") 
    title = "Welcome, "+obj.name
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_school==True and user.email == obj.email:
            ownprofile = True
            if request.method == 'POST':
                obj.name = request.POST.get('name')
                obj.mobno = request.POST.get('mobno')
                obj.board = request.POST.get('board')
                obj.website = request.POST.get('website')
                obj.tillclass = request.POST.get('tillclass')
                obj.medium = request.POST.get('medium')
                obj.fees = request.POST.get('fees')
                obj.location = request.POST.get('location')
                obj.save()
                return redirect(profileschool,id)
        else:
            ownprofile= False
    else:
        obj.count+=1
        obj.save()
        ownprofile = False
    parms = {
        'title':title,
        'obj':obj,
        'ownprofile':ownprofile,
    }
    return render(request, 'profileschool.html', parms)

def sell(request):
    title = "Sell your second hand books here in Azamgarh"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_seller == True:
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                url = fs.url(filename)
                image = url
                bookname = request.POST.get('bookname')
                selleremail = request.POST.get('selleremail')
                sellerno = request.POST.get('sellerno')
                sellername = request.POST.get('sellername')
                sellprice = request.POST.get('sellprice')
                orgprice = request.POST.get('orgprice')
                quantity = request.POST.get('quantity')
                overview = request.POST.get('overview')
                books(bookname=bookname,sellername=sellername,sellerno=sellerno,selleremail=selleremail,sellprice=sellprice,orgprice=orgprice,quantity=quantity,overview=overview,image=image).save()
                return redirect(success,who=3)
        else:
            messages.info(request,'Register with a Seller account first!')
            return redirect('logout')
    else:
        return redirect(signup)
    return render(request,'sell.html',{'title':title,})

def buy(request):
    title = "Buy Second Hand Books in Azamgarh!"
    minbookdata = books.objects.filter().values_list('bookname','overview').annotate(Min('sellprice')).order_by('sellprice')[0]
    minbook = minbookdata[0]
    minoverview = minbookdata[1]
    minprice = minbookdata[2]
    query = request.GET.get('q')
    if query is not None:
        object_list = books.objects.filter(
            Q(bookname__icontains = query) | Q(sellprice__icontains = query) | Q(selllername__icontains = query)
        )
        parms = {
            'title':title,
            'object_list':object_list,
            'minprice':minprice,
            'minbook':minbook,
            'minoverview':minoverview,
        }
    else:
        object_list = books.objects.all()
        parms = {
            'title':title,
            'object_list':object_list,
            'minbook':minbook,
            'minprice':minprice,
            'minoverview':minoverview,
        }
    return render(request, 'buy.html', parms)

def profilebook(request, id):
    try:
        obj = books.objects.get(pk=id)
    except:
        raise Http404("book Does Not Exist") 
    title = "Want to Buy - "+obj.bookname+"?"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_seller==True and user.email == obj.selleremail:
            ownprofile = True
            if request.method == 'POST':
                obj.bookname = request.POST.get('bookname')
                obj.sellerno = request.POST.get('selllerno')
                obj.sellername = request.POST.get('sellername')
                obj.sellprice = request.POST.get('sellprice')
                obj.orgprice = request.POST.get('orgprice')
                obj.quantity = request.POST.get('quantity')
                obj.overview = request.POST.get('overview')
                obj.save()
                return redirect(profilebook,id)
        else:
            ownprofile= False
    else:
        ownprofile = False
    parms = {
        'title':title,
         'obj':obj,
         'ownprofile':ownprofile,
    }
    return render(request, 'profilebook.html', parms)

def sharespace(request):
    title = "Register Your Free Space available for teaching and earn some Cash!"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_owner == True:
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                url = fs.url(filename)
                image = url
                location = request.POST.get('location')
                rooms = request.POST.get('rooms')
                equip = request.POST.get('equip')
                hours = request.POST.get('hours')
                charge = request.POST.get('charge')
                sellername = request.POST.get('sellername')
                sellerno = request.POST.get('sellerno')
                selleremail = request.POST.get('selleremail')
                spaces(location=location,rooms=rooms,equip=equip,hours=hours,charge=charge,sellername=sellername,sellerno=sellerno,selleremail=selleremail,image=image).save()
                return redirect(success,who=4)
        else:
            messages.info(request,'Register with a Owner account first!')
            return redirect('logout')
    else:
        return redirect('signup')
    return render(request,'sharespace.html',{'title':title,})

def needspace(request):
    title = "Need Space for teaching? Get rented Educational Rooms here in Azamgarh!"
    minspacedata = spaces.objects.filter().values_list('location','equip').annotate(Min('charge')).order_by('charge')[0]
    minlocation = minspacedata[0]
    minequip = minspacedata[1]
    mincharge = minspacedata[2]
    query = request.GET.get('q')
    if query is not None:
        object_list = spaces.objects.filter(
            Q(location__icontains = query) | Q(rooms__icontains = query) | Q(charge__icontains = query)
        )
        parms = {
            'title':title,
            'object_list':object_list,
            'minlocation':minlocation,
            'minequip':minequip,
            'mincharge':mincharge,
        }
    else:
        object_list = spaces.objects.all()
        parms = {
            'title':title,
            'object_list':object_list,
            'minlocation':minlocation,
            'minequip':minequip,
            'mincharge':mincharge,
        }
    return render(request, 'needspace.html', parms)

def profilespace(request, id):
    try:
        obj = spaces.objects.get(pk=id)
    except:
        raise Http404("Space Does Not Exist") 
    title = "Want to Rent - "+obj.location+"?"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_owner==True and user.email == obj.selleremail:
            ownprofile = True
            if request.method == 'POST':
                obj.location = request.POST.get('location')
                obj.rooms = request.POST.get('rooms')
                obj.equip = request.POST.get('equip')
                obj.hours = request.POST.get('hours')
                obj.charge = request.POST.get('charge')
                obj.sellername = request.POST.get('sellername')
                obj.sellerno = request.POST.get('sellerno')
                obj.save()
                return redirect(profilespace, id)
        else:
            ownprofile= False
    else:
        ownprofile = False
    parms = {
        'title':title,
         'obj':obj,
         'ownprofile':ownprofile,
    }
    return render(request, 'profilespace.html', parms)

def contact(request):
    title = "Stuck anywhere? Contact us Right Away!"
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        mobno = request.POST.get('mobno')
        contact(name=name,email=email,message=message,mobno=mobno).save()
        return redirect(success,who=5)
    parms ={
        'title':title,
    }
    return render(request,'contact.html',parms)

def about(request):
    title = "About Proxima Care"
    return render(request, 'about.html',{'title':title})

def reg_institute(request):
    title = "Register your Coaching Institute and get listed in Azamgarh!"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_institute == True:
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                url = fs.url(filename)
                image = url
                name = request.POST.get('name')
                email = request.POST.get('email')
                location = request.POST.get('location')
                major = request.POST.get('major')
                courses = request.POST.get('courses')
                years = request.POST.get('years')
                enroll = request.POST.get('enroll')
                foundername = request.POST.get('foundername')
                mobno = request.POST.get('mobno')
                website = request.POST.get('website')
                staff = request.POST.get('staff')
                institute(name=name,location=location,major=major,courses=courses,years=years,enroll=enroll,foundername=foundername,mobno=mobno,website=website,email=email,staff=staff,image=image).save()
                return redirect(success,who=6)
        else:
            messages.info(request,'Register with a Institute account first!')
            return redirect('logout')
    else:
        return redirect('signup')

    return render(request,'reg_institute.html',{'title':title,})

def institutesearch(request):
    title = "Institutes Available in Azamgarh"
    query = request.GET.get('q')
    if query is not None:
        object_list = institute.objects.filter(
            Q(name__icontains = query) | Q(location__icontains = query) | Q(major__icontains = query) | Q(courses__icontains = query) | Q(foundername__icontains = query)
        )
        parms = {
            'title':title,
            'object_list':object_list,
        }
    else:
        object_list = institute.objects.all()
        parms = {
            'title':title,
            'object_list':object_list,
        }
    return render(request, 'institutesearch.html', parms)

def profileinstitute(request, id):
    try:
        obj = institute.objects.get(pk=id)
    except:
        raise Http404("Institute Does Not Exist") 
    title = "Want to get enrolled to "+obj.name+"?"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_institute==True and user.email == obj.email:
            ownprofile = True
            if request.method == 'POST':
                obj.name = request.POST.get('name')
                obj.location = request.POST.get('location')
                obj.major = request.POST.get('major')
                obj.courses = request.POST.get('courses')
                obj.years = request.POST.get('years')
                obj.enroll = request.POST.get('enroll')
                obj.foundername = request.POST.get('foundername')
                obj.mobno = request.POST.get('mobno')
                obj.website = request.POST.get('website')
                obj.staff = request.POST.get('staff')
                obj.save()
                return redirect(profileinstitute,id)
        else:
            ownprofile= False
    else:
        obj.count+=1
        obj.save()
        ownprofile = False
    parms = {
        'title':title,
         'obj':obj,
         'ownprofile':ownprofile,
    }
    return render(request, 'profileinstitute.html', parms)

def signup(request):
    title = "Register with Proxima Care"
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        istype = request.POST['usertype']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
            else:
                if istype == 'is_student':
                    user = User.objects.create_user(username=username,password=password1,email=email).save()
                    extuser(email=email,is_student=True).save()
                    messages.info(request,'Student ID Created')
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('index')
                elif istype == 'is_tutor':
                    user = User.objects.create_user(username=username,password=password1,email=email).save()
                    extuser(email=email,is_tutor=True).save()
                    messages.info(request,'Tutor ID Created')
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('reg_tutor')
                elif istype == 'is_institute':
                    user = User.objects.create_user(username=username,password=password1,email=email).save()
                    extuser(email=email,is_institute=True).save()
                    messages.info(request,'Institute ID Created')
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('reg_institute')
                elif istype == 'is_school':
                    user = User.objects.create_user(username=username,password=password1,email=email).save()
                    extuser(email=email,is_school=True).save()
                    messages.info(request,'School ID Created')
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('reg_school')
                elif istype == 'is_owner':
                    user = User.objects.create_user(username=username,password=password1,email=email).save()
                    extuser(email=email,is_owner=True).save()
                    messages.info(request,'Owner ID Created')
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('sharespace')
                elif istype == 'is_seller':
                    user = User.objects.create_user(username=username,password=password1,email=email).save()
                    extuser(email=email,is_seller=True).save()
                    messages.info(request,'Seller ID Created')
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('sell')
                elif istype == 'is_college':
                    user = User.objects.create_user(username=username,password=password1,email=email).save()
                    extuser(email=email,is_college=True).save()
                    messages.info(request,'College ID Created')
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('reg_college')
                else:
                    messages.error(request,'Choose one type of account!')
        else:
            messages.info(request,'Password not matched')

    return render(request,'signup.html',{'title':title})

def login(request):
    title = "Login with Proxima Care"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'login.html',{'title':title})

def coursesearch(request):
    title = "Search Courses You Can Take Online/Offline!"
    query = request.GET.get('q')
    if query is not None:
        object_list = courses.objects.filter(
            Q(name__icontains = query) | Q(subject_icontains = query) | Q(tchrname__icontains = query) | Q(price__icontains = query) | Q(course_mode__icontains = query)
        )
        parms = {
            'title':title,
            'object_list':object_list,
        }
    else:
        object_list = courses.objects.all()
        parms = {
            'title':title,
            'object_list':object_list,
        }
    return render(request, 'coursesearch.html', parms)

def profilecourse(request,id):
    try:
        obj = courses.objects.get(pk=id)
    except:
        raise Http404("Course Does Not Exist") 
    title = "Want to get Buy "+obj.name+"?"
    obj.count+=1
    obj.save()
    parms = {
        'title':title,
         'obj':obj,
    }
    return render(request, 'profilecourse.html', parms)

        
def opencourse(request, id):
    title = "Welcome!"
    user = request.user
    if user.is_authenticated:
        isenroll = enroll.objects.filter(email=user.email)
        if isenroll[0].course_id == id:
            obj = courses.objects.get(pk=id)
            title = "Welcome to "+obj.name
            takeeps = epcourse.objects.filter(course_id=id)
            parms = {
                'title':title,
                'obj':obj,
                "takeeps":takeeps,
            }
    else:
        parms = {
            "title":title,
        }
        return redirect(loginenroll)
    
    return render(request, 'opencourse.html', parms)
    

def loginenroll(request):
    title = "Login from ID given by Admin to Access the Course!"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            isenroll = enroll.objects.filter(email=user.email)
            return redirect(opencourse,id=isenroll[0].course_id)
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'login.html',{'title':title})


def enrolldetails(request):
    title ="Enroll Easily with Proxima Edu Care!"
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        coursename = request.POST.get('coursename')
        mobno = request.POST.get('mobno')
        enrollcontact(name=name,email=email,coursename=coursename,mobno=mobno).save()
        return redirect(success,who=7)
    parms = {
        "title":title,
    }
    return render(request, 'enrolldetails.html',parms)

def collegesearch(request):
    title = "Search Colleges in Azamgarh"
    query = request.GET.get('q')
    if query is not None:
        object_list = college.objects.filter(
            Q(name__icontains = query) | Q(major_icontains = query) | Q(location__icontains = query)
        )
        parms = {
            'title':title,
            'object_list':object_list,
        }
    else:
        object_list = college.objects.all()
        parms = {
            'title':title,
            'object_list':object_list,
        }
    return render(request, 'collegesearch.html', parms)


def profilecollege(request, id):
    try:
        obj = college.objects.get(pk=id)
    except:
        raise Http404("College Does Not Exist") 
    title = "Welcome, "+obj.name
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_college==True and user.email == obj.email:
            ownprofile = True
            if request.method == 'POST':
                obj.name = request.POST.get('name')
                obj.mobno = request.POST.get('mobno')
                obj.major = request.POST.get('major')
                obj.website = request.POST.get('website')
                obj.fees = request.POST.get('fees')
                obj.location = request.POST.get('location')
                obj.save()
                return redirect(profilecollege, id)
        else:
            ownprofile= False
    else:
        obj.count+=1
        obj.save()
        ownprofile = False
    parms = {
        'title':title,
        'obj':obj,
        'ownprofile':ownprofile,
    }
    return render(request, 'profilecollege.html', parms)


def reg_college(request):
    title = "Register Your College and Check who's on the top"
    user = request.user
    if user.is_authenticated:
        istypes = extuser.objects.filter(email=user.email)
        if istypes[0].is_college == True:
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                url = fs.url(filename)
                image = url
                name = request.POST.get('name')
                email = request.POST.get('email')
                mobno = request.POST.get('mobno')
                major = request.POST.get('major')
                website = request.POST.get('website')
                fees = request.POST.get('fees')
                location = request.POST.get('location')
                college(name=name,email=email,mobno=mobno,major=major,website=website,fees=fees,location=location,image=image).save()
                return redirect(success,who=8)
        else:
            messages.info(request,'Register with a College account first!')
            return redirect('logout')
    else:
        return redirect('signup')
    return render(request,'reg_college.html',{'title':title,})