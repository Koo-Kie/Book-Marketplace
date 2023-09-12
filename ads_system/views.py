from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
import ast
import time
from authentication.gmail import sendingMessage
from django.template.loader import render_to_string
from django.contrib import messages


def home(request):
    ads = ClassifiedAd.objects.all()
    return render(request, 'home.html', {"ads": ads})

def support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        message = render_to_string('auth/email_confirmation.html',{
                'name': name,
                'email':email,
                'message':message
            })
        try:
            sendingMessage(email,"Demande de support", message)
        except:
            messages.error(request, "L'addresse email est invalide.")

        time.sleep(1)
        sendingMessage('kaisgrati5+support@gmail.com',"Demande de support", message)
        messages.success(request, 'Votre message a été transmi au support avec succès!')


    if request.user.is_authenticated:
        user = request.user
        return render(request, 'support/support.html', {'user': user})
    else:
        return render(request, 'support/support.html')

@login_required
def create_ad(request):
    if request.method == 'POST':

        ad_type = request.POST.get('ad_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        bundle_items = request.POST.get('bundle_items')


        if ad_type == 'single':
            ad = ClassifiedAd.objects.create(
                user= request.user,
                title=title,
                description=description,
                price=price,
                image=image,
                ad_type=ad_type
            )
            request.user.ads.add(ad)
        else:
            ad = ClassifiedAd.objects.create(
                user= request.user,
                title=title,
                description=description,
                price=price,
                image=image,
                ad_type=ad_type,
                bundle_items=bundle_items
            )
            request.user.ads.add(ad)


        
        return redirect('/')  # Redirect to the ad listing page after creating the ad

    return render(request, 'ads/create_ad.html')


def ad_view(request):
    ad_id = request.GET.get('ad_id')
    if ad_id == None:
        return redirect('/')
    else:
        ad = ClassifiedAd.objects.get(ad_id= ad_id)
        try:
            ad.bundle_items = ast.literal_eval(ad.bundle_items)
        except:
            pass
        if ad == None:
            return redirect('/')
        else:
            return render(request, 'ads/ad_page.html', {'ad':ad})

@login_required
def myads(request):
    ads = request.user.ads
    print(ads)
    return render(request, 'ads/myads.html', {'ads':ads})