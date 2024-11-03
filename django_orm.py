# models.py

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

# Example Queries

# 1. Retrieve the first user
user = User.objects.first()

# 2. Retrieve all users
users = User.objects.all()

# 3. Filter users by name
users_named_john = User.objects.filter(name='John')

# 4. Get a specific user by ID
user = User.objects.get(id=1)  # Raises `DoesNotExist` if not found

# 5. Exclude certain records
non_admin_users = User.objects.exclude(is_admin=True)

# 6. Count the number of users
user_count = User.objects.count()

# 7. Get users ordered by name
ordered_users = User.objects.order_by('name')

# 8. Perform an aggregate query (get average age)
from django.db.models import Avg
average_age = User.objects.aggregate(Avg('age'))

# 9. Chain multiple filters
users_filtered = User.objects.filter(name__startswith='J').filter(is_active=True)

# 10. Using Q objects for complex lookups (OR condition)
from django.db.models import Q
active_or_admin_users = User.objects.filter(Q(is_active=True) | Q(is_admin=True))

# 11. Update a user's email
User.objects.filter(id=1).update(email='newemail@example.com')

# 12. Delete a user
User.objects.filter(id=1).delete()

# 13. Group by and count users by role (assuming `role` field exists)
from django.db.models import Count
user_counts_by_role = User.objects.values('role').annotate(count=Count('id'))

# 14. Subquery to get users with specific conditions
from django.db.models import Subquery
subquery = User.objects.filter(is_admin=True).values('id')
users_with_admin_status = User.objects.filter(id__in=Subquery(subquery))

# 15. Complex join queries (assuming a Profile model is related to User)
users_with_profiles = User.objects.select_related('profile').filter(profile__age__gte=18)

# 16. Using HAVING clauses for filtering aggregates
roles_with_more_than_five_users = User.objects.values('role').annotate(count=Count('id')).filter(count__gt=5)

# 17. Raw SQL for custom complex queries
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM user WHERE age > %s", [18])
    results = cursor.fetchall()

# 18. Transactions for complex operations
from django.db import transaction
with transaction.atomic():
    user = User.objects.create(name="John", email="john@example.com")
    user.profile.create(age=30)

# 19. Select specific columns
user_data = User.objects.values('name', 'email')

# 20. Advanced filtering
users_with_name_in_list = User.objects.filter(name__in=['John', 'Jane'])
active_users_with_keyword = User.objects.filter(email__contains='example')
