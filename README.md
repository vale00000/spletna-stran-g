# Domača naloga: Varno shranjevanje gesel (DN8)

## Uvod
V tej domači nalogi bomo izboljšali varnost spletne aplikacije tako, da ne bomo več shranjevali gesel. To bo zmanjšalo tveganje, če bi nekdo pridobil dostop do baze podatkov.

## Vaša naloga

Namesto da bi gesla shranjevali direktno, boste implementirali tako imenovano **hash funkcijo**, ki bo shranjevala samo **dolžino gesla**.

**Opomba:** To je (zelo) slaba hash funkcija in se v praksi ne uporablja! Prava kriptografska hash funkcija (kot je recimo SHA-256) iz gesla ustvari niz iz katerega je težko uganiti katero geslo bi tak niz dalo.

## Koraki za implementacijo

### Korak 1: Sprememba baze podatkov

V datoteki `init_db.py` spremenite tabelo `users` tako, da stolpec `password` preimenujete v `password_hash`:

```python
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password_hash INTEGER NOT NULL
    )
''')
```

**Opomba:** Ne pozabite izbrisati stare baze podatkov (`test.db`), da boste lahko ustvarili novo (`uv run init_db.py`).

### Korak 2: Ustvarite hash funkcijo

Na vrhu datoteke `main.py` (pod vrstico `app = Flask(__name__)`), dodajte novo funkcijo:

```python
def hash_password(geslo):
    """
    Enostavna hash funkcija, ki vrne dolžino gesla.
    """
    return len(geslo)
```

### Korak 3: Spremenite registracijo

V funkciji `registracija_submit()` morate:

1. Namesto da shranjujete geslo direktno, uporabite hash funkcijo
2. Spremenite ime stolpca iz `password` v `password_hash`

**Pred spremembo:**
```python
insert_command = 'INSERT INTO users(username, password) VALUES("'+uporabnisko_ime+'", "'+geslo+'");'
```

**Po spremembi:**
```python
geslo_hash = hash_password(geslo)
insert_command = 'INSERT INTO users(username, password_hash) VALUES("'+uporabnisko_ime+'", '+str(geslo_hash)+');'
```

### Korak 4: Spremenite prijavo

V funkciji `prijava_submit()` morate:

1. Izračunati hash vnesenega gesla
2. Primerjati hash namesto gesla
3. Spremeniti ime stolpca iz `password` v `password_hash`

**Pred spremembo:**
```python
query = 'SELECT * FROM users WHERE username="'+uporabnisko_ime+'" AND password="'+geslo+'"'
```

**Po spremembi:**
```python
geslo_hash = hash_password(geslo)
query = 'SELECT * FROM users WHERE username="'+uporabnisko_ime+'" AND password_hash='+str(geslo_hash)
```

## Testiranje

1. **Izbrišite staro bazo podatkov:**
   ```bash
   rm test.db
   ```

2. **Ustvarite novo bazo podatkov:**
   ```bash
   uv run init_db.py
   ```

3. **Zaženite aplikacijo:**
   ```bash
   uv run main.py
   ```

4. **Testirajte:**
   - Registrirajte novega uporabnika (npr. username: `student`, geslo: `test1234`)
   - Odjavite se
   - Poskusite se prijaviti z istimi podatki
   - Prijava bi morala uspeti!
   - Poskusite se prijaviti z napačnim geslom ki pa ima isto dolžino (npr. `abcdefgh`), prijava bi morala prav tako uspeti!

5. **Preverite bazo podatkov:**
   ```bash
   sqlite3 test.db
   SELECT * FROM users;
   ```

   Videti bi morali nekaj takega:
   ```
   1|student|8
   ```

   Opazite, da je namesto gesla `test1234` shranjena številka `8` (dolžina gesla).

## Oddaja
Ko končate, kodo pushajte na github. V oddaji pošljite povezavo do vašega repozitorija.