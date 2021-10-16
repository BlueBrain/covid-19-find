import getdeaths as gd
import pandas as pd
import cdatabbp as bbp
import covidlib as cl
import datetime as dt
import os

useBBPdata = True
a=2

testcountries = ['ZZ']
# testcountries = ['CH','SV','LA']
# testcountries = ['CH','US','IT','FR','ES','IN','PH','GB','CA','EG','BR','PE']
# testcountries = ['GT','ZA','BO','CO','CL','BD','PL','CN','UA','MD','KG','NG']

def getdeathdata(countryname):
   df = gd.get_death_data_by_country(countryname)
   return df.fillna(0).reset_index()

test_df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/countrytests.csv")

def merge_with_test_data(df, countryname):
  col = test_df.columns
  if countryname in col:
    test_df.drop(test_df.tail(1).index,inplace=True)
#    test_df["Date"] = test_df["Row Labels"] + ".2020";
    test_df["Date"] = test_df["Row Labels"]
    test_df["Date"] = pd.to_datetime(test_df["Date"], format='%d.%m.%y')

    test_df["Date"] = test_df["Date"].astype(str) 
    df["Date"] = df["Date"].astype(str);

    specific_df = test_df[["Date", countryname]]
    new_df = pd.merge(df, specific_df, on="Date")

    df = new_df.rename(columns={countryname: 'tests'})
    
  else:
    print("WARNING: no country name in tests file for",countryname)
    df["tests"] = 0
  return df

def gettestcountries():
   global testcountries
   return testcountries

def getallcountrycodes():
   global countries
   return countries.keys()

def getcountrycode(countryname):
   global countries
   for code in countries.keys():
     if countries[code] == countryname:
        return code
   return 'XX'

def getcountryname(countrycode):
   global countries
   return countries[countrycode]

def fixparamnames(dict):
   hospbeds = dict['hospitalBeds']
   if hospbeds is None:
      hospbeds = dict['population']/1000
   propurb = dict['urbanPopulationProportion']
   if propurb is None:
      propurb = 0
   else:
      propurb=round(propurb,4)
   propactive =  dict['activePopulationProportion']
   if propactive is None:
      propactive = 0
   else:
      propactive=round(propactive,4)
   propoverage = dict['over64Proportion']
   if propoverage is None:
      propoverage = 0
   else:
      propoverage=round(propoverage,4)
   params={'total_pop':dict['population'],
    'hospital_beds':hospbeds,
    'prop_15_64':propactive,
    'age_gt_64':propoverage,
    'prop_urban':propurb,
    'prop_below_pl':0.2,
    'prop_woh':0.6,
    'staff_per_bed':2.5
   }
   return params

def getcountryparams(countrycode):
   global countryparamdata
   if useBBPdata:
      paramdata = bbp.get_country_params(countrycode)
      return bbp.get_fixed_parameters(paramdata)
   else:
      paramdata = countryparamdata[countrycode]
      return fixparamnames(paramdata)

def checkcountryparams(countrycode):
   global countryparamdata
   if useBBPdata:
      paramdata = bbp.get_country_params(countrycode)
   else:
      paramdata = countryparamdata[countrycode]
   return paramdata

def getcountrydata(countrycode):
   n_records=60
   countryname = getcountryname(countrycode)
   if useBBPdata:
       resultdf = bbp.get_country_df(countrycode)
   else:
       df = getdeathdata(countryname)
       df = merge_with_test_data(df, countryname)
       n = len(df)
       newdf = df.rename(columns = {'total_deaths': 'accumulated_deaths'}, inplace = False)
       newdf['accumulated_cases'] = 0
       resultdf = newdf.reset_index()[['Date','accumulated_deaths','tests','accumulated_cases']]
   day1 = dt.datetime.strptime(resultdf.iloc[0]['Date'],"%Y-%m-%d")-dt.timedelta(days=n_records)
# =============================================================================
#    empty_df=cl.create_empty_country_df(day1, n_records)
#    frames=[empty_df,resultdf]
#    resultdf=pd.concat(frames)
# =============================================================================
   return resultdf

countries = {
    'AF': 'Afghanistan',
#    'AX': 'Åland Islands',
    'AL': 'Albania',
    'DZ': 'Algeria',
#    'AS': 'American Samoa',
    'AD': 'Andorra',
    'AO': 'Angola',
#    'AI': 'Anguilla',
#    'AQ': 'Antarctica',
    'AG': 'Antigua and Barbuda',
    'AR': 'Argentina',
    'AM': 'Armenia',
#    'AW': 'Aruba',
    'AU': 'Australia',
    'AT': 'Austria',
    'AZ': 'Azerbaijan',
    'BS': 'Bahamas',
    'BH': 'Bahrain',
    'BD': 'Bangladesh',
    'BB': 'Barbados',
    'BY': 'Belarus',
    'BE': 'Belgium',
    'BZ': 'Belize',
    'BJ': 'Benin',
#    'BM': 'Bermuda',
    'BT': 'Bhutan',
    'BO': 'Bolivia',
 #   'BQ': 'Bonaire, Sint Eustatius and Saba',
    'BA': 'Bosnia and Herzegovina',
    'BW': 'Botswana',
 #   'BV': 'Bouvet Island',
    'BR': 'Brazil',
 #   'IO': 'British Indian Ocean Territory',
    'BN': 'Brunei',
    'BG': 'Bulgaria',
    'BF': 'Burkina Faso',
    'BI': 'Burundi',
    'KH': 'Cambodia',
    'CM': 'Cameroon',
    'CA': 'Canada',
    'CV': 'Cabo Verde',
#    'KY': 'Cayman Islands',
    'CF': 'Central African Republic',
    'TD': 'Chad',
    'CL': 'Chile',
    'CN': 'China',
#    'CX': 'Christmas Island',
#    'CC': 'Cocos (Keeling) Islands',
    'CO': 'Colombia',
    'KM': 'Comoros',
    'CG': 'Congo (Brazzaville)',
    'CD': 'Congo (Kinshasa)',
    # 'CK': 'Cook Islands',
    'CR': 'Costa Rica',
    'CI': 'Cote d\'Ivoire',
    'HR': 'Croatia',
    'CU': 'Cuba',
 #   'CW': 'Curaçao',
    'CY': 'Cyprus',
    'CZ': 'Czechia',
    'DK': 'Denmark',
    'DJ': 'Djibouti',
    'DM': 'Dominica',
    'DO': 'Dominican Republic',
    'EC': 'Ecuador',
    'EG': 'Egypt',
    'SV': 'El Salvador',
    'GQ': 'Equatorial Guinea',
    'ER': 'Eritrea',
    'EE': 'Estonia',
    'ET': 'Ethiopia',
#    'FK': 'Falkland Islands (Malvinas)',
#    'FO': 'Faroe Islands',
    'FJ': 'Fiji',
    'FI': 'Finland',
    'FR': 'France',
#    'GF': 'French Guiana',
#    'PF': 'French Polynesia',
#    'TF': 'French Southern Territories',
    'GA': 'Gabon',
    'GM': 'Gambia',
    'GE': 'Georgia',
    'DE': 'Germany',
    'GH': 'Ghana',
#    'GI': 'Gibraltar',
    'GR': 'Greece',
#    'GL': 'Greenland',
    'GD': 'Grenada',
#    'GP': 'Guadeloupe',
#    'GU': 'Guam',
    'GT': 'Guatemala',
#    'GG': 'Guernsey',
    'GN': 'Guinea',
    'GW': 'Guinea-Bissau',
    'GY': 'Guyana',
    'HT': 'Haiti',
#    'HM': 'Heard Island and McDonald Islands',
    'VA': 'Holy See',
    'HN': 'Honduras',
#    'HK': 'Hong Kong',
    'HU': 'Hungary',
    'IS': 'Iceland',
    'IN': 'India',
    'ID': 'Indonesia',
    'IR': 'Iran',
    'IQ': 'Iraq',
    'IE': 'Ireland',
#    'IM': 'Isle of Man',
    'IL': 'Israel',
    'IT': 'Italy',
    'JM': 'Jamaica',
    'JP': 'Japan',
#    'JE': 'Jersey',
    'JO': 'Jordan',
    'KZ': 'Kazakhstan',
    'KE': 'Kenya',
    # 'KI': 'Kiribati',
    # 'KP': 'Korea, Democratic People\'s Republic of',
    'KR': 'Korea, South',
    'XK': 'Kosovo',
    'KW': 'Kuwait',
    'KG': 'Kyrgyzstan',
    'LA': 'Laos',
    'LV': 'Latvia',
    'LB': 'Lebanon',
    'LS': 'Lesotho',
    'LR': 'Liberia',
    'LY': 'Libya',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
#    'MO': 'Macao',
#    'MK': 'North Macedonia',
    'MG': 'Madagascar',
    'MW': 'Malawi',
    'MY': 'Malaysia',
    'MV': 'Maldives',
    'ML': 'Mali',
    'MT': 'Malta',
#    'MH': 'Marshall Islands',
#    'MQ': 'Martinique',
    'MR': 'Mauritania',
    'MU': 'Mauritius',
#    'YT': 'Mayotte',
    'MX': 'Mexico',
 #   'FM': 'Micronesia, Federated States of',
    'MD': 'Moldova',
    'MC': 'Monaco',
    'MN': 'Mongolia',
#    'ME': 'Montenegro',
#    'MS': 'Montserrat',
    'MA': 'Morocco',
    'MZ': 'Mozambique',
    'MM': 'Burma',
    'NA': 'Namibia',
#    'NR': 'Nauru',
    'NP': 'Nepal',
    'NL': 'Netherlands',
#    'NC': 'New Caledonia',
    'NZ': 'New Zealand',
    'NI': 'Nicaragua',
    'NE': 'Niger',
    'NG': 'Nigeria',
#    'NU': 'Niue',
#    'NF': 'Norfolk Island',
#    'MP': 'Northern Mariana Islands',
    'NO': 'Norway',
    'OM': 'Oman',
    'PK': 'Pakistan',
#    'PW': 'Palau',
#    'PS': 'Palestine, State of',
    'PA': 'Panama',
    'PG': 'Papua New Guinea',
    'PY': 'Paraguay',
    'PE': 'Peru',
    'PH': 'Philippines',
#    'PN': 'Pitcairn',
    'PL': 'Poland',
    'PT': 'Portugal',
#    'PR': 'Puerto Rico',
    'QA': 'Qatar',
#    'RE': 'Réunion',
    'RO': 'Romania',
    'RU': 'Russia',
    'RW': 'Rwanda',
#    'BL': 'Saint Barthélemy',
#    'SH': 'Saint Helena, Ascension and Tristan da Cunha',
    'KN': 'Saint Kitts and Nevis',
    'LC': 'Saint Lucia',
#    'MF': 'Saint Martin (French part)',
#    'PM': 'Saint Pierre and Miquelon',
    'VC': 'Saint Vincent and the Grenadines',
#    'WS': 'Samoa',
#    'SM': 'San Marino',
    'ST': 'Sao Tome and Principe',
    'SA': 'Saudi Arabia',
    'SN': 'Senegal',
    'RS': 'Serbia',
    'SC': 'Seychelles',
    'SL': 'Sierra Leone',
    'SG': 'Singapore',
    # 'SX': 'Sint Maarten (Dutch part)',
    'SK': 'Slovakia',
    'SI': 'Slovenia',
    'SB': 'Solomon Islands',
    'SO': 'Somalia',
    'ZA': 'South Africa',
#    'GS': 'South Georgia and the South Sandwich Islands',
    'SS': 'South Sudan',
    'ES': 'Spain',
    'LK': 'Sri Lanka',
    'SD': 'Sudan',
    'SR': 'Suriname',
#    'SJ': 'Svalbard and Jan Mayen',
#    'SZ': 'Eswatini',
    'SE': 'Sweden',
    'CH': 'Switzerland',
    'SY': 'Syria',
    'TW': 'Taiwan*',
    'TJ': 'Tajikistan',
    'TZ': 'Tanzania',
    'TH': 'Thailand',
    'TL': 'Timor-Leste',
    'TG': 'Togo',
    # 'TK': 'Tokelau',
    # 'TO': 'Tonga',
    'TT': 'Trinidad and Tobago',
    'TN': 'Tunisia',
    'TR': 'Turkey',
    # 'TM': 'Turkmenistan',
    # 'TC': 'Turks and Caicos Islands',
    # 'TV': 'Tuvalu',
    'UG': 'Uganda',
    'UA': 'Ukraine',
    'AE': 'United Arab Emirates',
    'GB': 'United Kingdom',
    'US': 'US',
#    'UM': 'United States Minor Outlying Islands',
    'UY': 'Uruguay',
    'UZ': 'Uzbekistan',
#    'VU': 'Vanuatu',
    'VE': 'Venezuela',
    'VN': 'Vietnam',
#    'VG': 'Virgin Islands, British',
#    'VI': 'Virgin Islands, U.S.',
#    'WF': 'Wallis and Futuna',
#    'EH': 'Western Sahara',
    'YE': 'Yemen',
    'ZM': 'Zambia',
    'ZW': 'Zimbabwe'
    }

countryparamdata = {
    'AF': {'countryCode': 'AF', 'population': 38928000, 'activePopulationProportion': 0.54, 'urbanPopulationProportion': 0.25, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.02926857274969174, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AX': None ,
    'AL': {'countryCode': 'AL', 'population': 2878000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.6, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.15895413481584433, 'hospitalBeds': 5756, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'DZ': {'countryCode': 'DZ', 'population': 43851000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.72, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.07331087090374223, 'hospitalBeds': 43851, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AS': None ,
    'AD': None ,
    'AO': {'countryCode': 'AO', 'population': 32866000, 'activePopulationProportion': 0.5, 'urbanPopulationProportion': 0.65, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.02436539280715633, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AI': {'countryCode': 'AI', 'population': 15000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AQ': None ,
    'AG': {'countryCode': 'AG', 'population': 98000, 'activePopulationProportion': 0.69, 'urbanPopulationProportion': 0.24, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.10165306122448982, 'hospitalBeds': 294, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AR': {'countryCode': 'AR', 'population': 45196000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.91, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.12159494203026819, 'hospitalBeds': 225980, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AM': {'countryCode': 'AM', 'population': 2963000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.63, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.12990853864326699, 'hospitalBeds': 11852, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AW': None ,
    'AU': {'countryCode': 'AU', 'population': 25500000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.86, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.17269113725490196, 'hospitalBeds': 76500, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AT': {'countryCode': 'AT', 'population': 9006000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.58, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.20371974239395957, 'hospitalBeds': 63042, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AZ': {'countryCode': 'AZ', 'population': 10139000, 'activePopulationProportion': 0.7000000000000001, 'urbanPopulationProportion': 0.55, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0757190058191143, 'hospitalBeds': 40556, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BS': {'countryCode': 'BS', 'population': 393000, 'activePopulationProportion': 0.7, 'urbanPopulationProportion': 0.83, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08522137404580155, 'hospitalBeds': 786, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BH': {'countryCode': 'BH', 'population': 1702000, 'activePopulationProportion': 0.78, 'urbanPopulationProportion': 0.89, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.030726204465334906, 'hospitalBeds': 3404, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BD': {'countryCode': 'BD', 'population': 164689000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.36, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05674097237824019, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BB': {'countryCode': 'BB', 'population': 287000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.31, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.17927177700348432, 'hospitalBeds': 1435, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BY': {'countryCode': 'BY', 'population': 9449000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.78, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.16940300560905916, 'hospitalBeds': 103939, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BE': {'countryCode': 'BE', 'population': 11590000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.98, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.20455711820534947, 'hospitalBeds': 69540, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BZ': {'countryCode': 'BZ', 'population': 398000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.45, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.054595477386934675, 'hospitalBeds': 398, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BJ': {'countryCode': 'BJ', 'population': 12123000, 'activePopulationProportion': 0.54, 'urbanPopulationProportion': 0.47, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.035981687701064094, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BM': None ,
    'BT': {'countryCode': 'BT', 'population': 772000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.4, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06693911917098445, 'hospitalBeds': 772, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BO': {'countryCode': 'BO', 'population': 11673000, 'activePopulationProportion': 0.61, 'urbanPopulationProportion': 0.69, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08022196521888118, 'hospitalBeds': 11673, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BQ': {'countryCode': 'BQ', 'population': 26000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BA': {'countryCode': 'BA', 'population': 3281000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.48, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.193559585492228, 'hospitalBeds': 9843, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BW': {'countryCode': 'BW', 'population': 2352000, 'activePopulationProportion': 0.61, 'urbanPopulationProportion': 0.69, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.04973767006802722, 'hospitalBeds': 2352, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BV': None ,
    'BR': {'countryCode': 'BR', 'population': 212559000, 'activePopulationProportion': 0.69, 'urbanPopulationProportion': 0.86, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.10405319934700485, 'hospitalBeds': 425118, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'IO': None ,
    'BN': {'countryCode': 'BN', 'population': 437000, 'activePopulationProportion': 0.72, 'urbanPopulationProportion': 0.77, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06257894736842104, 'hospitalBeds': 874, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BG': {'countryCode': 'BG', 'population': 6948000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.75, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.22807570523891765, 'hospitalBeds': 41688, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BF': {'countryCode': 'BF', 'population': 20903000, 'activePopulationProportion': 0.52, 'urbanPopulationProportion': 0.29, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.026756111562933546, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BI': {'countryCode': 'BI', 'population': 11891000, 'activePopulationProportion': 0.52, 'urbanPopulationProportion': 0.13, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.026823984526112187, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KH': {'countryCode': 'KH', 'population': 16719000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.23, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05341192655063102, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CM': {'countryCode': 'CM', 'population': 26546000, 'activePopulationProportion': 0.54, 'urbanPopulationProportion': 0.56, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.02997992164544564, 'hospitalBeds': 26546, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CA': {'countryCode': 'CA', 'population': 37742000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.81, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.19382738063695618, 'hospitalBeds': 75484, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CV': {'countryCode': 'CV', 'population': 556000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.65, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05269064748201439, 'hospitalBeds': 1112, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KY': None ,
    'CF': {'countryCode': 'CF', 'population': 4830000, 'activePopulationProportion': 0.52, 'urbanPopulationProportion': 0.41, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03094927536231884, 'hospitalBeds': 4830, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TD': {'countryCode': 'TD', 'population': 16426000, 'activePopulationProportion': 0.5, 'urbanPopulationProportion': 0.23, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.027603859734567148, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CL': {'countryCode': 'CL', 'population': 19116000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.87, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.13203159656831973, 'hospitalBeds': 38232, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CN': {'countryCode': 'CN', 'population': 1439324000, 'activePopulationProportion': 0.71, 'urbanPopulationProportion': 0.59, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.1302421032373531, 'hospitalBeds': 5757296, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CX': None ,
    'CC': None ,
    'CO': {'countryCode': 'CO', 'population': 50883000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.8, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.09813018100347855, 'hospitalBeds': 50883, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KM': {'countryCode': 'KM', 'population': 870000, 'activePopulationProportion': 0.5700000000000001, 'urbanPopulationProportion': 0.28, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.034572413793103454, 'hospitalBeds': 1740, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CG': {'countryCode': 'CG', 'population': 5518000, 'activePopulationProportion': 0.55, 'urbanPopulationProportion': 0.66, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.030665277274374767, 'hospitalBeds': 5518, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CD': {'countryCode': 'CD', 'population': 89561000, 'activePopulationProportion': 0.5, 'urbanPopulationProportion': 0.44, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03313855361150501, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CK': {'countryCode': 'CK', 'population': 18000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CR': {'countryCode': 'CR', 'population': 5094000, 'activePopulationProportion': 0.6900000000000001, 'urbanPopulationProportion': 0.79, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.1110671378091873, 'hospitalBeds': 5094, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CI': {'countryCode': 'CI', 'population': 26378000, 'activePopulationProportion': 0.55, 'urbanPopulationProportion': 0.5, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03204553036621426, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'HR': {'countryCode': 'HR', 'population': 4105000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.56, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.22654591961023143, 'hospitalBeds': 20525, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CU': {'countryCode': 'CU', 'population': 11327000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.77, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.16881416085459525, 'hospitalBeds': 56635, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CW': None ,
    'CY': {'countryCode': 'CY', 'population': 1207000, 'activePopulationProportion': 0.6900000000000001, 'urbanPopulationProportion': 0.66, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.15430903065451532, 'hospitalBeds': 3621, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CZ': {'countryCode': 'CZ', 'population': 10709000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.73, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.21376020169950508, 'hospitalBeds': 64254, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'DK': {'countryCode': 'DK', 'population': 5792000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.87, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2128758632596685, 'hospitalBeds': 11584, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'DJ': {'countryCode': 'DJ', 'population': 988000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.77, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.051640688259109314, 'hospitalBeds': 988, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'DM': None ,
    'DO': {'countryCode': 'DO', 'population': 10848000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.81, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0817508296460177, 'hospitalBeds': 10848, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'EC': {'countryCode': 'EC', 'population': 17643000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.63, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08222819248427139, 'hospitalBeds': 17643, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'EG': {'countryCode': 'EG', 'population': 102334000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.42, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05846609142611447, 'hospitalBeds': 102334, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SV': {'countryCode': 'SV', 'population': 6486000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.72, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.09287804502004314, 'hospitalBeds': 6486, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GQ': {'countryCode': 'GQ', 'population': 1403000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.72, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.02637348538845332, 'hospitalBeds': 2806, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'ER': {'countryCode': 'ER', 'population': 3546000, 'activePopulationProportion': 0.55, 'urbanPopulationProportion': 0.35, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.048706711787930054, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'EE': {'countryCode': 'EE', 'population': 1327000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.68, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.21670158251695548, 'hospitalBeds': 6635, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'ET': {'countryCode': 'ET', 'population': 114964000, 'activePopulationProportion': 0.55, 'urbanPopulationProportion': 0.2, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03861151316933997, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'FK': {'countryCode': 'FK', 'population': 3000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'FO': None ,
    'FJ': {'countryCode': 'FJ', 'population': 896000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.56, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06479464285714287, 'hospitalBeds': 1792, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'FI': {'countryCode': 'FI', 'population': 5541000, 'activePopulationProportion': 0.62, 'urbanPopulationProportion': 0.85, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2383322504963003, 'hospitalBeds': 22164, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'FR': {'countryCode': 'FR', 'population': 65274000, 'activePopulationProportion': 0.62, 'urbanPopulationProportion': 0.8, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2194590189049238, 'hospitalBeds': 391644, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GF': {'countryCode': 'GF', 'population': 299000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06159866220735786, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PF': None ,
    'TF': None ,
    'GA': {'countryCode': 'GA', 'population': 2226000, 'activePopulationProportion': 0.59, 'urbanPopulationProportion': 0.89, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.038530098831985625, 'hospitalBeds': 13356, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GM': {'countryCode': 'GM', 'population': 2417000, 'activePopulationProportion': 0.53, 'urbanPopulationProportion': 0.61, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.027755482002482415, 'hospitalBeds': 2417, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GE': {'countryCode': 'GE', 'population': 3989000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.58, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.16435748307846582, 'hospitalBeds': 7978, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'DE': {'countryCode': 'DE', 'population': 83784000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.77, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.22979689439511125, 'hospitalBeds': 670272, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GH': {'countryCode': 'GH', 'population': 31073000, 'activePopulationProportion': 0.59, 'urbanPopulationProportion': 0.56, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03499784378721076, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GI': None ,
    'GR': {'countryCode': 'GR', 'population': 10423000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.79, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.23514496785954137, 'hospitalBeds': 41692, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GL': None ,
    'GD': {'countryCode': 'GD', 'population': 113000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.36, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.10645132743362831, 'hospitalBeds': 339, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GP': {'countryCode': 'GP', 'population': 400000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.20635500000000004, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GU': None ,
    'GT': {'countryCode': 'GT', 'population': 17916000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.51, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05452199151596338, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GG': None ,
    'GN': {'countryCode': 'GN', 'population': 13133000, 'activePopulationProportion': 0.53, 'urbanPopulationProportion': 0.36, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03273166831645473, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GW': {'countryCode': 'GW', 'population': 1968000, 'activePopulationProportion': 0.54, 'urbanPopulationProportion': 0.43, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03200558943089431, 'hospitalBeds': 1968, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GY': {'countryCode': 'GY', 'population': 787000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.26, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0767420584498094, 'hospitalBeds': 787, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'HT': {'countryCode': 'HT', 'population': 11403000, 'activePopulationProportion': 0.61, 'urbanPopulationProportion': 0.55, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.056446549153731464, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'HM': None ,
    'VA': {'countryCode': 'VA', 'population': 1000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'HN': {'countryCode': 'HN', 'population': 9905000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.57, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05407672892478546, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'HK': {'countryCode': 'HK', 'population': 7497000, 'activePopulationProportion': 0.71, 'urbanPopulationProportion': 1.0, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.19647485660931036, 'hospitalBeds': 29988, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'HU': {'countryCode': 'HU', 'population': 9660000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.71, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2155302277432712, 'hospitalBeds': 67620, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'IS': {'countryCode': 'IS', 'population': 341000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.93, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.16768035190615835, 'hospitalBeds': 1023, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'IN': {'countryCode': 'IN', 'population': 1380004000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.34, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.07224416813284598, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'ID': {'countryCode': 'ID', 'population': 273524000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.55, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06927224302072213, 'hospitalBeds': 273524, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'IR': {'countryCode': 'IR', 'population': 83993000, 'activePopulationProportion': 0.6900000000000001, 'urbanPopulationProportion': 0.74, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.07235532722965007, 'hospitalBeds': 83993, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'IQ': {'countryCode': 'IQ', 'population': 40223000, 'activePopulationProportion': 0.58, 'urbanPopulationProportion': 0.7, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03764192128881485, 'hospitalBeds': 40223, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'IE': {'countryCode': 'IE', 'population': 4938000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.63, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.1555372620494127, 'hospitalBeds': 9876, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'IM': None ,
    'IL': {'countryCode': 'IL', 'population': 8656000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.92, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.13228512014787433, 'hospitalBeds': 25968, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'IT': {'countryCode': 'IT', 'population': 60462000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.7, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2453680989712547, 'hospitalBeds': 181386, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'JM': {'countryCode': 'JM', 'population': 2961000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.55, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.09825295508274232, 'hospitalBeds': 2961, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'JP': {'countryCode': 'JP', 'population': 126476000, 'activePopulationProportion': 0.59, 'urbanPopulationProportion': 0.91, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2961958395268667, 'hospitalBeds': 1644188, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'JE': None ,
    'JO': {'countryCode': 'JO', 'population': 10203000, 'activePopulationProportion': 0.61, 'urbanPopulationProportion': 0.9, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.04314858374987749, 'hospitalBeds': 10203, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KZ': {'countryCode': 'KZ', 'population': 18777000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.57, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08686776375352824, 'hospitalBeds': 112662, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KE': {'countryCode': 'KE', 'population': 53771000, 'activePopulationProportion': 0.5700000000000001, 'urbanPopulationProportion': 0.27, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.027991724163582605, 'hospitalBeds': 53771, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KI': {'countryCode': 'KI', 'population': 119000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.54, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.046630252100840326, 'hospitalBeds': 119, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KP': {'countryCode': 'KP', 'population': 25779000, 'activePopulationProportion': 0.7, 'urbanPopulationProportion': 0.61, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.10263846541758796, 'hospitalBeds': 335127, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KR': {'countryCode': 'KR', 'population': 51269000, 'activePopulationProportion': 0.72, 'urbanPopulationProportion': 0.81, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.1711017769022216, 'hospitalBeds': 563959, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'XK': None ,
    'KW': {'countryCode': 'KW', 'population': 4271000, 'activePopulationProportion': 0.75, 'urbanPopulationProportion': 1.0, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03585038632638726, 'hospitalBeds': 8542, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KG': {'countryCode': 'KG', 'population': 6524000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.36, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.053090282035561015, 'hospitalBeds': 26096, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LA': {'countryCode': 'LA', 'population': 7276000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.35, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.047087135788894986, 'hospitalBeds': 7276, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LV': {'countryCode': 'LV', 'population': 1886000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.68, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.22040986214209968, 'hospitalBeds': 9430, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LB': {'countryCode': 'LB', 'population': 6825000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.88, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08212395604395605, 'hospitalBeds': 13650, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LS': {'countryCode': 'LS', 'population': 2142000, 'activePopulationProportion': 0.62, 'urbanPopulationProportion': 0.28, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.054155462184873944, 'hospitalBeds': 2142, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LR': {'countryCode': 'LR', 'population': 5058000, 'activePopulationProportion': 0.55, 'urbanPopulationProportion': 0.51, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0366089363384737, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LY': {'countryCode': 'LY', 'population': 6871000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.8, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.049414204628147294, 'hospitalBeds': 20613, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LI': None ,
    'LT': {'countryCode': 'LT', 'population': 2722000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.67, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.21921013960323288, 'hospitalBeds': 19054, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LU': {'countryCode': 'LU', 'population': 626000, 'activePopulationProportion': 0.6900000000000001, 'urbanPopulationProportion': 0.9, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.15399520766773164, 'hospitalBeds': 2504, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MO': {'countryCode': 'MO', 'population': 649000, 'activePopulationProportion': 0.75, 'urbanPopulationProportion': 1.0, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.13238983050847455, 'hospitalBeds': 3245, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MK': {'countryCode': 'MK', 'population': 2083000, 'activePopulationProportion': 0.6900000000000001, 'urbanPopulationProportion': 0.57, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.15686269803168507, 'hospitalBeds': 8332, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MG': {'countryCode': 'MG', 'population': 27691000, 'activePopulationProportion': 0.56, 'urbanPopulationProportion': 0.37, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0344186919937886, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MW': {'countryCode': 'MW', 'population': 19130000, 'activePopulationProportion': 0.53, 'urbanPopulationProportion': 0.16, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.028976842655514905, 'hospitalBeds': 19130, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MY': {'countryCode': 'MY', 'population': 32366000, 'activePopulationProportion': 0.6900000000000002, 'urbanPopulationProportion': 0.76, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.07868522523635911, 'hospitalBeds': 32366, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MV': {'countryCode': 'MV', 'population': 541000, 'activePopulationProportion': 0.76, 'urbanPopulationProportion': 0.39, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03942698706099815, 'hospitalBeds': 2164, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'ML': {'countryCode': 'ML', 'population': 20251000, 'activePopulationProportion': 0.49, 'urbanPopulationProportion': 0.42, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0273004296084144, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MT': {'countryCode': 'MT', 'population': 442000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.94, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.22631221719457015, 'hospitalBeds': 1768, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MH': None ,
    'MQ': {'countryCode': 'MQ', 'population': 375000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.23133599999999996, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MR': {'countryCode': 'MR', 'population': 4650000, 'activePopulationProportion': 0.56, 'urbanPopulationProportion': 0.53, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.035118709677419355, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MU': {'countryCode': 'MU', 'population': 1272000, 'activePopulationProportion': 0.7000000000000001, 'urbanPopulationProportion': 0.4, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.13620833333333332, 'hospitalBeds': 3816, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'YT': {'countryCode': 'YT', 'population': 273000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.045135531135531134, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MX': {'countryCode': 'MX', 'population': 128933000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.8, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08274784578036654, 'hospitalBeds': 128933, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'FM': {'countryCode': 'FM', 'population': 115000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.22, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05008695652173914, 'hospitalBeds': 345, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MD': {'countryCode': 'MD', 'population': 4034000, 'activePopulationProportion': 0.72, 'urbanPopulationProportion': 0.42, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.1374444719881011, 'hospitalBeds': 20170, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MC': None ,
    'MN': {'countryCode': 'MN', 'population': 3278000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.68, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.04805369127516779, 'hospitalBeds': 22946, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'ME': {'countryCode': 'ME', 'population': 628000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.66, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.17023885350318474, 'hospitalBeds': 2512, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MS': {'countryCode': 'MS', 'population': 5000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MA': {'countryCode': 'MA', 'population': 36911000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.62, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08379851534772832, 'hospitalBeds': 36911, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MZ': {'countryCode': 'MZ', 'population': 31255000, 'activePopulationProportion': 0.52, 'urbanPopulationProportion': 0.35, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.031363141897296436, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MM': {'countryCode': 'MM', 'population': 54410000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.3, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06921630215034001, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NA': {'countryCode': 'NA', 'population': 2541000, 'activePopulationProportion': 0.59, 'urbanPopulationProportion': 0.5, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03939315230224321, 'hospitalBeds': 5082, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NR': None ,
    'NP': {'countryCode': 'NP', 'population': 29137000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.19, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06346614270515152, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NL': {'countryCode': 'NL', 'population': 17135000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.91, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2128484972278961, 'hospitalBeds': 68540, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NC': None ,
    'NZ': {'countryCode': 'NZ', 'population': 4822000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.86, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.17467026130236415, 'hospitalBeds': 9644, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NI': {'countryCode': 'NI', 'population': 6625000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.58, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0622680754716981, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NE': {'countryCode': 'NE', 'population': 24207000, 'activePopulationProportion': 0.47, 'urbanPopulationProportion': 0.16, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.02866951708183582, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NG': {'countryCode': 'NG', 'population': 206140000, 'activePopulationProportion': 0.53, 'urbanPopulationProportion': 0.5, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.030504521199185015, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NU': {'countryCode': 'NU', 'population': 2000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'NF': None ,
    'MP': None ,
    'NO': {'countryCode': 'NO', 'population': 5421000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.82, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.18620660394761118, 'hospitalBeds': 16263, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'OM': {'countryCode': 'OM', 'population': 5107000, 'activePopulationProportion': 0.75, 'urbanPopulationProportion': 0.84, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.02798707656158215, 'hospitalBeds': 5107, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PK': {'countryCode': 'PK', 'population': 220892000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.36, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.047625948427285736, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PW': None ,
    'PS': {'countryCode': 'PS', 'population': 5101000, 'activePopulationProportion': 0.5700000000000001, 'urbanPopulationProportion': 0.76, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03513448343462066, 'hospitalBeds': 5101, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PA': {'countryCode': 'PA', 'population': 4315000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.67, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.09207809965237544, 'hospitalBeds': 8630, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PG': {'countryCode': 'PG', 'population': 8947000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.13, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.040015759472448856, 'hospitalBeds': 35788, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PY': {'countryCode': 'PY', 'population': 7133000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.61, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.07388279826160105, 'hospitalBeds': 7133, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PE': {'countryCode': 'PE', 'population': 32972000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.77, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.09428448380444011, 'hospitalBeds': 32972, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PH': {'countryCode': 'PH', 'population': 109581000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.46, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.060647064728374445, 'hospitalBeds': 109581, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PN': None ,
    'PL': {'countryCode': 'PL', 'population': 37847000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.6, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.20170230137131082, 'hospitalBeds': 227082, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PT': {'countryCode': 'PT', 'population': 10197000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.65, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.24047111895655585, 'hospitalBeds': 30591, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'PR': {'countryCode': 'PR', 'population': 2861000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.93, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.2211786088780147, 'hospitalBeds': 8583, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'QA': {'countryCode': 'QA', 'population': 2881000, 'activePopulationProportion': 0.85, 'urbanPopulationProportion': 0.99, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.019735161402290872, 'hospitalBeds': 2881, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'RE': {'countryCode': 'RE', 'population': 895000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.13760111731843577, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'RO': {'countryCode': 'RO', 'population': 19238000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.53, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.20609143362095855, 'hospitalBeds': 115428, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'RU': {'countryCode': 'RU', 'population': 145934000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.74, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.1682757547932627, 'hospitalBeds': 1167472, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'RW': {'countryCode': 'RW', 'population': 12952000, 'activePopulationProportion': 0.5700000000000001, 'urbanPopulationProportion': 0.17, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03466337245213094, 'hospitalBeds': 12952, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'BL': {'countryCode': 'BL', 'population': 10000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SH': {'countryCode': 'SH', 'population': 6000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'KN': None ,
    'LC': {'countryCode': 'LC', 'population': 184000, 'activePopulationProportion': 0.71, 'urbanPopulationProportion': 0.18, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.11080978260869566, 'hospitalBeds': 184, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'MF': None ,
    'PM': {'countryCode': 'PM', 'population': 6000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'VC': {'countryCode': 'VC', 'population': 111000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.52, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.10750450450450452, 'hospitalBeds': 222, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'WS': {'countryCode': 'WS', 'population': 198000, 'activePopulationProportion': 0.56, 'urbanPopulationProportion': 0.18, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05614141414141415, 'hospitalBeds': 198, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SM': None ,
    'ST': {'countryCode': 'ST', 'population': 219000, 'activePopulationProportion': 0.54, 'urbanPopulationProportion': 0.72, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03350228310502284, 'hospitalBeds': 438, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SA': {'countryCode': 'SA', 'population': 34814000, 'activePopulationProportion': 0.71, 'urbanPopulationProportion': 0.83, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03893910495777561, 'hospitalBeds': 69628, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SN': {'countryCode': 'SN', 'population': 16744000, 'activePopulationProportion': 0.53, 'urbanPopulationProportion': 0.47, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.034169493549928334, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'RS': {'countryCode': 'RS', 'population': 8737000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.56, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.20370664987982146, 'hospitalBeds': 43685, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SC': {'countryCode': 'SC', 'population': 98000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.56, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08942857142857144, 'hospitalBeds': 294, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SL': {'countryCode': 'SL', 'population': 7977000, 'activePopulationProportion': 0.55, 'urbanPopulationProportion': 0.42, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03226601479252852, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SG': {'countryCode': 'SG', 'population': 5850000, 'activePopulationProportion': 0.76, 'urbanPopulationProportion': 1.0, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.14782803418803417, 'hospitalBeds': 11700, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SX': None ,
    'SK': {'countryCode': 'SK', 'population': 5460000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.53, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.18007893772893774, 'hospitalBeds': 27300, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SI': {'countryCode': 'SI', 'population': 2079000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.54, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.22137181337181336, 'hospitalBeds': 8316, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SB': {'countryCode': 'SB', 'population': 687000, 'activePopulationProportion': 0.56, 'urbanPopulationProportion': 0.23, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.040113537117903934, 'hospitalBeds': 687, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SO': {'countryCode': 'SO', 'population': 15893000, 'activePopulationProportion': 0.5, 'urbanPopulationProportion': 0.44, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03201547851255269, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'ZA': {'countryCode': 'ZA', 'population': 59309000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.66, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06058500396229915, 'hospitalBeds': 118618, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GS': None ,
    'SS': None ,
    'ES': {'countryCode': 'ES', 'population': 46755000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.8, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.21135401561330344, 'hospitalBeds': 140265, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'LK': {'countryCode': 'LK', 'population': 21413000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.18, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.12199159389156118, 'hospitalBeds': 64239, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SD': {'countryCode': 'SD', 'population': 43849000, 'activePopulationProportion': 0.55, 'urbanPopulationProportion': 0.34, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.040322515906862186, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SR': {'countryCode': 'SR', 'population': 587000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.66, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.07759795570698468, 'hospitalBeds': 1761, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SJ': None ,
    'SZ': {'countryCode': 'SZ', 'population': 1160000, 'activePopulationProportion': 0.5700000000000001, 'urbanPopulationProportion': 0.23, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.04334827586206898, 'hospitalBeds': 2320, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SE': {'countryCode': 'SE', 'population': 10099000, 'activePopulationProportion': 0.62, 'urbanPopulationProportion': 0.87, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.21408812753737994, 'hospitalBeds': 20198, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'CH': {'countryCode': 'CH', 'population': 8655000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.73, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.20232131715771232, 'hospitalBeds': 34620, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'SY': {'countryCode': 'SY', 'population': 17501000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.54, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.053564482029598307, 'hospitalBeds': 17501, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TW': {'countryCode': 'TW', 'population': 23817000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.17193731368350337, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TJ': {'countryCode': 'TJ', 'population': 9538000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.27, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03606951142797232, 'hospitalBeds': 38152, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TZ': {'countryCode': 'TZ', 'population': 59734000, 'activePopulationProportion': 0.53, 'urbanPopulationProportion': 0.33, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.029215756520574544, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TH': {'countryCode': 'TH', 'population': 69800000, 'activePopulationProportion': 0.71, 'urbanPopulationProportion': 0.49, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.14090723495702007, 'hospitalBeds': 139600, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TL': {'countryCode': 'TL', 'population': 1318000, 'activePopulationProportion': 0.5700000000000001, 'urbanPopulationProportion': 0.3, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.046722306525037935, 'hospitalBeds': 6590, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TG': {'countryCode': 'TG', 'population': 8279000, 'activePopulationProportion': 0.55, 'urbanPopulationProportion': 0.41, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.03221403551153521, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TK': {'countryCode': 'TK', 'population': 1000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TO': {'countryCode': 'TO', 'population': 106000, 'activePopulationProportion': 0.58, 'urbanPopulationProportion': 0.23, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.06412264150943395, 'hospitalBeds': 212, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TT': {'countryCode': 'TT', 'population': 1399000, 'activePopulationProportion': 0.68, 'urbanPopulationProportion': 0.53, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.12508220157255182, 'hospitalBeds': 4197, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TN': {'countryCode': 'TN', 'population': 11819000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.68, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.09712919874777898, 'hospitalBeds': 23638, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TR': {'countryCode': 'TR', 'population': 84339000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.75, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.09732689503076869, 'hospitalBeds': 168678, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TM': {'countryCode': 'TM', 'population': 6031000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.51, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05349693251533742, 'hospitalBeds': 42217, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'TC': None ,
    'TV': None ,
    'UG': {'countryCode': 'UG', 'population': 45741000, 'activePopulationProportion': 0.51, 'urbanPopulationProportion': 0.23, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.02202872696268118, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'UA': {'countryCode': 'UA', 'population': 43734000, 'activePopulationProportion': 0.67, 'urbanPopulationProportion': 0.69, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.1825051447386473, 'hospitalBeds': 349872, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'AE': {'countryCode': 'AE', 'population': 9890000, 'activePopulationProportion': 0.84, 'urbanPopulationProportion': 0.86, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.015157431749241659, 'hospitalBeds': 9890, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'GB': {'countryCode': 'GB', 'population': 67886000, 'activePopulationProportion': 0.63, 'urbanPopulationProportion': 0.83, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.19727496096396904, 'hospitalBeds': 135772, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'US': {'countryCode': 'US', 'population': 331003000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.82, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.17824813068159504, 'hospitalBeds': 662006, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'UM': None ,
    'UY': {'countryCode': 'UY', 'population': 3474000, 'activePopulationProportion': 0.64, 'urbanPopulationProportion': 0.95, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.16053396660909613, 'hospitalBeds': 6948, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'UZ': {'countryCode': 'UZ', 'population': 33469000, 'activePopulationProportion': 0.66, 'urbanPopulationProportion': 0.5, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.05396109832979772, 'hospitalBeds': 133876, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'VU': {'countryCode': 'VU', 'population': 307000, 'activePopulationProportion': 0.5700000000000001, 'urbanPopulationProportion': 0.25, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.039921824104234525, 'hospitalBeds': 307, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'VE': {'countryCode': 'VE', 'population': 28436000, 'activePopulationProportion': 0.65, 'urbanPopulationProportion': 0.88, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.08715842593895062, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'VN': {'countryCode': 'VN', 'population': 97339000, 'activePopulationProportion': 0.69, 'urbanPopulationProportion': 0.35, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0865622206926309, 'hospitalBeds': 194678, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'VG': None ,
    'VI': {'countryCode': 'VI', 'population': 104000, 'activePopulationProportion': 0.6, 'urbanPopulationProportion': 0.95, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.21955769230769234, 'hospitalBeds': 1872, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'WF': {'countryCode': 'WF', 'population': 11000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': None, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'EH': {'countryCode': 'EH', 'population': 597000, 'activePopulationProportion': None, 'urbanPopulationProportion': None, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.039010050251256284, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'YE': {'countryCode': 'YE', 'population': 29826000, 'activePopulationProportion': 0.57, 'urbanPopulationProportion': 0.36, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.0323380607523637, 'hospitalBeds': None, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'ZM': {'countryCode': 'ZM', 'population': 18384000, 'activePopulationProportion': 0.52, 'urbanPopulationProportion': 0.43, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.023562336814621408, 'hospitalBeds': 36768, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} ,
    'ZW': {'countryCode': 'ZW', 'population': 14863000, 'activePopulationProportion': 0.54, 'urbanPopulationProportion': 0.32, 'urbanPopulationInDegradedHousingProportion': None, 'over64Proportion': 0.033074614815313194, 'hospitalBeds': 14863, 'highContactPopulation': None, 'remoteAreasPopulationProportion': None} 
    }
