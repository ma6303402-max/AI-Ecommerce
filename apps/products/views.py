from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from .models import Product, Category, ProductViewHistory
from apps.recommendations.engine import RecommendationEngine

class ProductCatalogView(View):
    def get(self, request):
        category_slug = request.GET.get('category')
        search_query = request.GET.get('q', '').strip()
        sort_by = request.GET.get('sort', '-created_at')

        products = Product.objects.all()

        if category_slug:
            products = products.filter(category__slug=category_slug)

        if search_query:
            products = products.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__icontains=search_query)
            )

        if sort_by in ['price', '-price', 'title', '-created_at', '-view_count']:
            products = products.order_by(sort_by)

        categories = Category.objects.all()
        paginator = Paginator(products, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # AI Recommendations for Catalog
        engine = RecommendationEngine()
        trending_products = engine.get_trending_products(limit=4)

        context = {
            'page_obj': page_obj,
            'categories': categories,
            'selected_category': category_slug,
            'search_query': search_query,
            'trending_products': trending_products,
        }
        return render(request, 'products/catalog.html', context)

class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)

        # Increment view count
        Product.objects.filter(pk=product.pk).update(view_count=F('view_count') + 1)
        product.refresh_from_db()

        # Log View History
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        ProductViewHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key,
            product=product
        )

        # Get AI recommendations with explanations
        engine = RecommendationEngine()
        similar_recommendations = engine.get_similar_products(product, limit=4)

        context = {
            'product': product,
            'similar_recommendations': similar_recommendations,
        }
        return render(request, 'products/detail.html', context)

def product_search_api(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(title__icontains=query) | Q(tags__icontains=query)
    )[:5]

    results = [{
        'id': p.id,
        'title': p.title,
        'price': str(p.price),
        'image_url': p.image_url,
        'url': f"/product/{p.slug}/",
        'category': p.category.name
    } for p in products]

    return JsonResponse({'results': results})
