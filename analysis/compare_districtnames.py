__author__ = 'Jonas I Liechti'
import pickle
from distance import levenshtein

year = 1900
mapping = {}
replacing = {}
mapping['Biel (BE)'] = 'BielBienne'
replacing['Saas '] = 'Saas-'

with open('pickles/VZ_data/' + str(year) + '_district_names.p', 'r') as p_f:
    vz_names = pickle.load(p_f)
with open('pickles/map/district_names.p', 'r') as p_f:
    map_names = pickle.load(p_f)

map_names = map(lambda x: unicode(x), map_names)
#vz_names = map(lambda x: unicode(x.decode("ISO-8859_1")), vz_names)
out_counter = 0
out_districts = []
ok_districts = []
vz_names.sort()
for vz_name in vz_names:
    if vz_name in map_names:
        ok_districts.append(vz_name)
        #print 'IN: ', "'"+vz_name+"'"
    else:
        if '/' in vz_name:
            if vz_name.replace('/', '') in map_names:
                ok_districts.append(vz_name)
            else:
                out_counter += 1
                out_districts.append(vz_name)
                dists = [levenshtein(vz_name, map_names[i]) for i in xrange(len(map_names))]
                print
                #print 'OUT:', "'"+vz_name+"'", map_names[dists.index(min(dists))]
        elif 'Saas ' in vz_name:
            if vz_name.replace('Saas ', 'Saas-') in map_names:
                ok_districts.append(vz_name)
            else:
                out_counter += 1
                out_districts.append(vz_name)
                dists = [levenshtein(vz_name, map_names[i]) for i in xrange(len(map_names))]
                print
                #print 'OUT:', "'"+vz_name+"'", map_names[dists.index(min(dists))]
        elif vz_name in mapping:
            if mapping[vz_name] in map_names:
                ok_districts.append(vz_name)
            else:
                out_counter += 1
                out_districts.append(vz_name)
                dists = [levenshtein(vz_name, map_names[i]) for i in xrange(len(map_names))]
                print
                #print 'OUT:', "'"+vz_name+"'", map_names[dists.index(min(dists))]
        else:
            out_counter += 1
            out_districts.append(vz_name)
            #dists = [levenshtein(vz_name, map_names[i]) for i in xrange(len(map_names))]
            #print 'OUT:', "'"+vz_name+"'", #map_names[dists.index(min(dists))]

with open('pickles/mapping_' + str(year) + '_district_names.p', 'wb') as f:
    pickle.dump(mapping, f)
lakes = filter(lambda x: 'see' in x, map_names)
lakes.extend([u'Thunersee', u'Brienzersee'])
lakes.extend([u'Lac L\xe9man (VD)', u'Lac de Neuch\xe2tel (NE)', u'Lac de Neuch\xe2tel (VD)',
              u'Lac de Neuch\xe2tel (FR)', u'Lac L\xe9man (GE)', u'Lac de Neuch\xe2tel (VD)',
              u'Lac de Neuch\xe2tel (FR)', u'Lac L\xe9man (VD)', u'Lac L\xe9man (VS)', u'Lac de la Gruy\xe8re',
              u'Lac de Joux', u'Lac de Neuch\xe2tel (VD)', u'Lac L\xe9man (GE)', u'Lac de Neuch\xe2tel (BE)',
              u'Lac de Neuch\xe2tel (VD)'])
lakes.extend([u'Lago Maggiore', u'Lago di Lugano', u"Campione d'Italia (IT) (Lago)"])
ok_districts.extend(filter(lambda x: 'see ' in x, map_names))
ok_districts.extend(lakes)


with open('pickles/matched_' + str(year) + '_district_names.p', 'wb') as f:
    pickle.dump(ok_districts, f)

print 'missmatches', out_counter
out_districts.sort()
for o_d in out_districts:
    print o_d
missing_map_names = filter(lambda x: x not in ok_districts, map_names)
print len(missing_map_names)
print missing_map_names
#print vz_names[-2], map_names[map_names.index(u'Seleute')]
map_names.sort()
vz_names.sort()
comb = zip(map_names, vz_names)

#print map_names
#print vz_names
#print filter(lambda x: x[0] != x[1], comb)
#print filter(lambda x: 'see ' in x, map_names)
#for i in xrange(len(map_names)):
#    print i, map_names[i]