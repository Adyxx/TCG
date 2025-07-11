from backend.models.match import Match
from backend.schemas.match import MatchCreate, MatchUpdate
from typing import Optional

class MatchService:

    @staticmethod
    def get_all():
        return Match.objects.all()

    @staticmethod
    def get_by_id(match_id: int) -> Optional[Match]:
        return Match.objects.filter(id=match_id).first()

    @staticmethod
    def create(match_in: MatchCreate) -> Match:
        match = Match(**match_in.dict())
        match.save()
        return match

    @staticmethod
    def update(match: Match, match_in: MatchUpdate) -> Match:
        for field, value in match_in.dict(exclude_unset=True).items():
            setattr(match, field, value)
        match.save()
        return match

    @staticmethod
    def delete(match: Match) -> None:
        match.delete()
