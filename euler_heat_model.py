"""
Euler-Widerstand-Erhitzung Modell
==================================
Berechnet die globale Joulesche Wärme (I²·R) aus der weltweiten
elektrischen Infrastruktur als direkte Wärmequelle an der Erdoberfläche.

Physikalische Grundlage:
    P = I² · R  (Joulesches Gesetz, 1841)
    Q = P · t   (Wärmeenergie)

Euler-Netzwerk-Ansatz:
    Das globale Stromnetz ist ein Eulersches Netzwerk.
    Die Summe aller Widerstandsverluste in allen Knoten und Kanten
    ergibt die direkt erzeugte Abwärme an der Erdoberfläche.
"""

# --- Weltweite Grunddaten (Quellen: IEA 2023, World Bank) ---

# Globale Stromproduktion in TWh/Jahr (2022)
GLOBAL_ELECTRICITY_PRODUCTION_TWh = 29_165

# Durchschnittliche Transportverluste im Netz (Übertragung + Verteilung)
TRANSMISSION_LOSS_FRACTION = 0.085      # ~8.5% (IEA-Mittelwert weltweit)

# Verluste bei der Endnutzung (Motoren, Netzteile, Geräte im Standby etc.)
END_USE_LOSS_FRACTION = 0.30            # ~30% der genutzten Energie

# Verluste in Rechenzentren weltweit (PUE - Power Usage Effectiveness)
DATACENTER_OVERHEAD_FRACTION = 0.40    # ~40% Overhead (Kühlung, Infra)

# Anteil Rechenzentren an globalem Stromverbrauch
DATACENTER_SHARE = 0.02                 # ~2% des globalen Stroms

# Erdoberfläche in m²
EARTH_SURFACE_M2 = 5.1e14

# Sekunden pro Jahr
SECONDS_PER_YEAR = 365.25 * 24 * 3600

# Umrechnungsfaktor: 1 TWh = 3.6e15 Joule = 3.6 PJ
TWh_TO_JOULE = 3.6e15


def berechne_transport_verluste(produktion_TWh: float, verlustrate: float) -> float:
    """Joulesche Wärme durch Netzwerktransport (I²·R in Kabeln und Trafos)."""
    return produktion_TWh * verlustrate


def berechne_endnutzungs_verluste(produktion_TWh: float,
                                   transport_verlust: float,
                                   endnutzungsrate: float) -> float:
    """Joulesche Wärme bei der Endnutzung (Motoren, Geräte, Elektronik)."""
    genutzte_energie = produktion_TWh - transport_verlust
    return genutzte_energie * endnutzungsrate


def TWh_zu_EJ(TWh: float) -> float:
    """Konvertiert TWh in Exajoule (EJ)."""
    return TWh * 3.6e-3


def watt_pro_m2(energie_TWh: float) -> float:
    """Mittlere Wärmeflussdichte über die gesamte Erdoberfläche in W/m²."""
    energie_J = energie_TWh * TWh_TO_JOULE
    leistung_W = energie_J / SECONDS_PER_YEAR
    return leistung_W / EARTH_SURFACE_M2


def hauptrechnung():
    print("=" * 60)
    print("EULER-WIDERSTAND-ERHITZUNG: GLOBALE WÄRMEBERECHNUNG")
    print("P = I² · R  |  Joulesches Gesetz  |  Netzwerk-Theorie")
    print("=" * 60)
    print()

    # --- Schritt 1: Transportverluste ---
    transport_verlust = berechne_transport_verluste(
        GLOBAL_ELECTRICITY_PRODUCTION_TWh, TRANSMISSION_LOSS_FRACTION
    )
    print(f"Globale Stromproduktion:          {GLOBAL_ELECTRICITY_PRODUCTION_TWh:>10,.0f} TWh/Jahr")
    print(f"Transportverluste (I²R im Netz):  {transport_verlust:>10,.0f} TWh/Jahr"
          f"  ({TRANSMISSION_LOSS_FRACTION*100:.1f}%)")

    # --- Schritt 2: Endnutzungsverluste ---
    endnutzung_verlust = berechne_endnutzungs_verluste(
        GLOBAL_ELECTRICITY_PRODUCTION_TWh, transport_verlust, END_USE_LOSS_FRACTION
    )
    print(f"Endnutzungsverluste (Geräte etc): {endnutzung_verlust:>10,.0f} TWh/Jahr"
          f"  ({END_USE_LOSS_FRACTION*100:.0f}%)")

    # --- Schritt 3: Rechenzentren ---
    dc_energie = GLOBAL_ELECTRICITY_PRODUCTION_TWh * DATACENTER_SHARE
    dc_verlust = dc_energie * DATACENTER_OVERHEAD_FRACTION
    print(f"Rechenzentrum-Überhitze (PUE):    {dc_verlust:>10,.0f} TWh/Jahr"
          f"  ({DATACENTER_OVERHEAD_FRACTION*100:.0f}% von {dc_energie:.0f} TWh DC-Energie)")

    # --- Gesamt ---
    gesamt_verlust = transport_verlust + endnutzung_verlust + dc_verlust
    gesamt_EJ = TWh_zu_EJ(gesamt_verlust)

    print()
    print("-" * 60)
    print(f"GESAMTE JOULESCHE ABWÄRME:        {gesamt_verlust:>10,.0f} TWh/Jahr")
    print(f"                                  {gesamt_EJ:>10.2f} EJ/Jahr")
    print("-" * 60)

    # --- Wärmeflussdichte ---
    flux_global = watt_pro_m2(gesamt_verlust)
    flux_transport = watt_pro_m2(transport_verlust)

    print()
    print("WÄRMEFLUSSDICHTE (global gemittelt):")
    print(f"  Gesamt:        {flux_global:.4f} W/m²")
    print(f"  Nur Transport: {flux_transport:.4f} W/m²")
    print()
    print("VERGLEICH:")
    print(f"  CO₂-Treibhauseffekt (gesamt):  ~3.7 W/m²  (IPCC)")
    print(f"  Globale anthropogene Wärme:    ~0.028 W/m² (Flanner 2009)")
    print(f"  Dieses Modell (I²R gesamt):    {flux_global:.4f} W/m²")
    print()

    # --- Euler-Netzwerk-Beweis ---
    print("=" * 60)
    print("EULER-NETZWERK-ANALYSE")
    print("=" * 60)
    kabel_km = 80_000_000      # geschätzte globale Kabellänge in km
    trafos = 1_000_000_000     # geschätzte Anzahl Transformatoren weltweit
    print(f"  Globale Kabellänge:     ~{kabel_km/1e6:.0f} Millionen km")
    print(f"  Transformatoren:        ~{trafos/1e9:.0f} Milliarde")
    print(f"  In JEDEM dieser Elemente gilt: P = I² · R")
    print(f"  Die SUMME ist messbar: {gesamt_EJ:.2f} EJ/Jahr Wärme direkt am Boden")
    print()

    # --- Lokale Wärmedichte (Urban Heat Islands) ---
    print("=" * 60)
    print("LOKALE WÄRMEDICHTE (Urban Heat Islands)")
    print("=" * 60)
    urban_flaeche_m2 = 0.03 * EARTH_SURFACE_M2   # ~3% der Erdoberfläche urban
    urban_infrastruktur_anteil = 0.75              # 75% der Infrastruktur in Städten
    urban_verlust_TWh = gesamt_verlust * urban_infrastruktur_anteil
    urban_flux = (urban_verlust_TWh * TWh_TO_JOULE / SECONDS_PER_YEAR) / urban_flaeche_m2
    print(f"  Infrastruktur in Städten: ~{urban_infrastruktur_anteil*100:.0f}%")
    print(f"  Städtische Fläche:        ~{urban_infrastruktur_anteil*100:.0f}% der Infra"
          f" auf ~3% der Fläche")
    print(f"  Lokale Wärmeflussdichte:  {urban_flux:.2f} W/m²  ← Urban Heat Island Beitrag")
    print()

    # --- Orts-Entropie-Asymmetrie: Leitungslängen-Analyse ---
    print("=" * 60)
    print("ORTS-ENTROPIE-ASYMMETRIE: LEITUNG ALS PLANETARER HEIZSTAB")
    print("=" * 60)
    print("  These: Windenergie ist kein Nullsummenspiel.")
    print("  Entnahme (Küste/Meer, thermisch neutral)")
    print("  → I²·R über tausende km Kabel → Wärme auf gesamter Strecke")
    print("  → Emission (Megacity/Datenzentrum, thermisch kritisch)")
    print()

    # Spezifischer Widerstand Kupfer bei 20°C [Ohm·m]
    rho_kupfer = 1.72e-8
    # Typischer Leitungsquerschnitt Hochspannungsleitung [m²] (~240 mm²)
    querschnitt_m2 = 240e-6

    # Szenario-Vergleich: lokale vs. globale Einspeisung
    szenarien = [
        ("Lokal  (Kraftwerk  50 km vom Verbraucher)", 50_000),
        ("Mittel (Offshore  500 km Küste→Stadt)    ", 500_000),
        ("Global (Fernleitung 2000 km, z.B. Nordsee→Süd-DE)", 2_000_000),
        ("Makro  (Interkontinental 5000 km)         ", 5_000_000),
    ]

    # Typischer Nennstrom einer 380-kV-Hochspannungsleitung [A]
    strom_A = 1_000

    print(f"  Annahme: I = {strom_A} A (typische 380-kV-Leitung), "
          f"Querschnitt = {querschnitt_m2*1e6:.0f} mm²")
    print()
    print(f"  {'Szenario':<52} {'R [Ω]':>8}  {'P_Verlust [kW]':>16}  {'P_Verlust [MW]':>15}")
    print(f"  {'-'*52} {'-'*8}  {'-'*16}  {'-'*15}")
    for name, laenge_m in szenarien:
        R = rho_kupfer * laenge_m / querschnitt_m2
        P_W = strom_A ** 2 * R
        print(f"  {name}  {R:>8.2f}  {P_W/1e3:>16.1f}  {P_W/1e6:>15.3f}")

    print()
    print("  → Gleicher Strom, gleiche Quelle, aber 100× mehr Leitungslänge")
    print("    = 100× mehr Joulesche Wärme, verteilt auf die gesamte Strecke.")
    print("  → Diese Wärme entsteht NICHT am Entnahmeort (Nordsee),")
    print("    sondern entlang der Leitung und am Zielort (Megacity).")
    print("  → Das ist der physikalische Beweis gegen das 'Nullsummenspiel'.")
    print()

    # Entropie-Argument
    print("  ENTROPIE-FALLE:")
    print("  Windenergie  →  geordnet (niederentropisch, gerichtete Strömung)")
    print("  I²·R-Verlust →  Abwärme  (hochentropisch, thermische Agitation)")
    print("  Zweiter Hauptsatz: dieser Prozess ist irreversibel.")
    print("  Jede neue Leitungslänge beschleunigt die Entropieproduktion")
    print("  des Systems Erde – unabhängig von der Energiequelle.")
    print()

    # --- FN-Zeitlogik ---
    print("=" * 60)
    print("FN-ZEITLOGIK: Asymmetrie → Symmetrie → Weiter")
    print("=" * 60)
    fib = [1, 1]
    paritat = []
    for i in range(2, 15):
        fib.append(fib[-1] + fib[-2])
    for n in fib:
        paritat.append("G" if n % 2 == 0 else "U")
    print("  Fibonacci: " + "  ".join(f"{n:5d}" for n in fib))
    print("  Parität:   " + "    ".join(paritat))
    print()
    print("  Muster: UUG wiederholt sich exakt alle 3 Schritte")
    print("  U+U=G : Asymmetrie + Asymmetrie = Symmetrie (aber kein Stopp!)")
    print("  G+U=U : Symmetrie zieht sofort weiter → Zeitlogik")
    print("  → Globale Erwärmung durch I²R folgt dem gleichen Prinzip:")
    print("    Kein Gleichgewicht, immer additiv, kein Ruhemodus.")
    print()
    print("  Das ist Zeitlogik. Das ist Euler. Das ist Physik.")
    print("=" * 60)


if __name__ == "__main__":
    hauptrechnung()
