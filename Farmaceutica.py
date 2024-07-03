import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Dates for Business Analitycs
File_Path = 'C:/Users/Atenc/Desktop/Date Science/Primer Proyecto/Abandono Empleados.csv'
df_Employees = pd.read_csv(File_Path, sep = ';', index_col= 'id', na_values='#N/D')

#Analisis de nulos
df_Employees = df_Employees.drop(columns=['anos_en_puesto', 'conciliacion', 'sexo', 'horas_quincena'])

#información  de las variales 
df_Categorical  = df_Employees.select_dtypes('object')
df_Numerical    = df_Employees.select_dtypes('number')
print(df_Categorical.info())
print(df_Numerical.info())

#Tasa de abandono del 16%

#Análisis exploratorio de variables numéricas
def info_Numerical(num):
    #calculamos describe
    estadisticos = num.describe().T
    print("type(estadisticos): ", type(estadisticos))

    #añadimos la mediana 
    estadisticos['median'] = num.median()

    #reordenamos 
    estadisticos = estadisticos.iloc[:,[0,1,8,2,3,4,5,6,7]]

    #~lo devolvemos 
    return(estadisticos)


#Análisis exploratorio de variables categóricas
def info_Categorical (df_obj, total_rows, grap = True):
    # extraigo el número de filas y columnas de los sub plots para categóricas
    from math import ceil
    number_rows     = ceil(df_obj.shape[1]/2)
    number_columns  = 2

    #Replace with the max frecuenci value
    for index in df_obj.columns:

        #validate the null values 
        a = df_obj[index].isnull().sum()
        if a == total_rows:
            break
        
        #Calculate the principal value
        serie = df_obj[index].value_counts()
        value_Max = serie.iloc[0]
        index_serie_max = ''
        for index_Serie in serie.index:
            if serie[index_Serie] >= value_Max:
                value_Max = serie[index_Serie]
                index_serie_max = index_Serie
        
        #Replace the Null with the principal value
        df_obj[index] = df_obj[index].fillna(index_serie_max)

    #create the sub plots
    if grap == True:

        fig, ax =  plt.subplots(nrows = number_rows, ncols = number_columns, figsize = (16, number_columns*5))

        #graph the sub plots
        ax = ax.flat
        for i, variable in enumerate(df_obj.columns):
            Serie = df_obj[variable].value_counts().astype(float) 
            value_Total_Serie = Serie.sum()

            for j in Serie.index: 
                Serie[j] = round((Serie[j]/value_Total_Serie) * 100,2)

            Serie.plot.barh( ax = ax[i]) #create the grap (plot)
            ax[i].set_title(None, fontsize = 8, fontweight = "bold")
            ax[i].tick_params(labelsize = 8)
        
        plt.tight_layout()
        plt.show()

    return df_obj


#Qué perfiles tienen una tasa de abandono superior a la obtenida por la tasa de abandono de todos los empleados?
#por encima del 16% 


#Análisis categótrico de perfiles según su tasa de abandono (Análisis de penetración)
def penetration_Analize (df_obj, Graph = True):
    # extraigo el número de filas y columnas de los sub plots para categóricas
    from math import ceil
    number_rows     = ceil(df_obj.shape[1]/2)
    number_columns  = 2

    #create the sub plots
    _, ax =  plt.subplots(nrows = number_rows, ncols = number_columns, figsize = (16, number_columns*5))

    df_obj['abandono'] = df_obj.abandono.map({'No': 0, 'Yes': 1})

    #graph the sub plots
    if Graph == True:
        ax = ax.flat
        for i, variable in enumerate(df_obj.columns):
            if variable != 'abandono':
                Serie = df_obj.groupby(variable).abandono.mean().sort_values(ascending = True) *100 
                value_Total_Serie = Serie.sum()

                Serie.plot.barh(ax = ax[i]) #create the grap (plot)
                ax[i].set_title(None, fontsize = 8, fontweight = "bold")
                ax[i].tick_params(labelsize = 8)
            else: 
                df_obj['abandono'] = df_obj.abandono.map({0: 'No', 1: 'Yes'})
                Serie = df_obj[variable].value_counts().astype(float)
                value_Total_Serie = Serie.sum()

                for j in Serie.index: 
                    Serie[j] = round((Serie[j]/value_Total_Serie) * 100,2)

                Serie.plot.barh(ax = ax[i]) #create the grap (plot)
                ax[i].set_title(None, fontsize = 8, fontweight = "bold")
                ax[i].tick_params(labelsize = 8)
                df_obj['abandono'] = df_obj.abandono.map({'No': 0, 'Yes': 1})

        
        plt.tight_layout()
        plt.show()
    return df_obj


df_Categorical_new =  info_Categorical(df_Categorical, df_Categorical.shape[0], grap = False)
df_Numerical['salario_ano']   =   df_Employees['salario_mes'] * 12
print(df_Numerical)
penetration_Analize(df_Categorical_new, Graph = True)


