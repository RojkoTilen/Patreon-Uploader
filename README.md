# PATREON UPLOADER
### Aplikacija, ki omogoča samodejno nalaganje skladb na portal Patreon. Ob tem pa se pridobi tudi povezava do Google Drive mape, ki vsebuje vse datoteke za posamezno skladbo.

Iz poljubno določenega direktorija se dinamično preberejo vse mape, nato pa program iz posameznih map razbere posamezne datoteke, ki so potrebne za nalaganje na Patreon storitev. Prav tako se takoj zažene overjanje uporabnika za Google storitev Drive, na kateri imamo shranjene datoteke, ki pripadajo določeni skladbi. Pridobljene poveza skrajšamo z pomočjo URL Shortener-ja. S pomočjo Google Drive knjižnice pridobimo povezave do map, ki vsebujejo pripadajoče datoteke, nato pa povezave še okrajšamo in jih dodamo v sam opis skladbe. Ko se opis generira, lahko začnemo z iterativnim nalaganjem skladb na Patreon portal.

### Tehnološki sklad

* Python
* Selenium 
* Google Drive knjižnica
* URL Shortener.

### Vpostavitev aplikacije:

* Prenos paketa.
* Prenos Selenium knjižnice, Google Drive knjižnice.
* Pridobitev potrebnih google akreditacij
* Zagon
