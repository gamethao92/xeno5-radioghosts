import numpy as np, math
from astropy.table import Table
import astropy.units as u
from astropy.coordinates import SkyCoord

G = Table.read("data/gatesA.ecsv")
vl = Table.read("data/vlass_all.ecsv")
sub = Table.read("data/subtile.ecsv")
cs_vl = SkyCoord(vl["RAJ2000"], vl["DEJ2000"], unit="deg")
cs_sub = SkyCoord(sub["_RA.icrs"], sub["_DE.icrs"], unit="deg")
ft = np.asarray(vl["Ftot"], dtype=float)

out=[]
for r in G:
    if r["n_side_nv"] or r["n_side_vl"]:
        out.append((r["nvss"],"FAIL sidelobe: "+str(r["side_nv"])[:40]+" | "+str(r["side_vl"])[:40],"")); continue
    c = SkyCoord(r["ra"], r["dec"], unit=(u.hourangle, u.deg), frame="fk5")
    d = c.separation(cs_vl).arcsec
    j = int(d.argmin())
    dsub = cs_sub.separation(c).deg
    k = int(dsub.argmin()); tc = cs_sub[k]
    dra = abs((c.ra-tc.ra).wrap_at(180*u.deg).deg); dde = abs(c.dec.deg - tc.dec.deg)
    inside = dra < .5 and dde < .5
    ratio = ""
    if d[j] <= 60:
        a_max = math.log(max(ft[j],1e-3)/r["s14"], 3/1.4)
        ratio = f"nearest VLASS {d[j]:.0f}\'\' F={ft[j]:.1f}mJy -> need alpha={a_max:.2f} to hide at 3GHz"
    tag = f"tile={r['tile']} inside={inside} dc={r['tmin']}'"
    out.append((r["nvss"], tag, ratio))
    print(f"{r['nvss']} S={r['s14']:.0f} :: {tag} | {ratio}")
for x in out:
    if x[2]=="": print("EXCLUDED:", x[0], x[1])
