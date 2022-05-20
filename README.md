# KESKITETTY HAKURATKAISU

Keskitetty hakuratkaisu (KEHA) on avoimen lähdekoodin sovellus, jota voidaan käyttää esimerkiksi www-sivujen hakuratkaisuna. KEHA koostuu seuraavista (itsenäisistä) sovelluksista:
* **Käyttöliittymä** - React-sovellus, joka voidaan upottaa www-sivuille. Käyttöliittymän ulkoasua voidaan muokata muun sivuston mukaiseksi. Käyttöliittymä voidaan upottaa koko sivun tapaiseksi hakusivuksi tai pieneksi erilliseksi hakuelementiksi esimerkiksi www-sivujen otsikkopalkkiin.
* **Haku-backend** - Python Flask-sovellus, joka välittää käyttöliittymältä tulevat hakusanat hakumoottorille ja vastaavasti välittää hakumoottorin antamat hakutulokset käyttöliittymälle
* **Elasticsearch** - Hakumoottori, jonka indekseihin www-sivujen sisällöt tallennetaan. 
* **Web crawler** - Python Scrapy-sovellus, jonka avulla voidaan kerätä www-sivuilta tietoja hakumoottorin indeksiin.

Sovelluksen eri osia voidaan ajaa esimerkiksi Docker-konteissa, mutta niiden ajaminen ilman Dockeria on mahdollista.

**Lisenssitieto:**

Keskitetty hakuratkaisu julkaistaan [MIT -lisenssillä](./LICENSE.md) pois lukien alla mainitut osat.

Crawler noudattaa Scrapy:n lisenssiehtoja. Lisenssiehdot löytyvät crawler -projektikansiossa olevasta [LICENSE -tiedostosta](./crawler/LICENSE.md).

Elasticsearchin hakuominaisuudet noudattavat [ELv2 -lisenssiä](https://www.elastic.co/licensing/elastic-license).

---

Sisällysluettelo:

- [KESKITETTY HAKURATKAISU](#keskitetty-hakuratkaisu)
  - [Keskeiset ominaisuudet](#keskeiset-ominaisuudet)
  - [Soveltuuko Keskitetty hakuratkaisu meille?](#soveltuuko-keskitetty-hakuratkaisu-meille)
    - [Crawler](#crawler)
    - [Käyttöliittymä](#käyttöliittymä)
    - [WWWW-sivujen 'best practises' KEHA:n kannalta](#wwww-sivujen-best-practises-kehan-kannalta)
- [Käsitteistöä](#käsitteistöä)
  - [Asiasanat:](#asiasanat)
  - [Sisältötyypit:](#sisältötyypit)
  - [Teemat:](#teemat)
    - [Kaupunginosa Xyz:n päiväkodin sivu](#kaupunginosa-xyzn-päiväkodin-sivu)
    - [Henkilön Zyx yhteystietosivu](#henkilön-zyx-yhteystietosivu)
    - [Tapahtuma Yx:n aikataulusivu](#tapahtuma-yxn-aikataulusivu)

---

## Keskeiset ominaisuudet

Keskitetyn hakuratkaisun perusideana on ollut toteuttaa yleiskäyttöinen sovellus, jonka on minkä tahansa kuntaorganisaation käyttöönotettavissa itsenäisesti. Hakuratkaisun crawlerilla on mahdollista kerätä tietoja julkisilta www-sivuilta, eli esimerkiksi kuntaorganisaation www-sivuilta. Web crawlerista on pyritty tekemään konfiguroitava, jolloin erilaisia www-sivutoteutuksia on pyritty tukemaan mahdollisimman laajasti. Tarkemmat vaatimukset, konfiguraation asetukset ja tekniset rajoitteet löytyvät dokumentaatiosta. 

KEHA tukee erikielisiä www-sivuja, jolloin organisaation www-sivujen eri kieliversioilla on omat sisällöt käytettävissään. Hakumoottori pyrkii myös ymmärtämään suomen kielen taivutusmuotoja.

Käyttöönottajalla on mahdollista vaikuttaa sivustolta poimittaviin tietoihin, haun painotuksiin ja sisältöasetuksiin.

---

## Soveltuuko Keskitetty hakuratkaisu meille?

### Crawler 

* Web crawler pystyy keräämään tietoja julkisilta www-sivuilta. (Kirjautumisen takana oleville sivuille on mahdollista rakentaa tuki.)
  * Jos sivusto on organisaation sisäverkossa, voidaan crawler määrittää keräämään myös niiltä tietoja, kunhan crawlerilla on pääsy ko. sivustolle.
* Pienimmällä määrällä konfigurointia pääsee, jos sivuston rakenne on yhdenmukainen koko sivuston laajuudelta. 
  * Dokumentaatiossa on valmis esimerkkikonfiguraatio, jota hyödyntämällä pääsee alkuun.
* Jos sivusto on toteutettu single-page-appina, crawler ei välttämättä pysty keräämään tietoja sivustolta. 
* Crawlerille voidaan määrittää erilaisia *spidereita*, jotka voivat käydä rakenteeltaan erilaisia sivuja läpi.
* Sivujen html-tagin lang-attribuutissa tulee olla kieli määritettynä. Jos kieltä ei ole määritetty, kyseistä sivua ei indeksoida.

### Käyttöliittymä

Käyttöliittymän pystyy upottamaan mihin tahansa nykyaikaiseen Internet-sivuun. Käyttöliittymän vaatimuksena on suhteellisen tuore selainversio (Edge, Chrome, Firefox, Safari...). Itse käyttöliittymäkomponentti on tehty responsiiviseksi, joten hakuratkaisua pystyy käyttämään myös mobiililaitteilla. Käyttöliittymä on myös saavutettavuusdirektiivin mukainen.


### WWWW-sivujen 'best practices' KEHA:n kannalta

* Web crawler käyttää navigoimiseen linkkejä, joten jokaiselle sivulle on oltava linkki, jotta sivulle voidaan päätyä.
  * Crawlerille voidaan kuitenkin määrittää useita aloitussivuja.
* Sitemap-tiedoston olemassaolo helpottaa ja nopeuttaa crawlausta, koska sitemap-tiedosto voidaan asettaa aloitussivuksi.
* Sivustojen sivujen rakenteen tulisi olla samanlainen koko sivuston laajuudelta.
  * Jos sivuston eri osioiden rakenne eroaa merkittävästi toisistaan, voidaan kuitenkin määrittää useita eri *spidereitä*, jotka käyvät läpi vain tietyn osion sivustosta.
* Sivulla olevat tiedot tulisi laittaa omiin kuvaaviin elementteihinsä (esimerkiksi käyttämällä kuvaavaa elementtiä tai luokkia). Jos esimerkiksi *toimipisteen* yhteystiedot ovat leipätekstin seassa, niitä ei voida kerätä erikseen. Jos taas yhteystiedot ovat omassa elementissään (esimerkiksi `<div class="address">Esimerkkikatu 8</div>`), voidaan kyseisen elementin sisältö poimia haluttuun kenttään käyttöliittymässä.
* Sivun kieli tulee olla jokaisen html-sivun juuressa `lang`-attribuutissa. (Esimerkiksi `<html lang="fi">`)
* Sivun enkoodauksen tulee olla kunnossa (tai ainakin yhtäläinen koko sivuston laajuudelta), esimerkiksi UTF-8.
* Jos sivustolla on käytetty kuvia osoittamaan tiettyä sisältöä (esimerkiksi kuva puhelimesta indikoimaan puhelinnumeroa), haun on mahdotonta löytää tietoa 

# Käyttöönotto

Dokumentaatiokansiosta (docs) löytyy dokumentaatiot eri osioiden konfigurointiin. Käyttöönotto-ohjeet löytyvät myös dokumentaatiokansiosta ([tai täältä](./docs/kayttoonotto.md)).

# Käsitteistöä

## Asiasanat:
* Sivulla erilliseen elementtiin sijoitettu listaus sanoja, jotka kuvaavat sivuston sisältöä tai aihealuetta
* Sanat voivat olla lähtökohtaisesti mitä tahansa ja niitä ei välttämättä ole määritelty tai rajoitettu etukäteen
* Vaikuttavat hakutuloksiin, mutta eivät välttämättä tuloksien sisältöön

## Sisältötyypit:
* Hakutuloksen rakenteeseen liittyvä määritys, joka kertoo, minkälaista tietoa sivu sisältää
* Ennalta määritelty joukko
  * Tyyppeihin on liitetty tietyt tietorakenteet ja sisällöt
  * UI:ssa voidaan esittää eri sisältötyypit eri tavalla
* Sisältötyypit voivat vaikuttaa hakutuloksiin sekä niiden sisältöön
* Tyyppien perusteella voidaan tehdä tarvittaessa rajauksia ja järjestää hakutuloksia

## Teemat:
* Sivun sisältöön liittyvä määritys, jolla määritellään tiettyyn aihealueeseen liittyvät sivut
* Voi olla ennalta määritelty, mutta voi olla myös johonkin ominaisuuteen sidottu dynaaminen määritys
* Sivulla voi olla useita teemoja, jotka voivat tulla useista eri lähteistä
  * Teema voidaan tulkita mm. osoitteesta, sivulla sijaitsevasta tiedosta, metatiedossa olevasta tiedosta
* Teemat voivat olla hierarkisia, mutta eivät välttämättä ole sitä
* Teemat vaikuttavat hakutuloksiin, mutta eivät välttämättä tuloksien sisältöön
* Teemojen perusteella voidaan tehdä tarvittaessa rajauksia ja järjestää hakutuloksia

##Luokitus:
* Yleisluontoinen termi, jolla ei KEHAssa tarkoiteta suoraaan mitään, mutta 'sisältää' sisältötyypit ja teemat.


**Esimerkkejä**
### Kaupunginosa Xyz:n päiväkodin sivu
* Sivun osoite on www.sivut.fi/kasvatus-ja-koulutus/varhaiskasvatus/kaupunginosa_xyz-paivakoti
* Sisältötyypiksi on annettu [tietosivu]
* Asiasanoihin on annettu mm. [varhaiskasvatus, päiväkoti, kaupunginosa_xyz]
* Teema on määritelty sivuston osoitteen perusteella esim. [kasvatus ja koulutus, varhaiskasvatus]

### Henkilön Zyx yhteystietosivu
* Sivun osoite on www.sivut.fi/yhteystiedot/zyx
* Sisältötyypiksi on määritelty [yhteystieto]
* Asiasanat on jätetty antamatta
* Teema on määritelty sivun osoitteen perusteella [yhteystiedot]

### Tapahtuma Yx:n aikataulusivu
* Sivun osoite on www.sivut.fi/tapahtumat/yx/esiintyjat
* Sisältötyypiksi on määritelty [tietosivu]
* Asiasanoihin on annettu mm. [Yx, tapahtuma, esiintyjät, nuoret]
* Teema on määritelty sivun osoitteesta esim. [tapahtumat, yx]