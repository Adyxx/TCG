from backend.models.users import User
from backend.schemas.users import UserCreate, UserUpdate
from django.contrib.auth.hashers import make_password
from typing import Optional

class UserService:

    @staticmethod
    def get_all():
        return User.objects.all()

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def create(user_in: UserCreate) -> User:
        user_data = user_in.dict()
        user_data['password'] = make_password(user_data['password'])
        user = User(**user_data)
        user.save()
        return user

    @staticmethod
    def update(user: User, user_in: UserUpdate) -> User:
        for field, value in user_in.dict(exclude_unset=True).items():
            if field == 'password':
                value = make_password(value)
            setattr(user, field, value)
        user.save()
        return user

    @staticmethod
    def delete(user: User) -> None:
        user.delete()
