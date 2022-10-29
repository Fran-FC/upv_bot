from requests_html import HTMLSession
import random
import time
from bs4 import BeautifulSoup

list_of_hours = [
    [(1,0), False],
    [(2,0), False],
    [(10,2), False],
    [(11,2), False],
    [(11,3), False],
    [(12,3), False]
]

data = {
    "id": "c",
    "estilo": "500",
    "vista": "",
    "param": "",
    "cua": "miupv",
    "dni": "21699594",
    "clau": "4241"
}

session = HTMLSession()

r = session.post("https://intranet.upv.es/pls/soalu/est_aute.intraalucomp",data=data)
r = session.get("https://intranet.upv.es/pls/soalu/sic_depact.HSemActividades?p_campus=V&p_tipoact=6607&p_codacti=20705&p_vista=intranet&p_idioma=c&p_solo_matricula_sn=&p_anc=filtro_actividad")

print(r.content)
# hours_booked = False
# while not hours_booked:
