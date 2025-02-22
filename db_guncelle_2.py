import sqlite3

conn = sqlite3.connect('C:/grok/eczane.db')
cursor = conn.cursor()

# Eczaneler tablosuna koordinat sütunları ekle
cursor.execute('''
    ALTER TABLE eczaneler ADD COLUMN lat REAL;
''')
cursor.execute('''
    ALTER TABLE eczaneler ADD COLUMN lng REAL;
''')

# Örnek koordinatlarla güncelle
eczane_koordinatlari = [
    ('Kadıköy Eczanesi', 40.9903, 29.0270),
    ('Moda Eczanesi', 40.9833, 29.0260),
    ('Beşiktaş Eczanesi', 41.0431, 29.0067),
    ('Çankaya Eczanesi', 39.9208, 32.8541),
    ('Yenimahalle Eczanesi', 39.9662, 32.7146),
]

for isim, lat, lng in eczane_koordinatlari:
    cursor.execute('UPDATE eczaneler SET lat = ?, lng = ? WHERE isim = ?', (lat, lng, isim))

conn.commit()
conn.close()
print("Eczanelere koordinatlar eklendi!")