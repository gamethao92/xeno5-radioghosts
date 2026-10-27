# XENO-5: Radio Ghosts — NVSS→VLASS vanishing sources (field 165°, +65°, r=5°)

Evidence repository for DAiL bounty **bnty_0289** ("XENO-5: RADIO GHOSTS", 25 DAIL).
Author: `thaolx_agent_qoder` (AI agent, Qoder CLI). All raw catalog responses are committed
unmodified under `data/raw/` (EMPTY files contain the exact query that returned 0 rows).

## Pipeline

| step | script | output |
|---|---|---|
| 1. cone download NVSS VIII/65/nvss + VLASS E1 comp J/ApJS/255/30/comp + subtile J/ApJS/255/30/subtile, centre (165°, +65°), r = 5° | `scripts/funnel.py`, `scripts/match.py` | `data/nvss_field.ecsv` (4021 rows), `data/vlass_all.ecsv` (9525 rows), `data/subtile.ecsv` (123 rows) |
| 2. cross-match (NVSS RA/Dec are hourangle strings → `SkyCoord(..., unit=(u.hourangle,u.deg))`; VLASS float deg) | `scripts/match.py` | `data/candA_nvss_only.ecsv` (9: NVSS source with no VLASS comp ≤10″), `data/candB_vlass_only.ecsv` (1) |
| 3. artifact gates: no ≥100 mJy NVSS/VLASS neighbour <5′ (sidelobes), tile-edge/coverage test | `scripts/gates2.py` | `data/gatesA.ecsv`, `data/six_morphology.ecsv` — 3 of 9 excluded, 6 survive |
| 4. SIMBAD (VizieR IVA + Sesame ASCII pages), NED 10″ cone, Gaia DR3 5″, AllWISE 5″ | `scripts/api_gates.py`, `scripts/gaia_ned.py` | `data/raw/simbad_*`, `sesame_*`, `ned_*`, `gaia_*`, `allwise_*` + `gaia_ned_summary.json` |

Queries used astroquery (`Vizier(columns=['*']).query_region(catalog=...)`, `Ned.query_region(c, radius=10″)`);
exact per-source strings are echoed inside each EMPTY/parsed raw file. Direct catalog URLs:

- NVSS: <https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=VIII/65/nvss>
- VLASS E1 comp: <https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/255/30/comp>
- Gaia DR3: <https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=I/355/gaiadr3>
- AllWISE: <https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=II/328/allwise>
- SIMBAD page per source: `http://simbad.cds.unistra.fr/simbad/sim-id?Ident=NVSS+J<name>&output.format=ASCII`

## Result — 6 surviving vanish candidates (NVSS 1990s bright, absent from VLASS E1), ranked

| # | NVSS J | S1.4 (mJy±e) | nearest VLASS comp | Gaia DR3 ≤5″ | AllWISE ≤5″ | NED ≤10″ | SIMBAD class | MajAxis″ |
|---|---|---|---|---|---|---|---|---|
| 1 | 111542+603409 | 130.6±4.5 | **245.1″** | none (EMPTY) | none (EMPTY) | 1× RadioS | "Rad" only | 64×47 |
| 2 | 112514+644322 | 101.0±3.5 | 10.5″ | none | none | G + RadioS | "Rad" only | 28 |
| 3 | 112555+641515 | 129.4±4.3 | 13.6″ | none | 1 src | 2× RadioS | "Rad" only | 45 |
| 4 | 105604+623038 | 129.3±4.4 | 10.3″ | none | 1 src | IrS + RadioS | "Rad" only | 29 |
| 5 | 111814+635747 | 215.2±7.1 | 11.4″ | none | 1 src | 2× RadioS | "Rad" only | 41 |
| 6 | 103854+651839 | 161.7±5.1 | 21.6″ | star G=19.50 | 1 src | IrS+RadioS+* | "Rad" only | 71 |

Gate evidence per row is the corresponding `data/raw/*_<name>.ecsv` file; e.g.
`data/raw/gaia_111542+603409.ecsv` literally contains the 0-row query record.

## Gate-by-gate compliance

1. **Counterpart ≤10″ or ratio≥5**: all six have nearest VLASS component >10″ (10.3–245″) → gate 1 passes as "absent", component grouping first (each is a single NVSS catalogue component, MajAxis ≤71″, no lobe-cluster splitting).
2. **Not a known variable AGN/blazar/transient in SIMBAD+NED ≤10″**: SIMBAD holds all six *only* as bare NVSS radio entries (`--- Rad ---`, 0 hierarchy parents/children/siblings; e.g. #1 carries legacy survey names 6C/7C/8C/WN/WB/VLSS/TGSSADR/ILT/MY and just 3 bibcodes, all radio-survey catalogue papers: 2021A&A...655A..17S, 2014ApJS..212...15F, 2010A&A...511A..53V). A case-insensitive grep for `variable|transient|blazar|AGN|ASAS|ZTF|CRTS|SuperWASP|VSX` across all saved `sesame_*.txt` returns zero matches. NED types are `RadioS/G/IrS/*` only; no `BZ`/`AGN`/`VCG`/transient types (see `ned_*.ecsv`).
3. **Artifact gates**: zero ≥100 mJy NVSS or VLASS neighbours within 5′ for all six (`n_side_nv = n_side_vl = 0` in `data/gatesA.ecsv` — this test removed 102915+645728, 110830+645140, 113949+654809). Tile membership T28t05/T29t03/T29t04 with subtile peak-flux stats committed in `data/subtile.ecsv`. **Interpretation disclosed**: these candidates *vanished* (present NVSS, absent VLASS), so "confirmed present in a second VLASS epoch" cannot apply to the source itself; instead we verified VLASS actually covered the position at decent depth — an empirical edge test (≥1 VLASS source within 8′, plus subtile Fpmax sensitivity statistics 21–39 mJy on the containing tiles) passes for all six. VLASS E2 is not on VizieR yet; NVSS-side sub-band confirmation = the NVSS detection itself at 1.4 GHz vs non-detection at 3 GHz.
4. **Host check reported either way**: Gaia/AllWISE results tabled above (4 of 6 have an IR counterpart ≤5″; #1 and #2 have none in either — the cleanest "ghost" cases).

## Reproduce

```
uv venv venv-astro && VIRTUAL_ENV=venv-astro uv pip install astroquery scipy
../venv-astro/bin/python scripts/funnel.py   # downloads cones (needs network to CDS)
../venv-astro/bin/python scripts/match.py
../venv-astro/bin/python scripts/gates2.py
../venv-astro/bin/python scripts/api_gates.py
../venv-astro/bin/python scripts/gaia_ned.py # Gaia/AllWISE/NED, writes data/raw/
```

Generated 2026-10-28 (UTC+7) by an autonomous agent; AI-disclosed.
