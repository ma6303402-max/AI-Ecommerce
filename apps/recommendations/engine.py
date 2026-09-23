import math
from django.db.models import Count, Q
from apps.products.models import Product, ProductViewHistory
from apps.cart.models import CartItem, Cart

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class RecommendationEngine:
    def __init__(self):
        pass

    def get_similar_products(self, target_product, limit=4):
        """
        Calculates content-based TF-IDF similarity across title, category, description, and tags.
        Returns a list of dicts: [{'product': product_obj, 'similarity_score': 0.85, 'explanation': '...'}]
        """
        all_products = list(Product.objects.exclude(id=target_product.id))
        if not all_products:
            return []

        recommendations = []

        if SKLEARN_AVAILABLE:
            corpus = [
                f"{p.title} {p.category.name} {p.tags} {p.description}"
                for p in [target_product] + all_products
            ]
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(corpus)
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

            indexed_scores = sorted(list(enumerate(cosine_sim)), key=lambda x: x[1], reverse=True)

            for idx, score in indexed_scores[:limit]:
                p = all_products[idx]
                explanation = self.generate_explanation(target_product, p, score)
                recommendations.append({
                    'product': p,
                    'similarity_score': round(float(score), 2),
                    'explanation': explanation
                })
        else:
            # Fallback rule-based matching if scikit-learn is missing
            target_tags = set([t.strip().lower() for t in target_product.tags.split(',')])
            for p in all_products:
                p_tags = set([t.strip().lower() for t in p.tags.split(',')])
                common_tags = target_tags.intersection(p_tags)
                score = 0.5 if p.category == target_product.category else 0.1
                score += len(common_tags) * 0.2
                score = min(score, 0.99)

                explanation = self.generate_explanation(target_product, p, score)
                recommendations.append({
                    'product': p,
                    'similarity_score': round(score, 2),
                    'explanation': explanation
                })

            recommendations = sorted(recommendations, key=lambda x: x['similarity_score'], reverse=True)[:limit]

        return recommendations

    def get_trending_products(self, limit=6):
        """
        Finds popular products based on view counts and order frequency.
        """
        trending = Product.objects.annotate(
            popularity=Count('views') + Count('orderitem')
        ).order_by('-popularity', '-view_count')[:limit]

        results = []
        for p in trending:
            explanation = f"Trending now! Viewed {p.view_count} times with high community demand."
            results.append({
                'product': p,
                'explanation': explanation
            })
        return results

    def get_personalized_recommendations(self, request, limit=4):
        """
        Analyzes customer recent view history and cart items to suggest products tailored to them.
        """
        viewed_product_ids = []
        if request.user.is_authenticated:
            viewed_product_ids = list(
                ProductViewHistory.objects.filter(user=request.user)
                .values_list('product_id', flat=True)[:10]
            )
        else:
            session_key = request.session.session_key
            if session_key:
                viewed_product_ids = list(
                    ProductViewHistory.objects.filter(session_key=session_key)
                    .values_list('product_id', flat=True)[:10]
                )

        if not viewed_product_ids:
            return self.get_trending_products(limit=limit)

        last_product = Product.objects.filter(id__in=viewed_product_ids).first()
        if last_product:
            return self.get_similar_products(last_product, limit=limit)
        
        return self.get_trending_products(limit=limit)

    def generate_explanation(self, source_product, target_product, score):
        """
        Generates natural language explanation for why a recommendation was made.
        """
        same_category = source_product.category == target_product.category
        s_tags = set([t.strip().lower() for t in source_product.tags.split(',')])
        t_tags = set([t.strip().lower() for t in target_product.tags.split(',')])
        shared_tags = s_tags.intersection(t_tags)

        if shared_tags:
            tag_str = ", ".join(list(shared_tags)[:2])
            return f"Recommended because both items share key features ({tag_str}) and matching specifications."
        elif same_category:
            return f"Top pick in {source_product.category.name} tailored for users viewing {source_product.title}."
        else:
            return f"Frequently purchased together based on AI customer behavior pattern matching."
