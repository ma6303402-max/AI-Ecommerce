from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderItem
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial sample data for AI-Powered E-Commerce System'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # Create Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@aiecommerce.com',
                'role': 'administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))

        # Create Sample Customer
        customer_user, created = User.objects.get_or_create(
            username='customer',
            defaults={
                'email': 'customer@example.com',
                'role': 'customer',
            }
        )
        if created:
            customer_user.set_password('customer123')
            customer_user.save()
            self.stdout.write(self.style.SUCCESS("Created customer user: customer / customer123"))

        # Create Categories
        categories_data = [
            {'name': 'AI Gadgets & Robotics', 'description': 'Cutting-edge autonomous consumer electronics and smart assistant robotics.'},
            {'name': 'Audio & Wearables', 'description': 'High-fidelity acoustic gear, active noise canceling headphones, and smartwatches.'},
            {'name': 'Smart Home Tech', 'description': 'Automated climate, lighting, security cameras, and intelligent home hubs.'},
            {'name': 'Computing & Laptops', 'description': 'Next-gen neural computing rigs, ultra-portable laptops, and vision displays.'},
        ]

        categories_dict = {}
        for cat_info in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=cat_info['name'],
                defaults={'description': cat_info['description']}
            )
            categories_dict[cat_info['name']] = cat

        # Products Seed Data
        products_data = [
            {
                'category': 'AI Gadgets & Robotics',
                'title': 'Aura AI Vision Smart Companion Robot',
                'description': 'Interactive personal assistant powered by real-time spatial vision models, spatial navigation, voice synthesis, and local neural processing.',
                'price': 499.99,
                'stock': 15,
                'tags': 'ai, robot, companion, smart, vision, neural',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&auto=format&fit=crop&q=80',
            },
            {
                'category': 'AI Gadgets & Robotics',
                'title': 'Quantum Neural AI Pocket Translator',
                'description': 'Instant offline voice-to-voice neural translation across 80+ languages with noise-isolated microphone array.',
                'price': 189.50,
                'stock': 25,
                'tags': 'ai, translator, voice, pocket, neural, smart',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1546776310-eef45dd6d63c?w=600&auto=format&fit=crop&q=80',
            },
            {
                'category': 'Audio & Wearables',
                'title': 'Pulse ANC Neural Spatial Headphones',
                'description': 'Over-ear audiophile headphones featuring adaptive AI active noise cancellation, lossless Bluetooth 5.4, and spatial audio calibration.',
                'price': 299.00,
                'stock': 30,
                'tags': 'audio, headphones, anc, spatial, bluetooth, noise canceling',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80',
            },
            {
                'category': 'Audio & Wearables',
                'title': 'Zenith Pro Smart Fitness Watch',
                'description': 'Titanium smartwatch with continuous ECG, AI sleep coaching, SPO2 tracking, and 14-day battery life.',
                'price': 249.99,
                'stock': 40,
                'tags': 'watch, fitness, bio, health, audio, wearable, smart',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80',
            },
            {
                'category': 'Smart Home Tech',
                'title': 'OmniSmart AI Climate & Energy Controller',
                'description': 'Predictive thermostat that learns room usage patterns to reduce electricity consumption by up to 35%.',
                'price': 129.95,
                'stock': 50,
                'tags': 'smart home, climate, energy, thermostat, ai, energy saving',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1558002038-1055907df827?w=600&auto=format&fit=crop&q=80',
            },
            {
                'category': 'Smart Home Tech',
                'title': 'Sentinel AI 4K Security Camera Hub',
                'description': 'Local AI facial recognition security camera system with night vision infrared and encrypted edge storage.',
                'price': 349.00,
                'stock': 20,
                'tags': 'smart home, camera, security, 4k, vision, edge ai',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1557324232-b8917d3c3dcb?w=600&auto=format&fit=crop&q=80',
            },
            {
                'category': 'Computing & Laptops',
                'title': 'Hyperion X1 Neural Workstation Laptop',
                'description': '16-inch OLED laptop with built-in NPU delivering 45 TOPS of AI acceleration for developer models and 3D rendering.',
                'price': 1899.99,
                'stock': 10,
                'tags': 'computing, laptop, workstation, oled, npu, neural, developer',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80',
            },
            {
                'category': 'Computing & Laptops',
                'title': 'Vortex Curved 4K AI Color Studio Monitor',
                'description': '32-inch curved Quantum-Dot display with dynamic ambient lighting adjustment and AI auto-calibration.',
                'price': 799.00,
                'stock': 12,
                'tags': 'computing, monitor, display, 4k, curved, color studio',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop&q=80',
            },
        ]

        for p_data in products_data:
            cat_name = p_data.pop('category')
            category = categories_dict[cat_name]
            p, created_p = Product.objects.get_or_create(
                title=p_data['title'],
                defaults={**p_data, 'category': category}
            )
            if created_p:
                self.stdout.write(self.style.SUCCESS(f"Added product: {p.title}"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
