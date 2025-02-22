import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect('C:/grok/eczane.db')
cursor = conn.cursor()

# Reçeteler tablosunu oluştur
cursor.execute('''
    CREATE TABLE IF NOT EXISTS receteler (
        kod TEXT PRIMARY KEY,
        ilaclar TEXT
    )
''')

# Sabit reçete verileri
receteler = [
    ('RX1001', '[{"isim": "Paracetamol", "doz": "500 mg", "miktar": "20 tablet"}, {"isim": "İbuprofen", "doz": "400 mg", "miktar": "15 tablet"}]'),
    ('RX1002', '[{"isim": "Amoksisilin", "doz": "1g", "miktar": "10 kapsül"}, {"isim": "Asetilsalisilik Asit", "doz": "100 mg", "miktar": "30 tablet"}]'),
    ('RX1003', '[{"isim": "Metformin", "doz": "850 mg", "miktar": "60 tablet"}, {"isim": "Losartan", "doz": "50 mg", "miktar": "30 tablet"}]'),
    ('RX1004', '[{"isim": "Omeprazol", "doz": "20 mg", "miktar": "14 kapsül"}, {"isim": "Levotiroksin", "doz": "100 mcg", "miktar": "50 tablet"}]'),
    ('RX1005', '[{"isim": "Paracetamol", "doz": "500 mg", "miktar": "20 tablet"}, {"isim": "Amoksisilin", "doz": "1g", "miktar": "10 kapsül"}, {"isim": "İbuprofen", "doz": "400 mg", "miktar": "15 tablet"}]'),
]

cursor.executemany('INSERT OR REPLACE INTO receteler (kod, ilaclar) VALUES (?, ?)', receteler)

# Değişiklikleri kaydet ve kapat
conn.commit()
conn.close()
print("Veritabanı C:/grok/eczane.db içinde oluşturuldu!")