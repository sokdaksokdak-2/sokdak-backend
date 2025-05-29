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