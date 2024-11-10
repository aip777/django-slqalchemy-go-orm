## Django SQLAlchemy GO ORM

## 1. Retrieve the first user
```bash
### Django ORM

user = User.objects.first()

### SQLAlchemy
user = session.query(User).first()

### GORM
var user User
db.First(&user)

### Postgresql
SELECT * FROM user ORDER BY id ASC LIMIT 1;
```
## 2. Retrieve all users
```bash
### Django
users = User.objects.all()

### SQLAlchemy
users = session.query(User).all()

### GORM
var users []User
db.Find(&users)

### Postgresql
SELECT * FROM user;
```

## 3. Filter users by name
```bash
### Django
users_named_john = User.objects.filter(name='John')

### SQLAlchemy
users_named_john = session.query(User).filter(User.name == 'John').all()

### GORM
db.Where("name = ?", "John").Find(&users)

### Postgresql
SELECT * FROM user WHERE name = 'John';
```

## 4. Get a specific user by ID
```bash
### Django
user = User.objects.get(id=1)  # Raises `DoesNotExist` if not found

### SQLAlchemy
user = session.query(User).get(1)  # Returns `None` if not found

### GORM
db.First(&user, 1)  // Find user with primary key 1

### Postgresql
SELECT * FROM user WHERE id = 1;
```

## 5. Exclude certain records
```bash
### Django
non_admin_users = User.objects.exclude(is_admin=True)

### SQLAlchemy
non_admin_users = session.query(User).filter(User.is_admin == False).all()

### GORM
db.Not("is_admin", true).Find(&users)

### Postgresql
SELECT * FROM user WHERE is_admin = FALSE;
```

## 6. Count the number of users
```bash
### Django
user_count = User.objects.count()

### SQLAlchemy
user_count = session.query(User).count()

### GORM
var count int64
db.Model(&User{}).Count(&count)

### Postgresql
SELECT COUNT(*) FROM user;
```

## 7. Get users ordered by name
```bash
### Django
ordered_users = User.objects.order_by('name')

### SQLAlchemy
ordered_users = session.query(User).order_by(User.name).all()

### GORM
db.Order("name").Find(&users)

### Postgresql
SELECT * FROM user ORDER BY name ASC;
```

## 8. Perform an aggregate query (get average age)
```bash
### Django
from django.db.models import Avg
average_age = User.objects.aggregate(Avg('age'))

### SQLAlchemy
from sqlalchemy import func
average_age = session.query(func.avg(User.age)).scalar()

### GORM
var avgAge float64
db.Model(&User{}).Select("AVG(age)").Scan(&avgAge)

### Postgresql
SELECT AVG(age) FROM user;
```

## 9. Chain multiple filters
```bash
### Django
users_filtered = User.objects.filter(name__startswith='J').filter(is_active=True)

### SQLAlchemy
users_filtered = session.query(User).filter(User.name.like('J%'), User.is_active == True).all()

### GORM
db.Where("name LIKE ?", "J%").Where("is_active = ?", true).Find(&users)

### Postgresql
SELECT * FROM user WHERE name LIKE 'J%' AND is_active = TRUE;
```

## 10. Using OR conditions
```bash
### Django
from django.db.models import Q
active_or_admin_users = User.objects.filter(Q(is_active=True) | Q(is_admin=True))

### SQLAlchemy
from sqlalchemy import or_
active_or_admin_users = session.query(User).filter(or_(User.is_active == True, User.is_admin == True)).all()

### GORM
db.Where("is_active = ? OR is_admin = ?", true, true).Find(&users)

### Postgresql
SELECT * FROM user WHERE is_active = TRUE OR is_admin = TRUE;
```

## 11. Update a user's email
```bash
### Django
User.objects.filter(id=1).update(email='newemail@example.com')

### SQLAlchemy
session.query(User).filter(User.id == 1).update({User.email: 'newemail@example.com'})
session.commit()

### GORM
db.Model(&User{}).Where("id = ?", 1).Update("email", "newemail@example.com")

### Postgresql
SELECT * FROM user WHERE is_active = TRUE OR is_admin = TRUE;
```

## 12. Delete a user
```bash
### Django
User.objects.filter(id=1).delete()

### SQLAlchemy
session.query(User).filter(User.id == 1).delete()
session.commit()

### GORM
db.Delete(&User{}, 1)

### Postgresql
DELETE FROM user WHERE id = 1;
```

## 13. Group by and Count (e.g., Count users by role)
```bash
### Django
from django.db.models import Count
user_counts_by_role = User.objects.values('role').annotate(count=Count('id'))

### SQLAlchemy
from sqlalchemy import func
user_counts_by_role = session.query(User.role, func.count(User.id)).group_by(User.role).all()

### GORM
type RoleCount struct {
Role  string
Count int64
}
var results []RoleCount
db.Model(&User{}).Select("role, COUNT(id) as count").Group("role").Scan(&results)

### Postgresql
SELECT role, COUNT(id) AS count FROM user GROUP BY role;
```

## 14. Subquery to Get Users with Specific Conditions
```bash
### Django
from django.db.models import Subquery
subquery = User.objects.filter(is_admin=True).values('id')
users_with_admin_status = User.objects.filter(id__in=Subquery(subquery))

### SQLAlchemy
from sqlalchemy.orm import aliased
admin_users_subquery = session.query(User.id).filter(User.is_admin == True).subquery()
users_with_admin_status = session.query(User).filter(User.id.in_(admin_users_subquery)).all()

### GORM
var adminUserIds []int
db.Model(&User{}).Where("is_admin = ?", true).Pluck("id", &adminUserIds)
db.Where("id IN ?", adminUserIds).Find(&users)

### Postgresql
SELECT * FROM user WHERE id IN (SELECT id FROM user WHERE is_admin = TRUE);
```

## 15. Complex Join Queries
```bash
### Django
from django.db.models import F
users_with_profiles = User.objects.select_related('profile').filter(profile__age__gte=18)

### SQLAlchemy
from sqlalchemy.orm import joinedload
users_with_profiles = session.query(User).options(joinedload(User.profile)).filter(User.profile.has(age >= 18)).all()

### GORM
db.Joins("JOIN profiles ON users.id = profiles.user_id").Where("profiles.age >= ?", 18).Find(&users)

### Postgresql
SELECT user.* FROM user
JOIN profile ON user.id = profile.user_id
WHERE profile.age >= 18;
```

## 16. Using HAVING Clauses for Filtering Aggregates
```bash
### Django
from django.db.models import Count
roles_with_more_than_five_users = User.objects.values('role').annotate(count=Count('id')).filter(count__gt=5)

### SQLAlchemy
user_counts = session.query(User.role, func.count(User.id).label('user_count')).group_by(User.role).having(func.count(User.id) > 5).all()

### GORM
db.Model(&User{}).Select("role, COUNT(id) as user_count").Group("role").Having("COUNT(id) > ?", 5).Scan(&results)

### Postgresql
SELECT role, COUNT(id) AS user_count FROM user GROUP BY role HAVING COUNT(id) > 5;
```

## 17. Raw SQL for Custom Complex Queries
```bash
### Django
from django.db import connection
with connection.cursor() as cursor:
cursor.execute("SELECT * FROM user WHERE age > %s", [18])
results = cursor.fetchall()

### SQLAlchemy
result = session.execute("SELECT * FROM user WHERE age > :age", {"age": 18}).fetchall()

### GORM
db.Raw("SELECT * FROM users WHERE age > ?", 18).Scan(&users)

### Postgresql
SELECT * FROM user WHERE age > 18;
```

## 18. Transactions for Complex Operations
```bash
### Django
from django.db import transaction
with transaction.atomic():
user = User.objects.create(name="John", email="john@example.com")
user.profile.create(age=30)

### SQLAlchemy
from sqlalchemy.exc import IntegrityError
try:
with session.begin():
new_user = User(name="John", email="john@example.com")
session.add(new_user)
session.flush()  # Ensure the new user ID is generated
new_profile = Profile(user_id=new_user.id, age=30)
session.add(new_profile)
except IntegrityError:
session.rollback()

### GORM
err := db.Transaction(func(tx *gorm.DB) error {
if err := tx.Create(&User{Name: "John", Email: "john@example.com"}).Error; err != nil {
    return err
  }
if err := tx.Create(&Profile{UserID: 1, Age: 30}).Error; err != nil {
    return err
  }
return nil
})
if err != nil {
  // handle error
}

### Postgresql
BEGIN;

INSERT INTO user (name, email) VALUES ('John', 'john@example.com');
INSERT INTO profile (user_id, age) VALUES (1, 30);

COMMIT;

#### If an error occurs:
ROLLBACK;
```

## 19. Select Specific Columns
```bash
### Django
user_data = User.objects.values('name', 'email')

### SQLAlchemy
user_data = session.query(User.name, User.email).all()

### GORM
db.Select("name, email").Find(&users)

### Postgresql
SELECT name, email FROM user;
```

## 20. Advanced Filtering with __in, __contains, etc.
```bash
### Django
users_with_name_in_list = User.objects.filter(name__in=['John', 'Jane'])
active_users_with_keyword = User.objects.filter(email__contains='example')

### SQLAlchemy
users_with_name_in_list = session.query(User).filter(User.name.in_(['John', 'Jane'])).all()
active_users_with_keyword = session.query(User).filter(User.email.like('%example%')).all()

### GORM
db.Where("name IN ?", []string{"John", "Jane"}).Find(&users)
db.Where("email LIKE ?", "%example%").Find(&users)

### Postgresql
#### Filter with IN
SELECT * FROM user WHERE name IN ('John', 'Jane');

#### Filter with LIKE for partial matches
SELECT * FROM user WHERE email LIKE '%example%';
```





















