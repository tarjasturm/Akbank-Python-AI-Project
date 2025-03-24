# Akbank-Python-AI-Project
Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu) 
Proje Amacı: Bu projede, bir metro ağı üzerinde BFS (Breadth-First Search) ve A* algoritmalarını kullanarak iki istasyon arasındaki en hızlı ve en az aktarmalı rotayı bulmaya yönelik bir simülasyon geliştirilecektir. Gerçek dünya problemlerine algoritmik bir yaklaşım ile çözüm getirilmesi hedeflenmektedir.

Proje Python diliyle hazırlanmıştır ve import edilen kütüphanelerin açıklamarı şu şekildedir:

heapq: A* algoritmasının çalışma prensibine göre en düşük maliyetliyi daha hızlı seçebilmek için kullanılmıştır.
collections: BFS algoritmasının "İlk giren ilk çıkar" çalışma şekline göre çalışan bir kuyruk yapısını deque ile oluşturmaya yarar.
typing: Dict, list, tuple, optional gibi veri tiplerini tanımlar.


Kullanılan Algoritmalar ve Kullanım Nedenleri

BFS Algoritması:

Bu algoritma geniş öncelikli arama algoritması olarak bilinir. Tüm grafiği katmanlar halinde gezerek en kısa yolu bulmaya çalışır. Bu projede başlangıç istasyonundan hareket ederken, ilk olarak komşu istasyonlar keşfedilir ve sıraya eklenir. Ardından sıradaki her yeni istasyonun komşuları sırasıyla keşfedilir. BFS algoritması, her bir istasyonu yalnızca bir kez ziyaret eder, bu sayede en az aktarmalı yolu bulur. FIFO (İlk giren, ilk çıkar) prensibiyle çalışan bir kuyruk yapısı kullanılarak istasyonlar sıraya eklenir ve çıkarılır. Hedef istasyona ulaşana kadar bu işlem devam eder. Bulunamazsa none döndürülür.

Bu algoritmayı kullanma sebebimiz BFS algoritmasının tüm komşuları gezme prensibinin en kısa yolu bulmaya FIFO prensibiyle çalışması sayesinde uygunluğu diyebiliriz.

A* Algoritması:

Bu algoritma bir temel olarak bir şeyin en az maliyetli yolunu bulmaya çalışırken kullanılır. Bu projede de maliyet süreyi ifade etmektedir. A* algoritması, öncelik kuyruğu kullanarak her adımda en düşük toplam maliyete sahip istasyonu işler. Bu sayede en hızlı rota bulma hedeflenir. Eğer hedef istasyona ulaşılabiliyorsa, yol ve toplam süre döndürülür. Eğer ulaşılamazsa, none döndürülür.

Bu algoritmayı kullanma sebebimiz A* algoritmasının öngörüsel bilgi kullanması sayesinde hem gerçek maliyeti hem de hedefe olan tahmini mesafeyi göz önüne alarak çalışmasıdır. Bu sayede ulaşım planları gibi karmaşık sistemlerde A* algoritması birçok etmeni göz önünde bulundurarak en düşük maliyeti seçme işlemi yapabilir.

Örnek Kullanım
"""
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

"""
Çıktı: 
=== Test Senaryoları ===

1. AŞTİ'den OSB'ye:
En az aktarmalı rota: AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB
Aktarmalar:
Kızılay (Mavi Hat) -> Kızılay (Kırmızı Hat)

2. Batıkent'ten Keçiören'e:
En hızlı rota (21 dakika): Batıkent -> Demetevler -> Gar -> Keçiören
Aktarmalar:

3. Keçiören'den AŞTİ'ye:
En hızlı rota (19 dakika): Keçiören -> Gar -> Gar -> Sıhhiye -> Kızılay -> AŞTİ
Aktarmalar:
Gar (Turuncu Hat) -> Gar (Mavi Hat)

Projeyi Geliştirme Fikirleri

Burada görüleceği üzere aktarmanın hangi hattan hangi hatta yapılacağı kafa karışıklığını önlemek için gösterilmesini sağlayan bir çıktı daha yazdım. Bu sayede daha katmanlı ve karmaşık ulaşım sistemleri üzerinde daha net bir rota planı yapılabilir.


