from models.member import Member
from sqlalchemy.orm import Session
from typing import Optional

def register_member(db: Session, email: str, password: str) :
    member = Member(email=email, password=password, nickname=email)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def get_member_by_email(db: Session, email: str) -> Member | None :
    return db.query(Member).filter(Member.email == email).first()

def get_member_by_member_seq(db: Session, member_seq: int) -> Member | None :
    return db.query(Member). filter(Member.member_seq == member_seq).first()

def update_character_name(db: Session, member: Member, new_character_name: str) :
    member.character_name = new_character_name
    db.commit()
    db.refresh(member)

def update_nickname(db: Session, member: Member, new_nickname: str) :
    member.nickname = new_nickname
    db.commit()
    db.refresh(member)

def delete_member_by_member_seq(db: Session, member_seq: int):
    return db.query(Member).filter(Member.member_seq == member_seq).delete()

