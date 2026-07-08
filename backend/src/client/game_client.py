import requests

from business_object.game import Game
from business_object.player import Player


class GameClient:
    """Client responsible for fetching game data from an external API."""

    def get_games(self) -> list[Game]:
        """
        Fetches games from the API and converts them into Game business objects.

        Returns:
            list[Game]: A list of Game objects.
        """
        try:
            response = requests.get("http://localhost:5555", timeout=5)
            response.raise_for_status()
            games_data = response.json()

            games = []
            for item in games_data:
                p1 = Player(
                    username=item["players_list"][0],
                    password=None,
                    elo=None,
                    email=None,
                )
                p2 = Player(
                    username=item["players_list"][1],
                    password=None,
                    elo=None,
                    email=None,
                )

                winner = None
                if item["winner_name"]:
                    if p1.username == item["winner_name"]:
                        winner = p1
                    elif p2.username == item["winner_name"]:
                        winner = p2

                g = Game(
                    id_game=int(item["id"]),
                    player1=p1,
                    player2=p2,
                    game_mode=item["mode_type"],
                    winner=winner,
                    description=item["details"],
                    timestamp=None,
                )

                games.append(g)

            return games

        except requests.exceptions.RequestException as e:
            print(f"Error fetching games: {e}")
            return []
