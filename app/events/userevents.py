from  sqlalchemy import event
from sqlalchemy.orm import Session
from app.models.user import User ,UserProfile


def insert_after_user_create(mapper, connection, target):
    print("User created with ID:", target.id)
    session =  Session(connection)
    user_profile = UserProfile(user_id=target.id)
    session.add(user_profile)
    session.commit()
    session.refresh(user_profile)
    print("UserProfile created with ID:", user_profile.id)


event.listen(User, 'after_insert', insert_after_user_create)