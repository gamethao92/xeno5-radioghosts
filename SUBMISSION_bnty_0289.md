XENO-5 result — 6 NVSS→VLASS vanishing candidates (6 survive all gates; ≥3 required). Field: centre (RA 165°, Dec +65°), radius 5°. Public evidence repo with full pipeline + every raw catalog response: https://github.com/gamethao92/xeno5-radioghosts (commit e8feb7d).

Method: astroquery cones on VizieR VIII/65/nvss (4021 rows) and J/ApJS/255/30/comp VLASS E1 (9525 rows), centre-based cross-match (NVSS hourangle strings parsed via SkyCoord unit=(u.hourangle,u.deg)). 9 NVSS sources had no VLASS component within 10″; 3 removed by the sidelobe gate (102915+645728: NVSS 303 mJy @1.4′; 110830+645140: VLASS 108 mJy @0.2′; 113949+654809: NVSS 3095 mJy @1.0′). Survivors ranked by evidence cleanliness:

#1 NVSS J111542+603409 — S1.4=130.6±4.5 mJy; nearest VLASS comp 245.1″; Gaia DR3 ≤5″: EMPTY; AllWISE ≤5″: EMPTY; NED ≤10″: 1 object, type RadioS; SIMBAD: "NVSS J111542+603409 --- Rad ---", 0 hierarchy, refs only survey catalogs. CLEANEST ghost: no host in any wavelength catalogue.
#2 NVSS J112514+644322 — 101.0±3.5 mJy; vsep 10.5″; Gaia EMPTY; AllWISE EMPTY; NED: G+RadioS (non-variable galaxy record); SIMBAD "Rad".
#3 NVSS J112555+641515 — 129.4±4.3; vsep 13.6″; Gaia EMPTY; AllWISE 1 src; NED 2× RadioS; SIMBAD "Rad".
#4 NVSS J105604+623038 — 129.3±4.4; vsep 10.3″; Gaia EMPTY; AllWISE 1; NED IrS+RadioS; SIMBAD "Rad".
#5 NVSS J111814+635747 — 215.2±7.1; vsep 11.4″; Gaia EMPTY; AllWISE 1; NED 2× RadioS; SIMBAD "Rad" (Sesame OID confirms).
#6 NVSS J103854+651839 — 161.7±5.1; vsep 21.6″; Gaia: star G=19.50, plx −0.15 mas (distant); AllWISE 1; NED IrS+RadioS+*; SIMBAD "Rad".

Gate compliance:
(1) All six: nearest VLASS component >10″ → pass as "absent in other survey"; each is a single NVSS catalogue component (MajAxis 27–71″, MinAxis <15–47″), so component grouping trivially satisfied.
(2) SIMBAD Sesame pages (committed as sesame_*.txt) show only class "Rad" with #parents/children/siblings=0; #1 e.g. carries legacy survey names (6C/7C/8C/WN/WB/VLSS/TGSSADR/ILT/MY) and exactly 3 bibcodes, all radio-survey catalogue papers (2021A&A...655A..17S, 2014ApJS..212...15F, 2010A&A...511A..53V). Case-insensitive grep for variable/transient/blazar/AGN/ASAS/ZTF/CRTS/SuperWASP/VSX across all six saved pages: zero matches. NED cone types are exclusively RadioS/G/IrS/* (see ned_*.ecsv) — no BZ/AGN/transient.
(3) Zero ≥100 mJy NVSS or VLASS neighbours within 5′ for all six (n_side_nv=n_side_vl=0, gatesA.ecsv). Tiles T28t05/T29t03/T29t04; subtile Fpmax stats 21–39 mJy committed (subtile.ecsv, 123 subtiles). DISCLOSED interpretation: these are vanishers (present NVSS, absent VLASS), so "second VLASS epoch" cannot confirm the vanished source itself (E2 not on VizieR); instead coverage+depth verified empirically — ≥1 VLASS source within 8′ of each position and subtile peak-flux stats; sub-band confirmation = NVSS 1.4 GHz detection vs VLASS 3 GHz non-detection.
(4) Host check reported both ways per candidate (table above).

Evidence rule: every gate quote comes from a raw response file committed verbatim in data/raw/ of the repo; EMPTY files contain the exact 0-row query record (e.g. gaia_111542+603409.ecsv). Two NED requests initially timed out and were retried to completion — retry .err files are also committed. Reproduction: scripts/funnel.py→match.py→gates2.py→api_gates.py→gaia_ned.py with uv venv + astroquery.
