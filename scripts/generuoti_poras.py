"""
KrepšelisAI – etaloninių (X, y) porų generatorius.

X = vartotojo užklausa laisvu tekstu.
y = teisingas sistemos atsakymas: atpažintas sąrašas, krepšelio sumos
    kiekviename tinkle, pigiausias tinklas, geriausias 2 parduotuvių derinys
    ir žmogiškas atsakymas.

Atpažintas sąrašas (ką LLM turi ištraukti iš teksto) užrašytas ranka,
o visi skaičiai apskaičiuojami iš data/kainos.csv, todėl y visada sutampa
su kainų katalogu.

Paleidimas:  python scripts/generuoti_poras.py
"""

import csv
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PROMPTS = ROOT / "prompts"
TINKLAI = ["Rimi", "IKI", "Norfa"]

PAVYZDZIAI = [
    {
        "id": "01",
        "pavadinimas": "Kasdieniai pusryčiai",
        "X": "Reikia pieno, duonos, 10 kiaušinių ir sviesto",
        "sarasas": [
            {"preke_id": "pienas_1l", "kiekis": 1},
            {"preke_id": "duona_800g", "kiekis": 1},
            {"preke_id": "kiausiniai_10", "kiekis": 1},
            {"preke_id": "sviestas_200g", "kiekis": 1},
        ],
        "nerasta": [],
    },
    {
        "id": "02",
        "pavadinimas": "Vakarienė su kiekiais",
        "X": "Vakarienei reikės 1 kg vištienos filė, pakelio spagečių, 2 l pieno ir pusės kilogramo sūrio",
        "sarasas": [
            {"preke_id": "vistiena_kg", "kiekis": 1},
            {"preke_id": "makaronai_500g", "kiekis": 1},
            {"preke_id": "pienas_1l", "kiekis": 2},
            {"preke_id": "suris_kg", "kiekis": 0.5},
        ],
        "nerasta": [],
    },
    {
        "id": "03",
        "pavadinimas": "Savaitės apsipirkimas",
        "X": "Savaitei: 2 kg bananų, pusantro kilogramo obuolių, malta kava, 2 duonos ir 20 kiaušinių",
        "sarasas": [
            {"preke_id": "bananai_kg", "kiekis": 2},
            {"preke_id": "obuoliai_kg", "kiekis": 1.5},
            {"preke_id": "kava_500g", "kiekis": 1},
            {"preke_id": "duona_800g", "kiekis": 2},
            {"preke_id": "kiausiniai_10", "kiekis": 2},
        ],
        "nerasta": [],
    },
    {
        "id": "04",
        "pavadinimas": "Prekė, kurios nėra kataloge",
        "X": "pienas, sviestas ir 3 avokadai",
        "sarasas": [
            {"preke_id": "pienas_1l", "kiekis": 1},
            {"preke_id": "sviestas_200g", "kiekis": 1},
        ],
        "nerasta": ["avokadai (3 vnt.)"],
    },
]


def eur(x: float) -> str:
    return f"{x:.2f}".replace(".", ",") + " €"


def skaityti_kainas():
    kainos, prekes = {}, {}
    with open(DATA / "kainos.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            kainos[(r["preke_id"], r["tinklas"])] = {
                "be_korteles": float(r["kaina"]),
                "su_kortele": float(r["kaina_su_kortele"]),
            }
            prekes[r["preke_id"]] = {"preke": r["preke"], "vienetas": r["vienetas"]}
    return kainos, prekes


def apskaiciuoti(pv, kainos, prekes):
    sarasas = [
        {**e, "preke": prekes[e["preke_id"]]["preke"], "vienetas": prekes[e["preke_id"]]["vienetas"]}
        for e in pv["sarasas"]
    ]

    def suma(tinklas, tipas):
        return round(sum(kainos[(e["preke_id"], tinklas)][tipas] * e["kiekis"] for e in sarasas), 2)

    sumos = {t: {"be_korteles": suma(t, "be_korteles"), "su_kortele": suma(t, "su_kortele")} for t in TINKLAI}
    pig_su = min(TINKLAI, key=lambda t: sumos[t]["su_kortele"])
    pig_be = min(TINKLAI, key=lambda t: sumos[t]["be_korteles"])
    brang_su = max(TINKLAI, key=lambda t: sumos[t]["su_kortele"])

    # Geriausias 2 parduotuvių derinys (kainos su kortele): kiekvienai prekei pigesnis iš dviejų tinklų.
    geriausias = None
    for a, b in combinations(TINKLAI, 2):
        pirkiniai = {a: [], b: []}
        viso = 0.0
        for e in sarasas:
            ka = kainos[(e["preke_id"], a)]["su_kortele"]
            kb = kainos[(e["preke_id"], b)]["su_kortele"]
            t = a if ka <= kb else b
            pirkiniai[t].append(e["preke"])
            viso += min(ka, kb) * e["kiekis"]
        viso = round(viso, 2)
        if geriausias is None or viso < geriausias["suma"]:
            geriausias = {"tinklai": [a, b], "suma": viso, "pirkti": pirkiniai}
    sutaupymas_derinio = round(sumos[pig_su]["su_kortele"] - geriausias["suma"], 2)
    verta = sutaupymas_derinio >= 1.00  # mažiau nei 1 € neapsimoka važiuoti į antrą parduotuvę
    geriausias["sutaupoma_lyginant_su_pigiausiu"] = sutaupymas_derinio
    geriausias["verta"] = verta

    skirtumas = round(sumos[brang_su]["su_kortele"] - sumos[pig_su]["su_kortele"], 2)

    tekstas = (
        f"Pigiausia apsipirkti {pig_su}: su kortele {eur(sumos[pig_su]['su_kortele'])}"
        f" (be kortelės pigiausia {pig_be}, {eur(sumos[pig_be]['be_korteles'])}). "
        f"Brangiausia su kortele {brang_su}, {eur(sumos[brang_su]['su_kortele'])}, tad sutaupysite {eur(skirtumas)}. "
    )
    if verta:
        a, b = geriausias["tinklai"]
        tekstas += (
            f"Jei nepatingite užsukti į dvi parduotuves, {a} ir {b} derinys kainuos "
            f"{eur(geriausias['suma'])}, dar {eur(sutaupymas_derinio)} pigiau."
        )
    else:
        tekstas += "Pirkti dviejose parduotuvėse neapsimoka, skirtumas mažesnis nei 1 €."
    if pv["nerasta"]:
        tekstas += f" Kataloge neradau: {', '.join(pv['nerasta'])}, į sumą jos neįtrauktos."

    return {
        "atpazintas_sarasas": [
            {"preke_id": e["preke_id"], "preke": e["preke"], "kiekis": e["kiekis"], "vienetas": e["vienetas"]}
            for e in sarasas
        ],
        "nerasta": pv["nerasta"],
        "sumos_eur": sumos,
        "pigiausias_tinklas": {"su_kortele": pig_su, "be_korteles": pig_be},
        "sutaupoma_vs_brangiausia_eur": skirtumas,
        "geriausias_2_parduotuviu_derinys": geriausias,
        "atsakymas": tekstas,
    }


def katalogas_md(prekes, kainos):
    eil = ["| Prekė | Vienetas | Rimi | Rimi su kortele | IKI | IKI su kortele | Norfa | Norfa su kortele |",
           "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for pid, p in prekes.items():
        cells = []
        for t in TINKLAI:
            k = kainos[(pid, t)]
            cells += [f"{k['be_korteles']:.2f}", f"{k['su_kortele']:.2f}"]
        vnt = "€/kg" if p["vienetas"] == "kg" else "€/vnt."
        eil.append(f"| {p['preke']} (`{pid}`) | {vnt} | " + " | ".join(cells) + " |")
    return "\n".join(eil)


def main():
    kainos, prekes = skaityti_kainas()
    sisteminis = (PROMPTS / "system_prompt.md").read_text(encoding="utf-8")
    katalogas = katalogas_md(prekes, kainos)

    poros = []
    for pv in PAVYZDZIAI:
        y = apskaiciuoti(pv, kainos, prekes)
        pora = {"id": pv["id"], "pavadinimas": pv["pavadinimas"], "X": pv["X"], "y": y}
        poros.append(pora)
        (DATA / f"pavyzdys_{pv['id']}.json").write_text(json.dumps(pora, ensure_ascii=False, indent=2), encoding="utf-8")

        testas = (
            f"# Testavimo promptas {pv['id']}: {pv['pavadinimas']}\n\n"
            "Nukopijuokite visą tekstą žemiau nuo linijos ir įklijuokite į ChatGPT (ar kitą GPT agentą).\n"
            f"Teisingas atsakymas: `data/pavyzdys_{pv['id']}.json` (laukas `y`).\n\n---\n\n"
            f"{sisteminis.strip()}\n\n## Kainų katalogas (EUR)\n\n{katalogas}\n\n"
            f"## Vartotojo užklausa\n\n{pv['X']}\n"
        )
        (PROMPTS / f"test_prompt_{pv['id']}.md").write_text(testas, encoding="utf-8")

    with open(DATA / "poros.jsonl", "w", encoding="utf-8") as f:
        for p in poros:
            f.write(json.dumps({"X": p["X"], "y": p["y"]}, ensure_ascii=False) + "\n")

    with open(DATA / "poros.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "X", "y_pigiausias_tinklas", "y_suma_su_kortele_eur", "y_atsakymas"])
        for p in poros:
            t = p["y"]["pigiausias_tinklas"]["su_kortele"]
            w.writerow([p["id"], p["X"], t, f"{p['y']['sumos_eur'][t]['su_kortele']:.2f}", p["y"]["atsakymas"]])

    for p in poros:
        print(f"{p['id']}: {p['y']['atsakymas']}")


if __name__ == "__main__":
    main()
