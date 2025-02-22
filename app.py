from flask import Flask, request, jsonify
import sqlite3
import json
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('eczane.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/recete/<kod>', methods=['GET'])
def get_recete(kod):
    conn = get_db_connection()
    cursor = conn.cursor()
    recete = cursor.execute('SELECT * FROM receteler WHERE kod = ?', (kod,)).fetchone()
    conn.close()
    
    if recete:
        ilaclar = json.loads(recete['ilaclar'])
        return jsonify({'kod': recete['kod'], 'ilaclar': ilaclar})
    return jsonify({'error': 'Reçete bulunamadı'}), 404

@app.route('/api/eczaneler', methods=['GET'])
def get_eczaneler():
    il = request.args.get('il')
    ilce = request.args.get('ilce')
    recete_kodu = request.args.get('recete_kodu')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    recete = cursor.execute('SELECT ilaclar FROM receteler WHERE kod = ?', (recete_kodu,)).fetchone()
    if not recete:
        conn.close()
        return jsonify({'error': 'Reçete bulunamadı'}), 404
    recete_ilaclar = [ilac['isim'] for ilac in json.loads(recete['ilaclar'])]

    query = 'SELECT * FROM eczaneler WHERE il = ? AND ilce = ?'
    params = (il, ilce)
    eczaneler = cursor.execute(query, params).fetchall()
    conn.close()
    
    if not eczaneler:
        return jsonify({'error': 'Bu il/ilçede eczane bulunamadı'}), 404
    
    sonuc = []
    for eczane in eczaneler:
        stok = json.loads(eczane['stok'])
        ulasim = json.loads(eczane['ulasim'])
        stok_ilaclar = [ilac['isim'] for ilac in stok]
        
        stokta_olan = [ilac for ilac in recete_ilaclar if ilac in stok_ilaclar]
        stokta_olmayan = [ilac for ilac in recete_ilaclar if ilac not in stok_ilaclar]
        
        sonuc.append({
            'isim': eczane['isim'],
            'adres': eczane['adres'],
            'telefon': eczane['telefon'],
            'stok': stok,
            'ulasim': ulasim,
            'lat': eczane['lat'],
            'lng': eczane['lng'],
            'stokta_olan': stokta_olan,
            'stokta_olmayan': stokta_olmayan
        })
    
    return jsonify(sonuc)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reçete Ara</title>
        <link rel="stylesheet" href="/static/style.css">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" 
              integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" 
                integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    </head>
    <body>
        <h1>Reçete Ara</h1>
        <input id="receteKodu" placeholder="Reçete Kodu (ör: RX1001)">
        <select id="il">
            <option value="">İl Seç</option>
            <option value="İstanbul">İstanbul</option>
            <option value="Ankara">Ankara</option>
        </select>
        <select id="ilce">
            <option value="">İlçe Seç</option>
        </select>
        <button onclick="ara()">Eczaneleri Bul</button>
        <div id="loading" style="display: none;">Yükleniyor...</div>
        <div id="sonuc"></div>
        <div id="map" style="height: 400px; width: 100%; margin-top: 20px;"></div>
        
        <script>
            const iller = {
                "İstanbul": ["Kadıköy", "Beşiktaş"],
                "Ankara": ["Çankaya", "Yenimahalle"]
            };
            
            let map;
            let markers = [];

            map = L.map('map').setView([41.0082, 28.9784], 10);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap'
            }).addTo(map);

            document.getElementById("il").onchange = function() {
                const il = this.value;
                const ilceSelect = document.getElementById("ilce");
                ilceSelect.innerHTML = '<option value="">İlçe Seç</option>';
                if (il && iller[il]) {
                    iller[il].forEach(ilce => {
                        const option = document.createElement("option");
                        option.value = ilce;
                        option.text = ilce;
                        ilceSelect.appendChild(option);
                    });
                }
            };

            function ara() {
                const kod = document.getElementById("receteKodu").value;
                const il = document.getElementById("il").value;
                const ilce = document.getElementById("ilce").value;
                if (!il || !ilce || !kod) {
                    alert("Lütfen reçete kodu, il ve ilçe seçin!");
                    return;
                }
                
                document.getElementById("loading").style.display = "block";
                document.getElementById("sonuc").innerHTML = "";
                
                fetch(`/api/recete/${kod}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            document.getElementById("sonuc").innerHTML = "Reçete bulunamadı!";
                            document.getElementById("loading").style.display = "none";
                            return;
                        }
                        let html = `<h2>Reçetedeki İlaçlar (${data.ilaclar.length} adet):</h2><ul>`;
                        data.ilaclar.forEach(ilac => {
                            html += `<li>${ilac.isim} ${ilac.doz} - ${ilac.miktar}</li>`;
                        });
                        html += "</ul>";
                        document.getElementById("sonuc").innerHTML = html;
                        
                        fetch(`/api/eczaneler?il=${il}&ilce=${ilce}&recete_kodu=${kod}`)
                            .then(response => response.json())
                            .then(eczaneler => {
                                document.getElementById("loading").style.display = "none";
                                if (eczaneler.error) {
                                    document.getElementById("sonuc").innerHTML += "<p>Eczane bulunamadı!</p>";
                                } else {
                                    let eczaneHtml = "<h2>Eczaneler:</h2><ul>";
                                    markers.forEach(marker => marker.remove());
                                    markers = [];
                                    const bounds = [];
                                    
                                    eczaneler.forEach(eczane => {
                                        eczaneHtml += `
                                            <li>
                                                <strong>${eczane.isim}</strong><br>
                                                <span class="adres">Adres: ${eczane.adres}</span><br>
                                                <span class="telefon">Telefon: ${eczane.telefon}</span><br>
                                                <span class="stok-baslik">Stokta Olan (${eczane.stokta_olan.length} adet):</span>
                                                <ul class="stok-liste stok-olan">
                                                    ${eczane.stokta_olan.map(i => `<li>${i}</li>`).join('')}
                                                </ul>
                                                <span class="stok-baslik stok-olmayan-baslik">Stokta Olmayan (${eczane.stokta_olmayan.length} adet):</span>
                                                <ul class="stok-liste stok-olmayan">
                                                    ${eczane.stokta_olmayan.map(i => `<li>${i}</li>`).join('')}
                                                </ul>
                                                <span class="ulasim">Ulaşım:</span> 
                                                Toplu Taşıma: ${eczane.ulasim.toplu_tasima}, 
                                                Araç: ${eczane.ulasim.arac}, 
                                                Yaya: ${eczane.ulasim.yaya}
                                            </li>`;
                                        const marker = L.marker([eczane.lat, eczane.lng])
                                            .addTo(map)
                                            .bindPopup(`
                                                <b>${eczane.isim}</b><br>
                                                ${eczane.adres}<br>
                                                <b>Stokta Olan:</b> ${eczane.stokta_olan.join(', ')}<br>
                                                <b>Stokta Olmayan:</b> ${eczane.stokta_olmayan.join(', ')}<br>
                                                <a href="https://maps.google.com/?q=${eczane.lat},${eczane.lng}" target="_blank" style="color: #007bff; text-decoration: none;">Yol Tarifi Al</a>
                                            `);
                                        markers.push(marker);
                                        bounds.push([eczane.lat, eczane.lng]);
                                    });
                                    eczaneHtml += "</ul>";
                                    document.getElementById("sonuc").innerHTML += eczaneHtml;
                                    
                                    if (bounds.length > 0) {
                                        map.fitBounds(bounds, { padding: [50, 50] });
                                    }
                                }
                            });
                    });
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)