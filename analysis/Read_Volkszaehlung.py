__author__ = 'Jonas I Liechti'
import csv
import pickle

year = '2000'

with open('Data/Volkszaehlungen/Volkszaehlung_' + year + '.csv', 'rb') as csv_f:
    dialect = csv.Sniffer().sniff(csv_f.read(1024))
    csv_f.seek(0)
    spamreader = csv.reader(csv_f, dialect)
    #spamreader = csv.reader(csv_f, delimiter=' ', quotechar='|')
    cantons = []
    per_cantons = []
    districts = []
    per_districts = []
    for row in spamreader:
        if len(row):
            #print ', '.join(row)
            if '- Kanton' in row[0]:
                cantons.append(row[0].replace('- Kanton ', ''))
                per_cantons.append(int(row[1]))
            elif '......' in row[0]:
                districts.append(' '.join(row[0].split(' ')[1:]))
                if row[1] != '...':
                    per_districts.append(int(row[1]))
                else:
                    per_districts.append(0)
#fix the names
cantons = map(lambda x: unicode(x.decode("ISO-8859_1")), cantons)
districts = map(lambda x: unicode(x.decode("ISO-8859_1")), districts)
print cantons
print per_cantons
print districts
print per_districts

with open('pickles/VZ_data/' + year + '_district_names.p', 'w') as p_f:
    pickle.dump(districts, p_f)
with open('pickles/VZ_data/' + year + '_district_counts.p', 'w') as p_f:
    pickle.dump(per_districts, p_f)
with open('pickles/VZ_data/' + year + '_canton_names.p', 'w') as p_f:
    pickle.dump(cantons, p_f)
with open('pickles/VZ_data/' + year + '_canton_counts.p', 'w') as p_f:
    pickle.dump(per_cantons, p_f)
