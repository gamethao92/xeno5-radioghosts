import os
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.vizier import Vizier

CENTER, RADIUS = "165d +65d", 5*u.deg
OUT = "data"; os.makedirs(OUT, exist_ok=True)

def save(name, table):
    table.write(f"{OUT}/{name}.ecsv", overwrite=True)
    print(name, len(table), "rows")

v = Vizier(columns=['*'], row_limit=200000)
vlass = v.query_region(SkyCoord(CENTER), radius=RADIUS, catalog="J/ApJS/255/30/comp")[0]
save("vlass_all", vlass)
nvss = v.query_region(SkyCoord(CENTER), radius=RADIUS, catalog="VIII/65/nvss")[0]
save("nvss_field", nvss)

vb = vlass[(vlass["Ftot"]>150) & (vlass["QualFlag"]==0) & (vlass["DupFlag"]==0)]
save("vlass_bright_good", vb)
nb = nvss[nvss["S1.4"]>100]
save("nvss_bright", nb)

cs_v = SkyCoord(vlass["RAJ2000"], vlass["DEJ2000"], unit="deg")
cs_nv = SkyCoord(nvss["RAJ2000"], nvss["DEJ2000"], unit="deg")
cs_vb = SkyCoord(vb["RAJ2000"], vb["DEJ2000"], unit="deg")
cs_nb = SkyCoord(nb["RAJ2000"], nb["DEJ2000"], unit="deg")

i, s, _ = cs_vb.match_to_catalog_sky(cs_nv)
keep = s.to(u.arcsec) > 10*u.arcsec
candB = vb[keep]; candB["nvss_sep_arcsec"] = s[keep].to(u.arcsec).value
save("candB_vlass_only", candB)

i2, s2, _ = cs_nb.match_to_catalog_sky(cs_v)
keep2 = s2.to(u.arcsec) > 10*u.arcsec
candA = nb[keep2]; candA["vlass_sep_arcsec"] = s2[keep2].to(u.arcsec).value
save("candA_nvss_only", candA)
print("FUNNEL DONE")
