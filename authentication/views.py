from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from ads_system.models import CustomUser
from .forms import *
from django.contrib import messages
from .gmail import sendingMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            username=form.cleaned_data['email']
            email=form.cleaned_data['email']
            pass1=form.cleaned_data['password']
            pass2 = form.cleaned_data['verify_password']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']

            if CustomUser.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect('register')
        
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!!")
                return redirect('register')
            
            if len(first_name)>20 or len(last_name)>20:
                messages.error(request, "Le nom et le prénom ne doivent pas dépasser les 20 caractères.")
                return redirect('register')
            
            if len(first_name)<2 or len(last_name)<2:
                messages.error(request, "Le nom et le prénom doivent contenir au moins 2 caractères.")
                return redirect('register')
            
            if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('register')
            
            if not first_name.isalpha() or not first_name.isalpha():
                messages.error(request, "Name and Last Name must only contain letters!")
                return redirect('register')
            
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.is_active = False
            user.save()

            messages.success(request, 'Registration successful. We have sent you a confirmation email to activate your account.')

            current_site = get_current_site(request)
            email_subject = "Email de confirmation Bookaz"
            message = render_to_string('auth/email_confirmation.html',{
                
                'name': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            
            sendingMessage(user.username, email_subject, message)
            
        
            
            return redirect('login')  # Redirect to the login page or another appropriate page
    else:
        form = RegistrationForm()
        

    return render(request, 'auth/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('/')

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request,'auth/activation_failed.html')
    
@login_required
def settings(request):

    if request.method == 'POST':
        first_name = request.POST.get('fname').strip()
        last_name = request.POST.get('lname').strip()
        old_pass = request.POST.get('old_pass').strip()
        new_pass = request.POST.get('new_pass').strip()

        if len(first_name)>20 or len(last_name)>20:
                messages.error(request, "Le nom et le prénom ne doivent pas dépasser les 20 caractères.")
                return redirect('/settings')
            
        if len(first_name)<2 or len(last_name)<2:
            messages.error(request, "Le nom et le prénom doivent contenir au moins 2 caractères.")
            return redirect('/settings')
        
        if not first_name.isalpha() or not first_name.isalpha():
                messages.error(request, "Le nom et le prénom doivent contenir uniquement des letters!")
                return redirect('/settings')
        
        request.user.last_name = last_name
        request.user.first_name = first_name
        request.user.save()
        
        if old_pass == "" and new_pass == "":
            pass
        else:
            if old_pass == new_pass:
                messages.error(request, "Votre nouveau mot de passe est similaire à votre ancien!")
                return redirect('/settings')
            
            if check_password(old_pass, request.user.password):
                request.user.set_password(new_pass)
            else:
                messages.error(request, "Votre ancien mot de passe ne correspond pas!")
                return redirect('/settings')
        
        messages.success(request, 'Votre profile a été mis à jour avec succès.')
    return render(request, 'settings.html', {'user':request.user})