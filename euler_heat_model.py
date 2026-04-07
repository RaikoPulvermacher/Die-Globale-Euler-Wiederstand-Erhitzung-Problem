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


def ausgabe_spezifische_leitungslaenge(laenge_km: float,
                                        strom_A: float = 1_000,
                                        querschnitt_mm2: float = 240) -> dict:
    """
    Modellausgabe für eine spezifische Leitungslänge.

    Gibt Widerstand, Verlustleistung und Energieverlust pro Jahr zurück.

    Parameters
    ----------
    laenge_km       : Leitungslänge in Kilometern
    strom_A         : Nennstrom in Ampere (Standard: 1000 A / 380-kV-Leitung)
    querschnitt_mm2 : Leiterquerschnitt in mm² (Standard: 240 mm²)
    """
    rho_kupfer = 1.72e-8            # spez. Widerstand Kupfer [Ω·m]
    laenge_m = laenge_km * 1_000
    querschnitt_m2 = querschnitt_mm2 * 1e-6

    R_ohm = rho_kupfer * laenge_m / querschnitt_m2
    P_verlust_W = strom_A ** 2 * R_ohm
    P_verlust_MW = P_verlust_W / 1e6
    energie_verlust_TWh_pro_jahr = (P_verlust_W * SECONDS_PER_YEAR) / TWh_TO_JOULE

    return {
        "laenge_km": laenge_km,
        "R_ohm": R_ohm,
        "P_verlust_MW": P_verlust_MW,
        "energie_verlust_TWh_pro_jahr": energie_verlust_TWh_pro_jahr,
    }


def grad_pro_TWh_ballungsraum(flaeche_km2: float = 900,
                               grenzschicht_m: float = 1_500,
                               verlustrate: float = None,
                               stadt_name: str = "Typische Großstadt") -> dict:
    """
    Berechnet die Temperaturerhöhung in einem Ballungsraum
    pro Terawattstunde elektrischen Durchflusses.

    Zwei Ansätze:
    1. Adiabatisch  – theoretisches Maximum (keine Wärmeabgabe nach außen).
    2. Strahlungsgleichgewicht – realistischer Langzeitwert über die
       lokale Klimasensitivität (ΔT ≈ ΔF / λ, λ ≈ 0.8 °C per W/m²).

    Parameters
    ----------
    flaeche_km2     : Fläche des Ballungsraums in km² (Standard 900 km²)
    grenzschicht_m  : Höhe der urbanen Grenzschicht in m  (Standard 1500 m)
    verlustrate     : Gesamtanteil der Energie, der als Joule-Wärme lokal
                      deponiert wird (Standard: Transport + Endnutzung kombiniert)
    stadt_name      : Bezeichnung des Szenarios
    """
    if verlustrate is None:
        verlustrate = TRANSMISSION_LOSS_FRACTION + END_USE_LOSS_FRACTION * (
            1 - TRANSMISSION_LOSS_FRACTION
        )

    flaeche_m2 = flaeche_km2 * 1e6

    # --- Thermische Masse der urbanen Luftsäule ---
    rho_luft = 1.2          # kg/m³
    cp_luft = 1_005         # J/(kg·K)
    luftmasse_kg = flaeche_m2 * grenzschicht_m * rho_luft
    waermekapazitaet_J_pro_K = luftmasse_kg * cp_luft

    # --- Joule-Wärme pro 1 TWh Durchfluss ---
    joulewaerme_J = 1 * TWh_TO_JOULE * verlustrate        # J

    # --- Ansatz 1: Adiabatisch (Impuls-Wärme, kein Austausch) ---
    delta_T_adiabatisch = joulewaerme_J / waermekapazitaet_J_pro_K

    # --- Ansatz 2: Strahlungsgleichgewicht (kontinuierlich, 1 TWh/Jahr) ---
    leistung_W = joulewaerme_J / SECONDS_PER_YEAR          # W (Durchschnitt über 1 Jahr)
    flussdichte_W_m2 = leistung_W / flaeche_m2
    lambda_lokal = 0.8      # °C per W/m²  (lokale Klimasensitivität, urban)
    delta_T_gleichgewicht = flussdichte_W_m2 * lambda_lokal

    return {
        "stadt_name": stadt_name,
        "flaeche_km2": flaeche_km2,
        "verlustrate_pct": verlustrate * 100,
        "joulewaerme_TWh_pro_TWh": joulewaerme_J / TWh_TO_JOULE,
        "flussdichte_W_m2": flussdichte_W_m2,
        "delta_T_adiabatisch_K": delta_T_adiabatisch,
        "delta_T_gleichgewicht_K": delta_T_gleichgewicht,
    }


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

    # --- Gemini-Frage 1: Ausgabe für eine spezifische Leitungslänge ---
    print()
    print("=" * 60)
    print("GEMINI-FRAGE 1: MODELLAUSGABE FÜR EINE SPEZIFISCHE LEITUNGSLÄNGE")
    print("=" * 60)
    beispiel_km = 500
    ergebnis = ausgabe_spezifische_leitungslaenge(beispiel_km)
    print(f"  Leitungslänge:         {ergebnis['laenge_km']:>10,.0f} km")
    print(f"  Widerstand R:          {ergebnis['R_ohm']:>10.2f} Ω")
    print(f"  Verlustleistung P=I²R: {ergebnis['P_verlust_MW']:>10.3f} MW")
    print(f"  Joule-Energie/Jahr:    {ergebnis['energie_verlust_TWh_pro_jahr']:>10.4f} TWh/Jahr")
    print()
    print("  (Annahme: I = 1000 A, Querschnitt = 240 mm², Kupfer)")
    print()

    # --- Gemini-Frage 2: °C pro TWh in einem Ballungsraum ---
    print("=" * 60)
    print("GEMINI-FRAGE 2: TEMPERATURERHÖHUNG PRO TWh IN EINEM BALLUNGSRAUM")
    print("=" * 60)
    staedte = [
        ("Kleinstadt   (~100 km²)",  100, 1_000),
        ("Großstadt    (~500 km²)",  500, 1_500),
        ("Metropolraum (~900 km²)",  900, 1_500),
        ("Megacity    (~2000 km²)", 2_000, 2_000),
    ]
    print(f"  {'Szenario':<30}  {'Verlust':>8}  {'Flux W/m²':>10}  "
          f"{'ΔT adiab. [K]':>14}  {'ΔT Gleichgew. [K]':>18}")
    print(f"  {'-'*30}  {'-'*8}  {'-'*10}  {'-'*14}  {'-'*18}")
    for name, flaeche, grenzschicht in staedte:
        r = grad_pro_TWh_ballungsraum(flaeche_km2=flaeche,
                                       grenzschicht_m=grenzschicht,
                                       stadt_name=name)
        print(f"  {name:<30}  {r['verlustrate_pct']:>7.1f}%  "
              f"{r['flussdichte_W_m2']:>10.5f}  "
              f"{r['delta_T_adiabatisch_K']:>14.4f}  "
              f"{r['delta_T_gleichgewicht_K']:>18.6f}")
    print()
    print("  Erklärung der zwei Ansätze:")
    print("  • ΔT adiabatisch   = theoretisches Maximum (1 TWh in die Luftsäule,")
    print("                       keine Wärmeabgabe nach außen)")
    print("  • ΔT Gleichgewicht = realistischer Langzeitwert (1 TWh/Jahr kontinuierlich,")
    print("                       Strahlungsgleichgewicht: ΔT = Flux / 0.8 °C·m²/W)")
    print()
    print("  → Pro TWh Durchfluss hebt Joule-Wärme die Temperatur im Gleichgewicht")
    r_ref = grad_pro_TWh_ballungsraum(flaeche_km2=900, grenzschicht_m=1_500)
    print(f"    um ~{r_ref['delta_T_gleichgewicht_K']*1000:.3f} mK (Metropolraum 900 km²)")
    print(f"    oder adiabatisch um ~{r_ref['delta_T_adiabatisch_K']:.2f} K an.")
    print("=" * 60)


if __name__ == "__main__":
    hauptrechnung()
