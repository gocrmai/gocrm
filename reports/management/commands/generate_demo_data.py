"""
Management command to generate demo data for GOPOS Reports.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random

from reports.models import Store, DailySales, MonthlySummary


class Command(BaseCommand):
    help = 'Generate demo data for GOPOS Reports'

    def handle(self, *args, **options):
        self.stdout.write('Generating demo data...')
        
        # Create stores
        stores_data = [
            {'name': '銅鑼灣店', 'location': '銅鑼灣軒尼斯道500號'},
            {'name': '尖沙咀店', 'location': '尖沙咀彌敦道100號'},
            {'name': '中環店', 'location': '中環德輔道中100號'},
            {'name': '旺角店', 'location': '旺角彌敦道700號'},
            {'name': '九龍塘店', 'location': '九龍塘達之路80號'},
            {'name': '沙田店', 'location': '沙田連城廣場'},
            {'name': '屯門店', 'location': '屯門廣場'},
        ]
        
        stores = []
        for data in stores_data:
            store, created = Store.objects.get_or_create(
                name=data['name'],
                defaults={'location': data['location']}
            )
            stores.append(store)
            if created:
                self.stdout.write(f'  Created store: {store.name}')
            else:
                self.stdout.write(f'  Store exists: {store.name}')
        
        # Generate daily sales for last 90 days
        today = timezone.now().date()
        
        for store in stores:
            for days_ago in range(90):
                sale_date = today - timedelta(days=days_ago)
                
                # Random base revenue between 5000 and 20000
                base_revenue = random.randint(5000, 20000)
                
                # Weekend boost
                if sale_date.weekday() >= 5:  # Sat, Sun
                    base_revenue = int(base_revenue * 1.3)
                
                order_count = random.randint(80, 300)
                customer_count = int(order_count * random.uniform(1.5, 2.2))
                avg_order = base_revenue / order_count
                
                DailySales.objects.update_or_create(
                    store=store,
                    date=sale_date,
                    defaults={
                        'revenue': Decimal(str(base_revenue)),
                        'order_count': order_count,
                        'customer_count': customer_count,
                        'avg_order_value': Decimal(str(round(avg_order, 2)))
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully generated demo data for {len(stores)} stores over 90 days'
        ))