"""Web scraping'e ilk adım. Dosyayı yukarıdan aşağı okuyun.

Derste önce CANLI_SITE = False ile çalıştırın.
İkinci yarıda True yapıp KAC_SAYFA değerini 1, sonra 2 yapın.
"""

import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# --- derste değiştireceğiniz iki ayar ---
CANLI_SITE = True
KAC_SAYFA = 2

ORNEK_HTML = """
<html>
  <body>
    <h1>Kampüs Kitabevi</h1>
    <article class="kitap">
      <h2>Sefiller</h2>
      <p class="yazar">Victor Hugo</p>
      <span class="fiyat">89,90 TL</span>
    </article>
    <article class="kitap">
      <h2>Küçük Prens</h2>
      <p class="yazar">Antoine de Saint-Exupéry</p>
      <span class="fiyat">54,00 TL</span>
    </article>
    <article class="kitap">
      <h2>1984</h2>
      <p class="yazar">George Orwell</p>
    </article>
  </body>
</html>
"""


def fiyat_sayiya(metin):
    """'89,90 TL' -> 89.9    '£51.77' -> 51.77    boş -> None"""
    if not metin or not metin.strip():
        return None
    temiz = metin.replace("TL", "").replace("£", "").replace(" ", "").strip()
    # Türkçe sayıda binlik nokta, ondalık virgüldür: 1.250,00
    if "," in temiz:
        temiz = temiz.replace(".", "").replace(",", ".")
    try:
        return float(temiz)
    except ValueError:
        return None


# --- 1) HTML bir metindir. Soup onu ağaca çevirir. ---
print("--- 1) Elimizdeki HTML ---")
corba = BeautifulSoup(ORNEK_HTML, "html.parser")
print("Sayfa başlığı:", corba.find("h1").get_text(strip=True))

# class_ yazılır çünkü class, Python'da ayrı bir kelimedir.
for kart in corba.find_all("article", class_="kitap"):
    baslik = kart.find("h2").get_text(strip=True)
    yazar = kart.find("p", class_="yazar").get_text(strip=True)
    fiyat_etiketi = kart.find("span", class_="fiyat")
    if fiyat_etiketi is None:
        fiyat = None
    else:
        fiyat = fiyat_sayiya(fiyat_etiketi.get_text(strip=True))
    print(baslik, "|", yazar, "|", fiyat)


# --- 2) Aynı bakış, bu kez bir siteye. ---
if not CANLI_SITE:
    print("\nCanlı site kapalı. Açmak için dosyanın başında CANLI_SITE = True yapın.")
    raise SystemExit

print("\n--- 2) Kitap sitesi ---")
# books.toscrape.com scraping alıştırması için yayınlanmıştır.
adres = "https://books.toscrape.com/"
basliklar = {"User-Agent": "VeriBilimiDersBot/1.0 (egitim)"}
hepsi = []

for sayfa_no in range(1, KAC_SAYFA + 1):
    yanit = requests.get(adres, headers=basliklar, timeout=15)
    yanit.raise_for_status()
    yanit.encoding = "utf-8"
    sayfa = BeautifulSoup(yanit.text, "html.parser")
    print("Sayfa", sayfa_no, "durum", yanit.status_code)

    for kart in sayfa.select("article.product_pod"):
        link = kart.select_one("h3 a")
        fiyat_etiketi = kart.select_one("p.price_color")
        hepsi.append(
            {
                # Ekranda ad kesiktir. Tam ad, etiketin title özelliğindedir.
                "baslik": link.get("title"),
                "fiyat": fiyat_sayiya(fiyat_etiketi.get_text(strip=True)),
            }
        )
    print("  bu sayfada", len(sayfa.select("article.product_pod")), "kitap")

    sonraki = sayfa.select_one("li.next a")
    if sonraki is None:
        break
    # Link bazen catalogue/page-2.html, bazen page-3.html olur. urljoin ikisini de çözer.
    adres = urljoin(yanit.url, sonraki.get("href"))
    time.sleep(1)

yol = "kitaplar.csv"
with open(yol, "w", newline="", encoding="utf-8-sig") as dosya:
    yazici = csv.DictWriter(dosya, fieldnames=["baslik", "fiyat"])
    yazici.writeheader()
    yazici.writerows(hepsi)

print("Toplam", len(hepsi), "kitap yazıldı:", yol)
print("İlk üç kayıt:")
for kitap in hepsi[:3]:
    print(" ", kitap["baslik"], "|", kitap["fiyat"])
