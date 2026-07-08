from datetime import datetime

from pydantic import BaseModel

from schema.player_model import PlayerReadModel


class GamePlayModel(BaseModel):
    id_opponent: int
    game_mode: str
    params: dict = {}


class GameResponseModel(BaseModel):
    username1: str
    username2: str
    description: str
    winner: str | None
    new_elo1: int
    new_elo2: int


class GameReadModel(BaseModel):
    id_game: int
    player1: PlayerReadModel
    player2: PlayerReadModel
    game_mode: str
    winner: PlayerReadModel | None
    description: str
    timestamp: datetime
