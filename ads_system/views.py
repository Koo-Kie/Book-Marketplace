from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required

def home(request):
    ads = ClassifiedAd.objects.all()
    return render(request, 'home.html', {"ads": ads})

@login_required
def create_ad(request):
    if request.method == 'POST':
        print(request.POST)
        ad_type = request.POST.get('ad_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        bundle_items = request.POST.get('bundle_items')

        if ad_type == 'single':
            ad = ClassifiedAd.objects.create(
                title=title,
                description=description,
                price=price,
                image=image,
                ad_type=ad_type
            )
        else:
            ad = ClassifiedAd.objects.create(
                title=title,
                description=description,
                price=price,
                image=image,
                ad_type=ad_type,
                bundle_items=bundle_items
            )
        
        return redirect('/')  # Redirect to the ad listing page after creating the ad

    return render(request, 'ads/create_ad.html')
