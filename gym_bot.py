import requests
from bs4 import BeautifulSoup

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
        "Origin": "https://intranet.upv.es",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://intranet.upv.es/pls/soalu/est_intranet.NI_Portal_n?p_idioma=c",
        "Cookie": "mop=I; JS=1; T=foto2; AMFParams=dummy,false,false,false,false,true,linux,nc,firefox,106.0; AMFDetect=true; pintranet=; fotoprof=; accesible=HighContrast; iacclarge=; UPV_DEBUG=T=foto2,pintranet,fotoprof,accesible,iacclarge",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }, data=data)

resp = requests.get(
    "https://intranet.upv.es/pls/soalu/sic_depact.HSemActividades?p_campus=V&p_codacti=20705&p_vista=intranet&p_idioma=c&p_tipoact=6607&p_solo_matricula_sn=&p_anc=bloque_inscritas",
    headers={
        "Host": "intranet.upv.es",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": "JS=1; T=foto2; AMFParams=dummy,false,false,false,false,true,linux,nc,firefox,106.0; AMFDetect=true; pintranet=; fotoprof=; accesible=HighContrast; iacclarge=; UPV_DEBUG=T=foto2,pintranet,fotoprof,accesible,iacclarge; TDp=18415f28ab9.140d9530f3",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    })

soup = BeautifulSoup(resp.content, "html.parser")
tables = soup.find_all('table', class_="upv_listacolumnas")
rows = tables[1].select("tbody tr")

matrix = [['' for _ in range(5)] for _ in range(14)]

j = 0
for hour in rows:
    days_by_hour = hour.select("td")
    i = 0
    for day in days_by_hour:
        if i == 0:
            i+=1
            continue
        
        index = str(day).find("p_codgrupo_mat=")
        if index != -1:
            cod = str(day)[index+15:index+29]
            matrix[j][i-1] = cod
        i += 1
    j += 1
        
print(matrix)
reserva_url = "https://intranet.upv.es/pls/soalu/sic_depact.HSemActMatri?p_campus=V&p_codacti=20705&p_codgrupo_mat={0}&p_vista=intranet&p_tipoact=6607&p_idioma=c"
reserva_headers = {
        "Host": "intranet.upv.es",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://intranet.upv.es/pls/soalu/sic_depact.HSemActividades?p_campus=V&p_codacti=20705&p_vista=intranet&p_idioma=c&p_tipoact=6607&p_solo_matricula_sn=&p_anc=bloque_inscritas",
        "Cookie": "JS=1; T=foto2; AMFParams=dummy,false,false,false,false,true,linux,nc,firefox,106.0; AMFDetect=true; pintranet=; fotoprof=; accesible=HighContrast; iacclarge=; UPV_DEBUG=T=foto2,pintranet,fotoprof,accesible,iacclarge; TDp=18415f28ab9.140d9530f3",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }



list_of_hours = [
    matrix[8][0],
    matrix[9][0]
]


for hour in list_of_hours:
    if hour != '':
        print(reserva_url.format(hour))
        resp = requests.get(
            url=reserva_url.format(hour), 
            headers=reserva_headers)
        print(resp)
    else:
        print("ERR: Hour selected is empty!!")



