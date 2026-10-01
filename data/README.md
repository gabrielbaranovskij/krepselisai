# data/ – (X, y) poros

Čia yra etaloniniai End-To-End pavyzdžiai: ką vartotojas parašo (**X**) ir ką sistema turi atsakyti (**y**).

| Failas | Kas jame |
|---|---|
| `kainos.csv` | Pavyzdinis kainų katalogas: 10 prekių × 3 tinklai (Rimi, IKI, Norfa), kaina be kortelės ir su kortele. Kainos sugalvotos testavimui, jos nėra realios. |
| `poros.jsonl` | Visos (X, y) poros, viena eilutė = viena pora. |
| `poros.csv` | Tos pačios poros trumpai, patogu atsidaryti Excel'yje. |
| `pavyzdys_01.json` … `pavyzdys_04.json` | Kiekviena pora atskirai, gražiai suformatuota. |

## Pavyzdžiai

| Nr. | X (užklausa) | y (trumpai) | Ką tikrina |
|---|---|---|---|
| 01 | Reikia pieno, duonos, 10 kiaušinių ir sviesto | Rimi, 7,66 € su kortele | Paprastas sąrašas be kiekių |
| 02 | Vakarienei reikės 1 kg vištienos filė, pakelio spagečių, 2 l pieno ir pusės kilogramo sūrio | Rimi, 13,25 € su kortele | Kiekiai ir vienetai (kg, l, „pusė kilogramo“) |
| 03 | Savaitei: 2 kg bananų, pusantro kilogramo obuolių, malta kava, 2 duonos ir 20 kiaušinių | Norfa, 18,32 €; IKI + Norfa derinys 17,21 € | Kada apsimoka pirkti dviejose parduotuvėse |
| 04 | pienas, sviestas ir 3 avokadai | Rimi, 3,48 €; avokadų nerasta | Prekė, kurios nėra kataloge |

## y struktūra

```json
{
  "atpazintas_sarasas": [...],        // ką LLM ištraukė iš teksto
  "nerasta": [...],                   // prekės, kurių nėra kataloge
  "sumos_eur": {...},                 // krepšelio suma kiekviename tinkle
  "pigiausias_tinklas": {...},        // su kortele ir be kortelės
  "sutaupoma_vs_brangiausia_eur": 0,
  "geriausias_2_parduotuviu_derinys": {...},
  "atsakymas": "..."                  // žmogiškas tekstas vartotojui
}
```

Skaičiai `y` lauke turi sutapti tiksliai. Lauko `atsakymas` formuluotė gali skirtis, svarbu, kad jame būtų tie patys faktai.

## Kaip sugeneruoti iš naujo

```bash
python scripts/generuoti_poras.py
```

Skriptas iš `kainos.csv` perskaičiuoja visas sumas ir atnaujina šio aplanko failus bei `prompts/test_prompt_*.md`.
