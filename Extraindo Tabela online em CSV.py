# Importando biblioteca


from urllib.request import urlopen, urlretrieve, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd


# Obtendo a tabela

url = "https://www.fundamentus.com.br/resultado.php"
headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

req = Request(url,headers=headers)
response = urlopen(req)
html = response.read()
soup = BeautifulSoup(html,'html.parser')

# Obtendo as TAGs de interesse

lista =soup.find('table')



#quantidade ações
qtd = soup.findAll('span',class_='tips') 
qtd = range(int(len(qtd)-1)) #retira o ultimo registro para não ter erro
 
#Declarando variáveis cards
resumo = []


#pega as primeiras informações que não entram no for
papel =  lista.find('td').find('span',class_='tips').getText()
cotacao = lista.find('td').findNext('td').contents[0]
 
for i in qtd:
 
  acoes ={}
 
  PL = cotacao.findNext('td').contents[0]
  PVP = PL.findNext('td').contents[0]
  PSR = PVP.findNext('td').contents[0]
  DividendYied = PSR.findNext('td').contents[0]
  PAtivo = DividendYied.findNext('td').contents[0]
  PCapGiro = PAtivo.findNext('td').contents[0]
  PEbit= PCapGiro.findNext('td').contents[0]
  PAtivoCirc= PEbit.findNext('td').contents[0]
  EVEbit= PAtivoCirc.findNext('td').contents[0]
  EVEbita= EVEbit.findNext('td').contents[0]
  MrgEbit= EVEbita.findNext('td').contents[0]
  MrgLiq= MrgEbit.findNext('td').contents[0]
  LiqCorrente= MrgLiq.findNext('td').contents[0]
  ROIC= LiqCorrente.findNext('td').contents[0]
  ROE= ROIC.findNext('td').contents[0]
  Liq2Meses= ROE.findNext('td').contents[0]
  PatriLiquido= Liq2Meses.findNext('td').contents[0]
  DivBruta_por_Patri= PatriLiquido.findNext('td').contents[0]
  Cresc_5a= DivBruta_por_Patri.findNext('td').contents[0]
 
  acoes['id']= i
  acoes['Papel'] = papel
  acoes['Cotacao'] = cotacao
  acoes['PL'] = PL
  acoes['PVP']=PVP
  acoes['DividendYied']=DividendYied
  acoes['PAtivo']=PAtivo
  acoes['PCapGiro']=PCapGiro
  acoes['PEbit']=PEbit
  acoes['PAtivoCirc']=PAtivoCirc
  acoes['EVEbit']=EVEbit
  acoes['EVEbita']=EVEbita
  acoes['MrgEbit']=MrgEbit
  acoes['MrgLiq']=MrgLiq
  acoes['LiqCorrente']=LiqCorrente
  acoes['ROIC']=ROIC
  acoes['ROE']=ROE
  acoes['Liq2Meses']=Liq2Meses
  acoes['PatriLiquido']=PatriLiquido
  acoes['DivBruta_por_Patri']=DivBruta_por_Patri
  acoes['Cresc_5a']=Cresc_5a
 
  #Adicionando o dicionário de ações em uma lista
  resumo.append(acoes)
 
  #try retorna erro por a ultima linha não encontra o span
  try:
    papel = Cresc_5a.findNext('td').span.a.contents[0]
    cotacao = papel.findPrevious('td').findNext('td').contents[0]
 
  except HTTPError as e:
    print(e.status, e.reason)



# Criando data frame

dataset = pd.DataFrame(resumo)

dataset.head(10000)

display(dataset)



# Nomeando dataframe

tabela_acoes = dataset

#Tratamento de Dados Coluna PL  
tabela_acoes['PL'] = tabela_acoes['PL'].replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'PL': float}
tabela_acoes['PL']  = tabela_acoes['PL'].astype(convert_dict)
 
#Tratamento de Dados Coluna ROE
tabela_acoes['ROE'] = tabela_acoes['ROE'].replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'ROE': float}
tabela_acoes['ROE']  = tabela_acoes['ROE'].astype(convert_dict)/100
 
#Tratamento de Dados Coluna MrgLiq
tabela_acoes['MrgLiq'] = tabela_acoes['MrgLiq'].replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'MrgLiq': float}
tabela_acoes['MrgLiq']  = tabela_acoes['MrgLiq'].astype(convert_dict)/100
 
#Tratamento de Dados Coluna DivBruta_por_Patri  
tabela_acoes['DivBruta_por_Patri'] = tabela_acoes['DivBruta_por_Patri'].replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'DivBruta_por_Patri': float}
tabela_acoes['DivBruta_por_Patri']  = tabela_acoes['DivBruta_por_Patri'].astype(convert_dict)
 
#Tratamento de Dados Coluna Cresc_5a
tabela_acoes['Cresc_5a'] = tabela_acoes['Cresc_5a'].replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'Cresc_5a': float}
tabela_acoes['Cresc_5a']  = tabela_acoes['Cresc_5a'].astype(convert_dict)/100
 
#Tratamento de Dados Coluna DividendYied
dataset['DividendYied'] = dataset['DividendYied'].replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'DividendYied': float}
dataset['DividendYied']  = dataset['DividendYied'].astype(convert_dict)/100
 
#Tratamento de Dados Coluna ROIC
tabela_acoes['ROIC'] = tabela_acoes['ROIC'].replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'ROIC': float}
tabela_acoes['ROIC']  = tabela_acoes['ROIC'].astype(convert_dict)/100
 
#Tratamento de Dados Coluna MrgEbit
dataset['MrgEbit'] = dataset['MrgEbit'].replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'MrgEbit': float}
dataset['MrgEbit']  = dataset['MrgEbit'].astype(convert_dict)/100
 
#Tratamento de Dados Coluna PVP  
tabela_acoes['PVP'] = tabela_acoes['PVP'].replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'PVP': float}
tabela_acoes['PVP']  = tabela_acoes['PVP'].astype(convert_dict)
 
 
#Tratamento de Dados Coluna EVEbit
tabela_acoes['EVEbit'] = tabela_acoes['EVEbit'].replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'EVEbit': float}
tabela_acoes['EVEbit']  = tabela_acoes['EVEbit'].astype(convert_dict)
 
#Tratamento de Dados Coluna EVEbita
tabela_acoes['EVEbita'] = tabela_acoes['EVEbita'].replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'EVEbita': float}
tabela_acoes['EVEbita']  = tabela_acoes['EVEbita'].astype(convert_dict)

#Blacklist de ações descontinuadas
blacklist ={
    'PTPA3'
}
 
#Filtragem de dados
selecao = (tabela_acoes['PL'] >== 1) & (tabela_acoes['ROE'] > 0) & (tabela_acoes['ROE'] < 90) &  (tabela_acoes['MrgLiq'] > 0) & (tabela_acoes['DivBruta_por_Patri'] > 1.3) &  (tabela_acoes['Cresc_5a'] > 0.1)
 
melhores_acoes = tabela_acoes[selecao].sort_values('PL', ascending=False)
display(melhores_acoes)

#Blacklist de ações descontinuadas
blacklist ={
    'PTPA3'
}
 
#Filtragem de dados
selecao = (tabela_acoes['PL'] >== 1) & (tabela_acoes['ROE'] > 0) & (tabela_acoes['ROE'] < 90) &  (tabela_acoes['MrgLiq'] > 0) & (tabela_acoes['DivBruta_por_Patri'] > 1.3) &  (tabela_acoes['Cresc_5a'] > 0.1)
 
melhores_acoes = tabela_acoes[selecao].sort_values('PL', ascending=False)
display(melhores_acoes)

#configura visualização de dados pelo python

plt.rc('figure',figsize=(30,10))
 
plt.rc('font', family='serif', size=8)
 
area = plt.figure()

#cria o gráfico pelo python
dados_g1 = melhores_acoes.sort_values(by='PL', ascending=False)
g1.barh(dados_g1.Papel,dados_g1.PL)
g1.set_title('PL por ação')
 
dados_g2 = melhores_acoes.sort_values(by='PVP', ascending=False)
g2.barh(dados_g2.Papel,dados_g2.PVP)
g2.set_title('PVP')
 
area
