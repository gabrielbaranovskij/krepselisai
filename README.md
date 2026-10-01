# KrepšelisAI – sistemos modelis

AI pokalbių asistentas, kuris palygina pirkinių krepšelio kainą Lietuvos prekybos tinkluose (Rimi, IKI, Norfa; vėliau Maxima/Barbora ir Lidl) ir pasako, kur pigiausia apsipirkti.

## Generatyvinio DI vaidmuo
1. **Užklausos analizė**: laisvas tekstas („pienas, duona, 10 kiaušinių“) paverčiamas struktūruotu sąrašu.
2. **Prekių suderinimas**: skirtingai pavadintos tos pačios prekės skirtinguose tinkluose susiejamos su viena kanonine preke.
3. **Atsakymo generavimas**: skaičiai paverčiami aiškiu, žmogišku atsakymu su pigesnių alternatyvų pasiūlymais.

## Diagramos

| Nr. | Diagrama | PlantUML | Mermaid |
|---|---|---|---|
| 1 | Panaudos atvejų | `plantuml/01_panaudos_atvejai.puml` | `mermaid/01_panaudos_atvejai.mmd` |
| 2 | Klasių (domeno modelis) | `plantuml/02_klasiu_diagrama.puml` | `mermaid/02_klasiu_diagrama.mmd` |
| 3 | Komponentų | `plantuml/03_komponentu_diagrama.puml` | `mermaid/03_komponentu_diagrama.mmd` |
| 4 | Sekų (pokalbis → palyginimas) | `plantuml/04_seku_pokalbis.puml` | `mermaid/04_seku_pokalbis.mmd` |
| 5 | Veiklos (kasdienis kainų surinkimas) | `plantuml/05_veiklos_scrapinimas.puml` | `mermaid/05_veiklos_scrapinimas.mmd` |
| 6 | Duomenų bazės ER | `plantuml/06_er_duomenu_baze.puml` | `mermaid/06_er_duomenu_baze.mmd` |
| 7 | Išdėstymo (deployment) | `plantuml/07_isdestymo_diagrama.puml` | `mermaid/07_isdestymo_diagrama.mmd` |

Sugeneruoti paveikslėliai: `png/` (PlantUML) ir `png/mermaid/` (Mermaid).

## Kaip atidaryti
- **PlantUML**: https://www.plantuml.com/plantuml arba VS Code plėtinys „PlantUML“.
- **Mermaid**: https://mermaid.live arba tiesiog GitHub (`.md` failuose Mermaid blokai rodomi automatiškai).

## Pastabos apie Mermaid
Mermaid neturi atskiro panaudos atvejų ir išdėstymo diagramų tipo, todėl jos nubraižytos kaip `flowchart` (aktoriai, panaudos atvejai ir `«include»`/`«extend»` ryšiai išlaikyti). Kitos diagramos naudoja Mermaid natūralius tipus: `classDiagram`, `sequenceDiagram`, `erDiagram`.

## Technologijos
React · Node.js + Express (TypeScript) · fetch + cheerio scraperiai · node-cron · PostgreSQL · LLM API (OpenAI / Claude) · Docker + Nginx
