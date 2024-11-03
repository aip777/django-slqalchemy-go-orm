# models.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String, unique=True)
    age = Column(Integer)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

# Example Queries

# Create a session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///example.db')  # Example using SQLite
Session = sessionmaker(bind=engine)
session = Session()

# 1. Retrieve the first user
user = session.query(User).first()

# 2. Retrieve all users
users = session.query(User).all()

# 3. Filter users by name
users_named_john = session.query(User).filter(User.name == 'John').all()

# 4. Get a specific user by ID
user = session.query(User).get(1)  # Returns `None` if not found

# 5. Exclude certain records
non_admin_users = session.query(User).filter(User.is_admin == False).all()

# 6. Count the number of users
user_count = session.query(User).count()

# 7. Get users ordered by name
ordered_users = session.query(User).order_by(User.name).all()

# 8. Perform an aggregate query (e.g., get average age)
from sqlalchemy import func
average_age = session.query(func.avg(User.age)).scalar()

# 9. Chain multiple filters
users_filtered = session.query(User).filter(User.name.like('J%'), User.is_active == True).all()

# 10. Using OR conditions with `or_` operator
from sqlalchemy import or_
active_or_admin_users = session.query(User).filter(or_(User.is_active == True, User.is_admin == True)).all()

# 11. Update a user's email
session.query(User).filter(User.id == 1).update({User.email: 'newemail@example.com'})
session.commit()

# 12. Delete a user
session.query(User).filter(User.id == 1).delete()
session.commit()

# 13. Group by and count users by role (assuming `role` field exists)
user_counts_by_role = session.query(User.role, func.count(User.id)).group_by(User.role).all()

# 14. Subquery to get users with specific conditions
admin_users_subquery = session.query(User.id).filter(User.is_admin == True).subquery()
users_with_admin_status = session.query(User).filter(User.id.in_(admin_users_subquery)).all()

# 15. Complex join queries (assuming a Profile model is related to User)
users_with_profiles = session.query(User).join(User.profile).filter(User.profile.age >= 18).all()

# 16. Using HAVING clauses for filtering aggregates
user_counts = session.query(User.role, func.count(User.id).label('user_count')).group_by(User.role).having(func.count(User.id) > 5).all()

# 17. Raw SQL for custom complex queries
result = session.execute("SELECT * FROM users WHERE age > :age", {"age": 18}).fetchall()

# 18. Transactions for complex operations
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

# 19. Select specific columns
user_data = session.query(User.name, User.email).all()

# 20. Advanced filtering
users_with_name_in_list = session.query(User).filter(User.name.in_(["John", "Jane"])).all()
active_users_with_keyword = session.query(User).filter(User.email.like('%example%')).all()
