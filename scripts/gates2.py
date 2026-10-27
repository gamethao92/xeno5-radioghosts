import numpy as np
from astropy.table import Table
import astropy.units as u
from astropy.coordinates import SkyCoord

A = Table.read("data/candA_nvss_only.ecsv")
nv = Table.read("data/nvss_field.ecsv")
vl = Table.read("data/vlass_all.ecsv")
sub = Table.read("data/subtile.ecsv")
cs_nv = SkyCoord(nv["RAJ2000"], nv["DEJ2000"], unit=(u.hourangle, u.deg))
cs_vl = SkyCoord(vl["RAJ2000"], vl["DEJ2000"], unit="deg")
cs_sub = SkyCoord(sub["_RA.icrs"], sub["_DE.icrs"], unit="deg")
s14 = np.asarray(nv["S1.4"], dtype=float)
ftot = np.asarray(vl["Ftot"], dtype=float)
names_nv = np.asarray(nv["NVSS"])
obs = np.asarray(sub["Fpmax"], dtype=float)

rows = []
for r in A:
    c = SkyCoord(r["RAJ2000"], r["DEJ2000"], unit=(u.hourangle, u.deg))
    dnv = c.separation(cs_nv).arcmin
    dvl = c.separation(cs_vl).arcmin
    dsub = c.separation(cs_sub).arcmin
    m_nv = (dnv < 5) & (s14 > 100) & ~((names_nv == r["NVSS"]) & (dnv < 1/60))
    m_vl = (dvl < 5) & (ftot > 100)
    j = int(dsub.argmin())
    rows.append(dict(nvss=str(r["NVSS"]), ra=str(r["RAJ2000"]), dec=str(r["DEJ2000"]), s14=float(r["S1.4"]), vsep=float(r["vlass_sep_arcsec"]),
        n_side_nv=int(m_nv.sum()), n_side_vl=int(m_vl.sum()),
        side_nv=";".join(f"{names_nv[i]}@{dnv[i]:.1f}'{s14[i]:.0f}mJy" for i in np.where(m_nv)[0][:4]),
        side_vl=";".join(f"{vl['CompName'][i]}@{dvl[i]:.1f}'{ftot[i]:.0f}mJy" for i in np.where(m_vl)[0][:4]),
        tile=str(sub["Tile"][j]), tmin=round(float(dsub[j]),2), fpmax=round(float(obs[j]),2), epoch=str(sub["Epoch"][j])))
for x in rows:
    print(f"{x['nvss']} S={x['s14']:.0f} vsep={x['vsep']:.0f}\" tile={x['tile']} d={x['tmin']}' fpmax={x['fpmax']} nbNVSS={x['n_side_nv']} nbVLASS={x['n_side_vl']} :: {x['side_nv'][:60]} | {x['side_vl'][:40]}")
Table(rows).write("data/gatesA.ecsv", overwrite=True)
