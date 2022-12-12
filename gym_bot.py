from requests_html import HTMLSession
import random
import time
from bs4 import BeautifulSoup
import logging
import yaml
import argparse

def main():
    list_of_hours = []

    data = {
        "id": "c",
        "estilo": "500",
        "vista": "",
        "param": "",
        "cua": "miupv",
        "dni": "",
        "clau": ""
    }

    time_delay_base = 5

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yml", help="Pass configuration filename")

    opts = parser.parse_args() 

    # read config file and store values
    with open(opts.config, "r") as fd:
        config = yaml.safe_load(fd)

        data["dni"] = config["dni"]
        data["clau"] = config["pin"]
    
        time_delay_base = config["time_delay"]

        for h in config["hours"]:
            list_of_hours.append([h, False])

        logging.basicConfig(filename=config["log_file"], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 

    reserva_url = "https://intranet.upv.es/pls/soalu/sic_depact.HSemActMatri?p_campus=V&p_codacti=20705&p_codgrupo_mat={0}&p_vista=intranet&p_tipoact=6607&p_idioma=c"


    session = None
    hours_booked = False
    while(not hours_booked):
        logging.info(data)

        if session:
            session.close()
        session = HTMLSession()

        try:
            r = session.post("https://intranet.upv.es/pls/soalu/est_aute.intraalucomp",data=data)
        except Exception as e:
            logging.error("POST authentication error {}".format(e))
            time.sleep(1)
            continue

        if r.status_code != 200:
            logging.error("Authentication error")
            continue
        logging.debug("Authenticated")

        try:
            r = session.get("https://intranet.upv.es/pls/soalu/sic_depact.HSemActividades?p_campus=V&p_tipoact=6607&p_codacti=20705&p_vista=intranet&p_idioma=c&p_solo_matricula_sn=&p_anc=filtro_actividad")
        except Exception as e:
            logging.error("request of activities error {}".format(e))
            time.sleep(1)
            continue

        if r.status_code != 200:
            logging.error("Authentication error")
            continue
        logging.debug("List of activities retrieved")

        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.find_all('table', class_="upv_listacolumnas")
        rows = None
        if len(tables) == 2:
            rows = tables[1].select("tbody tr")
        elif len(tables) == 1:
            rows = tables[0].select("tbody tr")
        else:
            logging.error("HTML TABLE READ ERROR!!!!")
            continue

        matrix = [['' for _ in range(5)] for _ in range(14)]

        j = 0
        for hour in rows:
            days_by_hour = hour.select("td")
            i = 0
            for day in days_by_hour[1:]:
                index = str(day).find("p_codgrupo_mat=")
                if index != -1:
                    cod = str(day)[index+15:index+29]
                    matrix[j][i] = cod
                    logging.info("Session ({0},{1}) available".format(j,i))
                    
                i += 1
            j += 1

        
        hours_booked = True
        for hour in list_of_hours:
            if not hour[1]:
                code_hour = matrix[hour[0][0]][hour[0][1]] 
                if code_hour != '': 
                    try:
                        resp = session.get(reserva_url.format(code_hour))
                        if resp.status_code != 200:
                            hours_booked = False
                            logging.error("Status code not accepted")
                            continue
                        logging.info("Session {} booked".format(hour[0]))
                    except:
                        logging.error("Exception requesting session {}".format(hour[0]))
                        hours_booked = False
                        continue
                    hour[1] = True
                else:
                    hours_booked = False
                    logging.warning("Session {} is not available!".format(hour[0]))

        logging.info("All hours booked: {}".format(hours_booked))
        rand_time = random.random() * 10 + time_delay_base
        logging.info("Sleeping %.2f seconds" % rand_time)
        time.sleep(rand_time)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.info("Exception in main(): {}".format(e))
