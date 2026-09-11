from business_object.game import Game
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class GameDao(metaclass=Singleton):
    """Class containing methods to access Players in the database."""

    @log
    def create(self, game) -> bool:
        """Create a player in the database.
        Args:
            Player to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO game(id_game,id_player1, id_player2, game_mode, id_winner, detail) VALUES "
                        "(%(id_game)s, %(id_player1)s, %(id_player2)s, %(game_mode)s, %(id_winner)s,%(detail)s) "
                        "RETURNING id_game;",
                        {
                            "id_game": game.id_game,
                            "id_player1": game.id_player1,
                            "id_player2": game.id_player2,
                            "game_mode": game.game_mode,
                            "id_winner": game.id_winner,
                            "detail": game.detail
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            game.id_player = res["id_player"]
            created = True

        return created

    @log
    def find_by_id(self, id_game: int) -> Game:
        """Find a player by their id.
        Args:
            id_player (int): The ID of the player to find
        Returns:
            Player matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM player                       "
                        " WHERE id_game = %(id_game)s;   ",
                        {"id_player": id_game},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        Game = None
        if res:
            Game = Game(
                username=res["username"],
                elo=res["elo"],
                email=res["email"],
                pokemon_fan=res["pokemon_fan"],
                id_player=res["id_player"],
                password=res["password"],
            )

        return Game

    @log
    def find_all(self) -> list[Game]:
        """List all players in the database.
        Returns:
            list[Player] sorted by username
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM   game                           "
                        " ORDER BY id_game;                     "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        players_list = []

        if res:
            for row in res:
                player = Game(
                    id_player=row["id_player"],
                    username=row["username"],
                    password=row["password"],
                    elo=row["elo"],
                    email=row["email"],
                    pokemon_fan=row["pokemon_fan"],
                )

                players_list.append(player)

        return players_list

    @log
    def update(self, player) -> bool:
        """Update a player in the database.
        Args:
            Player to be updated
        Returns:
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE player                                                  "
                        "   SET username = %(username)s,                                "
                        "       password = COALESCE(%(password)s, password),            "
                        "       elo = %(elo)s,                                          "
                        "       email = %(email)s,                                      "
                        "       pokemon_fan = %(pokemon_fan)s,                          "
                        "       access_token = COALESCE(%(access_token)s, access_token) "
                        " WHERE id_player = %(id_player)s;                              ",
                        {
                            "username": player.username,
                            "password": player.password,
                            "elo": player.elo,
                            "email": player.email,
                            "pokemon_fan": player.pokemon_fan,
                            "access_token": player.access_token,
                            "id_player": player.id_player,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    @log
    def delete(self, player) -> bool:
        """Delete a player from the database.
        Args:
            Player to delete from the database
        Returns:
            True if the player was successfully deleted, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM player                               "
                        " WHERE id_player = %(id_player)s                 ",
                        {"id_player": player.id_player},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0

    @log
    def login(self, username: str, password: str) -> Game:
        """Login using username and password.
        Args:
            username (str)
            password (str)
        Returns:
            Player or None
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                               "
                        "  FROM player                          "
                        " WHERE username = %(username)s         "
                        "   AND password = %(password)s;        ",
                        {"username": username, "password": password},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        player = None

        if res:
            player = Game(
                username=res["username"],
                password=res["password"],
                elo=res["elo"],
                email=res["email"],
                pokemon_fan=res["pokemon_fan"],
                access_token=res["access_token"],
                id_player=res["id_player"],
            )

        return player

    @log
    def find_by_token(self, access_token: str) -> Player:
        """Find a player by their access token.
        Args:
            access_token (str): The token to search for.
        Returns:
            Player object if found, otherwise None.
        """
        if not access_token:
            return None

        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM player                           "
                        " WHERE access_token = %(token)s;        ",
                        {"token": access_token},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(f"Error finding player by token: {e}")
            raise

        player = None
        if res:
            player = Player(
                id_player=res["id_player"],
                username=res["username"],
                password=res["password"],
                elo=res["elo"],
                email=res["email"],
                pokemon_fan=res["pokemon_fan"],
                access_token=res["access_token"],
            )

        return player
