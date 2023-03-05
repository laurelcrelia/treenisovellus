# Treenisovellus

Sovellus on treenipäiväkirja tyylinen toteutus, jolla voi pitää kirjaa tehdyistä treeneistä. Sovellukseen voi luoda käyttäjän ja olla vuorovaikutuksessa muiden käyttäjien kanssa.

## Sovelluksen toiminnallisuudet
- Käyttäjä voi luoda tunnuksen, jolla voi kirjautua sisään sekä ulos.
- Käyttäjä voi lisätä uuden treenin.
- Käyttäjä voi poistaa treenin.
- Käyttäjä näkee etusivullaan treenit kronologisessa järjestyksessä niin että uusin treeni näkyy ensin ja vanhin viimeisenä.
- Käyttäjä näkee etusivullaan myös koosteosion jossa lukee kaikkien omien treenien kokonaiskesto ja treenien lukumäärä.
- Treenille tulee sen luomishetkellä määritellä päivämäärä, treenin kesto tunteina ja minuutteina sekä laji. Nämä tiedot tallentuvat tietokantaan.
- Käyttäjä voi lähettää kaveripyynnön toiselle käyttäjälle etsimällä tämän käyttäjätunnuksen järjestelmästä.
- Kaverisuhde varmistuu kun kyseinen käyttäjä käy hyväksymässä lähettämäsi kaveripyynnön.
- Käyttäjä voi tarkastella kaverin etusivua ja treenejä.
- Sekä omalle että kaverin treenille voi lisätä kommentin.

## Ohjeet sovelluksen käynnistämiseen paikallisesti


1) Kloonaa tämä repositorio omalle koneellesi.

2) Jos et ole asentanut PostgreSQL:ää ja käytät Linuxia tee se [näiden](https://github.com/hy-tsoha/local-pg) ohjeiden avulla.    
  Muiden järjestelmien asennusohjeita löytyy [täältä](https://postgresql.org/download/).

3) Siirry uudessa komentorivi-ikkunassa hakemistoon, jossa äsken asentamasi PostgreSQL sijaitsee. Käynnistä tietokanta komennolla
    ```$ start-pg.sh```

4) Avaa taas uusi komentorivi-ikkuna ja avaa PostgreSQL-tulkki komennolla    
    ```$ psql```    
  Luo nyt uusi tietokanta sovellusta varten komennolla    
    ```$ CREATE DATABASE <tietokannan nimi>;```

5) Siirry sovelluksen juurikansioon ja luo sinne .env-tiedosto.   
  Määritä tiedoston sisältö seuraavanlaiseksi, mikäli asensit PostgreSQL:n ensimmäisen linkin ohjeen avulla:    
  ```
  DATABASE_URL=postgresql+psycopg2:///\<tietokannan nimi>    
  SECRET_KEY=\<salainen-avain>
  ```
  Muuten:   
  ```
  DATABASE_URL=postgresql:///\<tietokannan nimi>   
  SECRET_KEY=\<salainen-avain>
  ```

6) Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla    
  ```$ python3 -m venv venv```    
  ```$ source venv/bin/activate```    
  ```$ pip install -r ./requirements.txt```


7) Määritä vielä tietokannan skeema sovelluksen juurihakemistossa komennolla    
```$ psql -d <tietokannan nimi> < schema.sql```   


8) Nyt voit ajaa sovelluksen komennolla   
```$ flask run```

