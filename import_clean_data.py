import pandas as pd

def import_clean_airport_df(filename):

    print('importing data...')
    df = pd.read_csv(filename)
    #print(df.isnull().sum().reset_index().head(32))

    # Delay Flags ranges

    # cd = df[df['CARRIER_DELAY']>0].CARRIER_DELAY
    # wd = df[df['WEATHER_DELAY']>0].WEATHER_DELAY
    # nd = df[df['NAS_DELAY']>0].NAS_DELAY
    # sd = df[df['SECURITY_DELAY']>0].SECURITY_DELAY
    # ld = df[df['LATE_AIRCRAFT_DELAY']>0].LATE_AIRCRAFT_DELAY

    # Binarize delay flags

    print('Binarize delay types...')
    df.loc[df['CARRIER_DELAY']>0, 'CARRIER_DELAY'] = 1
    df.loc[df['WEATHER_DELAY']>0, 'WEATHER_DELAY'] = 1
    df.loc[df['NAS_DELAY']>0, 'NAS_DELAY'] = 1
    df.loc[df['SECURITY_DELAY']>0, 'SECURITY_DELAY'] = 1
    df.loc[df['LATE_AIRCRAFT_DELAY']>0, 'LATE_AIRCRAFT_DELAY'] = 1

    df.loc[df['DEP_DEL15']==0, 'CARRIER_DELAY'] = 0
    df.loc[df['DEP_DEL15']==0, 'WEATHER_DELAY'] = 0
    df.loc[df['DEP_DEL15']==0, 'NAS_DELAY'] = 0
    df.loc[df['DEP_DEL15']==0, 'SECURITY_DELAY'] = 0
    df.loc[df['DEP_DEL15']==0, 'LATE_AIRCRAFT_DELAY'] = 0

    # Delay sizes

    print('Creating delay size variables...')
    for delay in ['CARRIER_DELAY', 'WEATHER_DELAY', 'LATE_AIRCRAFT_DELAY', 'NAS_DELAY']:
        df.loc[(df[delay] == 1) & (df['DEP_DELAY_NEW'] >= 15), f'SIZE_{delay}'] = f'SMALL_{delay}'
        df.loc[(df[delay] == 1) & (df['DEP_DELAY_NEW'] > 30), f'SIZE_{delay}'] = f'MEDIUM_{delay}'
        df.loc[(df[delay] == 1) & (df['DEP_DELAY_NEW'] > 60), f'SIZE_{delay}'] = f'BIG_{delay}'

        df.loc[(df[f'SIZE_{delay}'].isna()) & (df['DEP_DEL15']==0), f'SIZE_{delay}'] = 'NO_DELAY'

    df.loc[df['DEP_DELAY_NEW'] < 15, f'SIZE_DELAY'] = f'NO_DELAY'
    df.loc[df['DEP_DELAY_NEW'] >= 15, f'SIZE_DELAY'] = f'SMALL_DELAY'
    df.loc[df['DEP_DELAY_NEW'] > 30, f'SIZE_DELAY'] = f'MEDIUM_DELAY'
    df.loc[df['DEP_DELAY_NEW'] > 60, f'SIZE_DELAY'] = f'BIG_DELAY'

    # Get dummies for delay sizes

    print('Getting dummy variables for delay sizes...')
    df = pd.get_dummies(df, columns=['SIZE_CARRIER_DELAY'])
    df = pd.get_dummies(df, columns=['SIZE_WEATHER_DELAY'])
    df = pd.get_dummies(df, columns=['SIZE_LATE_AIRCRAFT_DELAY'])
    df = pd.get_dummies(df, columns=['SIZE_NAS_DELAY'])
    df = pd.get_dummies(df, columns=['SIZE_DELAY'])

    df = df.fillna(0)

    # Keep categorical delay sizes variables
    
    for delay in ['CARRIER_DELAY', 'WEATHER_DELAY', 'LATE_AIRCRAFT_DELAY', 'NAS_DELAY']:
        df.loc[(df[delay] == 1) & (df['DEP_DELAY_NEW'] >= 15), f'SIZE_{delay}'] = f'SMALL_{delay}'
        df.loc[(df[delay] == 1) & (df['DEP_DELAY_NEW'] > 30), f'SIZE_{delay}'] = f'MEDIUM_{delay}'
        df.loc[(df[delay] == 1) & (df['DEP_DELAY_NEW'] > 60), f'SIZE_{delay}'] = f'BIG_{delay}'

        df.loc[(df[f'SIZE_{delay}'].isna()) & (df['DEP_DEL15']==0), f'SIZE_{delay}'] = 'NO_DELAY'

    df.loc[df['DEP_DELAY_NEW'] < 15, f'SIZE_DELAY'] = f'NO_DELAY'
    df.loc[df['DEP_DELAY_NEW'] >= 15, f'SIZE_DELAY'] = f'SMALL_DELAY'
    df.loc[df['DEP_DELAY_NEW'] > 30, f'SIZE_DELAY'] = f'MEDIUM_DELAY'
    df.loc[df['DEP_DELAY_NEW'] > 60, f'SIZE_DELAY'] = f'BIG_DELAY'

    return df