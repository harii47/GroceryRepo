from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from testapp.models import Grocery_Item_Model, User_Model,Bought_Item
import re

all_item = Grocery_Item_Model.objects.all()


def home(request):
    items = Grocery_Item_Model.objects.all()
    try:
        usr = request.session['user']
        print(usr)
        user = User_Model.objects.get(email=usr)
    except:
        return render(request, 'index.html', {'all_item': items})
    # Bought_Item.objects.get(user.id
    return render(request, 'index.html', {'all_item': items, 'user':user})


def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = str(request.POST.get('mobile'))
        email = request.POST.get('email')
        typo = "Registration"
        if (re.findall('^[9|8|7|6]', mobile)) == "9" or '8' or '7' or '6':
            if len(mobile) >= 10:
                request.session['user'] = email
                password = request.POST.get('password')
                if len(password) < 5:
                    reply = "Invalid Password please enter valid password"
                    return render(request, 'user_login_register.html', {'reply': reply, 'type': typo})
                try:
                    User_Model.objects.get(mobile=mobile)
                except User_Model.DoesNotExist:
                    try:
                        User_Model.objects.get(email=email)
                    except User_Model.DoesNotExist:
                        address = request.POST.get('address')
                        User_Model(name=name, mobile=mobile, email=email, password=password, address=address).save()
                        return redirect('/home')
                    else:
                        msg = 'The Given Email Id Is Already Registered with User '
                        return render(request, "user_login_register.html", {'type': typo, 'msg': msg})
                else:
                    msg = 'The Given Mobile Number Is Already Registered with user '
                    return render(request, "user_login_register.html", {'type': typo, 'msg': msg})
            else:
                msg = 'Invalid Mobile Number'
                return render(request, "user_login_register.html", {'type': typo, 'msg': msg})
        else:
            msg = 'Invalid Mobile Number'
            return render(request, "user_login_register.html", {'type': typo, 'msg': msg})

    return render(request, 'user_login_register.html', {'type': 'Registration', 'all_item': all_item})


def log_out(request):
    try:
        print(request.session['user'])
        del request.session['user']
        # request.session.modified = True
    except:
        all = Grocery_Item_Model.objects.all()
        return render(request, 'index.html', {'all_item': all})
    else:
        all = Grocery_Item_Model.objects.all()
        return render(request, 'index.html', {'all_item': all})


def login(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        try:
            User_Model.objects.get(email=email)
        except User_Model.DoesNotExist:
            return render(request, 'user_login_register.html',
                          {'type': 'Login', 'msg': "The Given USERNAME isn't correct !!!", })
        try:
            valid_std = User_Model.objects.get(email=email, password=str(password))
            request.session['user'] = email
        except User_Model.DoesNotExist:
            return render(request, 'user_login_register.html', {'type': 'Login', 'msg': "Wrong Password !!!", })
        else:
            return redirect('/home')
    return render(request, 'user_login_register.html', {'type': 'Login', 'all_item': all_item})


def select_item(request):
    user_id = request.GET.get('item_id')
    if request.method == "POST":
        try:
            user_id = request.session['user']
            user = User_Model.objects.get(email=user_id)
        except:
            return redirect('/login')
        item_id = request.GET.get('item_id')
        Bought_Item(grocery_item_id=item_id, user_id=user.id).save()
        return redirect('/home')
    print(type(user_id))
    item = Grocery_Item_Model.objects.get(id=user_id)
    return render(request, 'add.html',{'all_item':item})