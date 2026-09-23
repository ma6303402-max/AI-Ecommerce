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
from django.conf import settings

@csrf_exempt
def ai_chat_recommendations_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
        user_msg = data.get('message', '').strip()
    except Exception:
        user_msg = request.POST.get('message', '').strip()

    if not user_msg:
        return JsonResponse({'reply': 'Please type a question!', 'products': []})

    # ── Build product catalogue context from DB ──────────────────────────────
    all_products = list(Product.objects.select_related('category').all())
    product_lines = []
    for p in all_products:
        product_lines.append(
            f"ID:{p.id} | {p.title} | Category:{p.category.name} | "
            f"Price:${p.price} | Tags:{p.tags}"
        )
    products_context = "\n".join(product_lines)

    # ── Cart context ──────────────────────────────────────────────────────────
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    cart_summary = ""
    if cart_items.exists():
        cart_summary = "User's current cart: " + ", ".join(
            [f"{ci.product.title} (x{ci.quantity})" for ci in cart_items]
        )
    else:
        cart_summary = "User's cart is currently empty."

    # ── Gemini prompt ─────────────────────────────────────────────────────────
    system_prompt = f"""You are an intelligent AI shopping assistant for an e-commerce store.
Your job is to help customers find the right products and answer any shopping question.

PRODUCT CATALOGUE (use ONLY these products):
{products_context}

{cart_summary}

RULES:
1. Always respond in the SAME LANGUAGE the user writes in (Arabic → Arabic, English → English).
2. Pick 1-3 most relevant product IDs from the catalogue based on the user's question.
3. If asked for "cheapest" or "lowest price", pick the product(s) with the lowest price.
4. If asked for "best" or "top rated", pick the most popular/feature-rich products.
5. If asked a general question (shipping, returns, etc.) answer helpfully without products.
6. Keep your reply short, friendly and helpful (2-3 sentences max).

RESPOND IN THIS EXACT JSON FORMAT (no markdown, no code block):
{{"reply": "your friendly response here", "product_ids": [1, 2, 3]}}

If no products are relevant, use: {{"reply": "your answer", "product_ids": []}}
"""

    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"{system_prompt}\n\nUser question: {user_msg}"
        )

        raw = response.text.strip()
        # Strip markdown code fences if Gemini wraps in ```json ... ```
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        parsed = json.loads(raw)
        reply = parsed.get('reply', 'Here are some recommendations for you!')
        product_ids = parsed.get('product_ids', [])

    except Exception as e:
        # Fallback: keyword matching if Gemini fails
        msg_lower = user_msg.lower()
        reply = "Here are some products that might interest you:"
        product_ids = []

        if any(w in msg_lower for w in ['cheap', 'lowest', 'budget', 'affordable', 'inexpensive', 'less expensive']):
            cheapest = Product.objects.order_by('price')[:3]
            product_ids = [p.id for p in cheapest]
            reply = "Here are our most affordable products sorted by lowest price! 💰"
        elif any(w in msg_lower for w in ['headphone', 'audio', 'music', 'earphone']):
            prods = Product.objects.filter(Q(title__icontains='headphone') | Q(tags__icontains='audio'))[:2]
            product_ids = [p.id for p in prods]
        elif any(w in msg_lower for w in ['laptop', 'computer', 'developer']):
            prods = Product.objects.filter(Q(title__icontains='laptop') | Q(tags__icontains='laptop'))[:2]
            product_ids = [p.id for p in prods]
        elif any(w in msg_lower for w in ['watch', 'fitness', 'health']):
            prods = Product.objects.filter(Q(title__icontains='watch') | Q(tags__icontains='watch'))[:2]
            product_ids = [p.id for p in prods]
        else:
            engine = RecommendationEngine()
            trending = engine.get_trending_products(limit=3)
            product_ids = [item['product'].id for item in trending]

    # ── Fetch selected products and build response ────────────────────────────
    products_data = []
    if product_ids:
        # Preserve order returned by Gemini
        id_to_product = {p.id: p for p in Product.objects.filter(id__in=product_ids).select_related('category')}
        for pid in product_ids:
            p = id_to_product.get(pid)
            if p:
                products_data.append({
                    'id': p.id,
                    'title': p.title,
                    'price': str(p.price),
                    'image_url': p.image_url,
                    'url': f"/product/{p.slug}/",
                    'explanation': f"{p.category.name} • ${p.price}",
                })

    return JsonResponse({'reply': reply, 'products': products_data})

