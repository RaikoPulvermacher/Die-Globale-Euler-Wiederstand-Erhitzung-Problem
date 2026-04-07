# Orts-Entropie-Asymmetrie: Warum „Erneuerbar" kein Nullsummenspiel ist

> **These (Raiko Pulvermacher):** Wir entziehen lokal kinetische Energie (z. B. dem Wind der Nordsee), die aber global ist – während wir lokal Wärme erzeugen **und** global für Erhitzung sorgen, weil der Wind nicht nur die Umwandlungsenergie lokal aufnimmt, sondern die neue Leitung global wirkt.

---

## Das klassische Gegenargument und sein Scheitern

Das Standardargument der Klimamodelle lautet:  
*„Windenergie ist ein Nullsummenspiel – wir entziehen der Atmosphäre kinetische Energie und geben sie an anderer Stelle als Wärme zurück."*

Diese Argumentation scheitert in drei strukturellen Punkten:

---

## 1. Ortsverschiebung (Spatial Decoupling)

| Ort | Vorgang | Thermische Wirkung |
|---|---|---|
| Nordsee / Küste | Windturbine entzieht Strömungsenergie | Lokal: Abkühlung der Strömung |
| Tausende km Leitung | I²·R entlang Kupfer/Aluminium | Wärme in thermisch belasteten Zwischenregionen |
| Megacity / Datenzentrum | Endnutzung + Restwiderstände | Wärme genau dort, wo Urban Heat Island schon existiert |

Die Energie wird an einem **thermisch neutralen Ort** entnommen (Meereswind, Wüstensolar) und an einem **thermisch kritischen Ort** emittiert.  
Das ist keine Umverteilung – das ist **aktive Umverteilung in Problemzonen**.

```
KLASSISCHES BILD:   Entnahme(Wind) ←→ Abgabe(Wärme)  =  Nullsumme ✗
                     (gleicher Ort, gleiche Thermodynamik)

REALES BILD:        Entnahme(Nordsee, thermisch neutral)
                         ↓  80 Mio. km Kabel  →  I²·R  →  Wärme auf Strecke
                    Abgabe(Megacity, thermisch kritisch)   ≠  Nullsumme ✓
                         +  Entropieerhöhung (irreversibel)
                         +  Urban Heat Island Verstärkung
```

---

## 2. Die Leitung als planetarer Heizstab

Das Kabel ist kein passiver Kanal – es ist eine **gestreckte Wärmequelle**:

```
P_Leitung = I² · R_gesamt   mit   R_gesamt = ρ · L / A
```

- `L` = Leitungslänge
- `ρ` = spezifischer Widerstand des Leitermaterials
- `A` = Querschnittsfläche

Je weiter die Energie transportiert wird (globaler Netzausbau = größeres `L`), desto höher ist `R_gesamt`, desto mehr Joulesche Wärme entsteht **entlang der gesamten Strecke** – nicht nur am Zielort.

> **Die „grüne" Lösung von heute (massiver Netzausbau) ist physikalisch der Einbau eines weltumspannenden Tauchsieders.**

Konkrete Szenarienwerte (I = 1 000 A, 240 mm² Kupfer):

| Szenario | Länge | R [Ω] | P_Verlust |
|---|---|---|---|
| Lokal (50 km) | 50 km | 3,6 | 3,6 MW |
| Offshore (500 km) | 500 km | 35,8 | 35,8 MW |
| Fernleitung (2 000 km) | 2 000 km | 143 | 143 MW |
| Interkontinental (5 000 km) | 5 000 km | 358 | 358 MW |

---

## 3. Die Entropie-Falle (Entropy Trap)

Windenergie ist **geordnete, niederentropische Energie** (gerichtete Luftbewegung).  
Joulesche Wärme durch Leitungswiderstand ist **ungeordnete, hochentropische Energie** (thermische Agitation).

```
S_Wind (niedrig) → Leitungstransport → S_Abwärme (hoch)
```

Dieser Prozess ist **irreversibel** (Zweiter Hauptsatz der Thermodynamik).  
Wir beschleunigen den Wärmetod des Systems Erde nicht primär durch die Energiequelle, sondern durch die **schiere Länge und Komplexität der Netzinfrastruktur**.

CO₂-Modelle erfassen diesen Entropie-Anstieg durch Infrastruktur nicht —  
**die Globale Euler-Widerstand-Erhitzung schon.**

---

## Bedeutung für die Klimapolitik

| Maßnahme | Wirkung auf CO₂ | Wirkung auf I²R-Wärme |
|---|---|---|
| CO₂-Steuer | Reduziert | Keine direkte Wirkung |
| Mehr Windparks + Fernleitungen | Reduziert | **Erhöht** (mehr Infrastruktur) |
| Dezentrale Energieerzeugung | Teilweise reduziert | **Stark reduziert** (kurze Leitungswege) |
| Abschaltung von Rechenzentren | Keine Wirkung | Direkte Reduktion |

> **Serverraum-Analogie:** Wenn der Serverraum zu heiß wird, hilft es nichts, die Software zu optimieren (CO₂-Steuer), wenn die Hardware (das globale Netz) einfach zu viel Strom zieht und die Kühlung (die Natur) nicht hinterherkommt.

---

→ [Zurück zur Übersicht](../README.md) | [Weiter: Satellitenbeweise →](05_satellitenbeweise.md)
