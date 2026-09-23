from django.test import TestCase
from apps.products.models import Category, Product
from apps.recommendations.engine import RecommendationEngine

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="AI Robotics", description="Smart robots")
        self.product = Product.objects.create(
            category=self.category,
            title="AI Companion Bot",
            description="Autonomous robot with neural vision",
            price=299.99,
            stock=5,
            tags="ai, robot, vision"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.slug, "ai-companion-bot")
        self.assertTrue(self.product.is_in_stock())

    def test_ai_recommendation_engine(self):
        p2 = Product.objects.create(
            category=self.category,
            title="AI Vision Camera",
            description="Smart camera with neural vision capabilities",
            price=149.99,
            stock=10,
            tags="ai, camera, vision"
        )
        engine = RecommendationEngine()
        recs = engine.get_similar_products(self.product, limit=2)
        self.assertGreater(len(recs), 0)
        self.assertEqual(recs[0]['product'].id, p2.id)
        self.assertIn("explanation", recs[0])
