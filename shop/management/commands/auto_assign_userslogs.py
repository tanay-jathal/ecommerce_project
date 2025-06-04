from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Order

class Command(BaseCommand):
    help = 'Assign Django User instances to Order.user based on name match'

    def handle(self, *args, **options):
        unassigned_orders = Order.objects.filter(user__isnull=True)  # use 'user', not 'Userlog'
        assigned = 0
        skipped = 0

        for order in unassigned_orders:
            try:
                # Match by username (or use email or other field)
                user = User.objects.get(username=order.user)
                order.user = user
                order.save()
                assigned += 1
                self.stdout.write(f"Assigned User '{user.username}' to Order #{order.id}")
            except User.DoesNotExist:
                self.stdout.write(f"No matching User for Order #{order.id} with name '{order.user}'")
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f"\nDone. Assigned: {assigned}, Skipped: {skipped}"))
