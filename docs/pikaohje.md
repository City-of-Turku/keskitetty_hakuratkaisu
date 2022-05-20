# Pikaohje (Keskitetty Hakuratkaisu)

Versio 0.1

Tämä dokumentti opastaa hakuratkaisun käyttöönotossa. Tässä ohjeessa käydään läpi ainoastaan peruskäyttöönotto sekä tarvittavat minimiasetukset ja -valinnat. Tämän ohjeen avulla saat otettua hakupalvelun käyttöön perusasetuksilla. Tarkempi dokumentaatio ja asetusten yksityiskohdat löytyvät erillisistä moduulikohtaisista dokumenteista. Tässä ohjeessa mainitut esimerkkikonfiguraatiot eivät välttämättä sisällä kaikkia asetuksia, joita konfiguraatiossa on.

HUOM! Asetusten muuttaminen ilman ymmärrystä kyseisen asetuksen vaikutuksesta palveluun ei ole suositeltavaa! Väärä konfiguraatio saattaa johtaa epätoivottuihin sisältöihin hakutuloksissa tai aiheuttaa jopa palvelunestohyökkäyksen.

## Ennakkovaatimukset

- keskitettyhakuratkaisu -repositorio ladattuna samannimiseen kansioon<br>
(https://github.com/City-of-Turku/keskitetty_hakuratkaisu)
- tietokoneessa on asennettuna Docker, jolla eri palveluita ajetaan<br>
(https://www.docker.com/)

## Config.yaml

Config.yaml -tiedosto sisältää kaikkien moduulien asetukset. Se sijaitsee projektin juurikansiossa. Toimintoja muokataan ja ohjataan muuttamalla sen sisältämiä arvoja. Konfiguraation sisältämät asetukset ladataan palveluiden Docker -konttien käynnistyessä.  Konfiguraatiotiedosto noudattaa YAML -merkintätyyliä (lisätietoja [YAML -dokumentaatiosta](https://yaml.org/spec/1.2.2/)).

## Työnkulku

1. Syötetään asetukset config.yaml tiedostoon
    - Search Backend
    - Elasticsearch
    - Scrapy
    - Elementtien poiminta
2. Buildataan Docker levykuvat
3. Käynnistetään palvelut
4. Ajastetaan sivustojen indeksointi

## 1. Asetukset

### Search Backend (__backend__):

- Backend asetukset toimivat oletuksilla.

### Elasticsearch (__elasticsearch__):

- `hosts` sisältää Elasticsearch -palvelimen osoitteen muodossa `hostname:port`.
- `index_prefix` on merkkijono, joka erittelee käytettävän dokumenttien tallennusindeksin.
- `index_reader_rolename` on käyttäjäroolin nimi, jota käytetään indeksejä luettaessa.
- `index_writer_rolename` on käyttäjäroolin nimi, jota käytetään indeksejä kirjoitettaessa.
- `languages` sisältää listan kielikoodeista, joita sivustolla käytetään ja kyseisen koodin sisältävät sivut halutaan indeksoida.

    ```yaml
    hosts: 
        - "elasticsearch:9200"
    index_prefix: "yleishaku"
    index_reader_rolename: "yleishaku_reader"
    index_writer_rolename: "yleishaku_writer
    languages:
        - "fi"
        - "sv"
        - "en"
    ```

### Scrapy (__SCRAPY_SETTINGS__): 

Sisältää useita alaosioita liittyen sivustojen indeksointiin ja datan poimintaan. Voi sisältää useita spidereita, joista kukin sisältää asetukset jonkin sivuston tai sivuston osion indeksointiin.

- `GENERAL`:
    - `DOWNLOAD_DELAY` asettaa vähimmäisviipeen sivustopyyntöjen välillä sekunteina. `(integer | float)`
    - `LOG_ENABLED` login kirjoitusvalinta. `(true | false)`
    - `LOG_FILE` määrittää tiedoston nimen, jos halutaan, että logi kirjoitetaan tiedostoon. Muussa tapauksessa arvoksi annetaan `null` jolloin logi kirjoitetaan konsoliin. `(string | null)`
    - `ROBOTSTXT_OBEY` määrittää, että noudatetaanko robots.txt:n ohjeita. `(true | false)`

    ```yaml
    GENERAL:
        DOWNLOAD_DELAY: 0.5
        LOG_ENABLED: true
        LOG_FILE: null
        ROBOTSTXT_OBEY: true
    ```

- `SPIDERS`:
    - `KuvaavaNimiSpider` on spiderin nimi (ja samalla osion otsake), joka voi olla mikä tahansa kuvaava crawlerikohtaisesti uniikki merkkijono.
        - `BOT_NAME` on indeksoitavalle sivustolle näkyvä asiakassovelluksen nimi.
        - `ALLOWED_DOMAINS` sisältää listan sallituista domain nimistä.
        - `START_URLS` sisältää listan osoitteista, joista halutaan sivuston sisällön poiminta aloittaa.
        - `LINK_EXTRACTOR_RULES` sisältää `allow` ja `deny` listat osoitepoluista, joilla sallitaan tai kielletään tietyt osoitepolut. Kieltävä sääntö ohittaa aina sallivan säännön eli jos jokin osoitepolku on millään säännöllä kielletty, niin se on aina kielletty, vaikka jossain se erikseen sallittaisiinkin.<br>
        (HUOM! Jos jokin osoitepolku on sallittu, niin silloin kaikki muut paitsi sallitut polut ovat kiellettyjä riippumatta kiellettyjen polkujen listasta.)
        - `CUSTOM_SETTINGS` sisältää tarkemmat sivuston sisällön poiminta-asetukset.
            - `CRAWL_LINKS_ONLY` sisältää osoitepolut, joista poimitaan vain linkit, joita 
            - `SCRAPER_SETTINGS` sisältää sivustolta poimittavat elementit sekä niihin liittyvät asetukset.<br>
            (HUOM! Tämän osion asetukset käydään läpi tarkemmin seuraavassa osiossa sekä erillisessä dokumentaatiossa!)
            - `CONTENT_TYPES_AND_THEMES` määrittelee mitä hakutuloksissa näytetään. Mistä poimituista elementeistä otetaan pakollisten kenttien arvot sekä mitä muita kenttiä esitetään hakutuloksissa ja mistä niiden arvot tulevat.
            (HUOM! Tämän osion asetukset käydään läpi tarkemmin seuraavassa osiossa sekä erillisessä dokumentaatiossa!)
    
        ```yaml
        KuvaavaNimiSpider:
            BOT_NAME: "yleishakubot"
            ALLOWED_DOMAINS:
                - "www.indeksoitava_sivusto.fi"
            START_URLS:
                - "https://www.indeksoitava_sivusto.fi"
            LINK_EXTRACTOR_RULES:
                allow:
                deny:
                    - "/login/"
                    - "/admin/"
            CUSTOM_SETTINGS:
                SCRAPER_SETTINGS:
                    ...jatkuu seuraavissa osioissa
                CONTENT_TYPES_AND_THEMES:
                    ...jatkuu seuraavissa osioissa
        ```

### Elementtien poiminta (__SCRAPER_SETTINGS__)

Sisältää sivuston sisältöjen poimintaan sekä poimittujen tietojen jäsentelyyn ja hakutuloksissa näyttämiseen liittyviä asetuksia.

- `SCRAPER_SETTINGS`
    - `lang` sisältää sijainnin, josta sivun kielikoodi poimitaan. Oletuksena poimitaan sivun html -elementin lang -attribuutista. Vaihtoehtoisesti koodi voidaan poimia sivun osoitteesta (katso tarkempi ohje dokumentaatiosta).
    - `head`:
        - `content_to_scrape` sisältää html -koodin head -elementissä sijaitsevien elementtien poiminta-, indeksointi- sekä hakuasetukset. Head -elementissä on yleensä sivun metatietoja kuten sivun otsikko (title). Elementtien asetukset syötetään seuraavan esimerkin mukaisesti. Elementtejä voi olla tarpeen mukaan useampia.<br>
        (HUOM! Indeksoinnin ja haun asetuksien tarkemmat ohjeet dokumentaatiossa!)

            ```yaml
            # YKSITTÄINEN POIMITTAVA HEAD-ELEMENTTIASETUS
            kuvaava_kohteen_nimi:
                element: "kohde_elementin_nimi"
                attribute: "valitsevan_attribuutin_arvo"
                attribute-key: "valitsevan_attribuutin_avain"
                attribute-value: "poimittavan_attribuutin_avain"
                indexing:
                    type: "text"
                search:
                    true
            ```

    - `body` sisältää html-koodin body -elementissä sijaitsevien elementtien poiminta-asetukset.<br>
        - `element` on pääsisällön sisältävän elementin nimi (esim. "body" tai "div"). Jos elementtiä ei rajata saattaa indeksoitavaksi päätyä epätoivottuja sisältöjä, kuten esimerkiksi valikoita tai bannereita.<br>
        (HUOM! Pakollinen arvo!)
        - `class` on pääsisällön elementin yksilöivä class -attribuutin arvo (esim. "l-main"). Voi olla myös null.
        - `id` on pääsisällön elementin yksilöivä id -attribuutin arvo (esim. "main-content"). Voi olla myös null.
        - `exclude_rules` sisältää indeksoinnin ulkopuolelle jätettävien elementtien tunnisteet. Tällä voidaan rajata haluttu elementti pois poimittavasta sisällöstä. (Valinta samalla periaatteella kuin pääelementti. Katso tarvittaessa tarkemmat ohjeet dokumentaatiosta!)
        - `content_to_scrape` sisältää html -koodin body -elementissä sijaitsevien elementtien poiminta-, indeksointi- sekä hakuasetukset. Body -elementissä on sivun varsinainen sisältö. Elementtien asetukset syötetään seuraavan esimerkin mukaisesti. Elementtejä voi olla tarpeen mukaan useampia.<br>
        (HUOM! Indeksoinnin ja haun asetuksien tarkemmat ohjeet dokumentaatiossa!)
        
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

Esimerkki SCRAPER_SETTINGS:
    
```yaml
SCRAPER_SETTINGS:
        lang:
            "html"
        head:
            content_to_scrape:
                og:title:
                    element: "meta"
                    attribute: "og:title"
                    attribute-key: "property"
                    attribute-value: "content"

        body:
            element: "div"
            class: "l-main"
            id: null
            content_to_scrape:
                header1:
                    element: "h1"
                    attributes:
                        class: null
                        id: null
                    indexing:
                        type: text
                    search:
                        true
                p_text:
                    element: "p"
                    attributes:
                        class: null
                        id: null
                    indexing:
                        type: "text"
                    search:
                        true
```

### Poimittujen tietojen kohdentaminen (__CONTENT_TYPES_AND_THEMES__)

- `CONTENT_TYPES_AND_THEMES`
    - `settings` sisältää asetukset muun muassa sivun sisältötyypin sekä teeman valintaan.<br>
    (HUOM! Tarkemmat ohjeet erillisessä dokumentaatiossa!)
        - `parse_content_type_from` määrittää valitaanko sivun sisältötyyppi osoitteen vai yksittäisen elementin perusteella.
        - `parse_themes_from` määrittää valitaanko sivun teema osoitteen, murupolun vai yksittäisen elementin perusteella.
        - `default_content_type` määrittää oletusarvon sisältötyypille, jos muuta tyyppiä pystytä asetusten mukaisesti valitsemaan.
        - `display_fields` sisältää hakuosumissa käyttöliittymälle saatavilla olevat kentät, mistä niiden arvot otetaan sekä niihin liittyvät asetukset.
            - `title`, `text`, `publish_date`, `modify_date`, `writer`, `location`, `date`, `time`, `url`, `image_url`, `keywords`, `content_type` ja `themes` ovat kenttiä, joiden tietoja voidaan näyttää käyttöliittymässä hakutulosten yhteydessä.
                - `default` sisältää kentän oletusarvon, jos muuta arvoa ei ole saatu sivulta poimittua.
                - `append_values` määrittää lisätäänkö kaikki arvot vai ainoastaan ensimmäinen löydetty.
                - `index_fields` määrittää poimitut kohteet, jotka liitetään tähän kenttään. Tähän voidaan valita _SCRAPER_SETTINGS_ -asetuksissa määritellyt poimittavat elementit. Arvo on kyseiselle poimittavalle kohteelle annettu nimi (esim. "og:title" tai "header1").
                - `suggest` määrittää käytetäänkö kentän arvoja hakuehdotuksien antamiseen.
    - `uutinen`, `blogi`, `yhteystieto`, `tapahtuma`, `palvelu_tai_asiointikanava` ja `tietosivu` ovat teemoja, jotka ovat saatavilla hakutuloksen _themes_ -kenttään. Jokainen kohta sisältää listan arvoista, joilla valitaan kyseinen vaihtoehto sivun teemaksi `settings` -kohdan asetuksien mukaisesti. Lista voi olla myös tyhjä.

Esimerkki:

    ```yaml
    CONTENT_TYPES_AND_THEMES:
        settings:
            parse_content_type_from: "url"
            parse_themes_from: "url"
            default_content_type: "tietosivu"
            display_fields:
                title:
                    default: "Not Found"
                    append_values: true
                    index_fields:
                        - "og:title"
                text:
                    append_values: false
                    index_fields:
                publish_date:
                    index_fields:
                modify_date:
                    index_fields:
                writer:
                    default: "Tuntematon kirjoittelija"
                    suggest: true
                    index_fields:
                location:
                    index_fields:
                    suggest: true
                date:
                    index_fields:
                time:
                    index_fields:
                url:
                    index_fields:
                image_url:
                    index_fields:
                keywords:
                    index_fields:
                    suggest: true
                content_type:
                    index_fields:
                        - "content_type"
                themes:
                    suggest: true
                    index_fields:
                        - "themes"
        uutinen:
            - "uutinen"
            - "uutiset"
        blogi:
            - "blogi"
            - "blog"
        yhteystieto:
            - "yhteystieto"
            - "henkilo"
            - "contact"
            - "toimipaikka"
            - "toimipiste"
        tapahtuma:
            - "tapahtumat"
        palvelu_tai_asiointikanava:
            - "palvelu"
            - "asiointikanava"
            - "service"
        tietosivu:
    ```
