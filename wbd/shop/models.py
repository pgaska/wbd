from django.db import models

# Create your models here.

class Dostawcy(models.Model):
    id_dostawcy = models.BigIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    nr_telefonu = models.CharField(max_length=15)
    nip = models.CharField(max_length=10)
    id_hurtowni = models.ForeignKey('Hurtownie', models.DO_NOTHING, db_column='id_hurtowni')

    class Meta:
        managed = False
        db_table = 'dostawcy'


class Dostawy(models.Model):
    id_dostawy = models.BigIntegerField(primary_key=True)
    data = models.DateField()
    id_dostawcy = models.ForeignKey(Dostawcy, models.DO_NOTHING, db_column='id_dostawcy')
    id_przewoznika = models.ForeignKey('Przewoznicy', models.DO_NOTHING, db_column='id_przewoznika')
    id_magazynu = models.ForeignKey('Magazyny', models.DO_NOTHING, db_column='id_magazynu')

    class Meta:
        managed = False
        db_table = 'dostawy'

class Hurtownie(models.Model):
    id_hurtowni = models.BigIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=64)
    nip = models.CharField(max_length=10)
    regon = models.CharField(max_length=9)
    miejscowosc = models.CharField(max_length=30)
    ulica = models.CharField(max_length=40, blank=True, null=True)
    nr_budynku = models.CharField(max_length=4)
    nr_lokalu = models.CharField(max_length=4, blank=True, null=True)
    id_poczty = models.ForeignKey('Poczta', models.DO_NOTHING, db_column='id_poczty')

    class Meta:
        managed = False
        db_table = 'hurtownie'

class Magazyny(models.Model):
    id_magazynu = models.BigIntegerField(primary_key=True)
    miejscowosc = models.CharField(max_length=30)
    ulica = models.CharField(max_length=40, blank=True, null=True)
    nr_budynku = models.CharField(max_length=4)
    nr_lokalu = models.CharField(max_length=4, blank=True, null=True)
    powierzchnia = models.FloatField()
    id_hurtowni = models.ForeignKey(Hurtownie, models.DO_NOTHING, db_column='id_hurtowni')
    id_poczty = models.ForeignKey('Poczta', models.DO_NOTHING, db_column='id_poczty')

    class Meta:
        managed = False
        db_table = 'magazyny'

class Pamiec(models.Model):
    id_pamieci = models.BigIntegerField(primary_key=True)
    typ = models.CharField(max_length=4)
    pojemnosc = models.BigIntegerField()
    id_towaru = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'pamiec'
        unique_together = (('id_pamieci', 'id_towaru'),)


class PlytaGlowna(models.Model):
    id_plyty_glownej = models.BigIntegerField(primary_key=True)
    chipset = models.CharField(max_length=15)
    standard_pamieci = models.CharField(max_length=4)
    id_towaru = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'plyta_glowna'
        unique_together = (('id_plyty_glownej', 'id_towaru'),)


class Poczta(models.Model):
    id_poczty = models.BigIntegerField(primary_key=True)
    miasto = models.CharField(max_length=30)
    kod_pocztowy = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'poczta'


class Procesor(models.Model):
    id_procesora = models.BigIntegerField(primary_key=True)
    liczba_rdzeni = models.BigIntegerField()
    taktowanie = models.FloatField()
    id_towaru = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'procesor'
        unique_together = (('id_procesora', 'id_towaru'),)


class Przewoznicy(models.Model):
    id_przewoznika = models.BigIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    nr_telefonu = models.CharField(max_length=15)
    id_hurtowni = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'przewoznicy'


class PunktySprzedazy(models.Model):
    id_punktu_sprzedazy = models.BigIntegerField(primary_key=True)
    miejscowosc = models.CharField(max_length=30)
    ulica = models.CharField(max_length=40, blank=True, null=True)
    nr_budynku = models.CharField(max_length=4)
    nr_lokalu = models.CharField(max_length=4, blank=True, null=True)
    powierzchnia = models.FloatField()
    id_hurtowni = models.ForeignKey(Hurtownie, models.DO_NOTHING, db_column='id_hurtowni')
    id_poczty = models.ForeignKey(Poczta, models.DO_NOTHING, db_column='id_poczty')

    class Meta:
        managed = False
        db_table = 'punkty_sprzedazy'

class SzczegolyDostawy(models.Model):
    id_dostawy = models.ForeignKey(Dostawy, models.DO_NOTHING, db_column='id_dostawy', primary_key=True)
    id_towaru = models.BigIntegerField()
    ilosc = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'szczegoly_dostawy'
        unique_together = (('id_dostawy', 'id_towaru'),)


class SzczegolyZamowienia(models.Model):
    id_zmowienia = models.BigIntegerField(primary_key=True)
    id_towaru = models.ForeignKey('Towary', models.DO_NOTHING, db_column='id_towaru')
    ilosc = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'szczegoly_zamowienia'
        unique_together = (('id_zmowienia', 'id_towaru'),)


class Towary(models.Model):
    id_towaru = models.BigIntegerField(primary_key=True)
    produent = models.CharField(max_length=60)
    kod_producenta = models.CharField(max_length=20)
    model = models.CharField(max_length=20, blank=True, null=True)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    id_magazynu = models.ForeignKey(Magazyny, models.DO_NOTHING, db_column='id_magazynu')

    class Meta:
        managed = False
        db_table = 'towary'


class Wlasciciele(models.Model):
    id_wlasciciela = models.BigIntegerField(primary_key=True)
    imie = models.CharField(max_length=20)
    nazwisko = models.CharField(max_length=40)
    data_od = models.DateField()
    data_do = models.DateField(blank=True, null=True)
    id_hurtowni = models.ForeignKey(Hurtownie, models.DO_NOTHING, db_column='id_hurtowni')

    class Meta:
        managed = False
        db_table = 'wlasciciele'


class Wynagrodzenia(models.Model):
    id_wynagrodzenia = models.BigIntegerField(primary_key=True)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    premia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_pracownika = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wynagrodzenia'


class Zamwienia(models.Model):
    id_zmowienia = models.BigIntegerField(primary_key=True)
    data = models.DateField()
    id_klienta = models.BigIntegerField()
    id_przewoznika = models.ForeignKey(Przewoznicy, models.DO_NOTHING, db_column='id_przewoznika', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zamówienia'