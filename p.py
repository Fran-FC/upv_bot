import requests
import random
import time
from bs4 import BeautifulSoup

cookie_base = "mop=dummy; JS=1; T=foto2; AMFParams=dummy,false,false,false,false,true,linux,nc,firefox,106.0; path=/; AMFDetect=true; pintranet=; fotoprof=; accesible=HighContrast; iacclarge=; UPV_DEBUG=T=foto2,pintranet,fotoprof,accesible,iacclarge"

data = {
    "id": "c",
    "estilo": "500",
    "vista": "",
    "param": "",
    "cua": "miupv",
    "dni": "21699594",
    "clau": "4241"
}

resp = requests.post("https://intranet.upv.es/pls/soalu/est_aute.intraalucomp", headers={
"Host": "intranet.upv.es",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
"Accept-Language": "es-ES,en-US;q=0.7,en;q=0.3",
"Accept-Encoding": "gzip, deflate, br",
"Content-Type": "application/x-www-form-urlencoded",
"Content-Length": "62",
"Origin": "https://www.upv.es",
"DNT": "1",
"Connection": "keep-alive",
"Referer": "https://intranet.upv.es/pls/soalu/est_intranet.NI_Portal_n?p_idioma=c",
"Cookie": "mop=I; JS=1; T=foto2; AMFParams=dummy,false,false,false,false,true,linux,nc,firefox,106.0; AMFDetect=true; pintranet=; fotoprof=; accesible=HighContrast; iacclarge=; UPV_DEBUG=T=foto2,pintranet,fotoprof,accesible,iacclarge",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User": "?1",
"Pragma": "no-cache",
"Cache-Control": "no-cache"
}, data=data
)


# index = resp.headers["Set-Cookie"].find(";")
# cookie = "{0}; {1}".format(cookie_base[7:], resp.headers["Set-Cookie"][:index])
cookie=cookie_base
print("Cookie: "+cookie_base)
print(resp.cookies)

resp = requests.get(
    "https://intranet.upv.es/pls/soalu/sic_depact.HSemActividades?p_campus=V&p_tipoact=6607&p_codacti=20705&p_vista=intranet&p_idioma=c&p_solo_matricula_sn=&p_anc=filtro_actividad",
    headers={
        "Host": "intranet.upv.es",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Cookie": "mop=I; JS=1; T=foto2; AMFParams=dummy,false,false,false,false,true,linux,nc,firefox,106.0; AMFDetect=true; pintranet=; fotoprof=; accesible=HighContrast; iacclarge=; UPV_DEBUG=T=foto2,pintranet,fotoprof,accesible,iacclarge",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    })

# print(resp.headers["Set-Cookie"])
# print(resp.content)

soup = BeautifulSoup(resp.content, "html.parser")
tables = soup.find_all('table', class_="upv_listacolumnas")
rows = tables[0].select("tbody tr")

# print(rows)