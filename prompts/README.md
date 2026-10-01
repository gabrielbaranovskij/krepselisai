# prompts/ – testavimo promptai

| Failas | Kas jame |
|---|---|
| `system_prompt.md` | KrepšelisAI sisteminis promptas: taisyklės ir atsakymo JSON formatas. |
| `test_prompt_01.md` … `test_prompt_04.md` | Pilni, paruošti įklijuoti testai: sisteminis promptas + kainų katalogas + viena vartotojo užklausa. |

## Kaip testuoti

1. Atsidarykite `test_prompt_01.md`.
2. Nukopijuokite viską žemiau linijos `---`.
3. Įklijuokite į ChatGPT (naują pokalbį) ir išsiųskite.
4. Palyginkite GPT atsakymą su `data/pavyzdys_01.json` lauku `y`.

Testas pavyko, jei sutampa atpažintas sąrašas, sumos kiekviename tinkle, pigiausias tinklas ir derinio rezultatas. Teksto formuluotė gali skirtis.

## Ko tikimės (01 pavyzdys)

Užklausa: *„Reikia pieno, duonos, 10 kiaušinių ir sviesto“*

Atsakymas: *„Pigiausia apsipirkti Rimi: su kortele 7,66 €. Brangiausia su kortele IKI, 8,02 €, tad sutaupysite 0,36 €. Pirkti dviejose parduotuvėse neapsimoka.“*
