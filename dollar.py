#Download
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import datetime

#Send
from email import message
from mailbox import Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Timestamp -  Subject
ya = datetime.datetime.now()
ya = ya.strftime('%d-%m-%Y %I:%M')



def download_data():

    global tabla_divisas_surcambio
    global tabla_divisas_unicambio
    global tabla_divisas_poblado

    url = 'https://surcambios.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tabla_divisas_surcambio = str(soup.find('table',{'class':'currency-exchange'}))


    url_unicambios = 'https://unicambios.com.co/servicios/#serv0'
    r_unicambios = requests.get(url_unicambios)
    soup_unicambios = BeautifulSoup(r_unicambios.text, 'html.parser')
    tabla_divisas_unicambio = str(soup_unicambios.find('table',))


    url_poblado = 'https://www.cambioselpoblado.com/'
    r_poblado = requests.get(url_poblado)
    soup_poblado = BeautifulSoup(r_poblado.text, 'html.parser')
    tabla_divisas_poblado = str(soup_poblado.find('table'))



def compose_():
    global df_sub
    global df_sub_unicambios
    global df_poblado_sub

    df_divisas_surcambios = pd.read_html(tabla_divisas_surcambio)[0]
    df_divisas_surcambios = df_divisas_surcambios.drop('Unnamed: 0', axis=1)
    ixd_valor_1 = []
    for indice, valor in zip(np.arange(len(df_divisas_surcambios)), df_divisas_surcambios['MonedaCurrency'].to_list()):
        if 'Americano' in valor:
            ixd_valor_1.append(indice)
    df_sub = df_divisas_surcambios.loc[ixd_valor_1,:]


    df_unicambios = pd.read_html(str(tabla_divisas_unicambio))[0]
    df_unicambios = df_unicambios.drop(df_unicambios.columns.to_list()[0], axis=1)
    idx_unicambios = []
    for nombre, indice in zip(df_unicambios['Unnamed: 1'].astype(str).to_list(), np.arange(len(df_unicambios))):
        if 'USD' in nombre:
            idx_unicambios.append(indice)
    df_sub_unicambios = df_unicambios.loc[idx_unicambios, :]
    df_sub_unicambios.columns = ['MonedaCurrency','CompraBuy','VentaSale']



    df_poblado = pd.read_html(tabla_divisas_poblado)[0]
    df_poblado.columns = ['MonedaCurrency','CompraBuy','VentaSale']
    idx_poblado = []
    for a,b in zip(df_poblado['MonedaCurrency'].astype(str).to_list(),np.arange(len(df_poblado))):
        if 'US' in a:
            idx_poblado.append(b)
    df_poblado_sub = df_poblado.loc[idx_poblado,:]


def compose_email():
    global body_final
    html = '<html>'
    texto_1 = """
    <h2>
    ¡Hola bebé!
    </h2>
    <h4>
    Escribí este Scriptcito para darle seguimiento al dólar y comprar cuando este bajo para le viaje a Cuba 
    </h4>
    """.replace("\n","")
    str_poblado = df_poblado_sub.to_html(index=False).replace("\n","")
    str_unicambios = df_sub_unicambios.to_html(index=False).replace("\n","")
    str_surcambios = df_sub.to_html(index=False).replace("\n","")
    body_final = html + texto_1 + "<h5> Cambios el Poblado </h5>" +  str_poblado  + "<br><hr><br>" +  "<h5> Unicambios </h5>" + str_unicambios + "<br><hr><br>" + "<h5> Surcambios </h5>" + str_surcambios + "<br><p>Te amo más de lo que crees posible!"



def send_mail():

    sender = ''
    password = ''
    receiver = ','
    part = MIMEText(body_final,'html')
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = (', ').join(receiver.split(','))
    message['Subject'] = 'Dolar : ' + ya
    message['Cc'] = ''
    message.attach(part)
    session = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    session.starttls() #enable security
    session.login(sender, password)

    rcp = receiver.split(",") + sender.split(",")

    session.sendmail(message['From'] ,rcp, message.as_bytes())
    session.quit()
    print('Mail Sent')


if __name__ == "__main__":
    download_data()
    compose_()
    compose_email()
    send_mail()
