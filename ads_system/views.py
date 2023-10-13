from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import *
from django.contrib.auth.decorators import login_required
import ast, json
import time
from authentication.gmail import sendingMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

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

        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '')
        image = request.FILES.get('image', '')
        bundle_items = request.POST.get('bundle_items', '')

        if len(ast.literal_eval(bundle_items)) == 1:
            ad_type = "Unitaire"
            return render(request, 'ads/create_ad.html')
        elif len(ast.literal_eval(bundle_items)) >= 2:
            ad_type = "Pack"
        else:
            messages.error(request, 'Veuillez ajouter au moins un livre dans votre annonce.')
            return render(request, 'ads/create_ad.html', {'title': title, 'description':description, 'price':price})
        
        ad = ClassifiedAd.objects.create(
            user= request.user,
            title=title,
            description=description,
            price=price,
            image=image,
            ad_type=ad_type
        )

        for item in ast.literal_eval(bundle_items):
            book = Book.objects.create(
                titre=item.get('title'),
                editeur=item.get('publisher'),
                classe=item.get('class'),
                isbn=int(item.get('isbn').replace('-', '')),
                matiere=item.get('subject'),
                ad=ad
            )
            ad.bundle_items.add(book)
        
        request.user.ads.add(ad)
        
        return redirect('/')  # Redirect to the ad listing page after creating the ad

    return render(request, 'ads/create_ad.html')


def ad_view(request):
    ad_id = request.GET.get('ad_id')
    if ad_id == None:
        return redirect('/')
    else:
        ad = ClassifiedAd.objects.get(ad_id= ad_id)
        if ad == None:
            return redirect('/')
        else:
            return render(request, 'ads/ad_page.html', {'ad':ad})

@login_required
def myads(request):
    ads = request.user.ads
    print(ads)
    return render(request, 'ads/myads.html', {'ads':ads})

@login_required
def delete_ad(request):
    user = request.user
    ad_id = int(request.GET.get('ad_id'))
    for ad in user.ads.all():
        if ad.ad_id == ad_id:
            user.ads.remove(ad)
            user.save()
            ad.delete()
            return redirect('/myads')
    return redirect('/myads')

@login_required
def edit_ad(request):
    user = request.user
    ad_id = int(request.GET.get('ad_id'))
    ad = False
    for ad in user.ads.all():
        if ad.ad_id == ad_id:
            ad = ad
            break
    if not ad:
        return render('/myads')
    
    if request.method == "POST":
        # [{'title': 'Encanta', 'publisher': 'Palto', 'isbn': '231323232233', 'bookClass': 'Terminale', 'subject': 'Espagnol'}, {'title': 'English Life', 'publisher': 'Oxford', 'isbn': '322323232332', 'bookClass': 'Terminale', 'subject': 'Anglais'}]
        books = ast.literal_eval(request.POST.get('bookList'))
        
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        if len(books) == 1:
            ad.ad_type = 'Unitaire'
        elif len(books) >= 2:
            ad.ad_type = 'Pack'

        ad.bundle_items.clear()
        for book in books:
            new_book = Book.objects.create(
                titre=book.get('title'),
                editeur=book.get('publisher'),
                classe=book.get('class'),
                isbn=int(book.get('isbn').replace('-', '')),
                matiere=book.get('subject'),
                ad=ad
            )
            ad.bundle_items.add(new_book)


        ad.title = title
        ad.description = description
        ad.price = price
        if not image == None:
            ad.image = image
        
        ad.save()
        return redirect('/myads')

    return render(request, 'ads/edit_ad.html', {'ad':ad})


def categories(request):
    
    return render(request, "ads/categories.html")

def search(request):

    if request.method == 'GET':
        classe = request.GET.get('class')
        matiere = request.GET.get('subject')
        titre = request.GET.get('title')
        editeur = request.GET.get('editor')
        isbn = request.GET.get('isbn')
        books = Book.objects.all()

        if None not in (titre, matiere, classe):
            print('Searching')
            
            if len(titre.strip()) > 1:
                books = books.filter(titre__icontains=titre)
            if len(matiere.strip()) > 1:
                books = books.filter(matiere__icontains=matiere)
            if len(classe.strip()) > 1:
                books = books.filter(classe__icontains=classe)
            if len(editeur.strip()) > 1:
                books = books.filter(editeur__icontains=editeur)
            if len(isbn.strip()) > 1:
                books = books.filter(isbn__icontains=isbn)

        ads = []
        for i in books:
            if i.ad not in ads:
                ads.append(i.ad)
        paginator = Paginator(ads, 50)
        page_number = request.GET.get('page')
        ads = paginator.get_page(page_number)
    
    return render(request, "ads/search.html", {'ads':ads})