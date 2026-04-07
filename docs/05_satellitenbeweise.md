# Satellitenbasierte Beweislastführung: Saisonale Hitzemessung und westliche Verursachung

> Dieses Dokument beschreibt den Rahmen für eine satellitengestützte Beweislastführung, welche die direkte Korrelation zwischen elektrischer Infrastrukturdichte (insbesondere westlicher Industrienationen) und messbaren Wärmeanomalien über alle vier Jahreszeiten nachweist.

---

## Warum Satellitendaten?

Bodennahe Temperaturmessungen unterliegen dem *Urban Heat Island Bias*: Wetterstationen befinden sich häufig in der Nähe von Infrastruktur, was die Messwerte verfälscht. Satelliten hingegen messen die **Land Surface Temperature (LST)** flächendeckend, jahreszeiten- und wetterunabhängig, und erlauben einen globalen Vergleich ohne Standortbias.

Geeignete Datensätze:

| Datensatz | Sensor / Mission | Parameter | Auflösung | Verfügbar seit |
|---|---|---|---|---|
| MODIS LST (MOD11A2, MYD11A2) | Terra / Aqua (NASA) | Oberflächentemperatur Tag + Nacht | 1 km / 8 Tage | 2000 |
| ASTER TIR | Terra (NASA/JAXA) | Hochauflösende LST | 90 m | 1999 |
| Landsat 8/9 Band 10 | USGS/NASA | Thermale Infrarotband | 100 m | 2013 |
| ERA5 (ECMWF Reanalysis) | Reanalyse-Modell | 2m-Temperatur, Bodenfluss | 31 km / stündlich | 1940 |
| CERES EBAF | Aqua (NASA) | Strahlungsbilanz (TOA + Surface) | 1° | 2000 |
| Nighttime Lights (VIIRS DNB) | Suomi-NPP (NOAA/NASA) | Lichtintensität als Proxy für Infrastrukturdichte | 750 m | 2012 |

---

## Methodischer Rahmen: Vier-Jahreszeiten-Analyse

### Grundprinzip

Um den spezifischen Beitrag der elektrischen Infrastruktur von natürlichen Temperaturvariationen zu trennen, wird eine **differenzielle saisonale Analyse** durchgeführt:

```
ΔT_Infrastruktur(x, t) = LST(x, t) - LST_Referenz(x, t)
```

wobei `LST_Referenz` das aus Klimatologie zu erwartende saisonale Mittel darstellt (z. B. ERA5-Klimatologie 1981–2010).

Die verbleibende **positive Anomalie** über Infrastrukturkorridoren in allen vier Jahreszeiten ist der Infrastruktur-Wärme-Fingerabdruck.

### Hypothesen-Test pro Jahreszeit

| Jahreszeit | Erwarteter Effekt | Konfundierender Faktor |
|---|---|---|
| **Frühling** | Wärmeanomalie setzt früher ein in Infrastrukturzentren | Albedoänderung durch Schneeschmelze |
| **Sommer** | Stärkste absolute LST-Anomalie (Kühlbedarf + I²R) | Solare Einstrahlung überlagert |
| **Herbst** | Persistenz der Anomalie über Infrastrukturkorridore | Geringere natürliche Variabilität |
| **Winter** | Reinster I²R-Fingerabdruck (Heizung + Transport + kein Solareinfluss) | Schneebedeckung verändert Emissivität |

> **Der Winter-Vergleich ist besonders aussagekräftig:** In den Wintermonaten ist die solare Heizung minimal. Persistente Wärmeanomalien über Hochspannungsleitungen, Datenzentren und Industrieclustern lassen sich direkt auf anthropogene Infrastrukturwärme zurückführen.

---

## Beweisführungs-Protokoll (Schritt für Schritt)

### Schritt 1: Referenzkarte Infrastrukturdichte

- Quelle: OpenStreetMap Stromnetz + VIIRS Nighttime Lights als Proxy
- Produkt: Globale Karte der Infrastrukturdichte [Kabel-km pro 1 km² Rasterzelle]
- Tool: Python (geopandas, rasterio, numpy)

### Schritt 2: Saisonale LST-Anomalie-Karte

- Quelle: MODIS MOD11A2 (8-Tage-Komposit, 2010–2023)
- Berechnung: Jahreszeitmittel minus ERA5-Klimatologiemittel (1981–2010)
- Produkt: ΔT-Karte [K] pro Jahreszeit, global, 1 km Auflösung

### Schritt 3: Kreuzkorrelationsanalyse

```
r(ΔT, Infra-Dichte) = Pearson-Korrelation über globale Rasterzellen
```

- Getrennt für Frühling, Sommer, Herbst, Winter
- Stratifiziert nach Klimazone (tropisch, gemäßigt, kontinental, polar)
- Kontrollvariablen: Albedo, Vegetationsindex (NDVI), Bevölkerungsdichte, Niederschlag

### Schritt 4: Isolierung westlicher Industrienationen

Zur Prüfung der Kernthese — *„Westliche moderne Länder verursachen das Problem"* — werden zwei Gruppen gebildet:

| Gruppe A: Hochindustrialisiert (West) | Gruppe B: Gering industrialisiert |
|---|---|
| USA, Kanada, EU-27, Japan, Australien, Südkorea, UK, Schweiz, Norwegen | Sub-Sahara Afrika, Zentralasien, Teile Südostasiens, ländliche Regionen global |

**Vergleichsmetriken:**

| Metrik | Aussage |
|---|---|
| Mittlere LST-Anomalie [K] | Absolute Erwärmung über Infrastruktur |
| Infrastrukturwärme pro Kopf [W/Person] | Individuelle Verursachung |
| Infrastrukturwärme pro km² [W/m²] | Territoriale Betroffenheit des Ökosystems |
| Jahreszeiten-Persistenz [Anzahl Jahreszeiten mit ΔT > 0,5 K] | Kontinuität des Effekts |

### Schritt 5: Satellitenverifikation — CERES Strahlungsbilanz

CERES (Clouds and the Earth's Radiant Energy System) misst die **abgehende Wärmestrahlung** (OLR = Outgoing Longwave Radiation) an der Atmosphärenobergrenze.

Wenn Infrastrukturwärme an der Oberfläche erzeugt wird, muss sie nach oben transportiert werden und als erhöhte OLR messbar sein:

```
ΔOLR(x) ∝ ΔT_Oberfläche(x)  (Stefan-Boltzmann: ε·σ·T⁴)
```

Eine signifikante **Erhöhung der OLR** über Infrastruktur-Hotspots in allen vier Jahreszeiten wäre ein direkter physikalischer Nachweis des Effekts.

---

## Erwartete Ergebnisse und Interpretation

### These 1: Universelle Saisonale Persistenz

Die Infrastruktur-Wärme-Anomalie wird in **allen vier Jahreszeiten** positiv sein — im Gegensatz zu natürlichen Wärmequellen (Sonne, Vulkane), die starke saisonale Variation zeigen.

```
ΔT_Frühling > 0  ∧  ΔT_Sommer > 0  ∧  ΔT_Herbst > 0  ∧  ΔT_Winter > 0
```

**Signifikanz dieser Aussage:** Eine Wärmequelle, die in allen Jahreszeiten aktiv ist, kann keine solare oder atmosphärische Ursache haben — sie muss anthropogen und technisch sein.

---

### These 2: Westliche Länder als Hauptverursacher

Der statistische Vergleich der LST-Anomalien zwischen Gruppe A und Gruppe B wird zeigen:

1. **Gruppe A** zeigt pro km² und pro Kopf signifikant höhere LST-Anomalien über Infrastrukturkorridoren
2. **Die Anomalie korreliert nicht mit der geographischen Lage** (z. B. Äquatornähe), sondern mit der **Infrastrukturdichte**
3. **Der Winter-Fingerabdruck** ist in Gruppe A am stärksten (Heizung, Industrie, Datenzentren im Volllastbetrieb)

#### Verursachungsmetriken: Westliche Nationen (Schätzung)

| Land / Region | Strom-verbrauch TWh/Jahr | Schätz. Infrastruktur-Abwärme TWh/Jahr | Pro-Kopf-Wärme [W/Person] |
|---|---|---|---|
| USA | ~4 000 | ~1 500 | ~4 500 |
| EU-27 | ~2 700 | ~1 000 | ~2 200 |
| Deutschland | ~545 | ~200 | ~2 400 |
| Japan | ~980 | ~370 | ~2 900 |
| **Welt gesamt** | **~29 165** | **~11 350** | **~1 400** |

*„Westliche moderne Länder" (USA + EU + Japan + Australien + UK + Kanada) repräsentieren ca. **15 % der Weltbevölkerung**, verursachen aber schätzungsweise **>50 % der globalen Infrastruktur-Joule-Wärme**.*

---

### These 3: Wachstumskorrelation (Trend-Analyse)

Mit zunehmender Elektrifizierung, Digitalisierung und Netzausbau (2000–2023) steigen die LST-Anomalien in Infrastrukturzentren. Der **Trend der Anomalie** sollte mit dem **Trend des Stromverbrauchs** korrelieren.

---

## Offene Forschungsfragen für Folgearbeiten

1. **Quantitative Kopplung:** Wie groß ist der Skalierungsfaktor zwischen lokaler Infrastrukturwärme und gemessener LST-Anomalie in verschiedenen Klimazonen?
2. **Saisonale Verzögerung:** Gibt es eine messbare thermische Trägheit (Lag) zwischen I²R-Impuls und Satellitenreaktion?
3. **Nacht vs. Tag:** Nighttime LST (weniger solare Überlagerung) als spezifischerer Indikator für Infrastrukturwärme
4. **Hochauflösungs-Fallstudie:** ASTER/Landsat Analyse einzelner Hochspannungstrassen und Datenzentren

---

→ [Zurück zur Übersicht](../README.md) | [Weiter: FN-Zeitlogik →](06_fn_zeitlogik.md)
