# Käyttöönotto (Keskitetty Hakuratkaisu)

Versio 0.1
# Vaiheet

1. Konfiguroi taustajärjestelmät ohjeiden mukaan:
   - Elasticsearch [(dokumentaatio)](./elastic_dokumentaatio.md)
   - Hakubackend [(dokumentaatio)](./hakubackend_dokumentaatio.md)
   - Crawler [(dokumentaatio)](./crawler_dokumentaatio.md)

2. Konfiguroi käyttöliittymä [(UI dokumentaatio)](./haku-ui_dokumentaatio.md)

3. Aja toteutusta esimerkiksi Dockerissa
   - anna tarvittavat tunnukset, salasanat ja palvelimien osoitteet docker-compose.yml -tiedostoon (voit hyödyntää esitäytettyä docker-compose_example.yml -pohjaa)
   - buildaa ja aja kontit ylös komennolla:<br>
      ```
      docker-compose up -d --build
      ```

4. Käynnistä crawler -kontti
   - käynnistä tarvittaessa NLP -kontti ([ohje](#nlp-kontti))
   - buildaa crawler -kontti komennolla:
      ```
      docker build -t crawler:latest -f .\crawler\Dockerfile .
      ```
   
   - käynnistä kontti komennolla (täydennä hakasulkeissa olevat arvot):
      ```
      docker run --rm --name crawler --net <elasticsearch_kontin_verkon_nimi> -v <elasticsearch_kontin_volumen_nimi>:/usr/share/elasticsearch -e elastic_write_username=<elastic_write_username> -e elastic_write_password=<elastic_write_password> crawler:latest
      ```

## STARTTAA KOKO SERVICE STACK (search_backend portissa 5000)
```
docker-compose up
```

Vaihtoehtoisesti detached mode -d parametrillä, jolloin esim. logien tarkastelu mahdollista
```
docker-compose up -d
docker logs <kontin-koko-nimi>
```

## NLP KONTTI
Jos halutaan käyttää NLP stemmausta, tarvitaan siihen erillinen Docker -kontti. NLP:n käyttö vaatii huomattavasti enemmän resursseja, kuin muut hakutoiminnot, joten sitä kannattaa ajaa vain tarpeen vaatiessa. Kontti vaatii vähintään noin neljä gigatavua vapaata muistia hakuratkaisun käyttämien resussien lisäksi. Ohjeet käynnistykseen [Crawlerin readme -tiedostossa](../crawler/README.md).

[Lisätietoja projektista](https://turkunlp.org/Turku-neural-parser-pipeline/).