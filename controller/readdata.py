import csv
import pandas as pd


def read_csv(filename):
    data = {}
    with open(filename, "r") as file:
        csv_reader = csv.reader(file, delimiter=";")
        headers = next(csv_reader)  # Baca baris pertama sebagai header
        date_keys = headers[2:]  # Ambil tanggal-tanggal dari indeks ke-2 hingga akhir
        for row in csv_reader:
            region = row[1]
            values = row[2:]  # Ambil nilai dari kolom ketiga hingga akhir
            data[region] = values
    return data, date_keys


def read_data(keys):
    filename = "alldata.csv"
    csv_data, date_keys = read_csv(filename)
    return date_keys, csv_data[keys]


filename = "alldata.csv"
csv_data, date_keys = read_csv(filename)

if __name__ == "__main__":
    for i in csv_data.keys():
        readdata = read_data(i)
        print(f"Data : {i} , Panjang data : {len(readdata[1])}")

#! my keys

# * 'Indonesia'
# * 'Aceh'
# * 'Bali'
# * 'Banten'
# * 'Bengkulu'
# * 'DI Yogyakarta'
# * 'DKI Jakarta'
# * 'Gorontalo'
# * 'Jambi'
# * 'Jawa Barat'
# * 'Jawa Tengah'
# * 'Jawa Timur'
# * 'Kalimantan Barat'
# * 'Kalimantan Selatan'
# * 'Kalimantan Tengah'
# * 'Kalimantan Timur'
# * 'Kalimantan Utara'
# * 'Kepulauan Bangka Belitung'
# * 'Kepulauan Riau'
# * 'Lampung'
# * 'Maluku'
# * 'Maluku Utara'
# * 'Nusa Tenggara Barat'
# * 'Nusa Tenggara Timur'
# * 'Papua'
# * 'Papua Barat'
# * 'Riau'
# * 'Sulawesi Barat'
# * 'Sulawesi Selatan'
# * 'Sulawesi Tengah'
# * 'Sulawesi Tenggara'
# * 'Sulawesi Utara'
# * 'Sumatera Barat'
# * 'Sumatera Selatan'
# * 'Sumatera Utara'
