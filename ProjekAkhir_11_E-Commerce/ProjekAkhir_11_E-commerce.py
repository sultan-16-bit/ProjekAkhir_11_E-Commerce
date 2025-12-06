import datetime

def utama():
    print("==== SELAMAT DATANG DI SAMURAI STORE ====\n")
    print("> Pilih mode User atau Admin <\n")

    pins = {"user": "2501", "admin": "2569"}

    saldo = {"admin": 500000, "user": 200000}

    pulsa = {"telkomsel": [], "indosat": [], "xl": [], "tri": [], "axis": []}
    ewallet = {"dana": [], "ovo": [], "gopay": [], "shopeepay": []}
    token = {"Token PLN": []}

    biaya_admin_pulsa = {op: 2000 for op in pulsa}
    biaya_admin_ewallet = {e: 2000 for e in ewallet}
    biaya_admin_token = 2000

    voucher = {"HEMAT10": 10, "DISKON20": 20}

    riwayat_user = []
    riwayat_admin = []
    permintaan_topup = []

    def minta_pin(prompt):
        while True:
            p = input(prompt).strip()
            if len(p) == 4 and p.isdigit():
                return p
            print("PIN harus 4 digit angka!")

    def minta_nomor(prompt):
        while True:
            n = input(prompt).strip()
            if n.isdigit() and 11 <= len(n) <= 12:
                return n
            print("Nomor / ID harus angka dan 11-12 digit!")

    def minta_nominal(prompt):
        while True:
            n = input(prompt).strip()
            if not n.isdigit():
                print("Nominal harus angka!")
                continue
            n = int(n)
            if n < 20000:
                print("Minimal nominal Rp20.000!")
            elif n > 1000000:
                print("Maksimal nominal Rp1.000.000!")
            else:
                return n

    def cetak_struk(detail):
        tgl = detail.get("tanggal", datetime.datetime.now())
        print("\n===== STRUK PEMBAYARAN =====")
        print("Tanggal      :", tgl.strftime("%d/%m/%Y %H:%M:%S"))
        print("Produk       :", detail.get("produk", "-"))
        if "nominal" in detail:
            print("Nominal      :", detail.get("nominal"))
        if "tujuan" in detail:
            print("Tujuan       :", detail.get("tujuan"))
        if detail.get("kode_voucher"):
            print(f"Voucher      : {detail.get('kode_voucher')} (Diskon {detail.get('diskon_pct',0)}%)")
        else:
            print("Voucher      : Tidak memakai kupon")
        print("Biaya Admin  : Rp", detail.get("biaya_admin", 0))
        print("Total Bayar  : Rp", detail.get("total_bayar"))
        print("Saldo Akhir  : Rp", detail.get("saldo_akhir"))
        print("=============================\n")

    def lihat_produk_user():
        while True:
            print("\n=== LIHAT PRODUK ===")
            print("1. Pulsa")
            print("2. E-Wallet")
            print("3. Token PLN")
            pilih = input("Pilih: ").strip()
            if pilih == "1":
                print("\nOperator Pulsa:")
                for op in pulsa:
                    print("-", op.title())
            elif pilih == "2":
                print("\nE-Wallet:")
                for e in ewallet:
                    print("-", e.title())
            elif pilih == "3":
                print("\nToken PLN tersedia.")
            else:
                print("Pilihan tidak valid!")
            while True:
                ulang = input("Lihat lagi? (y/n): ").strip().lower()
                if ulang in ("y","n"):
                    break
                print("Masukkan 'y' atau 'n'!")
            if ulang == "n":
                break

    def menu_user():
        while True:
            print("\n=== MENU USER ===")
            print("1. Lihat Produk")
            print("2. Beli Produk")
            print("3. Ajukan Top Up")
            print("4. Lihat Saldo")
            print("5. Ganti PIN User")
            print("6. Riwayat Transaksi")
            print("7. Logout")
            pilih = input("Pilih: ").strip()
            if pilih == "1":
                lihat_produk_user()

            elif pilih == "2":
                print("\n=== BELI PRODUK ===")
                print("1. Pulsa")
                print("2. E-Wallet")
                print("3. Token PLN")
                while True:
                    kat = input("Pilih (1-3): ").strip()
                    if kat in ("1","2","3"):
                        break
                    print("Input hanya 1, 2, atau 3!")

                if kat == "1":
                    # Pulsa
                    print("\nOperator tersedia:")
                    for op in pulsa:
                        print("-", op.title())
                    while True:
                        op = input("Masukkan operator: ").lower().strip()
                        if op in pulsa:
                            break
                        print("Operator tidak ditemukan!")
                    nominal = minta_nominal("Masukkan nominal (20k-1jt): ")
                    tujuan = minta_nomor("Masukkan nomor tujuan (11-12 digit): ")
                    biaya_admin = biaya_admin_pulsa.get(op, 2000)
                    total = nominal + biaya_admin

                    kode = input("Kode voucher (enter jika tidak ada): ").strip().upper()
                    diskon_pct = 0
                    if kode != "":
                        if kode in voucher:
                            diskon_pct = voucher[kode]
                            diskon_amt = total * diskon_pct // 100
                            total -= diskon_amt
                        else:
                            print("Voucher tidak valid, dilanjut tanpa voucher.")
                            kode = None
                    else:
                        kode = None

                    while True:
                        if minta_pin("Masukkan PIN user: ") == pins["user"]:
                            break
                        print("PIN salah! Ulangi.")
                    if saldo["user"] >= total:
                        saldo["user"] -= total
                        riwayat_user.append(f"Beli pulsa {op} {nominal} - Rp{total}")
                        riwayat_admin.append(f"User beli pulsa {op} {nominal} - Rp{total}")
                        detail = {
                            "tanggal": datetime.datetime.now(),
                            "produk": f"Pulsa {op.title()}",
                            "nominal": nominal,
                            "tujuan": tujuan,
                            "kode_voucher": kode,
                            "diskon_pct": diskon_pct,
                            "biaya_admin": biaya_admin,
                            "total_bayar": total,
                            "saldo_akhir": saldo["user"]
                        }
                        cetak_struk(detail)
                    else:
                        print("Saldo tidak cukup!")

                elif kat == "2":
                    print("\nE-Wallet tersedia:")
                    for e in ewallet:
                        print("-", e.title())
                    while True:
                        ew = input("Masukkan e-wallet: ").lower().strip()
                        if ew in ewallet:
                            break
                        print("E-wallet tidak ditemukan!")
                    nominal = minta_nominal("Masukkan nominal (20k-1jt): ")
                    tujuan = minta_nomor("Masukkan nomor tujuan (11-12 digit): ")
                    biaya_admin = biaya_admin_ewallet.get(ew, 2000)
                    total = nominal + biaya_admin

                    kode = input("Kode voucher (enter jika tidak ada): ").strip().upper()
                    diskon_pct = 0
                    if kode != "":
                        if kode in voucher:
                            diskon_pct = voucher[kode]
                            diskon_amt = total * diskon_pct // 100
                            total -= diskon_amt
                        else:
                            print("Voucher tidak valid, dilanjut tanpa voucher.")
                            kode = None
                    else:
                        kode = None

                    while True:
                        if minta_pin("Masukkan PIN user: ") == pins["user"]:
                            break
                        print("PIN salah! Ulangi.")
                    if saldo["user"] >= total:
                        saldo["user"] -= total
                        riwayat_user.append(f"Top up {ew} {nominal} - Rp{total}")
                        riwayat_admin.append(f"User top up {ew} {nominal} - Rp{total}")
                        detail = {
                            "tanggal": datetime.datetime.now(),
                            "produk": f"E-Wallet {ew.title()}",
                            "nominal": nominal,
                            "tujuan": tujuan,
                            "kode_voucher": kode,
                            "diskon_pct": diskon_pct,
                            "biaya_admin": biaya_admin,
                            "total_bayar": total,
                            "saldo_akhir": saldo["user"]
                        }
                        cetak_struk(detail)
                    else:
                        print("Saldo tidak cukup!")

                elif kat == "3":
                    nominal = minta_nominal("Masukkan nominal token (20k-1jt): ")
                    idpel = minta_nomor("Masukkan ID pelanggan (11-12 digit): ")
                    biaya_admin = biaya_admin_token
                    total = nominal + biaya_admin

                    kode = input("Kode voucher (enter jika tidak ada): ").strip().upper()
                    diskon_pct = 0
                    if kode != "":
                        if kode in voucher:
                            diskon_pct = voucher[kode]
                            diskon_amt = total * diskon_pct // 100
                            total -= diskon_amt
                        else:
                            print("Voucher tidak valid, dilanjut tanpa voucher.")
                            kode = None
                    else:
                        kode = None

                    while True:
                        if minta_pin("Masukkan PIN user: ") == pins["user"]:
                            break
                        print("PIN salah! Ulangi.")
                    if saldo["user"] >= total:
                        saldo["user"] -= total
                        riwayat_user.append(f"Beli token PLN {nominal} - Rp{total}")
                        riwayat_admin.append(f"User beli token PLN {nominal} - Rp{total}")
                        detail = {
                            "tanggal": datetime.datetime.now(),
                            "produk": "Token PLN",
                            "nominal": nominal,
                            "tujuan": idpel,
                            "kode_voucher": kode,
                            "diskon_pct": diskon_pct,
                            "biaya_admin": biaya_admin,
                            "total_bayar": total,
                            "saldo_akhir": saldo["user"]
                        }
                        cetak_struk(detail)
                    else:
                        print("Saldo tidak cukup!")

            elif pilih == "3":
                jumlah = minta_nominal("Masukkan jumlah top up (20k-1jt): ")
                ket = input("Keterangan / bukti (enter jika tidak ada): ").strip()
                req_id = len(permintaan_topup)
                permintaan_topup.append({"id": req_id, "jumlah": jumlah, "keterangan": ket})
                riwayat_user.append(f"Ajukan top up Rp{jumlah}")
                riwayat_admin.append(f"Permintaan top up masuk Rp{jumlah} (id={req_id})")
                print("Permintaan top up terkirim ke admin.")

            elif pilih == "4":
                print("Saldo Anda: Rp", saldo["user"])

            elif pilih == "5":
                while True:
                    if minta_pin("Masukkan PIN lama: ") == pins["user"]:
                        break
                    print("PIN lama salah! Ulangi.")
                baru = minta_pin("Masukkan PIN baru (4 digit): ")
                pins["user"] = baru
                riwayat_admin.append("User mengganti PIN")
                print("PIN berhasil diganti.")

            elif pilih == "6":
                print("\n=== RIWAYAT TRANSAKSI USER ===")
                if not riwayat_user:
                    print("Belum ada riwayat.")
                else:
                    for r in riwayat_user:
                        print("-", r)

            elif pilih == "7":
                print("Logout user...")
                break

            elif pilih == "1":
                lihat_produk_user()

            else:
                print("Input tidak valid!")

    def menu_admin():
        while True:
            print("\n=== MENU ADMIN ===")
            print("1. Lihat Permintaan Top Up")
            print("2. Proses Top Up")
            print("3. Riwayat Transaksi")
            print("4. CRUD Produk")
            print("5. Beli Produk (sebagai Admin)")
            print("6. Ganti PIN Admin")
            print("7. Logout Admin")
            pilih = input("Pilih: ").strip()

            if pilih == "1":
                if not permintaan_topup:
                    print("Tidak ada permintaan top up.")
                else:
                    print("\n=== PERMINTAAN TOP UP MASUK ===")
                    for req in permintaan_topup:
                        print(f"id={req['id']} | Rp{req['jumlah']} | {req['keterangan']}")

            elif pilih == "2":
                if not permintaan_topup:
                    print("Tidak ada permintaan.")
                    continue
                while True:
                    idx = input("Masukkan ID permintaan: ").strip()
                    if not idx.isdigit():
                        print("ID harus angka!")
                        continue
                    idx = int(idx)
                    found = None
                    for i, req in enumerate(permintaan_topup):
                        if req["id"] == idx:
                            found = (i, req)
                            break
                    if found:
                        break
                    print("ID tidak ditemukan!")
                i, req = found
                print(f"\nProses id={req['id']} | Rp{req['jumlah']}")
                while True:
                    aksi = input("1. Setujui  2. Tolak  (pilih 1/2): ").strip()
                    if aksi in ("1","2"):
                        break
                    print("Input harus 1 atau 2!")
                if aksi == "1":
                    saldo["user"] += req["jumlah"]
                    saldo["admin"] += req["jumlah"]
                    riwayat_user.append(f"Top up Rp{req['jumlah']} disetujui admin")
                    riwayat_admin.append(f"Admin setujui top up Rp{req['jumlah']}")
                    permintaan_topup.pop(i)
                    print("Top up disetujui.")
                else:
                    riwayat_user.append(f"Top up Rp{req['jumlah']} ditolak admin")
                    riwayat_admin.append(f"Admin tolak top up Rp{req['jumlah']}")
                    permintaan_topup.pop(i)
                    print("Top up ditolak.")

            elif pilih == "3":
                print("\n=== RIWAYAT USER ===")
                if riwayat_user:
                    for r in riwayat_user:
                        print("-", r)
                else:
                    print("Belum ada riwayat user.")
                print("\n=== LOG ADMIN ===")
                if riwayat_admin:
                    for r in riwayat_admin:
                        print("-", r)
                else:
                    print("Belum ada log admin.")

            elif pilih == "4":
                while True:
                    print("\n=== CRUD PRODUK (ADMIN) ===")
                    print("1. Lihat Produk")
                    print("2. Hapus Produk")
                    print("3. Tambah Produk")
                    print("4. Ubah Harga Produk (biaya admin)")
                    print("5. Kembali")
                    aksi = input("Pilih: ").strip()
                    if aksi == "1":
                        print("\n-- Pulsa --")
                        for op in pulsa:
                            print("-", op.title(), "| Biaya admin:", biaya_admin_pulsa.get(op, "N/A"))
                        print("\n-- E-Wallet --")
                        for e in ewallet:
                            print("-", e.title(), "| Biaya admin:", biaya_admin_ewallet.get(e, "N/A"))
                        print("\n-- Token --")
                        for t in token:
                            print("-", t, "| Biaya admin:", biaya_admin_token)
                    elif aksi == "2":
                        print("\nHapus produk dari kategori mana?")
                        print("1. Pulsa")
                        print("2. E-Wallet")
                        print("3. Token")
                        while True:
                            cat = input("Pilih (1-3): ").strip()
                            if cat in ("1","2","3"):
                                break
                            print("Input hanya 1,2,3!")
                        if cat == "1":
                            if len(pulsa) <= 1:
                                print("Tidak boleh menghapus. Harus tersisa minimal 1 operator pulsa.")
                                continue
                            while True:
                                print("Operator saat ini:")
                                for op in pulsa:
                                    print("-", op.title())
                                target = input("Masukkan operator yang ingin dihapus: ").lower().strip()
                                if target in pulsa:
                                    break
                                print("Operator tidak ditemukan!")
                            del pulsa[target]
                            biaya_admin_pulsa.pop(target, None)
                            riwayat_admin.append(f"Admin hapus operator pulsa {target}")
                            print(f"Operator {target.title()} berhasil dihapus.")
                        elif cat == "2":
                            if len(ewallet) <= 1:
                                print("Tidak boleh menghapus. Harus tersisa minimal 1 e-wallet.")
                                continue
                            while True:
                                print("E-Wallet saat ini:")
                                for e in ewallet:
                                    print("-", e.title())
                                target = input("Masukkan e-wallet yang ingin dihapus: ").lower().strip()
                                if target in ewallet:
                                    break
                                print("E-wallet tidak ditemukan!")
                            del ewallet[target]
                            biaya_admin_ewallet.pop(target, None)
                            riwayat_admin.append(f"Admin hapus ewallet {target}")
                            print(f"E-Wallet {target.title()} berhasil dihapus.")
                        else:
                            if len(token) <= 1:
                                print("Tidak boleh menghapus. Harus tersisa minimal 1 produk token.")
                                continue
                            while True:
                                print("Token saat ini:")
                                for t in token:
                                    print("-", t)
                                target = input("Masukkan nama token yang ingin dihapus (case sensitive): ").strip()
                                if target in token:
                                    break
                                print("Token tidak ditemukan!")
                            del token[target]
                            riwayat_admin.append(f"Admin hapus token {target}")
                            print(f"Token {target} berhasil dihapus.")

                    elif aksi == "3":
                        print("\nTambah produk ke kategori mana?")
                        print("1. Pulsa")
                        print("2. E-Wallet")
                        print("3. Token")
                        while True:
                            cat = input("Pilih (1-3): ").strip()
                            if cat in ("1","2","3"):
                                break
                            print("Input hanya 1,2,3!")
                        if cat == "1":
                            while True:
                                nama = input("Masukkan nama operator baru (tanpa spasi): ").lower().strip()
                                if nama == "" or not nama.isalpha():
                                    print("Nama operator harus huruf dan tidak kosong!")
                                    continue
                                if nama in pulsa:
                                    print("Operator sudah ada!")
                                    continue
                                break
                            pulsa[nama] = []
                            biaya_admin_pulsa[nama] = 2000
                            riwayat_admin.append(f"Admin tambah operator pulsa {nama}")
                            print(f"Operator {nama.title()} berhasil ditambahkan.")
                        elif cat == "2":
                            while True:
                                nama = input("Masukkan nama e-wallet baru (tanpa spasi): ").lower().strip()
                                if nama == "" or not nama.isalpha():
                                    print("Nama e-wallet harus huruf dan tidak kosong!")
                                    continue
                                if nama in ewallet:
                                    print("E-wallet sudah ada!")
                                    continue
                                break
                            ewallet[nama] = []
                            biaya_admin_ewallet[nama] = 2000
                            riwayat_admin.append(f"Admin tambah ewallet {nama}")
                            print(f"E-Wallet {nama.title()} berhasil ditambahkan.")
                        else:
                            while True:
                                nama = input("Masukkan nama token baru: ").strip()
                                if nama == "":
                                    print("Nama token tidak boleh kosong!")
                                    continue
                                if nama in token:
                                    print("Token sudah ada!")
                                    continue
                                break
                            token[nama] = []
                            riwayat_admin.append(f"Admin tambah token {nama}")
                            print(f"Token {nama} berhasil ditambahkan.")

                    elif aksi == "4":
                        print("\nUbah biaya admin untuk kategori / produk mana?")
                        print("1. Pulsa (per operator)")
                        print("2. E-Wallet (per provider)")
                        print("3. Token (global)")
                        while True:
                            cat = input("Pilih (1-3): ").strip()
                            if cat in ("1","2","3"):
                                break
                            print("Input hanya 1,2,3!")
                        if cat == "1":
                            while True:
                                print("Operator saat ini:")
                                for op in biaya_admin_pulsa:
                                    print("-", op.title(), "| Biaya admin:", biaya_admin_pulsa[op])
                                target = input("Masukkan operator yang ingin diubah biayanya: ").lower().strip()
                                if target in biaya_admin_pulsa:
                                    break
                                print("Operator tidak ditemukan!")
                            while True:
                                v = input(f"Masukkan biaya admin baru untuk {target.title()} (angka): ").strip()
                                if v.isdigit():
                                    biaya_admin_pulsa[target] = int(v)
                                    riwayat_admin.append(f"Admin ubah biaya admin pulsa {target} -> {v}")
                                    print("Biaya admin berhasil diubah.")
                                    break
                                print("Masukkan angka valid!")
                        elif cat == "2":
                            while True:
                                print("E-Wallet saat ini:")
                                for e in biaya_admin_ewallet:
                                    print("-", e.title(), "| Biaya admin:", biaya_admin_ewallet[e])
                                target = input("Masukkan e-wallet yang ingin diubah biayanya: ").lower().strip()
                                if target in biaya_admin_ewallet:
                                    break
                                print("E-wallet tidak ditemukan!")
                            while True:
                                v = input(f"Masukkan biaya admin baru untuk {target.title()} (angka): ").strip()
                                if v.isdigit():
                                    biaya_admin_ewallet[target] = int(v)
                                    riwayat_admin.append(f"Admin ubah biaya admin ewallet {target} -> {v}")
                                    print("Biaya admin berhasil diubah.")
                                    break
                                print("Masukkan angka valid!")
                        else:
                            while True:
                                v = input("Masukkan biaya admin baru untuk Token PLN (angka): ").strip()
                                if v.isdigit():
                                    nonlocal_biaya = int(v)
                                    break
                                print("Masukkan angka valid!")

                    elif aksi == "5":
                        break
                    else:
                        print("Pilihan tidak valid! Silakan pilih 1-5.")

            elif pilih == "5":
                print("\n=== BELI PRODUK (ADMIN) ===")
                print("1. Pulsa")
                print("2. E-Wallet")
                print("3. Token PLN")
                while True:
                    kat = input("Pilih (1-3): ").strip()
                    if kat in ("1","2","3"):
                        break
                    print("Input hanya 1,2,3!")
                if kat == "1":
                    print("\nOperator tersedia:")
                    for op in pulsa:
                        print("-", op.title())
                    while True:
                        op = input("Masukkan operator: ").lower().strip()
                        if op in pulsa:
                            break
                        print("Operator tidak ditemukan!")
                    nominal = minta_nominal("Nominal: ")
                    tujuan = minta_nomor("Nomor tujuan: ")
                    biaya_admin = biaya_admin_pulsa.get(op, 2000)
                    total = nominal + biaya_admin
                    kode = input("Kode voucher (enter skip): ").strip().upper()
                    diskon_pct = 0
                    if kode != "" and kode in voucher:
                        diskon_pct = voucher[kode]
                        total -= total * diskon_pct // 100
                    else:
                        kode = None
                    while True:
                        if minta_pin("Masukkan PIN admin untuk konfirmasi: ") == pins["admin"]:
                            break
                        print("PIN admin salah!")
                    if saldo["admin"] >= total:
                        saldo["admin"] -= total
                        riwayat_admin.append(f"Admin beli pulsa {op} {nominal} - Rp{total}")
                        detail = {
                            "tanggal": datetime.datetime.now(),
                            "produk": f"Pulsa {op.title()} (Admin)",
                            "nominal": nominal,
                            "tujuan": tujuan,
                            "kode_voucher": kode,
                            "diskon_pct": diskon_pct,
                            "biaya_admin": biaya_admin,
                            "total_bayar": total,
                            "saldo_akhir": saldo["admin"]
                        }
                        cetak_struk(detail)
                    else:
                        print("Saldo admin tidak cukup!")
                elif kat == "2":
                    print("\nE-Wallet tersedia:")
                    for e in ewallet:
                        print("-", e.title())
                    while True:
                        ew = input("Masukkan e-wallet: ").lower().strip()
                        if ew in ewallet:
                            break
                        print("E-wallet tidak ditemukan!")
                    nominal = minta_nominal("Nominal: ")
                    tujuan = minta_nomor("Nomor tujuan: ")
                    biaya_admin = biaya_admin_ewallet.get(ew, 2000)
                    total = nominal + biaya_admin
                    kode = input("Kode voucher (enter skip): ").strip().upper()
                    diskon_pct = 0
                    if kode != "" and kode in voucher:
                        diskon_pct = voucher[kode]
                        total -= total * diskon_pct // 100
                    else:
                        kode = None
                    while True:
                        if minta_pin("Masukkan PIN admin untuk konfirmasi: ") == pins["admin"]:
                            break
                        print("PIN admin salah!")
                    if saldo["admin"] >= total:
                        saldo["admin"] -= total
                        riwayat_admin.append(f"Admin top up {ew} {nominal} - Rp{total}")
                        detail = {
                            "tanggal": datetime.datetime.now(),
                            "produk": f"E-Wallet {ew.title()} (Admin)",
                            "nominal": nominal,
                            "tujuan": tujuan,
                            "kode_voucher": kode,
                            "diskon_pct": diskon_pct,
                            "biaya_admin": biaya_admin,
                            "total_bayar": total,
                            "saldo_akhir": saldo["admin"]
                        }
                        cetak_struk(detail)
                    else:
                        print("Saldo admin tidak cukup!")
                elif kat == "3":
                    nominal = minta_nominal("Nominal token: ")
                    idpel = minta_nomor("ID pelanggan: ")
                    biaya_admin = biaya_admin_token
                    total = nominal + biaya_admin
                    kode = input("Kode voucher (enter skip): ").strip().upper()
                    diskon_pct = 0
                    if kode != "" and kode in voucher:
                        diskon_pct = voucher[kode]
                        total -= total * diskon_pct // 100
                    else:
                        kode = None
                    while True:
                        if minta_pin("Masukkan PIN admin untuk konfirmasi: ") == pins["admin"]:
                            break
                        print("PIN admin salah!")
                    if saldo["admin"] >= total:
                        saldo["admin"] -= total
                        riwayat_admin.append(f"Admin beli token PLN {nominal} - Rp{total}")
                        detail = {
                            "tanggal": datetime.datetime.now(),
                            "produk": "Token PLN (Admin)",
                            "nominal": nominal,
                            "tujuan": idpel,
                            "kode_voucher": kode,
                            "diskon_pct": diskon_pct,
                            "biaya_admin": biaya_admin,
                            "total_bayar": total,
                            "saldo_akhir": saldo["admin"]
                        }
                        cetak_struk(detail)
                    else:
                        print("Saldo admin tidak cukup!")

            elif pilih == "6":
                while True:
                    if minta_pin("Masukkan PIN lama admin: ") == pins["admin"]:
                        break
                    print("PIN lama salah!")
                baru = minta_pin("Masukkan PIN admin baru (4 digit): ")
                pins["admin"] = baru
                riwayat_admin.append("Admin mengganti PIN")
                print("PIN admin berhasil diubah.")

            elif pilih == "7":
                print("Logout admin...")
                break

            else:
                print("Input tidak valid!")

    while True:
        print("\n=== PILIH MODE ===")
        print("1. Login User")
        print("2. Login Admin")
        print("3. Keluar")
        mode = input("Pilih: ").strip()
        if mode == "1":
            while True:
                if minta_pin("Masukkan PIN User: ") == pins["user"]:
                    print("Login user berhasil.")
                    menu_user()
                    break
                print("PIN salah!")
        elif mode == "2":
            while True:
                if minta_pin("Masukkan PIN Admin: ") == pins["admin"]:
                    print("Login admin berhasil.")
                    menu_admin()
                    break
                print("PIN salah!")
        elif mode == "3":
            print("Terima kasih telah menggunakan Samurai Store!")
            break
        else:
            print("Input tidak valid!")

if __name__ == "__main__":
    utama()
