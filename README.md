# Evolučné vysvetlenia kognitívnych skreslení
Tento repozitár obsahuje kompletný zdrojový kód a experimentálne dáta, ktoré tvoria praktickú časť bakalárskej práce: Evolučné vysvetlenia kognitívnych skreslení.

## O projekte

Hlavným cieľom tejto simulácie je z evolučnej perspektívy analyzovať vplyv a vývoj vybraných kognitívnych skreslení v prostredí s vysokou mierou neistotu. Model sleduje prežitie, adaptáciu a reprodukciu agentov rozdelených do 4 skupín:

- **NBA (Non Biased Agent)**: Kontrolná skupina (agenti sa rozhodujú náhodne).
- **LA (Loss Aversion)**: Agenti s averziou voči strate.
- **OC (Overconfidence)**: Agenti s efektom nadmernej sebadôvery.
- **BW (Bandwagon Effect)**: Agenti so stádovým efektom.

## Použité technológie

Simulácia bola implementovaná v jazyku Python a využíva nasledujúce knižnice:

- `mesa` (verzia 3.3.1) — agentovo orientované simulovanie
- 'solara' — vizualizácia a interaktívne webové rozhranie
- 'pandas' — zber a analýza vygenerovaných dát

## Inštalácia a spustenie

1. Nainštalovanie použitých knižníc
2. Spustenie vizualizácie simulácie: Pre spustenie vizualizácie zadajte do terminálu príkaz solara 'run visualization.py'
3. Spustenie viacerých iterácií: Pre spustenie viacerých iterácií stačí spustiť 'run_simulation.py'. V tomto súbore je možné upraviť parametre ako počet iterácií a počet krokov simulácie.
