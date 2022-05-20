# Elasticsearch Dokumentaatio (Keskitetty Hakuratkaisu)

Versio 0.1

Keskitetyssä hakuratkaisussa (KEHA) käytetään Elasticsearch -hakumoottoria. Elasticsearchin dokumentti-indeksiin syötetään dokumentit (esimerkiksi crawlerin läpikäymät www-sivut), joihin käyttäjän käyttöliittymässä tekemä haku kohdistetaan. KEHAn mukana on myös Kibana-käyttöliittymä Elasticsearchin ja indeksien hallintaan. 

Tämä dokumentti sisältää Elasticsearch -asetuksien dokumentaation KEHAn osalta. Tässä dokumentissa on esitelty ja mainittu vain ne asetukset, joita käyttöönottajan on mahdollisesti tarpeen muuttaa käyttöönoton yhteydessä. Lisäksi esitellään muutamia ylläpidollisia toimenpiteitä, joita voi tehdä Kibanan kautta. Tarvittaessa lisätietoja asetuksista löytyy Elasticsearchin omalta [dokumentaatiosivustolta](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html).

Elasticsearchin hakuominaisuudet noudattavat [ELv2 -lisenssiä](https://www.elastic.co/licensing/elastic-license).

## Config.yaml

Config.yaml -tiedosto sisältää kaikkien moduulien asetukset. Se sijaitsee projektin juurikansiossa. Elasticsearchin konfigurointiin liittyviä asetuksia on __elasticsearch__ -osiossa. Lisäksi hakulausekkeisiin ja painotuksiin liittyviä asetuksia on tiedostossa eri kohdissa. Konfiguraatiotiedosto noudattaa YAML -merkintätyyliä (lisätietoja [YAML -dokumentaatiosta](https://yaml.org/spec/1.2.2/)).

# Sisältö

1. [Elasticsearch -asetukset](#elasticsearch-asetukset)
2. [Analyzerit](#analyzerit)
    - [Character filterit](#character-filterit)
    - [Tokenizerit](#tokenizerit)
    - [Token filterit](#token-filterit)
3. [Analyzerin asetus sisällöstä poimittavalle elementille](#analyzerin-asetus-sisällöstä-poimittavalle-elementille)
4. [Kibana](#kibana)
    - [Kohdesivun indeksoitumisen tai indeksoitujen tietojen tarkistaminen](#kohdesivun-indeksoitumisen-tai-indeksoitujen-tietojen-tarkistaminen)
    - [Dokumentin poisto indeksistä](#dokumentin-poisto-indeksista)
    - [Kayttajien ja roolien hallinta](#kayttajien-ja-roolien-hallinta)
    - [Indeksien ja index templatejen poisto](#indeksien-ja-index-templatejen-poisto)

# Elasticsearch asetukset

Elasticsearchin yleisiin asetuksiin liittyvät kohdat löytyvät __elasticsearch__ -osiosta.

Esimerkki konfiguraation Elasticsearch -asetuksista:

```yaml
elasticsearch:
  hosts:
    - "elasticsearch:9200"
  index_prefix: "index_name_prefix"
  index_reader_rolename: "index_reader_rolename"
  index_writer_rolename: "index_writer_rolename"
  languages:
    - fi
    - sv
    - en
  analyzers:
    default:
      tokenizer: "standard"
      token_filters: 
        - "lowercase"
    fi:
      
```

`hosts:` (`list`)<br>
    Hosts listaan asetetaan Elasticsearch -instanssin (tai instanssien) osoitteet ja portit (esim. "elasticsearch:9200").

`index_prefix:` (`string`)<br>
    Indeksin nimen alkuosa, johon KEHAn crawlerin keräämät dokumentit tallennetaan. Varsinaisessa indeksin nimessä alkuosaan liitetään kielikoodi väliviivalla.

`index_reader_rolename:` (`string`)<br>
    Hakubackend-käyttäjän rooli. Roolilla on oikeudet ainoastaan KEHAn indeksien lukemiseen.

`index_writer_rolename:` (`string`)<br>
    Crawler käyttäjän rooli. Roolilla on oikeus lukea ja kirjoittaa dokumentteja KEHAn indekseihin sekä luoda tarvittaessa indeksit, jos niitä ei ole jo luotu palvelun käynnistyksen yhteydessä.

`languages:` (`list`)<br>
    Listaus sivuilla käytetyistä kielistä kielikoodeina, joille luodaan omat indeksit Elasticsearchiin. Jos sivustosta on pelkästään suomenkielinen versio, asetetaan listaan ainoastaan *fi*. Jos sivustosta on esimerkiksi suomen- ja ruotsinkieliset versiot, asetetaan listaan *fi* ja *sv*. Koodit noudattavat [RFC5646](https://datatracker.ietf.org/doc/html/rfc5646#section-2.2.1) mukaista määrittelyä kielikoodin primääristä alitagista (subtag). Koodi on kaksi tai kolme merkkiä pitkä ja sen tulee vastata `html`-tagin `lang`-attribuutin sisältämän arvon alitagia (subtag).

`analyzers: ` (`object`)<br>
    Sisältää määrittelyobjektit Elasticsearchin indeksointianalysaattoreille. Analysaattorit lisätään Elasticsearchin indeksiin niin sanotuiksi custom analyzereiksi. Ne käsittelevät indeksoitavat sekä hakuun syötettävät tekstit, jolloin ne saadaan paremmin kohdistumaan toisiinsa. Lisätietoa analysaattoreista alempana [Analyzer](#analyzerit) -kohdassa sekä [Elasticsearchin omasta dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html).
    
- `default: ` (`object`)<br>
    Oletusanalysaattori, jolla käsitellään kaikki tekstimuotoiset indeksoitavat kohteet, jos niille ei ole määritelty muuta analysaattoria.

    - `tokenizer: ` (`string` | `null`)<br>
        Oletuksena käytettävän tokenizerin nimi. Katso kuvaus seuraavan objektin `tokenizer` -kohdasta.

    - `token_filters: ` (`list` | `null`)<br>
        Lista oletuksena käytettävien token filtereiden nimistä. Katso kuvaus seuraavan objektin `token_filters` -kohdasta.

- `xx: ` (`object`)<br>
    Objekti, jonka nimi on kaksi- tai kolmemerkkinen kielikoodi, joka tulee löytyä myös `languages` listasta. Objektiin määritellään kyseiselle kielelle saatavilla olevat analysaattorit. Objekteja tulee olla yksi jokaista kieltä kohti.

    - `kuvaava_analysaattorin_nimi: ` (`object`)<br>
        Objekti, joka määrittelee kyseisen analysaattorin sisältämät `char filterit`, `tokenizerin` sekä `token filterit`. Nimeksi kannattaa antaa lyhyehkö analysaattorin toimintaa kuvaava nimi, kuten esimerkiksi "stop_stemmer". Tällä nimellä määritetään käytettävät analysaattorit eri elementeille crawlerin asetuksissa. 

        - `char_filters: ` (`list` | `null`)<br>
            Lista analysaattorissa käytettävistä character filtereistä. Character filter suodattaa vastaanotettavasta syötteestä tiettyjä merkkejä tai vaihtaa niitä toisiin ennen syötteen tokenisointia. Suurimmassa osassa tapauksista erillistä character filteriä ei tarvita. Character filtereiden käytöstä tarkemmin kohdassa [Character filterit](#character-filterit). Käytettävissä olevat filterit löytyvät [Elasticsearchin dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html).
            
        - `tokenizer: ` (`string` | `null`)<br>
            Määrittää analysaattorissa käytettävän tokenizerin. Tokenizer muun muassa paloittelee annetun syötteen yksittäisiksi tokeneiksi, joita käytetään hauissa. Yksittäinen token voi olla esimerkiksi välilyönnillä toisista erotettu sana. Suurimmassa osassa tapauksista kannattaa käyttää `"standard"` -tokenizeria, joka paloittelee syötteen Unicode -standardissa määriteltyjen segmentointisääntöjen perusteella. Käytettävissä olevat tokenizerit löytyvät [Elasticsearchin dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html).

        - `token_filters: ` (`list` | `null`)<br>
            Lista analysaattorissa käytettävistä token filtereistä (`string` | `object`). Token filter käsittelee tokenizerin tuottamia tokeneita. Se voi esimerkiksi poistaa tiettyjä tokeneita tai muokkata niitä ennen syötteen indeksointia. Token filtereiden käytöstä tarkemmin kohdassa [Token filterit](#token-filterit). Elasticsearchiin sisäänrakennetut käytettävissä olevat filterit löytyvät [Elasticsearchin dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html).

## Analyzerit

Elasticsearch käsittelee indeksoitavaksi annetut syötteet niin sanotuilla analysaattoreilla (analyzer). Ne ovat tekstiä käsitteleviä linjastoja, jotka käsittelevät niille annetut syötteet annettujen asetusten mukaisesti. Jokainen analysaattori sisältää nolla, yhden tai useampia character- tai token filtereitä sekä aina yhden tokenizerin.

Linjasto käsittelee annetun syötteen aina samassa järjestyksessä. Ensin character filterit muokkaavat haluttuja merkkejä syötteestä ennen tokenizer -vaihetta. Sen jälkeen tokenizer paloittelee syötteen tokenizerin määrittelemillä ehdoilla (esimerkiksi välilyönti erotinmerkkinä) yksittäisiksi tokeneiksi. Lopuksi token filter suodattaa tai muokkaa tuotettuja tokeneita ennen indeksointia.

Jotta haetut sanat kohdistuvat oikein indeksoituihin sisältöihin, täytyy myös hakusanat käsitellä samoilla työkaluilla kuin indeksoidut sisällöt. Elasticsearch tekee tämän automaattisesti käyttäen asetuksissa annettua analyzeria.

Lisätietoa analysaattoreista [Elasticsearchin omasta dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html).

### Character filterit

Character filterit käsittelevät syötteen ennen tokenisointia. Jos sivustolla on käytetty esimerkiksi sanoja, jotka eivät sovellu hakuun, voidaan ne vaihtaa tai poistaa syötteestä ennen niiden päätymistä indeksiin.

HUOM! Character filterin tekemät muutokset eivät vaikuta sivuston sisältöön, vaan ainoastaan hakusanojen osuvuuteen indeksoituun sisältöön.

Esimerkiksi jos elementtien poiminta-asetuksilla ei pystytä poistamaan jotakin indeksoitavissa elementeissä toistuvaa ylimääräistä sanaa, se voidaan poistaa tai vaihtaa indeksoitavasta sisällöstä käyttämällä Pattern Replace -character filteriä. Alla esimerkki kyseisestä konfiguraatiosta.

Lisätietoja character filtereistä [Elasticsearchin dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html).

```yaml
analyzers:
  default:
    ...
  fi:
    filtterin_nimi:
      char_filters:
        - type: "pattern_replace"
          pattern: "korvattava_merkkijono"
          replacement: "korvaava_merkkijono"
      tokenizer:
        "standard"
      token_filters:
        - "lowercase"
  sv:
    filters_namn:
      char_filters:
        - type: "pattern_replace"
          pattern: "växlande_sträng"
          replacement: "substituerande_sträng"
      tokenizer:
        "standard"
      token_filters:
        - "lowercase"
```

### Tokenizerit

Käytännössä oletuksena käytettävä "standard" -tokenizer pystyy käsittelemään suurimman osan sivustoista oikein. Joissain erityistapauksissa voi olla tarvetta käyttää toista tokenizeria, mutta se on erittäin harvinaista.

Oletustokenizer erottaa sanat toisistaan [Unicode -standardissa](https://unicode.org/reports/tr29/) määriteltyjen segmentointisääntöjen perusteella. Käytännössä se erottelee lauseet ja sanat toisistaan muun muassa välimerkkien sekä välilyöntien perusteella.

Lisätietoja tokenisoijista [Elasticsearchin dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html).

### Token filterit

Token filter käsittelee tokeneita, joita tokenizer tuottaa indeksoitavaksi tai haettavaksi annetusta syötteestä. Se voi suodattaa tai muokata yksittäistä tokenia. Filttereitä voi olla useita ja ne toimivat peräkkäin muodostaen käsittelylinjaston tokeneille. Vasta käsittelyn jälkeen tokenit tallennetaan Elasticsearchin indeksiin. Yleisimmin käytettyjä token filtereitä ovat `stop words`, `stemmer` sekä `synonym` -filtterit.

Stop words -filter suodattaa indeksoitavista lauseista usein esiintyviä ja merkitykseltään vähäisiä sanoja. Suodattimeen on saatavilla valmiita sanastoja useille eri kielille. Lisätietoja [Elasticsearchin stop -filter dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stop-tokenfilter.html).

Stemmer -filter yrittää poistaa indeksoitavien sanojen sijapäätteet sekä johtimet yrittäen saada lopputulokseksi indeksoitavan sanan vartalon. Vakiosuodatin ei osaa kovin hyvin käsitellä suomenkielen taivutuksia, mutta auttaa silti paljon erilaisilla sijapäätteillä varustettujen sanojen kohdistamisessa. Muilla kielillä stemmer toimii huomattavasti paremmin. Stemmer on myös saatavilla useille eri kielille. Lisätietoja [Elasticsearchin stemmer -filter dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stemmer-tokenfilter.html).

Synonym -filter käyttää haussa synonyymitiedostoon määriteltyjä sanayhdistelmiä. Tiedostoon synonyymeiksi määritellyillä sanoilla tehdään haun yhteydessä haku myös synonyymisanoilla. Lisätietoja sekä tarkemmat ohjeet [Elasticsearchin synonym -filter dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html).

Lisätietoja token filtereistä [Elasticsearchin dokumentaatiosta](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html).

```yaml
analyzers:
  default:
    ...
  fi:
    filtterin_nimi:
      char_filters:
        ...
      tokenizer:
        "standard"
      token_filters:
        - "lowercase"
        - type: "stop"
          stopwords: "_finnish_"
        - type: "stemmer"
          language: "finnish"
        - type: "synonym"
          synonym_path: "synonyms_fi.txt"
  sv:
    filters_namn:
      char_filters:
        ...
      tokenizer:
        "standard"
      token_filters:
        - "lowercase"
        - type: "stop"
          stopwords: "_swedish_"
        - type: "stemmer"
          language: "swedish"
```

## Analyzerin asetus sisällöstä poimittavalle elementille

Jokainen poimittu elementti menee analyzerin läpi ennen indeksointia. Oletuksena käytetään default -analyzeria, jos muuta ei ole määritelty. Oletusanalyzer määritellään `analyzers` -asetuksen `default` -objektiin.

Analyzers -asetuksessa määritellyt analysaattorit ovat käytössä elementtien poiminta-asetuksien yhteydessä. Jokaiselle elementille voidaan määrittää haluttu analysaattori kielikohtaisesti. Poimittavan elementin `indexing` -määritys voi sisältää `analyzer` -objektin, joka määrittelee eri kieliversioille käytettävän analyzerin.

Elementtien analyzer -asetuksen määrittelyssä täytyy muistaa tarkistaa, että kyseinen elementti soveltuu analyzerille. Analyzereita käytetään tekstin käsittelyyn, joten poimittavan tiedon tulee olla myös teksti -tyyppinen. Analysaattoreiden ei välttämättä tarvitse olla sama kaikilla kielillä.

HUOM! Toiselle kielelle määriteltyä analyzeria ei voi käyttää muissa kielissä!

Analyzerin käyttöönotto elementin poiminta-asetuksessa:
```yaml
# YKSITTÄINEN POIMITTAVA BODY-ELEMENTTIASETUS
kuvaava_kohteen_nimi:
  element: "kohde_elementin_nimi"
  attributes: 
    class: "class_attribuutin_arvo"
    id: "id_attribuutin_arvo"
  indexing:
    type: "text"
    analyzer:
      fi: "filtterin_nimi"
      sv: "filters_namn"
  search:
    true
```

# Kibana

Kibanan kautta voidaan hallita Elasticsearchin indeksejä ja niihin liityviä käyttöoikeuksia sekä indekseihin tallennettuja dokumentteja. Kibanan kautta voidaan hallita myös muun muassa indekseihin syötettävään dataan liittyviä index templateja. Lisäksi Kibanan kautta voidaan tarkistaa esimerkiksi onko jokin tietty kohdesivu indeksoitu tai mitä dataa tietystä sivusta on sinne tallennettu. Ohessa muutama päätoiminto, joiden avulla pystyy tallennettuja tietoja hallinnoimaan. Lisätietoja tarvittaessa Elasticsearchin [Kibana -dokumentaatiosta](https://www.elastic.co/guide/en/kibana/current/index.html).

## Kirjautuminen

Useimmat toimenpiteet voidaan tehdä Dev Tools -työkalulla. Osa indekseihin sekä käyttöoikeuksiin liittyvistä toimenpiteistä voidaan tehdä myös Stack Management -hallintapaneelin kautta.

1) Kirjaudu Kibanan ylläpitonäkymään ylläpitotunnuksilla
2) Navigoi vasemman reunan navigointinäkymän hampurilaisvalikosta (kolme viivaa päällekkäin) tarpeen mukaan johonkin seuraavista:
    - Dev Tools
    - Stack Management

## Kohdesivun indeksoitumisen tai indeksoitujen tietojen tarkistaminen

1) Kirjaudu ja avaa Dev Tools (kts. [Kirjautuminen](#kirjautuminen))
2) Hae kohdesivustoa sen kokonaisella www -osoitteella (esim. selaimesta kopioituna) seuraavalla hakulauseella (GET pyyntö):

```json
GET indeksin_nimi/_search
{
  "query": {
    "match": {
      "url": "haettavan_sivun_url"
    }
  }
}
```

Vastauksena tulevan JSON -objektin `hits` -osio kertoo, että löytyikö kyseisellä osoitteella dokumentteja indeksistä. Alla olevassa esimerkissä löytyi yksi kappale. Jos dokumentti löytyy indeksistä, niin kyseisestä vastausobjektista näkee myös indeksoidut tiedot. Kaikkien hakuun täsmäävien dokumenttien tiedot löytyvät `hits` -listasta.

```json
"hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score": 3.1415927,
    "hits": [
      {
        "...yksittäinen_hakutulos..."
      }
    ]

```

## Dokumentin poisto indeksista

1) Kirjaudu ja avaa Dev Tools (kts. [Kirjautuminen](#kirjautuminen))
2) Poistettavan dokumentin www-osoitetta (ilman `https://` -etuliitettä) tarvitaan poistamisessa
, esimerkiksi www.turku.fi/organisaatio/toimialat
3) Korvaa www-osoitteesta /-merkit merkkijonolla %2f (eli käytä url-enkoodattua osoitetta), 
esimerkiksi www.turku.fi%2forganisaatiot%2ftoimialat

4) Tee seuraavanlainen DELETE pyyntö käytössä olevaan indexiin:
   
```
DELETE /index_name/_doc/url_of_the_document_to_delete
```

esimerkin mukaan: (indeksin nimi 'demo-fi')

```
DELETE /demo-fi/_doc/www.demosivu.fi%2forganisaatiot%2ftoimialat
```

Vastauksena tulee: 

```json
{
  "_index" : "demo-fi",
  "_type" : "_doc",
  "_id" : "www.demosivu.fi/organisaatio/toimialat",
  "_version" : 2,
  "result" : "deleted",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 11400,
  "_primary_term" : 1
}
```

## Kayttajien ja roolien hallinta

Tavanomaisessa käytössä järjestelmä luo tarvittavat käyttäjät sekä roolit automaattisesti.  Jos esimerkiksi häiriötilanteen vuoksi on tarvetta tarkistaa käyttäjien ja roolien sekä niille määriteltyjen indeksien tilannetta, onnistuu se seuraavasti.

1) Kirjaudu ja avaa Stack Management (kts. [Kirjautuminen](#kirjautuminen))
2) Valitse vasemman reunan valikon `Security` -osiosta `Users` tai `Roles`

Käyttäjät (Users) sisältää käytettävissä olevat käyttäjät. Yleensä suurin osa käyttäjistä on Elasticsearchin sisäisiä käyttäjiä ja niihin ei tule tehdä muutoksia. Hakuratkaisu luo käynnistyessään ympäristömuuttujissa annettujen arvojen perusteella kaksi käyttäjää, joiden avulla tietoja kirjoitetaan ja luetaan. Toinen käyttäjistä on lukuoikeuksilla varustettu "reader" -käyttäjä, jota hakubackend käyttää hakujen tekemiseen. Toinen käyttäjä on luku- sekä kirjoitusoikeuksilla varustettu "writer" -käyttäjä, jota crawler käyttää indeksoidessaan tietoja. Käyttöoikeudet tulevat roolien kautta, joiden nimet on määritelty `config` -tiedostossa. Roolit näkyvät käyttäjän `Privileges` -osion `Roles` -näkymässä. Näkymässä voidaan lisätä ja poistaa rooleja käyttäjältä manuaalisesti tarpeen vaatiessa.

Roolit (Roles) sisältää käytettävissä olevat roolit. Yleensä suurin osa rooleista on Elasticsearchin sisäisiä rooleja ja niihin ei tule tehdä muutoksia. Hakuratkaisu luo käynnistyessään asetuksissa määritellylle indeksille luku- sekä kirjoitusroolin, jotka liitetään vastaavasti luotuun käyttäjään. Roolin `Index privileges` -osiossa määritellään mihin indeksiin ("Indices") roolilla on oikeuksia ja mitä kyseiset oikeudet ("Privileges") ovat. Indeksien nimissä voidaan käyttää jokerimerkkinä tähteä (*). Oikeuksissa voidaan käyttää "read" sekä "write" -oikeuksia.

## Indeksien ja index templatejen poisto

<strong>HUOM! Indeksi sekä siihen indeksoidut dokumentit poistetaan pysyvästi. Toimintoa ei voi peruuttaa, joten tätä ei tule tehdä jos ei ole täysin varma mitä on poistamassa! Tietojen palauttaminen vaatii sivujen uudelleenindeksoinnin.</strong>

Jos halutaan poistaa koko indeksi sekä siihen liittyvä index template, voidaan se tehdä Stack Managementin kautta seuraavasti.

1) Kirjaudu ja avaa Stack Management (kts. [Kirjautuminen](#kirjautuminen))
2) Valitse vasemman reunan valikon `Data` -osiosta `Index management`

Aukeavassa näkymässä on välilehtiä, joista löytyy muun muassa indeksien (`Indices`) sekä indeksimuottien (`Index Templates`) hallintanäkymät. Molemmissa näkymissä on saatavilla lista siihen kuuluvista kohteista.

Indeksi voidaan poistaa merkitsemällä kyseinen indeksi valituksi ja klikkaamalla `Manage index` -painiketta. Painikkeesta aukeaa valikko, josta voidaan valita `Delete index`.

Indeksimuotti (index template) voidaan poistaa merkitsemällä kyseinen index template valituksi ja klikkaamalla `Delete template` -painiketta. Muotti poistetaan pysyvästi, joten sitä ei tule poistaa ilman erityistä syytä!

HUOM! Indeksien muuttaminen ei ole suositeltavaa, vaikka se onkin mahdollista. Muokkauksia ei tule tehdä ilman asiantuntemusta muutoksien vaikutuksista. Ensisijainen tapa on poista vanhat indeksit ja indeksoida sisältö uudelleen uusilla config -tiedostoon määritellyillä indeksointiasetuksilla. Jos muokataan vanhaa indeksiä, saattaa se aiheuttaa häiriöitä hakutoiminnoissa tai hakutulosten muuttumista saavuttamattomiksi.