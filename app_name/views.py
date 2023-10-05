from django.shortcuts import render, get_object_or_404, redirect
from  .models import ContactUs, User, Product, WishList, Cart, ComplaintForm, Helpdesk, Checkout
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):
    products= Product.objects.all()
    return render(request, 'index.html', {'products':products})


def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email=request.POST.get('email', '')
        remark=request.POST.get('remark', '')

        if not name or not email or not remark:
            msgred = 'All fields are required!'
            return render(request, 'contactus.html', {'msgred': msgred})
        else:
            ContactUs.objects.create(
                name=name,
                email=email,
                remark=remark,
            )
        msg = 'We have recived your Contact Us Submission!'
        return render(request,'contactus.html',{"msg":msg})
    else:
        return render(request,'contactus.html')
    

def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        email = request.POST.get('email','')
        gender = request.POST.get('gender','')
        mobile = request.POST.get('mobile','')
        password = request.POST.get('password','')
        cpassword = request.POST.get('cpassword','')
        address = request.POST.get('address','')
        image = request.FILES.get('image', None)

        try:
            User.objects.get(email= email)
            msgred= 'Email is in use!'
            return render(request, 'signup.html', {'msgred':msgred})
        except:
            if password == cpassword:
                if not fname or not lname or not email or not gender or not mobile or not password or not cpassword or not address:
                    msgred = 'All fields are required, except Profile Image!'
                    return render (request, 'signup.html',{'msgred':msgred})
                else:
                    title= 'Sign Up OTP | BuyHere'
                    otp= random.randint(0000,9999)
                    message= f"YOur Sign Up OTP for BuyHere is {otp}."
                    sender= settings.EMAIL_HOST_USER
                    reciver= [email,]
                    send_mail(
                        title,
                        message,
                        sender,
                        reciver,
                        fail_silently= False
                    )
                    User.objects.create(
                        fname= fname,
                        lname= lname,
                        email= email,
                        gender= gender,
                        mobile= mobile,
                        password= password,
                        cpassword= cpassword,
                        address= address,
                        image = image,
                    )
                    msg = 'Sign Up Successfull, Verify OTP.'
                    return render (request, 'verify_signup_otp.html', {'msg':msg, 'email':email, "otp":otp})
            else:
                msgred = "Password and Confirm password don't match."
                return render (request, 'signup.html', {'msgred':msgred})
    else:
        return render (request, 'signup.html')
    

def verify_signup_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        otp2= request.POST['otp2']
        email= request.POST['email']
        if otp== otp2:
            user= User.objects.get(email=email)
            user.status= 'activate'
            user.save()
            msg= 'OTP Verified!'
            return render(request,'login.html', {'msg':msg})
        else:
            msgred= "OTP doesn't match!"
            return render(request, "verify_signup_otp.html", {'otp':otp, 'email':email, 'msgred':msgred})
    else:
        return render(request, 'verify_signup_otp.html')
    

def login(request):
    if request.method == 'POST':
        email= request.POST['email']
        enter_password= request.POST['password']
        try:
            user= User.objects.get(email= email, password= enter_password)
            wishlist= WishList.objects.filter(user= user)
            cart= Cart.objects.filter(user=user)
            request.session['email']= user.email
            request.session['fname']= user.fname
            request.session['image']= user.image.url
            request.session['wishlist']= len(wishlist)
            request.session['cart']= len(cart)
            msg= 'Log In Successfull!'
            return render (request, 'index.html',{'msg':msg})
        except ObjectDoesNotExist:
            msgred= 'Incorrect username and password!'
            return render(request, 'login.html', {'msgred':msgred})
    else:
        return render(request, 'login.html')
    
    

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['image']
        del request.session['wishlist']
        del request.session['cart']
        return render (request, 'login.html')
    except:
        del request.session['semail']
        del request.session['sfname']
        del request.session['simage']
        return render (request, 'login.html')

def user_change_password(request):
    if request.method=='POST':
        new_password= request.POST['new_password']
        confirm_password= request.POST['confirm_new_password']
        if new_password == confirm_password:
            try:
                user= User.objects.get(email = request.POST['email'],password = request.POST['current_password'])
                user.password= new_password
                user.cpassword= confirm_password
                user.save()
                return render(request, 'index.html', {'msg':'Password changeed successfully!'})
            except:
                msgred= "Current password dosen't match!"
                return render(request, 'user_change_password', {'msgred':msgred})
        else:
            msgred= "New password and Confirm password dosen't match"
            return render (request, 'user_change_password.html', {'msgred':msgred})   
    else:
        return render(request, 'user_change_password.html')
    

def seller_login(request):
    if request.method== "POST":
        email= request.POST['email']
        password= request.POST['password']
        try:
            user= User.objects.get(email= email, password= password)
            complaints = ComplaintForm.objects.filter()
            request.session['semail']= user.email
            request.session['sfname']= user.fname
            request.session['simage']= user.image.url
            msg= 'Seller Login Successfull!'
            return render(request, 'index.html', {'msg':msg})
        except:
            msgred= 'User not found!'
            return render(request, 'seller_login.html', {'msgred':msgred})
    else:
        return render (request, 'seller_login.html')
    

def seller_add_product(request):
    if request.method== 'POST':
        product_brand= request.POST['product_brand']
        product_model= request.POST['product_model']
        product_price= request.POST['product_price']
        product_desc= request.POST['product_desc']
        product_image= request.FILES['product_image']
        if not product_brand or not product_model or not product_price or not product_desc or not product_image:
            msgred= 'All Fields are required!'
            return render(request, 'seller_add_product.html', {'msgred':msgred})
        else:
            Product.objects.create(
                seller= User.objects.get(email= request.session['semail']),
                product_brand= product_brand,
                product_model= product_model,
                product_price= product_price,
                product_desc= product_desc,
                product_image= product_image,
            )
            msg= 'Product Added!'
            return render(request, 'seller_add_product.html',{'msg':msg})
    else:
        return render(request, 'seller_add_product.html')
    

def seller_view_product(request):
    seller= User.objects.get(email= request.session['semail'])
    products= Product.objects.filter(seller= seller)
    return render (request, 'seller_view_product.html', {'products':products})


def seller_product_details(request, product_id):
    product= get_object_or_404(Product, id=product_id)
    return render(request, 'seller_product_details.html', {'product':product})


def seller_edit_product(request, product_id):
    product= get_object_or_404(Product, id=product_id)
    if request.method== "POST":
        update_data= {
            'product_brand': request.POST['product_brand'],
            'product_model': request.POST['product_model'],
            'product_price': request.POST['product_price'],
            'product_desc': request.POST['product_desc'],
        }
        if 'product_image' in request.FILES:
            update_data['product_image']= request.FILES['product_image']

        for k,v in update_data.items():
            setattr(product,  k, v)

        try:
            msg= 'Edit saved!'
            product.save()
            return render(request, 'seller_product_details.html', {'product':product, "msg":msg})
        except:
            msgred= "An error occurred while saving the product."
            return render(request, 'seller_product_details.html', {'product':product, "msgred":msgred})
        
    else:
        return render(request, 'seller_edit_product.html', {'product':product})
    

def user_view_product(request, product_brand):
    brand_product= Product.objects.filter(product_brand= product_brand)
    products= Product.objects.all()
    return render (request, 'user_view_product.html', {'products':products, 'brand_product':brand_product})


def user_product_details(request, product_id):
        flag= False
        flag_cart= False
        user= User.objects.get(email= request.session['email'])
        product= get_object_or_404(Product, id=product_id)
        try:
            WishList.objects.get(user=user, product=product)
            flag= True
        except:
            pass
        try:
            Cart.objects.get(user=user, product=product)
            flag_cart= True
        except:
            pass
        return render(request, 'user_product_details.html', {'product':product, 'flag':flag, 'flag_cart':flag_cart})


def seller_delete_product(request, product_id):
    product= get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('seller_view_product')


def wishlist(request):
    flag= False
    user= User.objects.get(email= request.session['email'])
    wishlist= WishList.objects.filter(user= user)
    request.session['wishlist']= len(wishlist)
    try:
        product_id= WishList.objects.get(user=user).product_id
        Cart.objects.get(user=user, product_id=product_id)
        flag= True
    except:
        pass
    return render(request, 'wishlist.html', {'wishlist':wishlist, 'flag':flag})


def add_to_wishlist(request, product_id):
        user= User.objects.get(email= request.session['email'])
        product= Product.objects.get(id= product_id)
        wishlist= WishList.objects.filter(user= user)
        try:
            WishList.objects.get(product=product, user=user)
            msgred = "This product is already in your wishlist!"
            return render(request, 'wishlist.html', {'msgred':msgred,'wishlist':wishlist})
        except:
            WishList.objects.create(
                user=user,
                product=product,
            )
            msg= 'Product added to Wishlist!'
            return render(request, 'wishlist.html', {'msg':msg,'wishlist':wishlist})
        

def del_wishlist_product(request, product_id):
    user= User.objects.get(email= request.session['email'])
    product= Product.objects.get(id= product_id)
    wishlist_product= WishList.objects.get(user=user, product=product)
    wishlist_product.delete()
    wishlist= WishList.objects.filter(user= user)
    msg= 'Product Removed!'
    return render(request, 'wishlist.html',{'msg':msg,'wishlist':wishlist})


def add_to_cart(request, product_id):
    user= User.objects.get(email= request.session['email'])
    product= Product.objects.get(id= product_id)
    try:
        Cart.objects.get(product=product, user=user)
        msgred = "This product is already in your Cart!"
        return render(request, 'cart.html', {'msgred':msgred,'cart':cart})
    except:
        Cart.objects.create(
            user= user,
            product= product,
            price= product.product_price,
            total_price= product.product_price,
        )
        msg= 'Product added to Cart!'
        return redirect('cart')


def cart(request):
    user= User.objects.get(email= request.session['email'])
    cart= Cart.objects.filter(user= user)
    net_price= 0
    for i in cart:
        net_price= net_price + i.total_price
    request.session['cart']= len(cart)
    if user is None:
        msgred= 'No cart item found.'
        return render(request, 'cart.html',{'msgred':msgred})
    else:    
        return render(request, 'cart.html',{'cart':cart, 'net_price':net_price})
    

def del_cart_product(request, product_id):
    user = User.objects.get(email=request.session['email'])
    cart_product= Cart.objects.get(user=user, product_id=product_id)
    cart_product.delete()
    cart= Cart.objects.filter(user=user)
    request.session['cart']=len(cart)
    msg= 'Cart product removed!'
    return redirect('cart')


def change_qty(request):
    cart_product= Cart.objects.get(id= request.POST['id'])
    qty= request.POST['qty']
    cart_product.qty= qty
    cart_product.total_price= int(qty) * int(cart_product.price)
    cart_product.save()
    return redirect('cart')


def check(request):
    apple= Product.objects.filter(product_brand= "Apple")
    return render(request, 'check.html', {'apple': apple})


def complaint_form(request):
    seller_key= User.objects.all()
    product_key= Product.objects.all()

    if request.method== "POST":
        name= request.POST.get('name','')
        seller = request.POST.get('seller','')
        product = request.POST.get('product', '')
        email = request.POST.get('email', '')
        complaint = request.POST.get('complaint', '')

        if not seller or not product or not email or not complaint or not name:
            msgred = 'All fields are required!'
            return render(request, 'complaint_form.html', {'msgred': msgred, 'seller_key': seller_key, 'product_key': product_key})
        else:
            ComplaintForm.objects.create(
                name= name,
                seller= seller,
                product= product,
                email= email,
                complaint= complaint
            )
            msg = f'Seller have recived your Complaint!'
            return render(request,'complaint_form.html',{"msg":msg, 'seller_key': seller_key, 'product_key': product_key})
    else:
        return render (request, 'complaint_form.html', {'seller_key': seller_key, 'product_key': product_key})
    
    
def helpdesk(request):
        seller_key= User.objects.all()
        product_key= Product.objects.all()

        if request.method== "POST":
            name= request.POST.get('name','')
            seller = request.POST.get('seller','')
            product = request.POST.get('product', '')
            email = request.POST.get('email', '')
            note = request.POST.get('note', '')

            if not seller or not product or not email or not note or not name:
                msgred = 'All fields are required!'
                return render(request, 'helpdesk.html', {'msgred': msgred, 'seller_key': seller_key, 'product_key': product_key})
            else:
                Helpdesk.objects.create(
                    name= name,
                    seller= seller,
                    product= product,
                    email= email,
                    note= note
                )
                msg = 'Seller have recived your Note!'
                return render(request,'helpdesk.html',{"msg":msg, 'seller_key': seller_key, 'product_key': product_key})
        else:
            return render (request, 'helpdesk.html', {'seller_key': seller_key, 'product_key': product_key})


def complain_view(request):
        complaint= ComplaintForm.objects.filter(seller= request.session['semail'])
        if not complaint.exists():
            msg= "No Complaints!"
            return render(request, 'complain_view.html', {'complaint':complaint, 'msg':msg})
        else:
            return render(request, 'complain_view.html', {'complaint':complaint})


def delete_complaint(request,id):
    complaint= ComplaintForm.objects.get(id= id)
    complaint.delete()
    return redirect('complain_view')


def helpdesk_view(request):
    helpdesk_note= Helpdesk.objects.filter(seller= request.session['semail'])
    if not helpdesk_note.exists():
        msg= 'No help notes!'
        return render(request, 'helpdesk_view.html', {'helpdesk_note':helpdesk_note, 'msg':msg})
    else:
        return render(request, 'helpdesk_view.html', {'helpdesk_note':helpdesk_note})       


def delete_helpdesknote(request,id):
    helpdesk_note= Helpdesk.objects.get(id= id)
    helpdesk_note.delete()
    return redirect('helpdesk_view')


def checkout(request):
    user= User.objects.get(email= request.session['email'])
    cart= Cart.objects.filter(user= user)
    net_price= 0
    
    
    for i in cart:
        net_price= net_price + i.total_price


    if request.method == 'POST':
        name= request.POST.get('name','')
        email= request.POST.get('email','')
        mobile= request.POST.get('mobile','')
        city= request.POST.get('city','')
        state= request.POST.get('state','')
        zip= request.POST.get('zip','')
        address= request.POST.get('address','')
        
        if not name or not email or not mobile or not city or not state or not zip or not address:
            msgred = 'All fields are required!'
            return render(request,'checkout.html', {'cart':cart, "net_price":net_price, 'msgred':msgred})
        else:
            Checkout.objects.create(
                name= name,
                email= email,
                mobile=mobile,
                city=city,
                state=state,
                zip= zip,
                address= address,
            	)
            msg = 'Check out form created, Payment getaway will be added soon!'
            return render (request, 'checkout.html', {'cart':cart, "net_price":net_price, 'msg':msg})
    else:
        return render(request,'checkout.html', {'cart':cart, "net_price":net_price})