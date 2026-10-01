# KrepšelisAI

AI pokalbių asistentas, kuris palygina pirkinių krepšelio kainą Lietuvos prekybos tinkluose (Rimi, IKI, Norfa; vėliau Maxima/Barbora ir Lidl) ir pasako, kur pigiausia apsipirkti.

**Komanda:** Edvin Vilkanec, Gabriel Baranovskij

## Kaip tai veikia

Vartotojas parašo, pvz.: *„Reikia pieno, duonos, 10 kiaušinių ir sviesto“*.
Sistema atsako: *„Pigiausia apsipirkti Rimi: su kortele 7,66 €. Brangiausia IKI, 8,02 €, tad sutaupysite 0,36 €.“*

Generatyvinis DI atlieka tris darbus:
1. **Užklausos analizė**: laisvas tekstas paverčiamas struktūruotu sąrašu (prekė, kiekis, vienetas).
2. **Prekių suderinimas**: skirtingai pavadintos tos pačios prekės skirtinguose tinkluose susiejamos su viena kanonine preke.
3. **Atsakymo generavimas**: skaičiai paverčiami aiškiu, žmogišku atsakymu.

## Repozitorijos struktūra

```
data/            (X, y) poros: užklausos ir teisingi atsakymai, kainų katalogas
prompts/         sisteminis promptas ir paruošti testavimo promptai GPT agentui
scripts/         (X, y) porų generatorius
docs/diagrams/   7 diagramos PlantUML ir Mermaid formatais + PNG
```

## End-To-End pavyzdžiai

| Nr. | X (užklausa) | y (pigiausia) |
|---|---|---|
| 01 | Reikia pieno, duonos, 10 kiaušinių ir sviesto | Rimi, 7,66 € |
| 02 | Vakarienei reikės 1 kg vištienos filė, pakelio spagečių, 2 l pieno ir pusės kilogramo sūrio | Rimi, 13,25 € |
| 03 | Savaitei: 2 kg bananų, pusantro kilogramo obuolių, malta kava, 2 duonos ir 20 kiaušinių | Norfa, 18,32 € (IKI + Norfa derinys 17,21 €) |
| 04 | pienas, sviestas ir 3 avokadai | Rimi, 3,48 € (avokadų nerasta) |

Pilni atsakymai: `data/pavyzdys_*.json`. Kaip patikrinti su GPT: `prompts/README.md`.

## Diagramos

| Nr. | Diagrama | PlantUML | Mermaid |
|---|---|---|---|
| 1 | Panaudos atvejų | `docs/diagrams/plantuml/01_panaudos_atvejai.puml` | `docs/diagrams/mermaid/01_panaudos_atvejai.mmd` |
| 2 | Klasių (domeno modelis) | `.../02_klasiu_diagrama.puml` | `.../02_klasiu_diagrama.mmd` |
| 3 | Komponentų | `.../03_komponentu_diagrama.puml` | `.../03_komponentu_diagrama.mmd` |
| 4 | Sekų (pokalbis → palyginimas) | `.../04_seku_pokalbis.puml` | `.../04_seku_pokalbis.mmd` |
| 5 | Veiklos (kasdienis kainų surinkimas) | `.../05_veiklos_scrapinimas.puml` | `.../05_veiklos_scrapinimas.mmd` |
| 6 | Duomenų bazės ER | `.../06_er_duomenu_baze.puml` | `.../06_er_duomenu_baze.mmd` |
| 7 | Išdėstymo (deployment) | `.../07_isdestymo_diagrama.puml` | `.../07_isdestymo_diagrama.mmd` |

PNG paveikslėliai: `docs/diagrams/png/` (PlantUML) ir `docs/diagrams/png/mermaid/` (Mermaid).

Mermaid neturi atskiro panaudos atvejų ir išdėstymo diagramų tipo, todėl jos nubraižytos kaip `flowchart`, išlaikant aktorius ir `«include»`/`«extend»` ryšius.

## Technologijos

React · Node.js + Express (TypeScript) · fetch + cheerio scraperiai · node-cron · PostgreSQL · LLM API (OpenAI / Claude) · Docker + Nginx
