from sqlalchemy.orm import Session
from app.models.user import User

from uuid import UUID






class UserRepository: 
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        return db.query(User).filter(User.id == UUID(user_id)).first()
    
    @staticmethod
    def create_user(db: Session, email: str, username: str, hashed_password: str):
        new_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def update_refresh_token(db: Session, user: User, refresh_token: str):
        user.refresh_token = refresh_token
        db.commit()


    

    
