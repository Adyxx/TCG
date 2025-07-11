from backend.models.character import Character
from backend.schemas.character import CharacterCreate, CharacterUpdate
from typing import Optional

class CharacterService:

    @staticmethod
    def get_all():
        return Character.objects.all()

    @staticmethod
    def get_by_id(character_id: int) -> Optional[Character]:
        return Character.objects.filter(id=character_id).first()

    @staticmethod
    def create(character_in: CharacterCreate) -> Character:
        character = Character(**character_in.dict())
        character.save()
        return character

    @staticmethod
    def update(character: Character, character_in: CharacterUpdate) -> Character:
        for field, value in character_in.dict(exclude_unset=True).items():
            setattr(character, field, value)
        character.save()
        return character

    @staticmethod
    def delete(character: Character) -> None:
        character.delete()
