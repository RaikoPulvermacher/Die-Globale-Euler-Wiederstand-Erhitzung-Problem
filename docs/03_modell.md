# Das Quantitative Modell

> Datei: [`euler_heat_model.py`](../euler_heat_model.py)

---

## Modellstruktur: Input → Prozess → Output

```
INPUT:   Weltweit eingespeiste elektrische Energie [TWh/Jahr]
          (fossil + erneuerbar – die Quelle spielt physikalisch keine Rolle)
            |
PROZESS: Transport durch ~80 Millionen km Kabel
          + ~1 Milliarde Transformatoren weltweit
          + Transportverluste: ~8–15 % des erzeugten Stroms
          + Endnutzungsverluste: weitere ~20–40 %
          + Rechenzentrums-Overhead: ~40 % PUE-Verlust
            |
OUTPUT:  Q = I² · R · t  →  Wärmeabstrahlung direkt an Erdoberfläche [EJ/Jahr]
```

---

## Grunddaten und Annahmen (Stand 2022/2023)

| Parameter | Wert | Quelle |
|---|---|---|
| Globale Stromproduktion | 29 165 TWh/Jahr | IEA 2023 |
| Transportverluste (Übertragung + Verteilung) | 8,5 % | IEA-Mittelwert |
| Endnutzungsverluste (Motoren, Netzteile, Standby) | 30 % | IEA / EPRI |
| Rechenzentrums-Overhead (PUE-Faktor) | 40 % | Uptime Institute 2022 |
| Anteil Rechenzentren am globalen Stromverbrauch | 2 % | IEA 2022 |
| Globale Kabellänge (geschätzt) | ~80 Mio. km | Diverse Netzbetreiber |
| Transformatoren weltweit (geschätzt) | ~1 Mrd. | World Bank / IRENA |

---

## Ergebnisse (quantitativ)

### Globale Joulesche Abwärme

| Verlustkomponente | TWh/Jahr | EJ/Jahr |
|---|---|---|
| Transportverluste (I²R in Kabeln und Trafos) | 2 479 | 8,92 |
| Endnutzungsverluste (Geräte, Motoren, Elektronik) | 8 008 | 28,83 |
| Rechenzentrums-Overhead | 233 | 0,84 |
| **Gesamt** | **~11 350** | **~40,9** |

### Wärmeflussdichte

| Bezugsgröße | Wert |
|---|---|
| Global gemittelt (Gesamt) | ~0,025 W/m² |
| Global gemittelt (nur Transport) | ~0,0054 W/m² |
| Urbaner Raum (75 % Infra auf 3 % Fläche) | **~1,5 W/m²** |

### Vergleich mit anderen Wärmequellen

| Quelle | W/m² |
|---|---|
| CO₂-Treibhauseffekt (gesamt, IPCC AR6) | ~3,7 |
| Globale anthropogene Wärme (Flanner 2009) | ~0,028 |
| **Dieses Modell – I²R gesamt** | **~0,025** |
| **Dieses Modell – Urban (lokal)** | **~1,5** |

**Schlussfolgerung:** Die globale Infrastrukturwärme ist vergleichbar mit dem Gesamt-Anthropogeneffekt aus Flanner (2009). Im urbanen Bereich übersteigt sie diesen um **zwei Größenordnungen**.

---

## Leitungslängen-Analyse (Orts-Asymmetrie)

```
P_Leitung = I² · R_gesamt   mit   R_gesamt = ρ · L / A

ρ_Kupfer = 1,72 × 10⁻⁸ Ω·m
```

| Szenario | Länge | R [Ω] | P_Verlust [MW] |
|---|---|---|---|
| Lokal (Kraftwerk 50 km) | 50 km | 3,58 | 3,58 |
| Offshore (500 km Küste→Stadt) | 500 km | 35,8 | 35,8 |
| Fernleitung (2 000 km Nordsee→Süd-DE) | 2 000 km | 143,3 | 143,3 |
| Interkontinental (5 000 km) | 5 000 km | 358,3 | 358,3 |

*Annahme: I = 1 000 A (typische 380-kV-Leitung), Querschnitt = 240 mm²*

**Interpretation:** Gleicher Strom, gleiche Energiequelle – aber 100× mehr Leitungslänge bedeutet 100× mehr Joulesche Wärme, verteilt über die gesamte Strecke.

---

## Stadttemperatur-Erhöhung pro TWh (Modellausgabe)

| Szenario | Fläche | Flux [W/m²] | ΔT adiabatisch [K] | ΔT Gleichgewicht [mK] |
|---|---|---|---|---|
| Kleinstadt | 100 km² | 0,00036 | 0,75 | 0,29 |
| Großstadt | 500 km² | 0,000071 | 0,15 | 0,057 |
| Metropolraum | 900 km² | 0,000040 | 0,083 | 0,032 |
| Megacity | 2 000 km² | 0,000018 | 0,037 | 0,014 |

*Diese Werte gelten **pro TWh** Durchfluss. Die gesamte urbane Infrastruktur bringt das Vielfache davon.*

---

## Modell ausführen

```bash
python euler_heat_model.py
```

Das Modell ist eigenständig ausführbar und gibt alle Berechnungsschritte mit Zwischenergebnissen aus.

---

→ [Zurück zur Übersicht](../README.md) | [Weiter: Orts-Entropie-Asymmetrie →](04_orts_entropie_asymmetrie.md)
