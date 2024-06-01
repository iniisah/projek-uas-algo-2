import os
import datetime
import tabulate
import csv
from time import sleep
import pandas as pd


def fungsi_awal():
    print('='*100)
    print("||                     //                SELAMAT DATANG                    \\\\                       ||")
    print("||                    |||           Program Manajemen Laundry              |||                      ||")
    print("||                      \\\\                                              //                        ||")
    print('='*100)
    sleep(0.5)
    print("\nApakah anda sudah membuat akun?")
    while True:
        ipt = input("ya/tidak: ").lower()
        if ipt == 'ya':
            sign_in()
            break
        elif ipt == "tidak":
            sign_up()
            break
        else:
            print('\n>>> Masukkan jawaban yang benar! <<<\n')
            continue

#fungsi login dan register
def sign_in():
    os.system('cls' if os.name == 'nt' else 'clear')
    df = pd.read_csv('admin.csv')
    print('-------------------- SIGN IN --------------------\n')

    while True:
        username = input("Masukkan Username: ")
        password = int(input("Masukkan Password (angka): "))
        indeks = (df['Username'] == id).idxmax()
        if username in df['Username'].values and password in df['Password'].values:
            user_index = df.index[df['Username'] == username].tolist()[0]
            if df.loc[user_index, 'Password'] == password:
                menu()
                break
            else:
                print('\n>>> Password anda salah! <<<\n')
                continue
        else:
            print('\n>>> Username tidak ditemukan <<<\n')

def sign_up():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('-------------------- SIGN UP --------------------\n')
    nama = input("Masukkan Nama: ")
    while True:
        username = input("Masukkan Username yang ingin digunakan: ")
        try:
            df = pd.read_csv('admin.csv')
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Nama', 'Username', 'Password'])

        if username in df['Username'].values:
            print('\n*** Username telah digunakan, masukkan username yang lain! ***\n')
            continue
        password = int(input("Masukkan Password yang ingin digunakan (angka): "))
        
        new_entry = pd.DataFrame([[nama, username, password]], columns=['Nama', 'Username', 'Password'])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv('admin.csv', index=False)

        while True:
            verif = int(input("Masukkan kembali Password yang ingin digunakan (angka): "))
            if password == verif:
                print("\nData anda sedang diproses.....")
                sleep(2)
                print('-'*57)
                print('         Anda berhasil mendaftar! Silahkan login         ')
                print('-'*57)
                sleep(2.5)
                sign_in()
                break
            else:
                print("\n>>> Password anda salah, silahkan masukkan kembali password anda! <<<\n")
                continue

    
# fungsi menu
def menu ():
    os.system('cls')
    print("""
=========================================================================
|                     _   _   _____   __  _   _   _                     |
|     ______         | \_/ | | ____| |  \| | | | | |         ______     |
|     ******         |  _  | | __|_  |  _  | | |_| |         ******     |
|                    |_| |_| |_____| |_| |_|  \___/                     |
|                               M E N U                                 |
=========================================================================
silahkan pilih menu :
1. input data
2. edit data
3. cari data
4. Keluar
          """)
    while True :
        pilihan = input("Pilih menu(1/2/3/4) : ")
        if pilihan == '1' :
            input_data()
            break
        elif pilihan == '2' :
            edit_data()
            break
        elif pilihan == '3' :
            cari_data()
            break
        #elif pilihan == '4' :
        #    keluar()
        #    break
        else :
            print(f' >>> {pilihan} tidak ada di pilihan <<< ')
            continue

#fungsi input data
def input_data():
    os.system('cls' if os.name == 'nt' else 'clear')
    nama = input("Masukkan nama pelanggan: ")
    no_hp = int(input("Masukkan nomor handphone pelanggan: "))
    tanggal_masuk = datetime.date.today()

    data = pd.read_csv('jasa.csv')

    print(tabulate.tabulate(data, headers=["id", "jenis", "lama pengerjaan", "harga"], tablefmt="grid", showindex=False))

    while True:
        id_selected = input("Masukkan ID Layanan (1-9): ")
        if id_selected not in map(str, data['id'].tolist()):
            print(f'>>> {id_selected} tidak ada di pilihan. Silakan coba lagi. <<<')
            continue
        else:
            selected_service = data[data['id'] == int(id_selected)]
            berat = float(input("Masukkan Berat / kg: "))

            harga_per_kg = selected_service['harga'].values[0]
            lama_pengerjaan = int(selected_service['lama pengerjaan'].values[0])
            total_harga = berat * harga_per_kg
            jenis_layanan = selected_service['jenis'].values[0]

            tanggal_diambil = tanggal_masuk + datetime.timedelta(days=lama_pengerjaan)

            summary = [
                ["Nama Pelanggan", nama],
                ["Nomor HP", no_hp],
                ["Tanggal Masuk", tanggal_masuk],
                ["Tanggal Diambil", tanggal_diambil],
                ["Jenis Layanan", jenis_layanan],
                ["Berat (kg)", berat],
                ["Harga per kg", harga_per_kg],
                ["Total Harga", int(total_harga)],
                ["Status", "belum selesai"]
            ]

            data_to_append = pd.DataFrame({
                'Nama Pelanggan': [nama],
                'Nomor HP': [no_hp],
                'Tanggal Masuk': [tanggal_masuk],
                'Tanggal Diambil': [tanggal_diambil],
                'Jenis Layanan': [jenis_layanan],
                'Berat (kg)': [berat],
                'Harga per kg': [harga_per_kg],
                'Total Harga': [total_harga],
                'Status': ['belum selesai']
            })

            with open('nota.csv', mode='a', newline='') as file:
                data_to_append.to_csv(file, header=not os.path.exists('nota.csv'), index=False)

            print("Data berhasil ditambahkan!")
            sleep(1)

            print(" ================= NOTA ================= ")
            print(tabulate.tabulate(summary, headers=["Keterangan", "Detail"], tablefmt="grid"))
            while True:
                tanya = input("Apakah anda ingin kembali ke menu?(ya/tidak) : ").lower()
                if tanya == 'ya':
                    menu()
                    break
                elif tanya == 'tidak':
                    break
                else:
                    print("berikan jawaban yang benar!")
                    continue
            break

#fungsi cari data(bukan fitur)                                  
def cari_data():
    def merge_sort(df, col):
        if len(df) > 1:
            mid = len(df) // 2
            left_half = df.iloc[:mid].copy()
            right_half = df.iloc[mid:].copy()

            merge_sort(left_half, col)
            merge_sort(right_half, col)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half.iloc[i][col] < right_half.iloc[j][col]:
                    df.iloc[k] = left_half.iloc[i]
                    i += 1
                else:
                    df.iloc[k] = right_half.iloc[j]
                    j += 1
                k += 1

            while i < len(left_half):
                df.iloc[k] = left_half.iloc[i]
                i += 1
                k += 1

            while j < len(right_half):
                df.iloc[k] = right_half.iloc[j]
                j += 1
                k += 1

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('-------------------- CARI DATA --------------------\n')

        try:
            df = pd.read_csv('nota.csv', dtype={'NomorHP': int}) 
        except FileNotFoundError:
            print("File nota.csv tidak ditemukan.")
            return

        merge_sort(df, 'NomorHP')

        nomor_hp = int(input("Masukkan nomor handphone pelanggan: ").strip()) 

        left = 0
        right = len(df) - 1
        found = False
        while left <= right:
            mid = (left + right) // 2
            if df.loc[mid, 'NomorHP'] == nomor_hp:
                found = True
                break
            elif df.loc[mid, 'NomorHP'] < nomor_hp:
                left = mid + 1
            else:
                right = mid - 1

        if found:
            print("\nData ditemukan:")
            print(tabulate.tabulate(df.loc[[mid]], headers='keys', tablefmt='grid'))
        else:
            print("\nData tidak ditemukan untuk nomor handphone tersebut.")

        while True:
            tanya = input("Apakah anda ingin mencari data lagi? (ya/tidak): ").strip().lower()
            if tanya == 'ya':
                cari_data()
                break  
            elif tanya == 'tidak':
                menu()  
                break
            else:
                print("Jawaban tidak valid. Silakan coba lagi.")
                continue


#fungsi edit data(ubah status, tambah data, edit data)
def edit_data():
    def merge_sort(df, col):
        if len(df) > 1:
            mid = len(df) // 2
            left_half = df.iloc[:mid].copy()
            right_half = df.iloc[mid:].copy()

            merge_sort(left_half, col)
            merge_sort(right_half, col)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half.iloc[i][col] < right_half.iloc[j][col]:
                    df.iloc[k] = left_half.iloc[i]
                    i += 1
                else:
                    df.iloc[k] = right_half.iloc[j]
                    j += 1
                k += 1

            while i < len(left_half):
                df.iloc[k] = left_half.iloc[i]
                i += 1
                k += 1

            while j < len(right_half):
                df.iloc[k] = right_half.iloc[j]
                j += 1
                k += 1

    #sub menu --> tambah data
    def tambah_data_jasa(df):
        print('\n----- TAMBAH DATA JASA -----\n')
        id_jasa = input("Masukkan ID Jasa: ").strip()
        jenis = input("Masukkan Jenis Jasa: ").strip()
        lama_pengerjaan = input("Masukkan Lama Pengerjaan (hari): ").strip()
        harga = input("Masukkan Harga (per kg): ").strip()

        new_data = pd.DataFrame([[id_jasa, jenis, lama_pengerjaan, harga]], columns=df.columns)
        df = df.append(new_data, ignore_index=True)
        df.to_csv('jasa.csv', index=False)
        print("Data jasa berhasil ditambahkan.")

    #sub menu --> edit data
    def edit_data_jasa(df):
        print('\n----- EDIT DATA JASA -----\n')
        print(tabulate.tabulate(df, headers='keys', tablefmt='grid', showindex=False)) 
        while True:
            id_jasa = input("Masukkan ID Jasa yang ingin diedit: ").strip()

            if id_jasa in df['id'].astype(str).values: 
                kolom = input("Masukkan nama kolom yang ingin diubah (jenis/lama pengerjaan/harga): ").strip().lower()

                if kolom in df.columns:
                    new_value = int(input(f"Masukkan nilai baru untuk kolom '{kolom}': "))
                    df.loc[df['id'].astype(str) == id_jasa, kolom] = new_value  
                    df.to_csv('jasa.csv', index=False)
                    print("Data jasa berhasil diubah.")
                    while True:
                        tanya = input("Apakah anda ingin kembali ke menu? (ya/tidak): ").strip().lower()
                        if tanya == 'ya':
                            edit_data()
                            return
                        elif tanya == 'tidak':
                            return
                        else:
                            print("Jawaban tidak valid. Silakan coba lagi.")
                else:
                    print("Kolom tidak valid.")
            else:
                print("ID Jasa tidak ditemukan.")


    os.system('cls' if os.name == 'nt' else 'clear')
    print('-------------------- MENU --------------------\n')
    print('1. Ubah Status Pesanan')
    print('2. Edit Data Jasa')
    print('3. Tambah Data Jasa')
    print('4. Kembali')

    choice = input("Masukkan pilihan menu: ").strip()

    if choice == '1':
        #sub menu --> ubah status
        print('\n-------------------- UBAH STATUS PESANAN --------------------\n')
        try:
            df = pd.read_csv('nota.csv', dtype={'NomorHP': int}) 
        except FileNotFoundError:
            print("File nota.csv tidak ditemukan.")
            return

        merge_sort(df, 'NomorHP')

        nomor_hp = int(input("Masukkan nomor handphone pelanggan: ").strip())
        left = 0
        right = len(df) - 1
        found = False
        while left <= right:
            mid = (left + right) // 2
            if df.loc[mid, 'NomorHP'] == nomor_hp:
                found = True
                break
            elif df.loc[mid, 'NomorHP'] < nomor_hp:
                left = mid + 1
            else:
                right = mid - 1

        if found:
            if df.loc[mid, 'status'] == 'belum selesai':
                confirm = input("Apakah Anda ingin mengubah status pesanan menjadi selesai? (ya/tidak): ").strip().lower()
                if confirm == 'ya':
                    new_status = 'selesai'
                    df.loc[mid, 'status'] = new_status
                    df.to_csv('nota.csv', index=False)
                    print("Status berhasil diperbarui.")
                else:
                    print("Status pesanan tidak diubah.")
            else:
                print("Status pesanan telah selesai sebelumnya.")
        else:
            print("\nData tidak ditemukan untuk nomor handphone tersebut.")

        while True:
            tanya = input("Apakah anda ingin kembali ke menu? (ya/tidak): ").strip().lower()
            if tanya == 'ya':
                edit_data()
                break  
            elif tanya == 'tidak':
                menu()  
                return
            else:
                print("Jawaban tidak valid. Silakan coba lagi.") 

    elif choice == '2':
        try:
            df_jasa = pd.read_csv('jasa.csv')
        except FileNotFoundError:
            print("File jasa.csv tidak ditemukan.")
            return

        print("Data Jasa yang Tersedia:")
        print(df_jasa)
        edit_data_jasa(df_jasa)
    elif choice == '3':
        try:
            df_jasa = pd.read_csv('jasa.csv')
        except FileNotFoundError:
            print("File jasa.csv tidak ditemukan.")
            return

        tambah_data_jasa(df_jasa)

    elif choice == '4' :
        menu()

    else:
        print("Pilihan tidak valid.")

#fungsi keluar --> fitur untuk keluar
def keluar() :
    tanya = input('Apakah anda yakin ingin keluar dari program? (ya/tidak) : ').lower()
    while True :
        if tanya == 'ya' :
            break
        elif tanya == 'tidak' :
            menu()
            break
    



fungsi_awal()


#
#def nota():
#    no_hp = input("Masukkan nomor HP pelanggan yang ingin dicetak notanya: ")
#    with open('pelanggan.csv', 'r') as file:
#        reader = csv.DictReader(file)
#        found = False
#        for data in reader:
#            if data['no_hp'] == no_hp:
#                found = True
#                print("========== NOTA ==========")
#                print(f"Nama: {data['nama']}")
#                print(f"Nomor HP: {data['no_hp']}")
#                print(f"Tanggal Masuk: {data['tanggal_masuk']}")
#                print(f"Tanggal Ambil: {data['tanggal_ambil']}")
#                print(f"Alamat: {data['alamat']}")
#                print(f"Jenis Laundry: {data['jenis']}")
#                print(f"Kecepatan: {data['kecepatan']}")
#                print(f"Berat: {data['berat']} kg")
#                print(f"Harga: Rp {data['harga']}")
#                print(f"Status: {data['status']}")
#                print("==========================")
#                break
#        if not found:
#            print(f"Nomor HP {no_hp} tidak ditemukan dalam database.")
#    menu() 
#



#def edit_data() :
#    db = 'pelanggan.csv'
#    with open (db, 'r')as file :
#        csvr = csv.reader(file)
#
#    while True :
#        no_hp = input("Masukkan no HP :")
#        if no_hp in db['nomor hp']:
#                tanya=(f"Selesaikan pesanan?(Ya/Tidak):").lower()
#                if tanya == 'ya':
#                    data['status']= 'Selesai'
#                    print(f"Status pesanan untuk {data['nama']}  telah diperbaharui menjadi'Selesai'.")
#                    break
#                elif tanya ==" tidak":
#                    print(f"Status pesanan Belum Selesai")
#                else:
#                    print(f"{tanya} tidak ada dalam pilihan")
#        
#
#        if not found:
#            print(f"Nomor Hp{no_hp} tidak ditemukan dalam database")
#            break
#        menu()    
#               
# 
# 