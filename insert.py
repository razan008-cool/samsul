import pymongo  # meng-import library pymongo yang sudah kita install

client = pymongo.MongoClient("MASUKAN ID KALIAN")  
db = client['MyDatabase']  # ganti sesuai dengan nama database kalian
my_collections = db['MyCollection']  # ganti sesuai dengan nama collections kalian

# Data yang ingin dimasukkan
murid_1 = {'nama': 'John Doe', 'Jurusan': 'IPS', 'Nilai': 90}
murid_2 = {'nama': 'Jane Doe', 'Jurusan': 'IPA', 'Nilai': 85}

results = my_collections.insert_many([murid_1, murid_2])
print(results.inserted_ids)  # akan menghasilkan ID dari data yang kita masukkan

#get_result = my_collections.find()
#for x in get_result
    #print