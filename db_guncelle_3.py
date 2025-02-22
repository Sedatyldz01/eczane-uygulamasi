import sqlite3

conn = sqlite3.connect('C:/grok/eczane.db')
cursor = conn.cursor()

# Mevcut tabloları temizle ve yeniden oluştur
cursor.execute('DROP TABLE IF EXISTS receteler')
cursor.execute('DROP TABLE IF EXISTS eczaneler')

# Reçeteler tablosu
cursor.execute('''
    CREATE TABLE receteler (
        kod TEXT PRIMARY KEY,
        ilaclar TEXT
    )
''')

# Eczaneler tablosu
cursor.execute('''
    CREATE TABLE eczaneler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT,
        il TEXT,
        ilce TEXT,
        adres TEXT,
        telefon TEXT,
        stok TEXT,
        ulasim TEXT,
        lat REAL,
        lng REAL
    )
''')

# Güncellenmiş reçeteler (4-6 ilaç)
receteler = [
    ('RX1001', '[{"isim": "Paracetamol", "doz": "500 mg", "miktar": "20 tablet"}, {"isim": "İbuprofen", "doz": "400 mg", "miktar": "15 tablet"}, {"isim": "Amoksisilin", "doz": "1g", "miktar": "10 kapsül"}, {"isim": "Omeprazol", "doz": "20 mg", "miktar": "14 kapsül"}, {"isim": "Metformin", "doz": "850 mg", "miktar": "60 tablet"}]'),
    ('RX1002', '[{"isim": "Asetilsalisilik Asit", "doz": "100 mg", "miktar": "30 tablet"}, {"isim": "Levotiroksin", "doz": "100 mcg", "miktar": "50 tablet"}, {"isim": "Losartan", "doz": "50 mg", "miktar": "30 tablet"}, {"isim": "Amoksisilin", "doz": "1g", "miktar": "10 kapsül"}, {"isim": "Paracetamol", "doz": "500 mg", "miktar": "20 tablet"}, {"isim": "İbuprofen", "doz": "400 mg", "miktar": "15 tablet"}]'),
    ('RX1003', '[{"isim": "Metformin", "doz": "850 mg", "miktar": "60 tablet"}, {"isim": "Losartan", "doz": "50 mg", "miktar": "30 tablet"}, {"isim": "Omeprazol", "doz": "20 mg", "miktar": "14 kapsül"}, {"isim": "Levotiroksin", "doz": "100 mcg", "miktar": "50 tablet"}]'),
    ('RX1004', '[{"isim": "Omeprazol", "doz": "20 mg", "miktar": "14 kapsül"}, {"isim": "Levotiroksin", "doz": "100 mcg", "miktar": "50 tablet"}, {"isim": "Paracetamol", "doz": "500 mg", "miktar": "20 tablet"}, {"isim": "Asetilsalisilik Asit", "doz": "100 mg", "miktar": "30 tablet"}, {"isim": "İbuprofen", "doz": "400 mg", "miktar": "15 tablet"}]'),
    ('RX1005', '[{"isim": "Paracetamol", "doz": "500 mg", "miktar": "20 tablet"}, {"isim": "Amoksisilin", "doz": "1g", "miktar": "10 kapsül"}, {"isim": "İbuprofen", "doz": "400 mg", "miktar": "15 tablet"}, {"isim": "Metformin", "doz": "850 mg", "miktar": "60 tablet"}, {"isim": "Losartan", "doz": "50 mg", "miktar": "30 tablet"}, {"isim": "Omeprazol", "doz": "20 mg", "miktar": "14 kapsül"}]'),
]

cursor.executemany('INSERT INTO receteler (kod, ilaclar) VALUES (?, ?)', receteler)

# Güncellenmiş eczaneler (her ilçede 3-5 eczane, stoklar farklı)
eczaneler = [
    # İstanbul - Kadıköy
    ('Kadıköy Eczanesi', 'İstanbul', 'Kadıköy', 'Bağdat Cd. No: 123', '0216 123 45 67', 
     '[{"isim": "Paracetamol", "doz": "500 mg"}, {"isim": "İbuprofen", "doz": "400 mg"}, {"isim": "Amoksisilin", "doz": "1g"}, {"isim": "Omeprazol", "doz": "20 mg"}]', 
     '{"toplu_tasima": "Kadıköy Metro’ya 5 dk", "arac": "Bağdat Cd. 2 km", "yaya": "Merkezi konum"}', 40.9903, 29.0270),
    ('Moda Eczanesi', 'İstanbul', 'Kadıköy', 'Moda Sk. No: 45', '0216 987 65 43', 
     '[{"isim": "Paracetamol", "doz": "500 mg"}, {"isim": "Metformin", "doz": "850 mg"}]', 
     '{"toplu_tasima": "Tramvay Durağı’na 3 dk", "arac": "Moda Cd. 1 km", "yaya": "Sahile yakın"}', 40.9833, 29.0260),
    ('Fenerbahçe Eczanesi', 'İstanbul', 'Kadıköy', 'Fenerbahçe Mh. No: 78', '0216 555 22 11', 
     '[{"isim": "İbuprofen", "doz": "400 mg"}, {"isim": "Omeprazol", "doz": "20 mg"}, {"isim": "Losartan", "doz": "50 mg"}]', 
     '{"toplu_tasima": "Minibüs Durağı’na 200 m", "arac": "Stad çevresi 1.5 km", "yaya": "Parka 5 dk"}', 40.9750, 29.0450),
    ('Bahariye Eczanesi', 'İstanbul', 'Kadıköy', 'Bahariye Cd. No: 10', '0216 333 44 55', 
     '[{"isim": "Paracetamol", "doz": "500 mg"}, {"isim": "Amoksisilin", "doz": "1g"}, {"isim": "Metformin", "doz": "850 mg"}, {"isim": "Levotiroksin", "doz": "100 mcg"}]', 
     '{"toplu_tasima": "Bahariye Tramvay 2 dk", "arac": "Bahariye Cd. 1 km", "yaya": "Merkeze yakın"}', 40.9870, 29.0300),

    # İstanbul - Beşiktaş
    ('Beşiktaş Eczanesi', 'İstanbul', 'Beşiktaş', 'Barbaros Blv. No: 78', '0212 555 22 11', 
     '[{"isim": "Amoksisilin", "doz": "1g"}, {"isim": "İbuprofen", "doz": "400 mg"}, {"isim": "Asetilsalisilik Asit", "doz": "100 mg"}]', 
     '{"toplu_tasima": "Beşiktaş İskele’ye 5 dk", "arac": "Barbaros Blv. 1.5 km", "yaya": "Çarşıya yakın"}', 41.0431, 29.0067),
    ('Ortaköy Eczanesi', 'İstanbul', 'Beşiktaş', 'Ortaköy Sk. No: 15', '0212 666 77 88', 
     '[{"isim": "Paracetamol", "doz": "500 mg"}, {"isim": "Omeprazol", "doz": "20 mg"}, {"isim": "Levotiroksin", "doz": "100 mcg"}, {"isim": "Metformin", "doz": "850 mg"}]', 
     '{"toplu_tasima": "Ortaköy Otobüs 3 dk", "arac": "Kıyı Yolu 2 km", "yaya": "Sahile 5 dk"}', 41.0480, 29.0260),
    ('Akaretler Eczanesi', 'İstanbul', 'Beşiktaş', 'Süleyman Seba Cd. No: 22', '0212 444 33 22', 
     '[{"isim": "İbuprofen", "doz": "400 mg"}, {"isim": "Losartan", "doz": "50 mg"}]', 
     '{"toplu_tasima": "Akaretler Otobüs 4 dk", "arac": "Merkez 1 km", "yaya": "Yürüme mesafesi"}', 41.0400, 29.0000),

    # Ankara - Çankaya
    ('Çankaya Eczanesi', 'Ankara', 'Çankaya', 'Üsküp Cd. No: 56', '0312 456 78 90', 
     '[{"isim": "Metformin", "doz": "850 mg"}, {"isim": "Paracetamol", "doz": "500 mg"}, {"isim": "Losartan", "doz": "50 mg"}, {"isim": "Omeprazol", "doz": "20 mg"}]', 
     '{"toplu_tasima": "Kızılay Metro’ya 10 dk", "arac": "Üsküp Cd. 3 km", "yaya": "Parka 5 dk"}', 39.9208, 32.8541),
    ('Kavaklıdere Eczanesi', 'Ankara', 'Çankaya', 'Tunalı Hilmi Cd. No: 34', '0312 999 88 77', 
     '[{"isim": "Levotiroksin", "doz": "100 mcg"}, {"isim": "Asetilsalisilik Asit", "doz": "100 mg"}]', 
     '{"toplu_tasima": "Tunalı Otobüs 5 dk", "arac": "Merkez 2 km", "yaya": "Kavaklıdere’ye yakın"}', 39.9080, 32.8590),
    ('Üsküp Eczanesi', 'Ankara', 'Çankaya', 'Üsküp Sk. No: 12', '0312 777 66 55', 
     '[{"isim": "Paracetamol", "doz": "500 mg"}, {"isim": "İbuprofen", "doz": "400 mg"}, {"isim": "Amoksisilin", "doz": "1g"}]', 
     '{"toplu_tasima": "Çankaya Otobüs 6 dk", "arac": "Üsküp Sk. 1.5 km", "yaya": "Merkeze yakın"}', 39.9150, 32.8500),

    # Ankara - Yenimahalle
    ('Yenimahalle Eczanesi', 'Ankara', 'Yenimahalle', 'Ragıp Tüzün Cd. No: 12', '0312 123 45 67', 
     '[{"isim": "Omeprazol", "doz": "20 mg"}, {"isim": "Levotiroksin", "doz": "100 mcg"}, {"isim": "Metformin", "doz": "850 mg"}]', 
     '{"toplu_tasima": "Yenimahalle Metro’ya 7 dk", "arac": "Ragıp Tüzün Cd. 2 km", "yaya": "Merkeze yakın"}', 39.9662, 32.7146),
    ('Batıkent Eczanesi', 'Ankara', 'Yenimahalle', 'Batı Blv. No: 45', '0312 222 33 44', 
     '[{"isim": "Paracetamol", "doz": "500 mg"}, {"isim": "İbuprofen", "doz": "400 mg"}, {"isim": "Losartan", "doz": "50 mg"}, {"isim": "Asetilsalisilik Asit", "doz": "100 mg"}]', 
     '{"toplu_tasima": "Batıkent Metro 5 dk", "arac": "Batı Blv. 3 km", "yaya": "Batıkent merkez"}', 39.9700, 32.7250),
    ('Demetevler Eczanesi', 'Ankara', 'Yenimahalle', 'Demetevler Cd. No: 67', '0312 555 44 33', 
     '[{"isim": "Amoksisilin", "doz": "1g"}, {"isim": "Omeprazol", "doz": "20 mg"}]', 
     '{"toplu_tasima": "Demetevler Otobüs 4 dk", "arac": "Demetevler Cd. 1 km", "yaya": "Yürüme mesafesi"}', 39.9600, 32.7900),
]

cursor.executemany('INSERT INTO eczaneler (isim, il, ilce, adres, telefon, stok, ulasim, lat, lng) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', eczaneler)

conn.commit()
conn.close()
print("Veritabanı güncellendi: Daha fazla ilaç ve eczane eklendi!")