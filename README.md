# Treenisovellus

Sovellus on treenipäiväkirja tyylinen toteutus, jolla voi pitää kirjaa tehdyistä treeneistä. Sovellukseen voi luoda käyttäjän ja olla vuorovaikutuksessa muiden käyttäjien kanssa.

## Sovelluksen toiminnallisuudet
Sovelluksessa toimii tällä hetkellä seuraavat toiminnallisuudet.
- Käyttäjä voi luoda tunnuksen, jolla voi kirjautua sisään sekä ulos.
- Käyttäjä voi lisätä uuden treenin.
- Käyttäjä voi poistaa treenin.
- Käyttäjä näkee etusivullaan treenit kronologisessa järjestyksessä niin että uusin treeni näkyy ensin ja vanhin viimeisenä.
- Käyttäjä näkee etusivullaan myös koosteosion jossa lukee kaikkien omien treenien kokonaiskesto ja treenien lukumäärä.
- Treenille tulee sen luomishetkellä määritellä päivämäärä, treenin kesto tunteina ja minuutteina sekä laji. Nämä tiedot tallentuvat tietokantaan.
- Käyttäjä voi lisätä toisen käyttäjän kaverikseen etsimällä tämän käyttäjätunnuksen järjestelmästä.
- Käyttäjä voi tarkastella kaverin etusivua.

Sovellukseen tehdään vielä seuraavat asiat ennen loppupalautusta:
- Toiminnallisuus, jossa sekä omalle että kaverin treenille voi lisätä kommentin. (Tällä hetkellä vain omalle treenille voi lisätä kommentin).
- Käyttäjän oikeuksien ja tietoturvan tarkistus ja tarvittavien muutosten tekeminen näihin liittyen.
- Ulkoasusta vielä selkeämpi.

## Ohjeet sovelluksen käynnistämiseen paikallisesti
1) Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon.   

2) Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

> DATABASE_URL=\<tietokannan-paikallinen-osoite>   
> SECRET_KEY=\<salainen-avain>

3) Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

`$ python3 -m venv venv`  
`$ source venv/bin/activate`  
`$ pip install -r ./requirements.txt`

4) Määritä vielä tietokannan skeema komennolla

`$ psql < schema.sql`

5) Voit ajaa sovelluksen komennolla

`$ flask run`

