# crud/member_oauth.py

from models.member_oauth import MemberOAuth, OAuthProvider
from models.member import Member
from sqlalchemy.orm import Session

def get_member_by_oauth(db: Session, provider: OAuthProvider, oauth_id: str) -> Member | None :
    return db.query(MemberOAuth).filter(
        MemberOAuth.oauth_id == oauth_id,
        MemberOAuth.provider == provider
        ).first()

def register_oauth_account(db: Session, provider: OAuthProvider, oauth_id: str, member_seq: int):
        oauth_account = MemberOAuth(
            provider=provider,
            oauth_id=oauth_id,
            member_seq=member_seq
        )
        db.add(oauth_account)
        db.commit()
        db.refresh(oauth_account)

def delete_oauth_account_by_member_seq(db: Session, member_seq: int): # 커밋은 서비스계열에서 한번에 처리 
    return db.query(MemberOAuth).filter(MemberOAuth.member_seq == member_seq).delete()