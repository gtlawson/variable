# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 07:17:30 2018

@author: glawson
"""

#train = pd.read_csv('C:/Users/glawson/Documents/Python Scripts/SupervisorPerformanceData.csv')

#To use this function, specify the dataframe of independent variables (X) and the 
#target variables (y) to be used.
def forward(X,y):

    #import necessary packages
    import pandas as pd 
    import numpy as np
    import statsmodels.api as sm
    import math
    
    #Combine dataframes for use in correlation
    df = pd.concat([y, X], axis=1)
    #Add a constant
    df = sm.add_constant(df)
    
    df_corr = df.copy()
    
    #Assign a "target" variable
    target = y.name
    
    #Create several dataframes for use in the function
    variable_list = df.columns.drop('const') #This is the list of variables that will be passed through the correlation function
    FS_Order_const = ['const']
    FS_Order = []
    variable_order = []
    rsquared_value = []
    min_t_test = []
    max_p_val = []
    mse = []
    aic = []
    bic = []
    
    for i in range(len(df.columns)-2):
        corr0 = df_corr[variable_list].corr()
        corr0 = corr0.drop(target,0)
        corr = pd.DataFrame(abs(corr0[target]))
    
        corr.reset_index(level=0, inplace=True)
        corr_sorted = corr.sort_values([target], ascending=[False])
        #print(corr_sorted.iloc[0,0])
        max_corr_var = corr_sorted.iloc[0,0]
        FS_Order_const.append(max_corr_var)
        FS_Order.append(max_corr_var)
        variable_order.append(max_corr_var)
        
        model = sm.OLS(df[target], df[FS_Order_const]).fit()
        model.summary()
        resid = model.resid
        rsquared_result = model.rsquared
        
        max_p_val.append(max(model.pvalues[FS_Order]))
        min_t_test.append(abs(model.tvalues[max_corr_var]))
        rsquared_value.append(rsquared_result)
        mse.append(model.mse_resid)
        aic.append(model.aic)
        bic.append(model.bic)
        
        variable_list = variable_list.drop(max_corr_var,1)
        df_corr[target] = resid       
    
    root_mse = [math.sqrt(x) for x in mse]
    result = pd.DataFrame(np.column_stack([min_t_test, max_p_val, rsquared_value, mse, root_mse, aic, bic]), columns=['min_abs_(t)', 'max_p_value', 'r_squared', 'MSE', 'Root_MSE', 'AIC', 'BIC'])
    result.insert(0, 'variable', variable_order)
    print ('\n**********************   Forward Selection Results   ***********************\n')
    print (round(result,2))
    
    
   
    
def back(X,y):

    #import necessary packages
    import pandas as pd 
    import numpy as np
    import statsmodels.api as sm
    import math
    
    #Combine dataframes for use in correlation
    df = pd.concat([y, X], axis=1)
    #Add a constant
    df = sm.add_constant(df)
    
    #Assign a "target" variable
    target = y.name
    
    #Create several dataframes for use in the function
    variable_list = df.columns.drop(target) #This is the list of variables that will be passed through the correlation function
    BS_Order = X.columns
    variable_order = []
    rsquared_value = []
    min_t_test = []
    max_p_val = []
    mse = []
    aic = []
    bic = []
    
    for i in range(len(df.columns)-2):
        
        model = sm.OLS(df[target], df[variable_list]).fit()
        model.summary()
        resid = model.resid
        rsquared_result = model.rsquared
        
        
        min_t_val = min(abs(model.tvalues[BS_Order]))
        max_p_val.append(max(model.pvalues[BS_Order]))
        min_t_test.append(min_t_val)
        rsquared_value.append(rsquared_result)
        mse.append(model.mse_resid)
        aic.append(model.aic)
        bic.append(model.bic)
        
        min_t_var = pd.DataFrame(abs(model.tvalues[BS_Order]), columns=['min_t_val'])
    
        min_t_var.reset_index(level=0, inplace=True)
        min_t_var_sorted = min_t_var.sort_values(['min_t_val'], ascending=[True])
        #print(corr_sorted.iloc[0,0])
        min_t_val = min_t_var_sorted.iloc[0,0]
        BS_Order = BS_Order.drop(min_t_val)
        variable_list = variable_list.drop(min_t_val)
        variable_order.append(min_t_val)
        
                  
    root_mse = [math.sqrt(x) for x in mse]
    result = pd.DataFrame(np.column_stack([min_t_test, max_p_val, rsquared_value, mse, root_mse, aic, bic]), columns=['min_abs_(t)', 'max_p_value', 'r_squared', 'MSE', 'Root_MSE', 'AIC', 'BIC'])
    result.insert(0, 'variable', variable_order)
    print ('\n**********************   Backward Selection Results   ***********************\n')
    print (round(result,2))
    