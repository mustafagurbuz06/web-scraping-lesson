# Web scraping'e ilk adım

Beautiful Soup ile ilk ders. Anlatılacak kod tek dosyada: `scraping.py`.

Öğrenci dosyayı yukarıdan aşağı okur, çalıştırır, üstteki iki ayarı değiştirir. Başka modül, klasör ya da alıştırma dosyası yok.

## Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scraping.py
```

## Derste sıra

1. `CANLI_SITE = False` yapın, çalıştırın. Konu: HTML metindir, `find` / `find_all` kartı bulur, eksik fiyat `None` kalır.
2. `CANLI_SITE = True` ve `KAC_SAYFA = 1` yapın. Konu: `requests`, durum kodu, CSS seçici, kesik görünen başlığın `title` özelliğinde tam durması.
3. `KAC_SAYFA = 2` yapın. Konu: sonraki sayfa linkini takip etmek ve `kitaplar.csv`.

Canlı örnek [books.toscrape.com](https://books.toscrape.com/). Bu site scraping alıştırması için yayınlanmıştır. Başka sitede aynı kodu çalıştırmadan önce sitenin buna izin verip vermediğine bakın; istekler arasına bekleme koyun, giriş isteyen sayfaya girmeyin.
