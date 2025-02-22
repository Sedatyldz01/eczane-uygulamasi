import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect('C:/grok/eczane.db')
cursor = conn.cursor()

# Eczaneler tablosunu oluştur
cursor.execute('''
    CREATE TABLE IF NOT EXISTS eczaneler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT,
        il TEXT,
        ilce TEXT,
        adres TEXT,
        telefon TEXT,
        stok TEXT,  -- JSON formatında ilaç stokları
        ulasim TEXT -- JSON formatında ulaşım bilgileri
    )
''')

# Örnek eczane verileri
eczaneler = [
    ('Kadıköy Eczanesi', 'İstanbul', 'Kadıköy', 'Bağdat Cd. No: 123', '0216 123 45 67', 
     '[{"isim": "Paracetamol", "doz": "500 mg"}, {"isim": "İbuprofen", "doz": "400 mg"}]', 
     '{"toplu_tasima": "Kadıköy Metro’ya 5 dk", "arac": "Bağdat Cd. 2 km, otopark var", "yaya": "Merkezi konum"}'),
    ('Moda Eczanesi', 'İstanbul', 'Kadıköy', 'Moda Sk. No: 45', '0216 987 65 43', 
     '[{"isim": "Paracetamol", "doz": "500 mg"}]', 
     '{"toplu_tasima": "Tramvay Durağı’na 3 dk", "arac": "Moda Cd. 1 km", "yaya": "Sahile yakın"}'),
    ('Beşiktaş Eczanesi', 'İstanbul', 'Beşiktaş', 'Barbaros Blv. No: 78', '0212 555 22 11', 
     '[{"isim": "Amoksisilin", "doz": "1g"}, {"isim": "İbuprofen", "doz": "400 mg"}]', 
     '{"toplu_tasima": "Beşiktaş İskele’ye 5 dk", "arac": "Barbaros Blv. 1.5 km", "yaya": "Çarşıya yakın"}'),
    ('Çankaya Eczanesi', 'Ankara', 'Çankaya', 'Üsküp Cd. No: 56', '0312 456 78 90', 
     '[{"isim": "Metformin", "doz": "850 mg"}, {"isim": "Paracetamol", "doz": "500 mg"}]', 
     '{"toplu_tasima": "Kızılay Metro’ya 10 dk", "arac": "Üsküp Cd. 3 km", "yaya": "Parka 5 dk"}'),
    ('Yenimahalle Eczanesi', 'Ankara', 'Yenimahalle', 'Ragıp Tüzün Cd. No: 12', '0312 123 45 67', 
     '[{"isim": "Omeprazol", "doz": "20 mg"}, {"isim": "Levotiroksin", "doz": "100 mcg"}]', 
     '{"toplu_tasima": "Yenimahalle Metro’ya 7 dk", "arac": "Ragıp Tüzün Cd. 2 km", "yaya": "Merkeze yakın"}'),
]

cursor.executemany('INSERT OR REPLACE INTO eczaneler (isim, il, ilce, adres, telefon, stok, ulasim) VALUES (?, ?, ?, ?, ?, ?, ?)', eczaneler)

# Değişiklikleri kaydet ve kapat
conn.commit()
conn.close()
print("Eczaneler tablosu oluşturuldu ve veriler eklendi!")