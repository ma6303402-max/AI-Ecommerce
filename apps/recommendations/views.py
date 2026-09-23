from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.products.models import Product
from .engine import RecommendationEngine

def get_recommendations_api(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    engine = RecommendationEngine()
    similar = engine.get_similar_products(product, limit=4)

    data = []
    for item in similar:
        p = item['product']
        data.append({
            'id': p.id,
            'title': p.title,
            'price': str(p.price),
            'image_url': p.image_url,
            'url': f"/product/{p.slug}/",
            'similarity_score': item['similarity_score'],
            'explanation': item['explanation'],
            'category': p.category.name,
        })

    return JsonResponse({
        'source_product': product.title,
        'recommendations': data
    })

def personalized_recommendations_api(request):
    engine = RecommendationEngine()
    recs = engine.get_personalized_recommendations(request, limit=4)

    data = []
    for item in recs:
        p = item['product']
        data.append({
            'id': p.id,
            'title': p.title,
            'price': str(p.price),
            'image_url': p.image_url,
            'url': f"/product/{p.slug}/",
            'explanation': item['explanation'],
            'category': p.category.name,
        })

    return JsonResponse({'recommendations': data})

import json
from django.views.decorators.csrf import csrf_exempt
from apps.cart.cart import get_or_create_cart
from django.db.models import Q

@csrf_exempt
def ai_chat_recommendations_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_msg = data.get('message', '').strip().lower()
        except Exception:
            user_msg = request.POST.get('message', '').strip().lower()

        engine = RecommendationEngine()
        cart = get_or_create_cart(request)
        cart_items = cart.items.select_related('product').all()

        products_data = []

        # Intent 1: Headphones / Audio / Music
        if any(w in user_msg for w in ['headphone', 'audio', 'sound', 'music', 'earphone', 'speaker', 'listen', 'samma3a']):
            headphones = Product.objects.filter(Q(title__icontains='headphones') | Q(tags__icontains='audio')).first()
            smartwatch = Product.objects.filter(Q(title__icontains='watch') | Q(tags__icontains='watch')).first()

            reply = (
                "Here are smart audio & wearable recommendations for you: 🎧 <strong>Pulse ANC Spatial Headphones</strong> for audiophile acoustic playback.<br>"
                "💡 <strong>Pro-Tip Recommendation:</strong> Pair it with the ⌚ <strong>Zenith Pro Smartwatch</strong> so you can easily skip tracks, adjust volume, and control music playback directly from your wrist while on the go!"
            )

            for p, exp in [(headphones, "Top acoustic clarity & adaptive active noise cancellation"), (smartwatch, "Pairs logically: Control headphone track playback directly from your wrist!")]:
                if p:
                    products_data.append({
                        'id': p.id,
                        'title': p.title,
                        'price': str(p.price),
                        'image_url': p.image_url,
                        'url': f"/product/{p.slug}/",
                        'explanation': exp
                    })

        # Intent 2: Laptop / Computing / Workstation / Display
        elif any(w in user_msg for w in ['laptop', 'computer', 'workstation', 'screen', 'monitor', 'display', 'developer', 'code', 'render']):
            laptop = Product.objects.filter(Q(title__icontains='laptop') | Q(tags__icontains='laptop')).first()
            monitor = Product.objects.filter(Q(title__icontains='monitor') | Q(tags__icontains='monitor')).first()

            reply = (
                "Here is the ultimate developer & workstation recommendation: 💻 <strong>Hyperion X1 Neural Laptop</strong> with 45 TOPS NPU acceleration.<br>"
                "💡 <strong>Pro-Tip Recommendation:</strong> Connect it with the 🖥️ <strong>Vortex Curved 4K AI Display</strong> for dual-screen productivity, 3D rendering, and color-accurate video editing!"
            )

            for p, exp in [(laptop, "45 TOPS NPU neural processing for developer models"), (monitor, "Pairs logically: Dual-screen productivity & 4K color studio setup")]:
                if p:
                    products_data.append({
                        'id': p.id,
                        'title': p.title,
                        'price': str(p.price),
                        'image_url': p.image_url,
                        'url': f"/product/{p.slug}/",
                        'explanation': exp
                    })

        # Intent 3: Smart Home / Security / Camera / Climate
        elif any(w in user_msg for w in ['home', 'camera', 'security', 'thermostat', 'climate', 'house', 'smart home']):
            camera = Product.objects.filter(Q(title__icontains='camera') | Q(tags__icontains='camera')).first()
            thermostat = Product.objects.filter(Q(title__icontains='climate') | Q(tags__icontains='climate')).first()

            reply = (
                "Here are intelligent smart home ecosystem recommendations: 🏠 <strong>Sentinel 4K Security Camera Hub</strong> for edge AI facial recognition.<br>"
                "💡 <strong>Ecosystem Bundle:</strong> Add the 🌡️ <strong>OmniSmart AI Climate Controller</strong> to automatically reduce home energy consumption by up to 35%!"
            )

            for p, exp in [(camera, "Local edge AI facial recognition & 4K infrared security"), (thermostat, "Pairs logically: Learns room usage patterns & saves 35% energy")]:
                if p:
                    products_data.append({
                        'id': p.id,
                        'title': p.title,
                        'price': str(p.price),
                        'image_url': p.image_url,
                        'url': f"/product/{p.slug}/",
                        'explanation': exp
                    })

        # Intent 4: Watch / Fitness / Wearable
        elif any(w in user_msg for w in ['watch', 'fitness', 'health', 'sleep', 'wearable']):
            smartwatch = Product.objects.filter(Q(title__icontains='watch') | Q(tags__icontains='watch')).first()
            headphones = Product.objects.filter(Q(title__icontains='headphones') | Q(tags__icontains='headphones')).first()

            reply = (
                "Here is your wearable fitness recommendation: ⌚ <strong>Zenith Pro Smartwatch</strong> with continuous ECG & AI sleep coaching.<br>"
                "💡 <strong>Workout Pair Suggestion:</strong> Combine with 🎧 <strong>Pulse ANC Headphones</strong> for wireless workout sound and wrist playback control!"
            )

            for p, exp in [(smartwatch, "Titanium smartwatch with ECG & 14-day battery life"), (headphones, "Pairs logically: Workout audio controlled right from your smartwatch!")]:
                if p:
                    products_data.append({
                        'id': p.id,
                        'title': p.title,
                        'price': str(p.price),
                        'image_url': p.image_url,
                        'url': f"/product/{p.slug}/",
                        'explanation': exp
                    })

        # Intent 5: Cart Complements Query
        elif 'cart' in user_msg or 'my cart' in user_msg or 'buy' in user_msg:
            if cart_items.exists():
                recs = engine.get_personalized_recommendations(request, limit=3)
                reply = f"I analyzed your cart ({cart.get_total_items()} items). Here are smart complements recommended for your current setup:"
                for item in recs:
                    p = item['product']
                    products_data.append({
                        'id': p.id,
                        'title': p.title,
                        'price': str(p.price),
                        'image_url': p.image_url,
                        'url': f"/product/{p.slug}/",
                        'explanation': item['explanation']
                    })
            else:
                trending = engine.get_trending_products(limit=3)
                reply = "Your cart is currently empty! Here are top trending AI products to get you started:"
                for item in trending:
                    p = item['product']
                    products_data.append({
                        'id': p.id,
                        'title': p.title,
                        'price': str(p.price),
                        'image_url': p.image_url,
                        'url': f"/product/{p.slug}/",
                        'explanation': item['explanation']
                    })

        # Intent 6: Trending / Popular / Budget
        elif 'trend' in user_msg or 'popular' in user_msg or 'best' in user_msg or 'top' in user_msg:
            trending = engine.get_trending_products(limit=3)
            reply = "Here are the top trending & community favorite tech items right now:"
            for item in trending:
                p = item['product']
                products_data.append({
                    'id': p.id,
                    'title': p.title,
                    'price': str(p.price),
                    'image_url': p.image_url,
                    'url': f"/product/{p.slug}/",
                    'explanation': item['explanation']
                })

        # Fallback Intent: Keyword / TF-IDF Matching
        else:
            matching_products = Product.objects.all()
            if user_msg:
                matching_products = matching_products.filter(
                    Q(title__icontains=user_msg) | Q(description__icontains=user_msg) | Q(tags__icontains=user_msg)
                )
            if not matching_products.exists():
                matching_products = Product.objects.all()

            matched = list(matching_products[:3])
            reply = "Here are recommended AI tech products matching your request:"
            for p in matched:
                explanation = f"Top-rated match in {p.category.name} featuring neural performance."
                products_data.append({
                    'id': p.id,
                    'title': p.title,
                    'price': str(p.price),
                    'image_url': p.image_url,
                    'url': f"/product/{p.slug}/",
                    'explanation': explanation
                })

        return JsonResponse({
            'reply': reply,
            'products': products_data
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)
