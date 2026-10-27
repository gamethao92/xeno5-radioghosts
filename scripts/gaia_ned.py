import os, json
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table, vstack
from astroquery.vizier import Vizier
from astroquery.ned import Ned

os.makedirs("data/api", exist_ok=True)

def vizier_cone(cat, c, radius_arcsec):
    v = Vizier(columns=["*"], row_limit=50)
    out = []
    for tab in v.query_region(c, radius=radius_arcsec*u.arcsec, catalog=cat):
        if len(tab):
            out.append(tab)
    return vstack(out) if out else Table(names=["_empty"], rows=[])

summary = []
six = Table.read("data/six_morphology.ecsv")
for row in six:
    nm = str(row["NVSS"]).replace("NVSS J", "")
    c = SkyCoord(str(row["RAJ2000"]), str(row["DEJ2000"]), unit=(u.hourangle, u.deg))
    ent = {"name": nm, "ra": float(c.ra.deg), "dec": float(c.dec.deg)}

    for key, fn in [
        ("gaia",    lambda: vizier_cone("I/355/gaiadr3", c, 5.0)),
        ("allwise", lambda: vizier_cone("II/328/allwise", c, 5.0)),
        ("ned",     lambda: Ned.query_region(c, radius=10.0*u.arcsec)),
    ]:
        fname = f"data/api/{key}_{nm}.ecsv"
        try:
            t = fn()
            if len(t) == 0:
                open(fname, "w").write(
                    f"# {key} cone {c.to_string('decimal')}"
                    f" r={'5arcsec' if key != 'ned' else '10arcsec'} => EMPTY (0 rows)\n")
                ent[key] = "EMPTY"
            else:
                t.write(fname, overwrite=True)
                ent[key] = f"{len(t)} rows"
        except Exception as e:
            open(f"data/api/{key}_{nm}.err.txt", "w").write(f"{type(e).__name__}: {e}")
            ent[key] = f"ERR {type(e).__name__}: {e}"

    summary.append(ent)
    print(ent, flush=True)

json.dump(summary, open("data/api/gaia_ned_summary.json", "w"), indent=1)
