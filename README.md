<div align="center">
    <h1>Knækning af Pseudotilfældige Tal i Browseren</h1>
    <h3>Kryptoanalyse af <code>Math.random()</code>: Udnyttelse af xorshift128+-algoritmen gennem Symbolsk Solver til at Forudsige og Manipulere Spil i Browseren</h3>
    Asger Finding
    <br>
    Vejledere: Christian Bøge-Rasmussen (cbr), Mikkel Christensen Lund (mclu)
    <br>
    H. C. Ørsted Gymnasiet Lyngby
    <br>
    L3ak 23/26
    <br>
    Matematik A, Teknikfag (Digital Design og Udvikling) A
    <br>
    Afleveringsfrist: 12. dec. 2025
</div>

---

Dette repository gemmer kildekoden til SOP-afleveringen "Knækning af Pseudotilfældige Tal i Browseren" af Asger Finding.

# Navigering

> prng_example/

`xorshift128p.py`: eksempel på output fra xorshift128+-algoritmen implementeret i Python, med beskrivelse af hvert beregningstrin.

> statistics/

`autokorrelation.html`: autokorrelationsmetoden anvendt på Math.random() og JS-implementerede xorshift128+, xorshift128 og en lineær kongruentiel generator med gcc-parametrene. Visualiseret med graf i Chart.js og oversigtstabel. Kan åbnes i direkte browseren.

`chi2.html`: 𝜒²-metoden anvendt på Math.random() og JS-implementerede xorshift128+, xorshift128 og en lineær kongruentiel generator med gcc-parametrene. Visualiseret med graf i Chart.js og oversigtstabel. Kan åbnes i direkte browseren.

> solver/

`xorshift128pSolver.py`: main script til solveren

xorshift128+ predictor skrevet i Python med Z3 til tilstandsgendannelse.

- Installer nødvændige packages med `pip install -r requirements.txt`
- Kør `python xorshift128pSolver.py` for usage.

`V8Solver.py`: solver-class til V8/Chromium

`SpiderMonkeySolver.py`: solver-class til SpiderMonkey/Firefox

> web_exploit/

`server.js`: main script til det praktiske eksempel for et PRNG exploit. Skal køres med node (`node server.js`). Skal køres med node>^6.

`index.html`: klientkode til den visuelle roulette. Kan tilgås ved http://localhost:3000/ når server kører.
