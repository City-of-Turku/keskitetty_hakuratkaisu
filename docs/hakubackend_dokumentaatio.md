# Hakubackend Dokumentaatio (Keskitetty Hakuratkaisu)

Versio 0.1

Keskitetyssä hakuratkaisussa (KEHA) käyttäjälle tarjotaan haku-API, jonka yli käyttäjälle on mahdollisuus hakea verkkosivujen sisältöjä dokumentti-indeksiin tallennettuista sivustoista. API on toteutettu Pythonin Flask -frameworkilla. Flask on avoimen lähdekoodin sovelluskehys web-kehittämiseen. Haku-backend välittää http-pyyntöinä saamansa kyselyt eteenpäin Elasticsearch-hakumoottorille ja palauttaa hakutulokset vastauksena.

Hakuratkaisun käyttöliittymästä kohdistetaan hakupyynnöt tähän API:in, jossa niistä muodostetaan varsinaiset hakulausekkeet Elasticsearchin dokumentti-indeksiin. Backend palauttaa haussa löydetyt tulokset JSON -objektina. Objekti sisältää varsinaiset tulokset sekä metatietoa tuloksista. API:n yksityiskohdat ovat saatavilla API:n Swagger -dokumentaatiossa (_palvelimen_osoite_/swagger-ui/).

Tämä dokumentti sisältää hakubackendin dokumentaation. Tässä dokumentissa on esitelty ja mainittu vain ne asetukset, joita käyttöönottajan on mahdollisesti tarpeen muuttaa käyttöönoton yhteydessä. Muita kuin tässä dokumentaatiossa mainittuja asetuksia ei ole tarpeen muuttaa tavanomaisessa käytössä. Tarvittaessa lisätietoja asetuksista löytyy Flask:n omalta [dokumentaatiosivustolta](https://flask.palletsprojects.com/en/2.0.x/).

HUOM! Asetusten muuttaminen ilman ymmärrystä kyseisen asetuksen vaikutuksesta palveluun ei ole suositeltavaa! Väärä konfiguraatio saattaa johtaa epätoivottuihin sisältöihin hakutuloksissa tai aiheuttaa jopa palvelunestohyökkäyksen.

## Config.yaml

Config.yaml -tiedosto sisältää kaikkien moduulien asetukset. Se sijaitsee projektin juurikansiossa. Toimintoja muokataan ja ohjataan muuttamalla sen sisältämiä arvoja. Konfiguraation sisältämät asetukset ladataan palvelun Docker -konttien käynnistyessä. Hakubackendin konfigurointiin liittyviä asetuksia on pääasiallisesti `backend` -osiossa. Lisäksi haettavissa oleviin elementteihin ja niiden painotuksiin liittyviä asetuksia on tiedostossa eri kohdissa. Konfiguraatiotiedosto noudattaa YAML -merkintätyyliä (lisätietoja [YAML -dokumentaatiosta](https://yaml.org/spec/1.2.2/)).

# Sisältö

1. [Hakubackendin toiminta ja konfiguraation rakenne](#hakubackendin-toiminta-ja-konfiguraation-rakenne)
2. [Muut hakubackendin asetukset:](#muut-hakubackendin-asetukset)
3. [Poimittavien elementtien hakuasetukset](#poimittavien-elementtien-hakuasetukset)

# Hakubackendin toiminta ja konfiguraation rakenne

Suurin osa hakubackendin asetuksista on määritetty asetustiedoston `backend` -osiossa. Tämän lisäksi joitakin hakuun vaikuttavia asetuksia on myös `elasticsearch` -osiossa sekä elementtien poiminta-asetuksissa.

Esimerkki backend -asetuksista:
```yaml
backend:
  analytics:
    google_analytics_id: <id_here>
    google_tag_manager_id: <id_here>
    matomo:
      base_url: <url_here>
      site_id: <id_here>
```

`analytics: `(`object` | `null`)<br>
    Käyttöliittymä on mahdollista integroida Googlen ja Matomon analytiikkapalveluihin. Tämä elementti sisältää asetukset kyseisten palveluiden integraatiota varten.
    
  HUOM: Tämän elementin sisältö palautetaan `config` -rajapinnan kautta.

- `google_analytics_id: ` (`string`)<br>
    Google Analytics id.

- `google_tag_manager_id: ` (`string`)<br>
    Google Tag Manager id.
    

- `matomo: ` (`object`)<br>
    Matomon analytiikkatunnisteet.
  
  - `base_url: ` (`string`)<br>
  - `site_id: ` (`string`)<br>

# Muut hakubackendin asetukset

### Elasticsearch osion asetukset

Alla on listattu konfiguraatiotiedoston elasticsearch -osion hakubackendiin liittyvät asetukset.

```yaml
elasticsearch:
  hosts:
  index_prefix:
  index_reader_rolename:
  ...
  search_settings:
    field_boosts:
      jokin_kuvaava_boostin_nimi:
        field: "content_type"
        values: "uutinen"
        boost: 1.5
  suggest_settings:
    suggest1:
      completion:
        field: "content_type"
        skip_duplicates: true
        fuzzy:
          fuzzyness: 0
        size: 20
```
`hosts: ` (`list`)<br>
  Hakubackend käyttää tässä määritetty Elasticsearch instanssia hakumoottorina.

`index_prefix: ` (`string`)<br>
  Hakubackend käyttää tässä määritettyä indexsin etuliitettä kyselyissä.

`index_reader_rolename: ` (`string`)<br>
  Hakubackend käyttää tässä määritettyä roolia yhdistäessään Elasticsearchiin.

`search_settings: ` (`object`)<br>
  Hakubackend käyttää tässä määritettyjä asetuksia hakulausekkeen rakentamiseen.
  
- `field_boosts: ` (`object`)<br>
  Objekti, joka sisältää yksittäisiä `field boost` -asetuksia. Field boost antaa lisäpainoarvokertoimen ehdot täyttäville hakutuloksille.

  - `jokin_kuvaava_nimi: ` (`object`)<br>
    Anna jokin kuvaava nimi asetusobjektille, kuten esimerkiksi `uutinen_boost`. Nimi ei vaikuta haun toiminnallisuuteen.

    - `field: ` (`string`)<br>
      Määrittelee kohdekentän, josta annettuja arvoja etsitään. Kenttä voi olla esimerkiksi `content_type` tai `title`.

    - `values ` (`string`)<br>
      Määrittelee etsittävän arvon. Esimerkiksi, jos kohde on `content_type`, voi arvo olla vaikka `uutinen`.

    - `boost: ` (`int` | `float`)<br>
      Määrittelee lisäpainoarvokertoimen, jonka ehdot täyttävät hakutulokset saavat. Arvo tulee olla isompi kuin `0` tai `0.0`.<br>
      HUOM! Alle yhden arvolla ehdot täyttävä kenttä saa negatiivisen painoarvokertoimen.

`suggest_settings: ` (`object`) <br>
  Hakubackend käyttää tässä määritettyjä asetuksia hakusanan ehdottamisessa.

  - `jokin_kuvaava_nimi: ` (`object`)<br>
    Anna jokin kuvaava nimi asetusobjektille, kuten esimerkiksi `ehdotus1`. Nimi ei vaikuta haun toiminnallisuuteen.
    
    - `completion: ` (`object`)<br>
      Vakiotyyppi ehdotukselle. Arvo on aina `completion`.

      - `field: "suggest"` (`string`)<br>
        Kentän nimi josta ehdotuksia haetaan.
        
      - `skip_duplicates: true `(`boolean`)
        Ehdotuksista suodatetaan duplikaatit pois jos tosi.

      - `fuzzy: `(`object`)<br>
        `fuzziness: 0 `(`int`)<br>
        Määrittelee sumean haun voimakkuuden. Yleensä käytetään arvoa nolla.
      
      - `size:` (`int`)<br>
        Määrittelee kuinka monta ehdotusta palautetaan.

### SCRAPY_SETTINGS osion asetukset

Alla on listattu konfiguraatiotiedoston `SCRAPY_SETTINGS` -osion hakubackendiin liittyvät asetukset.

```yaml
SCRAPY_SETTINGS:
  SPIDERS:
    CUSTOM_SETTINGS:
      CONTENT_TYPES_AND_THEMES:
        settings:
          ...
          display_fields:
            ...
        tietosivu:
        uutinen:
        blogi:
        yhteystieto:
        tapahtuma:
        palvelu_tai_asiointikanava:
```

`display_fields: ` - Hakubackend palauttaa tässä määritetyt indeksin kentät kyselyn vastauksena. Ohjeet kenttien mäppäykseen löytyy [Crawlerin dokumentaatiosta](crawler_dokumentaatio.md#spiderin-asetukset).

`uutinen, blogi, yhteystieto, tapahtuma, palvelu_tai_asiointikanava, tietosivu`<br>
HUOM: Tämän objektin avaimet palautetaan `config` -rajapinnan kautta.

---

## Poimittavien elementtien hakuasetukset

Jokaisessa poimittavassa tekstielementissä on mahdollista määrittää hakuun liittyviä asetuksia. Asetukset määritellään elementin `search` -objektiin. Objektissa voidaan määritellä sisältyykö kyseinen elementti hakuun, mikä sen painoarvokerroin on hakutuloksissa sekä näytetäänkö siitä tekstinäyte (snippet) jos hakusana osuu sen sisältöön.

`search: ` (`object` | `boolean` | `null`)<br>
  Sisältää asetusobjektin tai boolean arvon. Jos arvoksi annetaan objekti, sisällytetään elementti hakuun annettujen asetusten mukaisesti. Jos arvo on `true`, sisällytetään elementti hakuun sellaisenaan. Jos arvo on `false`, `null` tai `search` -objekti puuttuu kokonaan, jätetään elementti haun ulkopuolelle erillisenä elementtinä.
  
  - `boost: ` (`int` | `float`)<br>
    Annettua arvoa käytetään haussa kertoimena painottamaan kyseiseen elementtiin osuvaa hakutulosta. Arvo on oltava vähintään `1` tai `1.0`. Jos arvoksi annetaan esimerkiksi 2.0 on kyseiseen elementtiin osuneen hakutuloksen score kaksinkertainen. Score määrittelee järjestyksen, jossa hakutulokset esitetään.

  - `highlight: ` (`boolean`, `object`)<br>
    Jos arvo on `true` tai `object`, palautetaan elementtiin osuneista hakutuloksista snippet (lyhyt näyte). Snippetin ominaisuuksia voidaan tarkentaa antamalla lisäasetuksia [Elasticsearchin dokumentaation mukaisesti](https://www.elastic.co/guide/en/elasticsearch/reference/current/highlighting.html).

```yaml
# YKSITTÄINEN POIMITTAVA BODY-ELEMENTTIASETUS
kuvaava_kohteen_nimi:
  element: "kohde_elementin_nimi"
  attributes: 
    ...
  indexing:
    ...
  search:
    boost: 2.5
    highlight: false
```