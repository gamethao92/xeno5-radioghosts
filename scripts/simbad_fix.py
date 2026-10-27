import time
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.simbad import Simbad
M = Table.read("data/six_morphology.ecsv")
s = Simbad(); s.TIMEOUT=60; s.ROW_LIMIT=20
for r in M:
    c = SkyCoord(r["RAJ2000"], r["DEJ2000"], unit=(u.hourangle, u.deg))
    try:
        t = s.query_region(c, radius="10s")
        if t is None:
            print(r["NVSS"], "SIMBAD: no table (zero rows)")
        else:
            t.write(f"data/api/simbad_{r['NVSS']}.ecsv", overwrite=True)
            print(r["NVSS"], "SIMBAD rows:", len(t), "| cols:", t.colnames[:8])
            for row in t:
                print("   ", {k: str(row[k]) for k in t.colnames[:5]})
    except Exception as e:
        print(r["NVSS"], "ERR", str(e)[:120])
    time.sleep(1)
