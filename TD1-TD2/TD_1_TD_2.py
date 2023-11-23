import json
import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# logging.basicConfig()
# logging.getLogger().setLevel(print) 


data_td1_json = './data/td1/evg_esp_veg.envpdiprboucle.json'

with open(data_td1_json, 'r') as f:
    randone = json.load(f)

rando = randone['values']



print('-'*10, 'PART ONE', '-'*10)
# 1.3 get variable type 
print(f'type of file {type(rando)}')
# 1.4 get lenght 
print(f'with lenght {len(rando)}')
print(f'Randonnée numb 10 name {rando[10]["nom"]}') # Name of hiking num 10



print('-'*10, 'PART TWO', '-'*10)
    
# 2.1 dataset in pandas
rando_df = pd.DataFrame.from_dict(rando)
# 2.2 get lenght 
print('Getting type')
# 2.3 Test iloc and loc
print(rando_df.iloc[:, 2:5])
print(rando_df.iloc[:, 3:8])
rando_df['denivele_num'] = rando_df['denivele'].str.replace('m', '').astype(int)
print(rando_df.iloc[:10, 10:])

print(rando_df['denivele_num'].max())
print(rando_df['denivele_num'].mean())
print(rando_df['denivele_num'].min())
print(rando_df['denivele'].value_counts())

rando_df['temps_parcours'] = rando_df['temps_parcours'].str.replace('min', '').astype(int)
print(rando_df['temps_parcours'].mean())
new_value = [i for i in rando_df['temps_parcours']]
rando_df['temps_parcours_test'] = [f"{i} mtr" for i in rando_df['temps_parcours']]
print(rando_df['temps_parcours_test'])
grouped = rando_df.groupby('difficulte')
print(grouped['temps_parcours'].mean()) #2.8
    



print('-'*10, 'PART TREE', '-'*10)

grouped.count()['temps_parcours'].plot.bar()
rando_df['temps_parcours'].sort_index(ascending=True) # 3.2
grouped.count().plot.pie(y='temps_parcours', figsize=(5, 5)) #3.3



print('-'*10, 'PART FOUR', '-'*10)
rando_df['longueur'] = rando_df['longueur'].str.replace("km", "").str.replace(",", ".") #4.1
rando_df['denivele'] = rando_df['denivele'].str.replace("m", "") #4.1
rando_df['longueur'] = [float(i) for i in rando_df['longueur']]
rando_df['denivele'] = [int(i) for i in rando_df['denivele']]

# rando_df['longueur']

# # Separate each group in a different dataframe to create the scatter with different axis
# moyen_df = rando_df[rando_df['difficulte'] == 'moyen']
# # moyen_df.iloc[:, [10, 13]]
# facile_df = rando_df[rando_df['difficulte'] == 'facile']
# # facile_df.iloc[:, [10, 13]] 
# difficile_df = rando_df[rando_df['difficulte'] == 'difficile']
# # difficile_df.iloc[:, [10, 13]] 

# ## Creating each scatter with different colors and labels
# ax_1 = moyen_df.plot.scatter(x ='longueur', y ='temps_parcours', color="DarkBlue", label="moyen")
# ax_2 = facile_df.plot.scatter(x ='longueur', y ='temps_parcours', color="Green", label="facile", ax=ax_1)
# difficile_df.plot.scatter(x ='longueur', y ='temps_parcours', color="Red", label="difficile", ax=ax_2)


# # # Get Correlation
# # To get correlation it is neccesary to get two columns to corelationate each one and use term `corr` from Pandas to make it, remember correlation of this process take values from -1 0 or 1 where if n is near -1 or 1 correlation is strong between variables x and y


# rando_df['longueur'] = [float(i) for i in rando_df['longueur']]



# df_corr = rando_df.iloc[:, [4,10,13]]

# # Here different coorrelations, as you can see there are more relation btween longueur and temps_parcours
# df_corr.corr()


# # # 5. Analyse sur plusieurs tables
# # 5.2
# df_caracte = pd.read_csv('../data/td2/caracteristiques-2018.csv')
# df_usagers = pd.read_csv('../data/td2/usagers-2018.csv')
# df_vehicles = pd.read_csv('../data/td2/vehicules-2018.csv')
# df_lieux = pd.read_csv('../data/td2/lieux-2018.csv')

# df_lieux.dtypes


# accidents_lyon = df_caracte

# # Conut number of occurrences for Lyon Code department 690
# count_lyon_acc = accidents_lyon['dep'].value_counts()[690]


# count_lyon_acc

# accidents_velo = df_vehicles
# joined_accidents = accidents_lyon.join(other=accidents_velo, lsuffix='_caller', rsuffix='_other')
# joined_accidents.iloc[:, [0,1,3,-1]]

# accidents_velo = df_vehicles
# accidents_velo = accidents_velo.loc[accidents_velo['manv'] == 1.0]
# accidents_velo                  


