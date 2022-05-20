# Crawler Dokumentaatio (Keskitetty Hakuratkaisu)

Versio 0.1

Keskitetyn Hakuratkaisun tiedonpoimintasovellus rakentuu Scrapy 2.5 -kehyksen ympärille. Scrapy on avoimeen lähdekoodiin perustuva sovelluskehys, jonka tarkoitus on käydä läpi verkkosivuja (crawl) sekä poimii sieltä tietoja (scrape). Crawler seuraa sivuilta löytyviä linkkejä annettujen sääntöjen puitteissa ja jatkaa crawlausta kunnes uusia linkkejä ei enää löydy. Scraper poimii asetuksissa määritellyt elementit ja lähettää ne indeksoitavaksi hakupalveluun.

Tämä dokumentti sisältää verkkosivucrawlerin ja -scraperin asetuksien dokumentaation. Tässä dokumentissa on esitelty ja mainittu vain ne asetukset, joita käyttöönottajan on mahdollisesti tarpeen muuttaa käyttöönoton yhteydessä. Muita kuin tässä dokumentaatiossa mainittuja asetuksia ei ole tarpeen muuttaa tavanomaisessa käytössä. Tarvittaessa lisätietoja asetuksista löytyy Scrapy:n omalta [dokumentaatiosivustolta](https://docs.scrapy.org).

HUOM! Asetusten muuttaminen ilman ymmärrystä kyseisen asetuksen vaikutuksesta palveluun ei ole suositeltavaa! Väärä konfiguraatio saattaa johtaa epätoivottuihin sisältöihin hakutuloksissa tai aiheuttaa jopa palvelunestohyökkäyksen.

Crawler noudattaa Scrapy:n lisenssiehtoja. Lisenssiehdot löytyvät crawler -projektikansiossa olevasta [LICENSE -tiedostosta](../crawler/LICENSE.md).

## Config.yaml

Config.yaml -tiedosto sisältää kaikkien moduulien asetukset. Se sijaitsee projektin juurikansiossa. Toimintoja muokataan ja ohjataan muuttamalla sen sisältämiä arvoja. Konfiguraation sisältämät asetukset ladataan palveluiden Docker -konttien käynnistyessä. Tämä dokumentti käsittelee erityisesti konfiguraatiotiedoston __SCRAPY_SETTINGS__ -osiota. Konfiguraatiotiedosto noudattaa YAML -merkintätyyliä (lisätietoja [YAML -dokumentaatiosta](https://yaml.org/spec/1.2.2/)).

# Sisältö

- [Crawler Dokumentaatio (Keskitetty Hakuratkaisu)](#crawler-dokumentaatio-keskitetty-hakuratkaisu)
  - [Config.yaml](#configyaml)
- [Sisältö](#sisältö)
- [Crawlerin toiminta ja konfiguraation rakenne](#crawlerin-toiminta-ja-konfiguraation-rakenne)
- [Crawlerin yleiset asetukset](#crawlerin-yleiset-asetukset)
- [Spiderin asetukset](#spiderin-asetukset)
- [Verkkosivuelementtien poiminta](#verkkosivuelementtien-poiminta)
  - [Verkkosivun määrittely spideriin](#verkkosivun-määrittely-spideriin)
- [Esimerkkikonfiguraatioita](#esimerkkikonfiguraatioita)

# Crawlerin toiminta ja konfiguraation rakenne

Crawler koostuu yhdestä tai useammasta yksittäisistä spiderista, jotka käytännössä suorittavat verkkosivujen latauksen ja tietojen poiminnan. Yhdellä spiderilla voidaan käsitellä rakenteeltaan ja elementtien attribuuteiltaan samankaltaiset ominaisuudet omaavat sivustot tai sivut. Esimerkiksi sisällönhallintajärjestelmien (esim. Drupal tai Wordpress) kautta hallitut sivustot ovat yleensä rakenteeltaan hyvin samankaltaisia ja ne voidaan yleensä crawlata yhdellä spiderilla.

Joissain tapauksissa osa sivustosta voi vaatia enemmän rajoituksia kuin muut osat tai se voi olla rakenteeltaan erilainen tai jostain osasta halutaan poimia vain eri tietoja kuin muualta vaikka rakenne olisikin samanlainen. Tällaisessa tapauksessa alisivustoa varten voidaan asettaa oma spider. Jos spider käsittelee vain osan sivustosta, täytyy se rajoittaa toimimaan vain kyseisellä osalla. Samalla kannattaa estää muut osat käsittelevän spiderin päätyminen toisen spiderin käsittelemälle sivuston osalle.

Jos sivustojen asetukset eivät ole lainkaan yhteensopivia, voidaan sivustot ääritapauksessa käsitellä kahdella erilaisilla asetustiedostoilla varustetuilla erillisillä crawlerilla esimerkiksi eri aikoihin ajettavissa erillisissä Docker -konteissa.

Crawlerin konfiguraatio (`SCRAPY_SETTINGS`) koostuu yleisestä `GENERAL` -osiosta sekä spidereiden asetukset sisältävästä `SPIDERS` -osiosta. Spiders -osio sisältää jokaisen spiderin omat asetukset. Spiderin asetusosio on hyvä nimetä spideria kuvaavalla nimellä, joka on vapaavalintainen crawlerikohtaisesti uniikki merkkijono.

```yaml
SCRAPY_SETTINGS:
    GENERAL:
        ...
    SPIDERS:
        PerusSpider:
            ...
        ErikoisSpider:
            ...
```

Jokainen spider sisältää omat asetuksensa, joilla hallitaan kyseisen spiderin etenemistä sivustolla sekä tietoja sisältävien elementtien poimimista. Näiden lisäksi asetuksissa on indeksointiin, hakuun sekä hakutulosten näyttämiseen liittyviä asetuksia, joita käsitellään yksityiskohtaisemmin [Elasticsearch](.\elastic_dokumentaatio.md) ja [Haku Backend](.\hakubackend_dokumentaatio.md) -dokumentaatioissa.

Spiderin yleisiä asetuksia ovat muun muassa botin nimi, sallitut verkkodomainit, aloitussivut sekä linkkien suodatussäännöt. Yleiset asetukset hallitsevat pääasiassa spiderin etenemistä sivustolla. Näiden lisäksi spiderin asetuksissa on `CUSTOM_SETTINGS` -osio, joka sisältää varsinaiset tietojen poiminnan asetukset sekä tietoihin liittyviä käsittelyasetuksia.

```yaml
SPIDERS:
    PerusSpider:
        BOT_NAME: ...
        ALLOWED_DOMAINS:
            ...
        START_URLS:
            ...
        LINK_EXTRACTOR_RULES:
            ...
        CUSTOM_SETTINGS:
            ...
    ErikoisSpider:
        ...
```

# Crawlerin yleiset asetukset

Seuraavat asetukset vaikuttavat koko crawlerin toimintaan sekä kaikkiin spidereihin. Kyseisen arvon oletusarvo on mainittu arvon nimen jälkeen jos sellainen on olemassa. Jos arvoa ei anneta, käytetään oletusarvoa.

`DEPTH_LIMIT: 0` (`integer`)<br>
    Crawlauksen maksimisyvyys. Arvo määrittelee "kuinka monen linkin syvyyteen" sivustolla mennään aloitussivusta. Yleensä syvyyttä ei ole tarpeen rajoittaa, mutta joissain tapauksissa tällä voidaan tarkemmin hallita ladattavia sivuja. Luku nolla ei rajoita syvyyttä lainkaan.
    
`DOWNLOAD_DELAY: 0` (`integer` | `float`)<br>
    Crawlerin tekemien peräkkäisten HTTP -pyyntöjen minimiviive sekunteina. Viive pyyntöjen välissä kasvattaa crawlauksen kokonaiskestoa, mutta aiheuttaa vähemmän hetkellistä kuormaa kohdesivustolle. Luku nolla ei rajoita pyyntöjen lähettämistä lainkaan ja crawler tekee pyyntöjä niin usein kuin käytössä olevat resurssit sallivat.

`DOWNLOAD_TIMEOUT: 180` (`integer`)<br>
    HTTP -pyynnön aikakatkaisun raja sekunteina. Arvo määrittelee kuinka kauan pyyntöön odotetaan vastausta sivulta ennen kuin pyyntö keskeytetään.

`LOG_ENABLED: true` (`boolean`)<br>
    Sallii tai kieltää logimerkintöjen kirjoituksen.

`LOG_FILE:` (`string` | `null`)<br>
    Kirjoitettavan logitiedoston nimi. Jos arvoksi annetaan `null` kirjoitetaan logimerkinnät konsoliin.

`LOG_FORMAT: '%(asctime)s [%(name)s] %(levelname)s: %(message)s'` (`string`)<br>
    Kirjoitettavan logimerkinnän formaatti. Formaattiasetus käyttää [Pythonin omaa merkintätyyliä](https://docs.python.org/3/library/logging.html#logrecord-attributes).

`LOG_LEVEL: 'DEBUG'` (`'CRITICAL'` | `'ERROR'` | `'WARNING'` | `'INFO'` | `'DEBUG'`)<br>
    Logituksen minimitaso. Debug ja Info -tasoilla logiin merkitään kaikki käsitellyt sivustot. Muilla tasoilla merkinnät rajoittuvat varoituksiin tai häiriöihin toiminnassa valitusta tasosta riippuen.

`LOGSTATS_INTERVAL: 60` (`integer`)<br>
    Crawlausstatistiikan logiinkirjaamisväli sekunteina. Annetuin aikavälein logiin kirjataan tiedot crawlattujen ja indeksoitujen sivujen määrästä sekä crawlaus- ja indeksointitahdista.

`ROBOTSTXT_OBEY: false` (`boolean`)<br>
    Noudatetaanko sivuston robots.txt -tiedoston rajoituksia. Rajoituksien noudattaminen voidaan kytkeä pois päältä esimerkiksi jonkin tietyn sivuston osan käsittelemiseksi jos ei se muuten ole mahdollista. Tällöin tulee riittävistä rajoituksista huolehtia spiderin deny -listauksen kautta!
    <br><br>
    HUOM! Robots.txt -tiedoston sääntöjä tulisi noudattaa aina jos ei ole jotain erityistä perusteltua syytä toimia toisin.

```yaml
# ESIMERKKI TOIMIVASTA KONFIGURAATIOSTA
SCRAPY_SETTINGS:
    GENERAL:
        DEPTH_LIMIT: 0
        DOWNLOAD_DELAY: 0.5
        DOWNLOAD_TIMEOUT: 120
        LOG_ENABLED: true
        LOG_FILE: '210124_crawler.log'
        LOG_FORMAT: '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
        LOG_LEVEL: 'INFO'
        LOGSTATS_INTERVAL: 60
        ROBOTSTXT_OBEY: true
```

# Spiderin asetukset

Seuraavat asetukset vaikuttavat vain kyseiseen spideriin, minkä asetuksissa ne on asetettu.

HUOM! Poikkeuksena tästä on `CUSTOM_SETTINGS` -osio, jossa voidaan asettaa myös samoja asetuksia kuin crawlerin GENERAL -osiossa. Kyseisessä osiossa annetut asetukset ylikirjoittavat crawlerin GENERAL -asetukset kaikkien spidereiden osalta, joten ne kannattaa pitää yhdessä paikassa crawlerin yhteisessä asetusosiossa. Kaikki tämän dokumentin spiderin asetuksia käsittelevässä osassa mainitut asetukset ovat spiderkohtaisia ja eivät vaikuta muiden spidereiden toimintaa.

```yaml
# SPIDERIN KONFIGURAATION RAKENNE
SpiderinNimiSpider:
    BOT_NAME: ...
    ALLOWED_DOMAINS:
        ...
    START_URLS:
        ...
    LINK_EXTRACTOR_RULES:
        ...
    CUSTOM_SETTINGS:
        ...
```

`SpiderinNimiSpider: ` (`string`)<br>
    Spiderin nimi on vapaavalintainen crawlerikohtaisesti uniikki merkkijono. Spiderille on hyvä antaa nimeksi jokin sen tarkoitusta kuvaava lyhyehkö nimi. Nimi ei vaikuta toiminnallisuuteen.

`BOT_NAME: scrapybot` (`string`)<br>
    Sivulataukset tekevän botin nimi.

`ALLOWED_DOMAINS: ` (`list`)<br>
    Lista sallituista domain -nimistä. Jos sivulta löydetty linkki johtaa domainiin, jota ei ole sallitulla listalla, se jätetään huomioimatta.

`START_URLS: ` (`list`)<br>
    Lista www-osoitteista, joista sivustojen läpikäynti aloitetaan. Jos indeksoitavaksi halutut sivut eivät linkity kunnolla tai spider ei jostain muusta syystä pääse linkkejä seuraamalla kaikkiin haluttuihin sivuihin, voidaan useammalla aloitussivulla varmistaa koko sivuston läpikäynti.

`LINK_EXTRACTOR_RULES: ` (`object`)<br>
    Sisältää `allow` ja `deny` listat säännöistä, joilla ohjataan ja rajoitetaan crawlerin etenemistä sivustoilla.

- `allow: ` (`string` | `list`)<br>
    Sisältää listan säännöllisiä lausekkeita, joita käytetään ehtona absoluuttisten url -linkkien poimintaan. Vain url:t, joiden polku sopii säännölliseen lausekkeeseen, päästetään jatkokäsittelyyn. Muita osoitteita ei käsitellä lainkaan. Jos tässä kohdassa sallitaan jokin polku, niin kaikki muut osoitteet ovat kiellettyjä riippumatta `deny` -listan sisällöstä. Tällä asetuksella voidaan rajoittaa indeksointi  tiettyyn polkuun antamalla arvoksi esimerkiksi '/yhteystiedot/'.
    <br><br>
    HUOM! Tämä rajoittaa vain osoitteen polkuosaa (path). Sallitut domainit annetaan `ALLOWED_DOMAINS` -kohdassa.

- `deny: ` (`string` | `list`)<br>
    Sisältää listan säännöllisiä lausekkeita, joita käytetään ehtona absoluuttisten url -linkkien hylkäämiseen. Jos url:n polku sopii annettuun säännölliseen lausekkeeseen, se hylätään. Vaikka url olisi erikseen sallittu `allow` -listassa, jos se sopii `deny` -listaan, se hylätään. Tällä voidaan estää jonkin tietyn polun alle kuuluvien alisivujen käsittely esimerkiksi antamalla arvoksi '/admin/'.
    <br><br>
    HUOM! Tämä rajoittaa vain osoitteen polkuosaa (path). Domainit ovat aina kiellettyjä jos niitä ei löydy `ALLOWED_DOMAINS` -kohdasta.

`CUSTOM_SETTINGS: ` (`object`)<br>
    Sisältää objektin, jossa on `CRAWL_LINKS_ONLY`, `REPLACE_CHARACTERS`, `ITEM_PIPELINES`, `NLP_SETTINGS`, `SCRAPER_SETTINGS` ja `CONTENT_TYPES_AND_THEMES` -asetukset. Nämä asetukset koskevat tietojen poimintaa sivuilta sekä poimitun tiedon käsittelyä.

```yaml
# CUSTOM_SETTINGS OSION RAKENNE
CUSTOM_SETTINGS:
    CRAWL_LINKS_ONLY:
        ...
    REPLACE_CHARACTERS:
        ...
    ITEM_PIPELINES:
        ...
    NLP_SETTINGS:
        ...
    SYNONYM_SETTINGS:
        ...
    SCRAPER_SETTINGS:
        ...
    CONTENT_TYPES_AND_THEMES:
        ...
```

`CRAWL_LINKS_ONLY: ` (`list`)<br>
    Sisältää listan osoitepoluista (path), joista ei poimita sisältöä, mutta sivujen linkkejä seurataan eteenpäin. Polku rajoittaa kaikkia kyseisen polun alle kuuluvia sivuja.

`REPLACE_CHARACTERS: ` (`object`)<br>
    Määrittelee avain-arvo -pareja (`'korvattava': 'korvaava'`), joilla tietty merkkijono korvataan toisella sivuilta poimitusta sisällöstä. Avain on korvattava merkkijono ja arvo on korvaava merkkijono (tyhjä merkkijono poistaa merkkijonon). Merkkijonoina voidaan käyttää myös Unicode hexadesimaaliarvoja `"\x"` -etuliitteellä, kuten esimerkiksi `'\xa0'`, joka vastaa non-breaking-space -merkkiä.

`ITEM_PIPELINES: ` (`object`)<br>
    Määrittelee poimitut tiedot käsittelevät pipeline -luokat sekä niiden järjestyksen. Tätä ei saa muuttaa, ellei pipelineihin ole tehty muutoksia itse. [Lisätietoja Scrapy:n dokumentaatiosta](https://docs.scrapy.org/en/latest/topics/item-pipeline.html).
    <br><br>
    Jos halutaan ajaa NLPPipelinea stemmer_override -analysaattorin käyttämän nlp_dictionary -tiedoston luomiseksi tai täydentämiseksi, voidaan NLPPipeline määritellä suoritettavaksi poimitulle tekstille. NLPPipeline poimii tekstistä sanat, jotka eivät vielä esiinny nlp_dictionary -tiedostossa. Poimitut sanat stemmataan perusmuotoon Turun yliopiston NLP -projektin kehittämän Turku-neural-parser-pipeline -kontin tarjoaman API:n avulla ja tallennetaan tiedostoon. NLP -kontti täytyy olla käynnissä ennen crawlerin ajoa. Kontti vaatii vähintään noin neljä gigatavua vapaata muistia Docker -ympäristöltä. Lisätietoja [NLP -projektista](https://turkunlp.org/finnish_nlp.html) ja [Turku-neural-parser-pipeline -kontista](https://turkunlp.org/Turku-neural-parser-pipeline/docker.html). Kontin käynnistysohje [crawlerin readme -tiedostossa](../crawler/README.md). Pipeline otetaan käyttöön antamalla alla oleva määritys Elasticsearch -pipelinen lisäksi.

```yaml
generic.generic.pipelines.NLPPipeline: 300
```

Jos halutaan kerätä synonyymisanastoon sisältöä crawlerilla, voidaan määrittää käyttööön SynonymGatheringPipeline. Se lisää poimittavaksi määritellyt sanat synonyymisanastotiedostoon, jota voidaan käyttää haussa synonym -token filterin avulla. Synonyymit voidaan kerätä erillisen spiderin avulla ja niitä ei tarvitse syöttää tavallisen indeksointi pipelinen läpi. Tämä mahdollistaa tarkemman määrittelyn lisättävien sanojen poimintaan. Tiedosto käyttää [Solr merkintätapaa](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html#_solr_synonyms). Lisätietoja [Elasticsearchin Synonym -filter dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html).

```yaml
generic.generic.pipelines.SynonymGatheringPipeline: 400
```

`NLP_SETTINGS: ` (`object` | `null`)<br>
    Sisältää NLPPipelinen asetusobjektin. Asetuksilla on merkitystä vain jos NLPPipeline on otettu käyttöön spiderin `ITEM_PIPELINES` -osiossa.

- `nlp_api_address: ` (`string` | `null`)<br>
    NLP -prosessoijan API:n osoite. Oletuksena "http://host.docker.internal:15000".

- `nlp_dictionary_path: ` (`string` | `null`)<br>
    Tiedoston sijaintipolku sekä nimi, johon käsitellyt sanat tallennetaan. Oletuksena käytetään Elasticsearch -kontin yhteydessä luodun volumen mountin polkua "/usr/share/elasticsearch/data/nlp_dictionary_fi.txt".

`SYNONYM_SETTINGS: ` (`object`)<br>
    Sisältään SynonymGatheringPipelinen asetusobjektin. Asetuksilla on merkitystä vain jos kyseinen pipeline on otettu käyttöön spiderin `ITEM_PIPELINES` -osiossa.

- `filepath: ` (`string`)<br>
    Tiedoston sijaintipolku sekä nimi, johon poimitut synonyymit tallennetaan.

- `bidirectional: true ` (`boolean`)<br>
    Määrittelee käytetäänkö kaikkia sanoja toistensa synonyymeinä vai käytetäänkö muita sanoja ainoastaan ensimmäisen sanan synonyyminä.

`SCRAPER_SETTINGS: ` (`object`)<br>
    Määrittelee sivuilta poimittavat tiedot sekä kyseisten tietojen indeksointi- ja hakuasetukset. Sisältää `lang`, `head` ja `body` -objektit.

- `lang: "html"` (`"html"` | `"url": { "path": integer }`)<br>
    \[_Pakollinen_\] Määrittelee mistä verkkosivun kielivalinta poimitaan. Oletuksena kielivalinta poimitaan sivun html -tagista, jolloin arvo on `"html"`. Vaihtoehtoisesti kielivalinta voidaan poimia sivun osoitteen polusta, jolloin arvoksi annetaan `url` -objekti, jossa arvo `path` määrittelee mistä kohdasta url:n polkua arvo poimitaan (`http://www.site.fi/0/1/2/3/etc`).

- `head: ` (`object` | `null`)<br>
    \[_Pakollinen_\] Määrittelee verkkosivun head -elementistä poimittavat tiedot sekä niiden indeksointi- ja hakuasetukset. Objekti voi olla myös `null` jos mitään tietoja ei haluta poimia head -elementistä. Sisältää `content_to_scrape` -objektin.

    - `content_to_scrape: ` (`object` | `null`)<br>
        Sisältää asetukset yksittäisille poimittaville elementeille. Objekti voi olla myös `null` jos mitään tietoja ei haluta poimia head -elementistä.

        - `kuvaava_poimittavan_kohteen_nimi: ` (`string`)<br>
            Vapaavalintainen spiderikohtaisesti uniikki merkkijono. Nimeksi kannattaa antaa merkkijono, joka kuvailee kohdetta ja mahdollisesti jotakin erityisominaisuutta asetuksessa, kuten esimerkiksi `"title_no_search"`. Nimi ei vaikuta toiminnallisuuteen.

            - `element: ` (`string` | `null`)<br>
                Poimittavaksi valittavan elementin nimi (esim. `"meta"` tai `"title"`).

            - `attribute-key: ` (`string` | `null`)<br>
                Poimittavaksi valittavan elementin sisältämän attribuutin nimi (esim. `"property"` tai `"name"`).

            - `attribute: ` (`string` | `null`)<br>
                Poimittavaksi valittavan elementin sisältämän attribuutin arvo (esim. `"title"` tai `"keywords"`).

            - `attribute-value: ` (`string` | `null`)<br>
                Poimittavan tiedon sisältävän attribuutin nimi (esim. `"content"` tai `"href"`).

            - `indexing: {'type': 'text}` (`object` | `null`)<br>
                Indeksointiasetukset poimittavalle tiedolle. Tarkempi kuvaus [elasticsearch -dokumentaatiossa](.\elastic_dokumentaatio.md).
                
            - `search: ` (`boolean` | `object` | `null`)<br>
                Hakuasetukset poimittavalle tiedolle. Arvolla `true` elementti sisältyy hakukoneella haettavissa oleviin tietoihin. Tarkemmat tiedot [hakubackend -dokumentaation](.\hakubackend_dokumentaatio.md) yhteydessä.

        ```yaml
        # YKSITTÄINEN POIMITTAVA HEAD-ELEMENTTIASETUS
        kuvaava_kohteen_nimi:
            element: "kohde_elementin_nimi"
            attribute-key: "valitsevan_attribuutin_avain"
            attribute: "valitsevan_attribuutin_arvo"
            attribute-value: "poimittavan_attribuutin_avain"
            indexing:
                type: "text"
            search:
                true
        ```

- `body: ` (`object`)<br>
    \[_Pakollinen_\] Määrittelee verkkosivun body -elementin sisältä poimittavat tiedot sekä niiden indeksointi- ja hakuasetukset. Lisäksi  määrittää sivun pääsisällön sisältävän elementin, jonka sisälle kaikki muut valinnat kohdistuvat, sekä valinnaiset määritykset erityisesti käsittelyn ulkopuolelle jätettävistä elementeistä. Objekti sisältää pääelementin valitsevat `element`, `class` ja `id` -merkkijonot sekä `exclude_rules` ja `content_to_scrape` -objektit.

    - `element: ` (`string` | `null`)<br>
        Määrittää elementin tagin nimen pääelementille, jonka sisältä muut tiedot poimitaan. Sivun sisällöstä valitaan ensimmäinen annetun niminen elementti ja kaikki sen lapsielementit. Tämä elementti toimii yhdessä `class` ja `id` -asetuksien kanssa rajoittaen elementtien valintaa.

    - `class: ` (`string` | `null`)<br>
        Määrittää merkkijonon, joka täytyy löytyä pääelementiksi valittavan elementin class -attribuuttin arvosta. Sivun sisällöstä valitaan ensimmäinen ehdon täyttävä elementti ja kaikki sen lapsielementit. Tämä elementti toimii yhdessä `element` ja `id` -asetuksien kanssa rajoittaen elementin valintaa.

    - `id: ` (`string` | `null`)<br>
        Määrittää merkkijonon, joka täytyy löytyä pääelementiksi valittavan elementin id -attribuuttin arvosta. Sivun sisällöstä valitaan ensimmäinen ehdon täyttävä elementti ja kaikki sen lapsielementit. Tämä elementti toimii yhdessä `element` ja `class` -asetuksien kanssa rajoittaen elementin valintaa.

    - `exclude_rules: ` (`object` | `null`)<br>
        Määrittää tunnisteet elementeille, jotka jätetään tietojenpoiminnan ulkopuolelle. Tällaisia voivat olla esimerkiksi valikko- tai navigointielementit tai jokin muu elementti, joka sisältää tietoa, jota ei haluta indeksoida hakukonetta varten.

        ```yaml
        # ESIMERKKI EXCLUDE -SÄÄNNÖSTÄ:
        exclude_rules:
            ruleset1:
                element: "div"
                class: "non-public"
                id: null
            ruleset2:
                ...
        ```

    - `content_to_scrape: ` (`object`)<br>
        \[_Pakollinen_\] Sisältää asetukset yksittäisille poimittaville elementeille. Objekti on pakollinen ja sen pitää sisältää vähintään yksi poimittava kohde.

        - `kuvaava_poimittavan_kohteen_nimi: ` (`string`)<br>
            Vapaavalintainen spiderikohtaisesti uniikki merkkijono. Nimeksi kannattaa antaa merkkijono, joka kuvailee kohdetta ja mahdollisesti jotakin erityisominaisuutta asetuksessa, kuten esimerkiksi `"div_infobox"` tai `"infobox_class_rightpanel"`. Nimi ei vaikuta toiminnallisuuteen.

            - `element: ` (`string` | `null`)<br>
                Poimittavaksi valittavan elementin nimi (esim. `"div"` tai `"p"`).

            - `attributes: ` (`object` | `null`)<br>
                Poimittavaksi valittavan elementin attribuuttien asetusobjekti. Sisältää esimerkiksi `class` ja `id` arvot.

                - `class: ` (`string` | `null`)<br>
                    Merkkijono, joka täytyy sisältyä poimittavaksi valittavan elementin sisältämään `class` -attribuutin arvoon.

                - `id: ` (`string` | `null`)<br>
                    Merkkijono, joka täytyy sisältyä poimittavaksi valittavan elementin sisältämään `id` -attribuutin arvoon.

            - `indexing: {'type': 'text}` (`object` | `null`)<br>
                Indeksointiasetukset poimittavalle tiedolle. Tarkempi kuvaus [elasticsearch -dokumentaatiossa](.\elastic_dokumentaatio.md).
                
            - `search: ` (`boolean` | `object` | `null`)<br>
                Hakuasetukset poimittavalle tiedolle. Antamalla arvon `true` tai asetusobjektin elementti sisältyy hakukoneella haettavissa oleviin tietoihin. Tarkemmat tiedot [hakubackend -dokumentaation](.\hakubackend_dokumentaatio.md) yhteydessä.
                
            - `image:` (`object`)<br>
                Jos halutaan poimia linkki kuvaan, niin poiminta-asetuksiin lisätään `image` -objekti, joka sisältää kuvan tietojen poiminta-asetukset.<br>
                HUOM! Tätä ei pidä lisätä mihinkään muuhun kuin kuvaelementin yhteyteen!

                - `target_element: ` (`string`)<br>
                    Kuvaelementin tagin nimi (yleensä `"img"`)

                - `target_attributes: `(`object`)<br>
                    Kohdekuvan attribuuttivalinnat. Kuvan attribuuttien arvojen täytyy sisältää annettujen attribuuttien arvot.
                    - `class: ` (`string` | `null`)
                    - `id: ` (`string` | `null`)

                - `content_attribute: ` (`string`)<br>
                    Kuvan url:n sisältävä attribuutti (yleensä `"src"`).

                - `alt_text: ` (`string`)<br>
                    Kuvan vaihtoehtoisen tekstin sisältävä attribuutti (yleensä `"alt"`).

                - `title: ` (`string`)<br>
                    Kuvan otsikon sisältävä attribuutti (yleensä `"title"`).
    
        ```yaml
        # YKSITTÄINEN POIMITTAVA BODY-ELEMENTTIASETUS
        kuvaava_kohteen_nimi:
            element: "kohde_elementin_nimi"
            attributes: 
                class: "class_attribuutin_arvo"
                id: "id_attribuutin_arvo"
            indexing:
                type: "text"
            search:
                true
        ```

`CONTENT_TYPES_AND_THEMES: ` (`object`)<br>
    Määrittää tietojen kohdentamisasetukset (mappings), jolla kohdennetaan indeksoinnin yhteydessä sivulta poimitut tiedot oikeisiin hakutulokseen sisältyviin tietokenttiin. Objekti sisältää sisältötyyppien asetuksia, joilla määritellään kyseisen sivun sisältötyypin valinta. Lisäksi objektiin sisältyy `settings` -osio, jossa määritellään tietojen valinta-asetuksia. 

- `settings: ` (`object`)<br>
    - `parse_content_type_from: ` (`"url"` | `"breadcrumb"` | `element_name`)<br>
        Määrittelee kohteen, mistä sivun sisältötyyppi poimitaan. Vaihtoehtoja ovat url, murupolku tai jokin muu sivulla sijaitseva elementti. Murupolusta ja url:sta poimitaan yksittäiset polun osat sisältötyyppien avainsanavertailuun.

    - `parse_themes_from: ` (`"url"` | `"breadcrumb"` | `null`)<br>
        Määrittelee kohteen, mistä sivun teemat poimitaan. Vaihtoehtoja ovat url, murupolku tai null jos tieto sijaitsee jossain muussa elementissä. Murupolusta ja url:sta poimitaan yksittäiset polun osat teemoiksi.

    - `default_content_type: "tietosivu" `(`string`)<br>
        Määrittää oletussisältötyypin. Jos mitään muuta tyyppiä ei pystytä valitsemaan sivun sisältötyypiksi, niin tyypiksi valitaan tämä.

    - `remove_last_part_from_url_path: ` (`boolean`)<br>
        Jos tosi, poimittaessa teemoja url:sta, jätetään pois viimeinen osa. Usein viimeinen osa on sivun oma nimi ja siten ei varsinaisesti ole osa sivun teemaa.

    - `remove_first_part_from_breadcrumb: ` (`boolean`)<br>
        Jos tosi, poimittaessa teemoja murupolusta, jätetään pois ensimmäinen osa. Usein ensimmäinen osa on etusivu tai jokin muu pysyvä aloitusteksti ja sen vuoksi se ei varsinaisesti ole osa sivun teemaa.

    - `remove_last_part_from_breadcrumb: ` (`boolean`)<br>
        Jos tosi, poimittaessa teemoja murupolusta, jätetään pois viimeinen osa. Usein viimeinen osa on sivun oma nimi ja siten ei varsinaisesti ole osa sivun teemaa.

    - `display_fields: ` (`object`)<br>
        Määrittelee hakutuloksissa näytettävät kentät ja niihin kohdentuvat sisällöt sekä kohdentamisen asetukset. Kenttiä ovat `title`, `text`, `publish_date`, `modify_date`, `writer`, `location`, `date`, `time`, `url`, `image_url`, `keywords`, `content_type` ja `themes`.

        - `kentan_nimi: ` (`object`)<br>
            Sisältää yksittäisen hakutulokseen sisältyvän kentän asetukset.

            - `default: ` (`string` | `null`)<br>
                Sisältää oletusarvon, jota käytetään jos mitään muuta tietoa ei sivulta saada poimittua.

            - `append_values: `(`boolean` | `null`)<br>
                Jos `true`, lisätään kaikki sivulta poimitut tiedot kentään. Jos `false`, kenttään lisätään ainoastaan ensimmäinen sivulta poimittu tieto. Eli jos `index_fields` kohtaan on laitettu useampi arvo (esim. "header1" ja "header2") ja `append_values` on `false`, päätyy ainoastaan ensimmäinen arvo ("header1") näytettäväksi. Jos arvo on `true`, näytetään molemmat arvot ("header1" sekä "header2").

            - `index_fields: ` (`list` | `null`)<br>
                Lista poimituista tiedoista, jotka tähän kenttään liitetään. Arvot ovat poimittujen arvojen nimiä, jotka on määritetty aiemmin `SCRAPER_SETTINGS` -asetuksissa.

            - `suggest: ` (`boolean` | `null`)<br>
                Jos `true`, sivulta poimittuja arvoja käytetään hakukoneen hakukentän sanojen täydennysehdotuksissa.

- `sisaltotyypin_nimi: ` (`list`)<br>
    Sisältää listan kyseiseen tietotyyppiin sisältyvistä avainsanoista. Jos avainsana esiintyy sivulla esimerkiksi url:ssa tai murupolussa valitaan kyseisen sanan sisältävä tyyppi sivun tietotyypiksi. Avainsanojen lähteet on määritelty tarkemmin `settings` -objektissa. Sisältötyyppejä ovat muun muassa `uutinen`, `blogi`, `yhteystieto`, `tapahtuma`, `palvelu_tai_asiointikanava` sekä `tietosivu`.

    ``` yaml
    CONTENT_TYPES_AND_THEMES:
        uutinen:
            - "uutinen"
            - "uutiset"
        blogi:
            - "blogi"
        yhteystieto:
            - "yhteystieto"
        tapahtuma:
            - "event"
        palvelu_tai_asiointikanava:
            - "service"
        tietosivu:

        settings:
            parse_content_type_from: "url"
            parse_themes_from: "breadcrumb"
            default_content_type: "tietosivu"
            remove_last_part_from_url_path: true
            remove_first_part_from_breadcrumb: true
            remove_last_part_from_breadcrumb: true
            display_fields:
                title: 
                    default: ""
                    append_values: true
                    index_fields:
                        - "title"
                        - "header1"
                text:
                    append_values: false
                    index_fields:
                        - "text_content"
                publish_date:
                    index_fields:
                modify_date:
                    index_fields:
                writer:
                    default: "Tuntematon kirjoittaja"
                    index_fields:
                location:
                    index_fields:
                date: 
                    index_fields:
                time:
                    index_fields:
                url:
                    index_fields:
                image_url:
                    index_fields:
                        - "content_image"
                keywords:
                    index_fields:
                        - "keywords"
                    suggest: true
                content_type: 
                    index_fields:
                        - "content_type"
                themes:
                    index_fields:
                        - "themes"
                    suggest: true
        
    ```

Esimerkki kokonaisesta `SCRAPY_SETTINGS` -asetuksesta.
```yaml
SCRAPY_SETTINGS:
    GENERAL:
        DEPTH_LIMIT: 0
        DOWNLOAD_DELAY: 0.5
        DOWNLOAD_TIMEOUT: 120
        LOG_ENABLED: true
        LOG_FILE: '210124_crawler.log'
        LOG_FORMAT: '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
        LOG_LEVEL: 'INFO'
        LOGSTATS_INTERVAL: 60
        ROBOTSTXT_OBEY: true
    SPIDERS:
        PerusSpider:
            BOT_NAME: "kehabot"
            ALLOWED_DOMAINS:
                - "https://www.some_site.fi"
            START_URLS:
                - "https://www.some_site.fi"
            LINK_EXTRACTOR_RULES:
                allow:
                deny:
                    - "/admin/"
                    - "/login/"
            CUSTOM_SETTINGS:
                CRAWL_LINKS_ONLY:
                    - "/page_listing/"
                REPLACE_CHARACTERS:
                    "\xa0": " "
                ITEM_PIPELINES:
                    generic.generic.pipelines.ElasticsearchPipeline: 500
                SCRAPER_SETTINGS:
                    lang: "html"
                    head:
                        content_to_scrape:
                            title:
                                element: "title"
                            keywords:
                                element: "meta"
                                attribute-key: "name"
                                attribute: "keywords"
                                attribute-value: "content"
                                indexing:
                                    type: "text"
                                search:
                                    true
                    body:
                        element: "div"
                        class: "l-main"
                        id: null
                        exclude_rules:
                            ruleset1:
                                element: "div"
                                class: "menu"
                                id: null
                        content_to_scrape:
                            header1:
                                element: "h1"
                                class: "main_header"
                                id: null
                                indexing:
                                    type: "text"
                                search:
                                    true
                            text_content
                                element: "p"
                                class: null
                                id: null
                                indexing:
                                    type: "text"
                                search:
                                    true
                            content_image:
                                element: "div"
                                    class: main_image
                                    id: null
                                    image:
                                        element: "img"
                                        target_attributes:
                                            class: null
                                            id: null
                                        content_attribute: "src"
                                        alt_text: "alt"
                                        title: "title"
                            keywords
                                element: "p"
                                class: null
                                id: null
                                indexing:
                                    type: "text"
                                search:
                                    true
                    
                CONTENT_TYPES_AND_THEMES:
                    tietosivu:
                    uutinen:
                        - "uutinen"
                        - "uutiset"
                    blogi:
                        - "blogi"
                    yhteystieto:
                        - "yhteystieto"
                    tapahtuma:
                        - "event"
                    palvelu_tai_asiointikanava:
                        - "service"
                    settings:
                        parse_content_type_from: "url"
                        parse_themes_from: "breadcrumb"
                        default_content_type: "tietosivu"
                        remove_last_part_from_url_path: true
                        remove_first_part_from_breadcrumb: true
                        remove_last_part_from_breadcrumb: true
                        display_fields:
                            title: 
                                default: ""
                                append_values: true
                                index_fields:
                                    - "title"
                                    - "header1"
                            text:
                                append_values: false
                                index_fields:
                                    - "text_content"
                            publish_date:
                                index_fields:
                            modify_date:
                                index_fields:
                            writer:
                                default: "Tuntematon kirjoittaja"
                                index_fields:
                            location:
                                index_fields:
                            date: 
                                index_fields:
                            time:
                                index_fields:
                            url:
                                index_fields:
                            image_url:
                                index_fields:
                                    - "content_image"
                            keywords:
                                index_fields:
                                    - "keywords"
                                suggest: true
                            content_type: 
                                index_fields:
                                    - "content_type"
                            themes:
                                index_fields:
                                    - "themes"
                                suggest: true
```

# Verkkosivuelementtien poiminta

Hakuratkaisun käyttöönottajalla tulee olla perusymmärrys HTML-sivujen rakenteesta. Alla on hyvin lyhyt kuvaus asetuksien tekoon tarvittavista HTML:n osista. Se ei ole kuitenkaan tyhjentävä ja joissain erikoistapauksissa sivun sisältö saattaa poiketa tästä kaavasta.

Verkkosivut koostuvat lähes aina HTML-tageista, joilla erotellaan erilaisia sisältöjä toisistaan. Tagi koostuu hakasulkeista, joiden sisälle on sijoitettu tagin tiedot, kuten nimi ja mahdollisesti muita arvoja. HTML -elementti koostuu yleensä aloitustagista, tekstisisällöstä sekä lopetustagista. Aloitustagissa on usein mukana myös attribuutteja, jotka sisältävät elementtien tunnisteita sekä erilaisia ominaisuuksia ja toiminnallisuuksia ohjaavia arvoja. Lopetustagin tunnistaa kauttaviivasta tagin ensimmäisenä merkkinä. Joskus lopetustagi on yhdistetty aloitustagiin, jolloin kauttaviiva on tagin viimeisenä merkkinä ennen hakasuljetta.

Alla olevissa esimerkeissä on kolme erilaista HTML-elementtiä. Kaksi ensimmäistä ovat tavallisia aloitus- ja lopetustageista rakentuvia tekstiä sisältäviä elementtejä. Nämä ovat yleisimmin HTML-sivun `body` -elementin sisällä esiintyviä sisältöelementtejä. Kolmas esimerkki koostuu vain avaavasta tagista, ja koska sillä ei ole varsinaista tekstisisältöä, sillä ei ole sulkevaa tagia. Näitä löytyy useimmin sivun `head` -elementin sisältä ja niissä varsinainen sisältö on sijoitettu attribuuttien arvoihin.

Esimerkki 1: `<div class="content" id="main">Jotain tekstisisältöä.</div>`

Esimerkki 2: `<a href="https://www.some_site.fi">Linkki Some Sitelle</a>`

Esimerkki 3: `<meta property="og:title" content="Etusivu">`

Verkkosivusisältöjen poiminta tehdään näissä asetuksissa pääosin kohdistamalla valinta oikeaan kohteeseen elementin nimen sekä attribuuttien perusteella. Elementin nimi on ensimmäinen html-tagin sisällä oleva teksti, kuten esimerkiksi `div`, `a` tai `meta`. Elementissä voi olla myös attribuutteja, jotka tulevat elementin nimen jälkeen. Attribuutin arvo on attribuutin nimen perässä erotettuna yhtäkuin -merkillä ja ympäröitynä lainausmerkeillä. Ylläolevassa esimerkissä attribuutteja ovat `class`, `id`, `href`, `property` sekä `content`.

## Verkkosivun määrittely spideriin

Hakukoneen indeksoimat ja sen käyttäjän haettavissa olevat kohteet määritellään konfiguraation `SPIDERS` -osion alla oleviin yksittäisiin spidereihin. Yksittäinen spider voi pitää sisällään määritykset useampaan sivustoon, tiettyyn yksittäiseen sivustoon tai tiettyyn sivuston osaan. Kun käyttäjä hakee hakusanalla sivua, kohdistetaan haku näiden spidereiden keräämiin tietoihin, jotka hakukone on indeksoinut asetusten mukaisesti.

HUOM! Jos spider ei poimi jotakin tietoa sivulta ja hakukone ei sitä indeksoi, sivua ei myöskään voi löytää kyseisellä tiedolla hakukoneesta!

Sivustoa tutkiessa kannattaa kirjata muistiin asetuksien tekoa varten tässä ohjeessa mainittujen elementtien tunnisteita. Muistiinpanot helpottavat asetuksien tekemistä, kun yksityiskohtia ei tarvitse etsiä sivuston koodista. 

Jokaisen osion loppuun on koottu ranskalaisilla viivoilla oleellisimmat tiedot helpottamaan tietojen keräämistä. Vastaamalla näihin kysymyksiin huolella pystyt tekemään suurimman osan spiderin määrittelystä.
    
Sivun HTML -elementtien tarkastelussa kannattaa käyttää hyväksi selaimen kehitystyökaluja. Esimerkiksi Firefoxissa on oma Inspect -työkalunsa ([Mozillan Inspect ohjesivu](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Open_the_Inspector)). Myös muilta selaimilta löytyy vastaavat työkalut.

1. Tunnista sivuston rakenne

    Tutustu ensin sivustoon laajemmin. Koostuuko sivusto useista eri alidomaineista (esim. www.site.fi, events.site.fi) vai onko kaikki saman domainin alla? Kaikki halutut domainit täytyy lisätä `ALLOWED_DOMAINS` -listalle, että ne pystytään käymään läpi. Samalla voidaan rajoittaa haku vain haluttuihin domaineihin.

    Crawlausasetuksien määrittely kannattaa aloittaa tutkimalla sivuston rakennetta HTML-koodista. Onko sivustolla jokin tietty toistuva rakenne. Usein sisällönhallintapalvelun (esim. Drupal) päälle rakennettu sivusto on hyvin homogeeninen rakenteeltaan ja valtaosa sivuista noudattaa tiettyä kaavaa. Tämä helpottaa määrittelyä huomattavasti.

    Etsi sivun pääelementti, joka sisältää kaiken varsinaisen sisällön. Etsi kyseisen elementin tunnisteet, kuten elementin nimi sekä elementin yksilöivät `class`- ja `id` -attribuutit. Yleensä pääelementille on annettu jokin kuvaava `class` -attribuutti, kuten `"main"` tai `"content"`. Näin ei kuitenkaan välttämättä aina ole. Jos sivustolla ei ole mitään erityistä pääelementtiä, voidaan käyttää `body` -elementtiä sellaisenaan. Pääelementin tiedot tulevat `CUSTOM_SETTINGS` > `SCRAPER_SETTINGS` > `body` -osion määrityksiin.

    Seuraavaksi kannattaa etsiä mahdolliset toistuvat rakenteet, joita ei haluta mukaan hakuun tai joista ei ole hakukoneen käyttäjälle hyötyä. Tällaisia ovat muun muassa valikot tai bannerit, joiden sisältö ei liity suoraan kyseiseen sivuun. Näiden elementtien tunnisteet lisätään `body` -osion `exclude_rules` -kohtaan. Jos elementti ei sisälly pääelementtiin, sitä ei tarvitse välttämättä lisätä, mutta siitä ei ole haittaakaan crawlauksen kannalta.

    Tarkista myös mitä eri kieliversioita sivustosta on tehty ja miten kielikoodit on merkitty sivustolle. Yleisimmät vaihtoehdot ovat sivun koodin html -tagiin sijoitettu lang -attribuutti sekä sivun osoitteeseen sijoitettu kielivalintaa osoittava polun osa. Tulevatko kaikki kieliversiot haun piiriin? Kielivalinnat vaikuttavat sivujen indeksointiin ja sitä kautta hakujen osuvuuteen eri kielillä.

    - Onko sivustolla useita eri domaineja, joiden tulee sisältyä hakuun?
    - Mistä sivuston sisällön kannalta oleelliset tiedot löytyvät?
    - Mikä on sivuston pääelementti ja miten se tunnistetaan?
    - Mitkä elementit halutaan jättää huomioimatta?
    - Mitä kieliversioita sivustolta löytyy ja mistä ne tunnistetaan?

2. Tunnista oleelliset elementit sivun `body` -elementistä

    HTML -koodissa sivun `body` -elementti sisältää sivun näkyvät osat. Siihen liittyvät kohteet määritellään spiderin asetuksien `CUSTOM_SETTINGS` > `SCRAPER_SETTINGS` > `body` > `content_to_scrape` -osiossa.

    Tutki `body` -elementin rakennetta ja tunnista siitä sellaiset elementit, jotka sisältävät oleellista tietoa. Erityisesti kannattaa kiinnittää huomiota tietoihin, joista on hyötyä kyseisen sivun sisällön erottelussa muista sivuista.

    Eriteltyjen tietojen vaikutusta hakuun on mahdollista muuttaa yksilöllisesti, mutta mikään ei estä poimimasta kaikkea esimerkiksi yhteen tietueeseen. Tällöin haku löytää kyllä sivun, mutta se ei välttämättä järjestä tuloksia kovin hyvin käyttäjän haluamaan järjestykseen.

    Usein erityisen hyödyllisiä rakenteita ovat muun muassa otsikot, avainsanat, erilliset ingressit, infolaatikot sekä muut vastaavat kohdennettua tietoa sisältävät elementit.

    Toisistaan pitää erotella myös sellaiset elementit, joiden painoarvoa haussa halutaan muuttaa. Tällaisia voivat olla esimerkiksi avainsanat, infolaatikot tai yhteystiedot. Leipätekstit (esim. `<p>` -elementit) kannattaa poimia myös erilleen muusta tiedosta, jolloin sen painoarvoa voidaan myös tarvittaessa muuttaa.

    Elementin tunnisteet tulisi määrittää sillä tarkkuudella, että poimitaan vain halutut tiedot. Jos poimittavia saman nimisiä elementtejä on useita, poimii crawler kaikki ehtoihin sopivat elementit sivulta. Tarkennuksessa voidaan käyttää attribuutteja.

    HUOM! Jos jotakin tietoa ei poimita sivulta, niin se ei myöskään löydy haussa!

    - Mitä sivulla olevia tietoja haluan erityisesti painottaa haussa?
    - Millä tunnisteilla löydän sivulta kyseiset tiedot?
    - Tuleeko kaikki tarvittava tieto hakuun mukaan?

3. Tunnista oleelliset elementit sivun `head` -elementistä

    HTML -koodissa sivun `head` -elementti sisältää metatietoja sivusta. Siihen liittyvät kohteet määritellään spiderin asetuksien `CUSTOM_SETTINGS` > `SCRAPER_SETTINGS` > `head` > `content_to_scrape` -osiossa.

    Tutki `head` -elementin sisältämiä tietoja ja tunnista niistä sellaiset elementit, jotka sisältävät oleellista tietoa. Erityisesti kannattaa kiinnittää huomiota tietoihin, joista on hyötyä kyseisen sivun erottelussa muista sivuista. Tällaisia tietoja voivat olla esimerkiksi otsikko, kuvaus, avainsanat tai muu vastaava sivun sisältöä tai merkitystä määrittelevä metatieto. Jos vain saatavilla, niin kannattaa hyödyntää hakukoneille ja muille sovelluksille määriteltyjä metatietoja, kuten esimerkiksi "og:" -alkuiset open graph -metatiedot.

    Yleensä `head` -elementin sisältämät elementit poikkeavat tavanomaisista elementeistä siinä, ettei niissä ole välttämättä erillistä tekstisisältöä (tagien välissä). Niiden varsinainen sisältö on usein attribuuteissa olevaa informaatiota. Attribuuteissa oleva tieto voidaan poimia `head` -elementistä indeksoitavaksi.

    - Mitä sivun metatiedoissa olevia tietoja halutaan haussa käyttää?
    - Millä tunnisteilla löydän sivulta kyseiset tiedot?

4. Onko jokin sivuston osa erilainen?

    Seuraavaksi kannattaa tutkia, että onko jokin sivuston osa rakenteeltaan erilainen kuin muu sivusto. Sivustolla voi olla esimerkiksi alisivusto yhteystiedoille, jossa ei ole kuin tiettyjä tietoja, joita ei muilla sivuilla yleensä ole. 

    Jos poimittavia elementtejä on paljon, niin voi olla järkevää luoda niitä varten erillinen spider, johon konfiguroidaan vain tämä osio. Hakukone rakentaa hakutulokset kaikkien spidereiden keräämistä tiedoista, joten ei haittaa, jos spidereissa on erilaiset poimittavat elementit.

    Jos alisivustolla on vain pieni määrä erillisiä poimittavia elementtejä, saattaa olla helpompaa muokata varsinaista spideria soveltumaan myös näille sivuille. Aina tämä ei kuitenkaan ole mahdollista jos esimerkiksi joudutaan asettamaan rajoituksia, jotka estävät toisen spiderin käytön. Tässä tapauksessa ainoaksi vaihtoehdoksi jää konfiguroida erillinen spider.

    Kun käytetään useampaa spideria, pitää muistaa rajoittaa spidereiden pääsyä toisen spiderin läpikäymälle alueelle. Tällä estetään sivujen indeksointi väärillä asetuksilla ja mahdollisesti vaillinaiset tiedot hakutuloksissa sekä sivujen huono löydettävyys.

    Alisivuston läpikäyvä spider on yksinkertaista rajoittaa konfiguroimalla sallituksi poluksi ainoastaan kyseinen alisivun polku. Toisiin spidereihin täytyy määrittää kyseinen polku kielletylle listalle. Molemmat asetukset löytyvät spiderin `LINK_EXTRACTOR_RULES` -osiosta.

    - Onko sivustolla osioita, jotka ovat rakenteeltaan poikkeavia?
    - Voinko yhdistää poikkeavat tiedot olemassa olevaan spideriin?
    - Onko poikkeavilla sivuilla paljon poimittavia elementtejä, joita ei muualla ole?
    - Millä rajauksilla saadaan estettyä spidereiden päällekkäinen toiminta?
    
5. Rajoitukset

    Crawleriin voidaan asettaa useita erilaisia sääntöjä, joilla ohjataan sen liikkumista ja toimintaa sivustolla. On tärkeää määrittää spiderin toiminta-alue oikein, ettei hakuun päädy sinne kuulumattomia tietoja ja, että hakuun kuuluvat tiedot tulevat indeksoiduksi.

    Crawlerin yleisissä asetuksista löytyy `ROBOTSTXT_OBEY` -asetus, joka määrittelee noudattaako crawler saatavilla olevaa robots.txt -tiedostoa. Tiedostoon kirjatuilla rajoituksilla voidaan rajoittaa tiettyjen alisivujen läpikäyntiä. Jos `ROBOTSTXT_OBEY` -asetus on `true`, ei crawler mene sivuille, jotka ovat tiedostossa kiellettyjä.
    
    Joissain tapauksissa voi syntyä tilanteita, jolloin robots.txt ei mahdollista pääsyä johonkin tiettyyn sivuun, joka halutaan kuitenkin haun piiriin. Tällöin voi olla perusteltua olla noudattamatta tiedoston rajoituksia. Siinä tapauksessa pitää kuitenkin erityisen tarkkaan huolehtia, että tarvittavat rajoitukset kirjataan kiellettyjen polkujen listalle `LINK_EXTRACTOR_RULES` -osion `deny` -sääntöihin!

    Jo aiemmin mainittu sallittujen domainien `ALLOWED_DOMAINS` -lista rajoittaa pääsyä sivuille. Jos ladattavan sivun tai sivulta kerätyn linkin domain ei ole listalla, ei crawler mene sivulle tai ota linkkiä huomioon lainkaan. Alidomainien rajoittaminen onnistuu lisäämällä listaan kaikki muut alidomainit, paitsi kyseinen pois jätettävä alidomain.

    Spiderin `LINK_EXTRACTOR_RULES` -osion `allow` ja `deny` -listat rajoittavat sivuilla olevien linkkien seuraamista. Listoihin määritellään polkuja (path), joita sisältäviä sivuja ei haluta käsiteltäväksi. Esimerkiksi, jos ei haluta indeksoida admin-sivua https://www.some_site.fi/blogit/admin/settings.html, niin deny -listaan voidaan lisätä esimerkiksi määritys `"/blogit/admin/"`. Silloin `/blogit/` -alkuiset osoitteet indeksoidaan normaalisti, mutta ei `/blogit/admin/` -alkuisia osoitteita.

    Jos halutaan sallia ainoastaan jotkin tietyt polut, niin voidaan määrittää kyseiset polut `allow` -listaan. Tässä tapauksessa kaikki muut polut ovat kiellettyjä. Tätä voidaan käyttää erityisesti erillisissä spidereissa, joissa määritellään jokin sivuston osa käsiteltäväksi.

    Jos sivustolla on sivuja, joilta ei haluta poimia tietoja, mutta niillä on kuitenkin linkkejä, jotka ovat tarpeellisia sivujen läpikäynnin kannalta, voidaan tällaiset polut määritellä `CRAWL_LINKS_ONLY` -asetukseen. Tällaisia sivuja voivat olla esimerkiksi hakemistolistaukset tai hakusivut. Jos sivun polku sisältää listassa määritellyn polun, niin siitä poimitaan ainoastaan linkit crawlattavaksi ja muut sisällöt jätetään kokonaan indeksoimatta.

    - Onko sivustolla käytössä robots.txt -tiedosto?
    - Mitkä ovat hakuun indeksoitavien sivustojen domain -nimet?
    - Onko tarvetta jättää sivuston osia haun ulkopuolelle?
    - Onko sivustolla sivuja, joista ei haluta poimia tietoja, mutta halutaan kuitenkin käydä niillä olevat linkit läpi?

6. Indeksoinnin saavuttavuus

    Crawler seuraa sivulta löytyviä linkkejä. Jos indeksointiin halutaan sisällyttää täysin erillisiä sivustoja, joita ei ole linkitetty toisiinsa, täytyy kaikista indeksoitavista sivustoista löytyä jokin aloitussivu. Jos linkkiä johonkin sivustoon ei ole missään indeksoitavassa sivussa olemassa ja siihen ei ole määritelty aloitussivua, niin sivusto jää indeksoimatta.

    Jokin sivuston osa saattaa myös jäädä indeksoinnissa käymättä läpi vahingossa, jos siihen linkittyvä sivu kuuluu rajoitettuihin sivuihin tai jostain muusta syystä linkitys ei toimi. Tässä tapauksessa aloitussivuja voi lisätä tarpeen mukaan lisää myöhemmin jos jokin osa ei indeksoidu ja sitä ei ole millään säännöllä rajoitettu.

    Jos haluat varmistua, että onko jokin sivu indeksoitunut, sen voi tarkistaa käyttämällä Elasticsearchin Dev Toolsia tai tarkistamalla logista, onko kyseinen sivu käyty läpi. Tarvittaessa lisätietoja Dev Toolsin käytöstä löytyy [indeksoinnin -dokumentaatiosta](.\elastic_dokumentaatio.md).

    - Tarvitaanko useita aloituspisteitä erillisille sivustoille?
    - Rajaavatko rajoitukset jonkin sivuston osan erilleen muusta sivustosta?

7. Mitä tietoa haetaan, ja mistä se löytyy?

    Tutustu sivuston sisältämiin tietoihin (`body` -elementti) sekä myös `head` -elementtin metatietoihin. Pohdi, mitä tietoja hakukoneen käyttäjä saattaa tarvita, ja mistä löytyvät juuri ne erityiset sanat, mitkä erottelevat juuri tämän oikean sivun muista sivuista.

    Määrittele `CUSTOM_SETTINGS` > `SCRAPER_SETTINGS` -osioon sivun `head` sekä `body` -elementtien sisältämät poimittavat tiedot. Molemmille löytyy oma `content_to_scrape` -asetus, jossa määritellään poimittavaksi erilaisia elementtejä tietyillä tunnisteilla. Poimittavat tiedot kannattaa nimetä kuvaavasti, jolloin niitä on helpompi hyödyntää muissa asetuksissa sekä tarvittaessa tunnistaa indeksoiduista tiedoista.

    Jos poimittu tieto halutaan indeksoida, sen indexing -asetukseen määritellään indeksointityyppi. Oletuksena tyyppi on `"text"`, mutta joissain tapauksissa se voi olla muukin. Tarkemmat tiedot indeksointiasetuksista löytyy [indeksoinnin dokumentaatiosta](.\elastic_dokumentaatio.md).

    Jos poimittua tietoa halutaan käyttää haussa, annetaan sille `search` -asetuksissa arvo `true` tai määritysobjekti. Jos asetuksen sisältö on mikä tahansa muu kuin `null` tai `false`, niin kyseinen poimittu tieto on haettavissa.
    
    Jos jotakin poimittua tietoa halutaan korostaa hakutuloksissa, sille voidaan määritellä `boost` -arvo. Arvo korostaa kyseisen tiedon sisältäviä hakutuloksia annetun kertoimen mukaisesti. Usein haun kannalta merkityksellisiä sanoja löytyy muun muassa otsikoista ja asiasanalistoista. Lisätietoja haun muokkauksesta [hakubackend -dokumentaatiossa](.\hakubackend_dokumentaatio.md).

    Spiderin asetuksien `CUSTOM_SETTINGS` > `CONTENT_TYPES_AND_THEMES` -osiosta löytyy joukko erilaisia sisältötyyppejä, joille voidaan määrittää kyseistä sisältöä sisältäviltä sivuilta löytyvä avainsana. Jos sivustolta löytyy vastaavia sivuja, niin sivuilta pyritään etsimään jokin termi, joka linkittää kyseiset sisältötyypit kyseisiin sivuihin. Esimerkiksi uutisen sisältävällä sivulla saattaa olla osoitepolussa tai murupolussa aina sana "uutinen" tai "news". Samoin blogisivuilta voi löytyä samalla tavalla sana "blogit" tai "blog".

    Sivuilta voidaan määritellään myös joukko muita tietoja esitettäväksi hakutuloksien yhteydessä. Spiderin `CUSTOM_SETTINGS` > `CONTENT_TYPES_AND_THEMES` > `settings` > `display_fields` -määrityksestä löytyy erilaisia sivuihin liittyviä vakiotietoja. Vakiotietoihin voidaan linkittää sivustolta poimittuja elementtejä, jolloin kyseiset tiedot tulevat näkyviin hakutuloksessa. Yksittäisten vakiotietojen alta löytyy `index_fields` -lista, johon voidaan lisätä sopivat `body` sekä `head` -elementtien `content_to_scrape` asetuksissa määritellyt elementtitunnisteet. Esimerkiksi jos `head` -elementistä on poimittu `"og:title"` -niminen otsikkotieto, niin se voidaan lisätä hakutuloksen otsikoksi `display_fields` > `title` -osion `index_fields` -listaan.

    - Mitkä elementit halutaan indeksoida ja sisällyttää hakuun?
    - Mitkä tiedot halutaan hakutuloksissa näyttää ja mistä ne löytyvät?
    - Ovatko jotkin elementit enemmän merkityksellisiä haussa kuin toiset?

## Esimerkkikonfiguraatioita

### Head

Minkä tahansa elementin tekstisisältö voidaan poimia indeksoitavaksi `head`-elementin sisältä.

Jos html -koodi on seuraavan kaltainen:

```html
<html>
    <head>
        ...
    <meta property="og:title" content="Yhteystiedot">
    ...
  </head>
</html>  
```

Voidaan arvo `Yhteystiedot`  tallentaa indeksiin seuraavanlaisella asetuksella: 

```yaml
title:
  element: "meta"
  attribute-key: "property"
  attribute: "og:title"
  attribute-value: "content"
```

`title` - propertyn nimi indeksissä johon arvo tallennetaan
`element` - elementin tyyppi HTML:ssä, josta tallennettava sisältö löytyy
`attribute-key` - avain jossa halutun metatiedon arvon osoittava avain on
`attribute`- attribuutin nimi HTML:ssä, joka osoittaa tallennettavan arvon
`attribute-value` - avain jossa halutun metatiedon arvo on

Esimerkkejä:  
```html
<meta property="og:type" content="article">
```
==>

```yaml
type:
  element: "meta"  
  attribute-key: "property"
  attribute: "og:type"
  attribute-value: "content"
```

--- 

```html
<meta name="dcterms.title" content="article">
```

==>

```yaml
title:
  element: "meta"
  attribute-key: "name"
  attribute: "dcterms.title"
  attribute-value: "content"
```

--- 

```html
<meta property="article:tag" content="tag1">
<meta property="article:tag" content="tag2">
<meta property="article:tag" content="tag3">
```

==>

```yaml
title:
  element: "meta"
  attribute-key: "property"
  attribute: "article:tag"
  attribute-value: "content"
```


### Body

Minkä tahansa elementin tekstisisältö voidaan poimia `body` -elementin sisältä.

Jos html -koodi on esimerkiksi seuraava:
```html
<div id="left-infobox" class="infobox">
    <h2>Tietolaatikon otsikko</h2>
    <p>Tietolaatikon sisältötekstiä.</p>
</div>
```
Voidaan kyseisen elementin kaikki tekstit poimia seuraavasti:
```yaml
infobox-tekstit:
    element: "div"
    attributes:
        id: "left-infobox"
        class: "infobox"
    ...
```
Tai poimia kaikki h2 -otsikkoelementtien ja/tai p -elementtien sisältämät tekstit omiin kenttiinsä.
```yaml
h2-otsikot:
    element: "h2"
    attributes:
        id: null
        class: null
p-tekstit:
    element: "p"
    attributes:
        id: null
        class: null
    ...
```

Jos html -koodi on esimerkiksi seuraava:

```html
<div id="content" class="content">
    <h1>Päätason otsikko</h1>
    <p>Jotakin sisältötekstiä.</p>
    <h2>Alaotsikko</h2>
    <p>Lisää leipätekstiä.</p>
<div id="left-infobox" class="infobox">
    <h2>Tietolaatikon otsikko</h2>
    <p>Tietolaatikon informaatiota.</p>
</div>
```

Voidaan esimerkin mukaisen ylemmän `div` -elementin sisältämien `p` -elementtien tekstit poimia lisäämällä pois jätettävä elementti `exclude_rules` -sääntöihin ja poimimalla muuten kaikki `p` -elementit. Tässä tapauksessa poimituksi tulisivat elementit, jotka sisältävät tekstit "Jotakin sisältötekstiä" sekä "Lisää leipätekstiä".

```yaml
body:
    ...
    exclude_rules:
        tietolaatikko:
            element: "div"
            class: null
            id: "left-infobox"
    content_to_scrape:
        leipateksti:
            element: "p"
            attributes:
                class: null
                id: null
            ...
```

Jos halutaan poimia esimerkiksi henkilökuvan linkki yhteystietojen yhteydestä seuraavanlaisesta html -koodista:

```html
<div id="person-contact-info" class="contact-info">
    <div class="person-name">Jeppe Jokinen</div>
    <div class="person-email">jeppe.jokinen@jokisenvehjejavekotin.fi</div>
    <img src="https://www.some_site.fi/img/jeppe_jokinen.jpg" alt="Kuva henkilöstä Jeppe Jokinen" title="Jeppe Jokinen">
</div>
```

Voidaan käyttää seuraavan kaltaista määrittelyä:

```yaml
henkilokuva:
    element: "div"
    attributes: 
        class: null
        id: "person-contact-info"
    indexing:
        type: "text"
    image:
        target_element: "img"
        target_attributes:
            class: null
            id: null
        content_attributes: "src"
        alt_text: "alt"
        title: "title"
```