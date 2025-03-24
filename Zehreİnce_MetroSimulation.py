from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur"""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None # Oluşturulanlar içinde başlangıç veya hedef bulunamazsa none döndürülür
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        # Ziyaret edilen istasyonları ve rotayı takip et
        ziyaret_edildi = set()
        kuyruk = deque([(baslangic, [baslangic])])  # Başlangıç istasyonu ve yol
        ziyaret_edildi.add(baslangic)

        while kuyruk:
            mevcut_istasyon, rota = kuyruk.popleft()

            # Hedef istasyonu bulduysak, rotayı ve aktarmaları döndürür
            if mevcut_istasyon == hedef:
                aktarma_yerleri = []
                for i in range(1, len(rota)):
                    if rota[i].hat != rota[i-1].hat:  # Hattın değiştiği yerler kaydedilir
                        aktarma_yerleri.append((rota[i-1].ad, rota[i-1].hat, rota[i].ad, rota[i].hat))
                return rota, aktarma_yerleri

            # Komşu istasyonları gezer
            for komsu, _ in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    yeni_rota = rota + [komsu]
                    kuyruk.append((komsu, yeni_rota))

        return None  # Rota bulunamazsa None döndürür


    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur"""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None # Hedef veya başlangıç bulunamazsa none döndürülür

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        pq = [(0, id(baslangic), baslangic, [baslangic])]
        
        ziyaret_edildi = set()
        
        g_costs = {baslangic: 0}  # Gerçek maliyet

        while pq:
            # En düşük maliyetli istasyon baz alınır
            toplam_sure, _, mevcut_istasyon, rota = heapq.heappop(pq)
            
            # Hedefe ulaşıldıysa rotayı, süreyi ve aktarmaları döndürür
            if mevcut_istasyon == hedef:
                aktarma_yerleri = []
                for i in range(1, len(rota)):
                    if rota[i].hat != rota[i-1].hat:  # Hattın değiştiği yerler kaydedilir
                        aktarma_yerleri.append((rota[i-1].ad, rota[i-1].hat, rota[i].ad, rota[i].hat))
                return rota, toplam_sure, aktarma_yerleri
            
            
            # Ziyaret edilen istasyon işaretlenir
            if mevcut_istasyon in ziyaret_edildi:
                continue
            ziyaret_edildi.add(mevcut_istasyon)
            
            # Komşular kontrol edilir
            for komsu, sure in mevcut_istasyon.komsular:
                yeni_sure = toplam_sure + sure
                if komsu not in ziyaret_edildi:
                    if komsu not in g_costs or yeni_sure < g_costs[komsu]:
                        g_costs[komsu] = yeni_sure
                        heapq.heappush(pq, (yeni_sure, id(komsu), komsu, rota + [komsu]))

        return None  # Hedefe ulaşılamadıysa none döndürülür

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
# Senaryo 1: AŞTİ'den OSB'ye
print("\n1. AŞTİ'den OSB'ye:")
rota, aktarma_yerleri = metro.en_az_aktarma_bul("M1", "K4")
if rota:
    print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    print("Aktarmalar:")
    for aktarma in aktarma_yerleri:
        # Aktarma yerlerini yazdırmak için doğru unpack yapıyoruz
        print(f"{aktarma[0]} ({aktarma[1]}) -> {aktarma[2]} ({aktarma[3]})")

# Senaryo 2: Batıkent'ten Keçiören'e
print("\n2. Batıkent'ten Keçiören'e:")
rota, sure, aktarma_yerleri = metro.en_hizli_rota_bul("T1", "T4")  # sureyi ve aktarmaları almak için unpack et
if rota:
    print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    print("Aktarmalar:")
    for aktarma in aktarma_yerleri:
        print(f"{aktarma[0]} ({aktarma[1]}) -> {aktarma[2]} ({aktarma[3]})")

# Senaryo 3: Keçiören'den AŞTİ'ye
print("\n3. Keçiören'den AŞTİ'ye:")
rota, sure, aktarma_yerleri = metro.en_hizli_rota_bul("T4", "M1")  # sureyi ve aktarmaları almak için unpack et
if rota:
    print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    print("Aktarmalar:")
    for aktarma in aktarma_yerleri:
        print(f"{aktarma[0]} ({aktarma[1]}) -> {aktarma[2]} ({aktarma[3]})")
