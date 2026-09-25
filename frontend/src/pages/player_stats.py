import streamlit as st

from utils import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.title("Players stat")
logger = get_page_logger("player_stat")
idplayer = st.query_params.get("id_player")
check_authentification()

if idplayer is not None:
    try:
        idplayer = int(idplayer)
        response = api_client.get(f"/player/{idplayer}")
        if response["status_code"] == 200:
            player = response["data"]
            st.subheader(f"{player['username']}")
    except OSError:
        print("Le joueur est introuvable")
