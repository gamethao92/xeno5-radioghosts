import json, time, pathlib
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
from astroquery.vizier import Vizier

M = Table = None
from astropy.table import Table
M = Table.read("data/six_morphology.ecsv")
out = pathlib.Path("data/api"); out.mkdir(exist_ok=True)
simbad = Simbad(); simbad.TIMEOUT = 60

records = []
for r in M:
    c = SkyCoord(r["RAJ2000"], r["DEJ2000"], unit=(u.hourangle, u.deg))
    rec = {"nvss": str(r["NVSS"]), "ra": r["RAJ2000"].replace(" ",":"), "dec": r["DEJ2000"], "coord_deg": c.to_string("decimal")}
    try:
        t = simbad.query_region(c, radius="10s")
        rec["simbad"] = "EMPTY" if t is None else [ (str(x["MAIN_ID"]), str(x["TYP"]) if "TYP" in x.colnames else "") for x in t ]
        if t is not None: t.write(f"data/api/simbad_{r['NVSS']}.ecsv", overwrite=True)
        elif t is None: rec["simbad_note"]="query_region returned None => zero rows"
    except Exception as e:
        rec["simbad"] = f"ERR {type(e).__name__}: {str(e)[:100]}"
    time.sleep(1)
    # Gaia DR3 + AllWISE within 5"
    for cat, tag in [("II/336/apass9", None)]: pass
    try:
        g = Vizier(columns=["*"], row_limit=5).query_region(c, radius="5s", catalog="I/355/gaiadr3")
        ok = g and len(g) and len(g[0])
        rec["gaia"] = "EMPTY" if not ok else list(g[0][0]["SOURCE_ID","phot_g_mean_mag"])
        if ok: g[0].write(f"data/api/gaia_{r['NVSS']}.ecsv", overwrite=True)
    except Exception as e:
        rec["gaia"] = f"ERR {type(e).__name__}: {str(e)[:80]}"
    time.sleep(1)
    try:
        w = Vizier(columns=["*"], row_limit=5).query_region(c, radius="5s", catalog="II/328/allwise")
        ok = w and len(w) and len(w[0])
        rec["allwise"] = "EMPTY" if not ok else "SEES_ECSV"
        if ok: w[0].write(f"data/api/allwise_{r['NVSS']}.ecsv", overwrite=True)
    except Exception as e:
        rec["allwise"] = f"ERR {type(e).__name__}: {str(e)[:80]}"
    time.sleep(1)
    records.append(rec); print(json.dumps(rec)[:250])
json.dump(records, open("data/api_gates.json","w"), indent=1)
