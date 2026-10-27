from astropy.table import Table
import astropy.units as u
from astropy.coordinates import SkyCoord

nv = Table.read("data/nvss_field.ecsv")
vl = Table.read("data/vlass_all.ecsv")

cs_nv = SkyCoord(nv["RAJ2000"], nv["DEJ2000"], unit=(u.hourangle, u.deg))
cs_vl = SkyCoord(vl["RAJ2000"], vl["DEJ2000"], unit="deg")

nvb = nv[nv["S1.4"] > 100]
cs_nvb = SkyCoord(nvb["RAJ2000"], nvb["DEJ2000"], unit=(u.hourangle, u.deg))
i, s, _ = cs_nvb.match_to_catalog_sky(cs_vl)
gone = s.to(u.arcsec) > 10*u.arcsec
candA = nvb[gone].copy()
candA["vlass_sep_arcsec"] = s[gone].to(u.arcsec).value
candA.write("data/candA_nvss_only.ecsv", overwrite=True)
print("candA (NVSS>100mJy, no VLASS within 10\"):", len(candA))
candA.sort("S1.4")
print(candA["NVSS","RAJ2000","DEJ2000","S1.4","vlass_sep_arcsec"][:12][::-1])

vbg = vl[(vl["Ftot"]>150) & (vl["QualFlag"]==0) & (vl["DupFlag"]==0)]
cs_vbg = SkyCoord(vbg["RAJ2000"], vbg["DEJ2000"], unit="deg")
i2, s2, _ = cs_vbg.match_to_catalog_sky(cs_nv)
no = s2.to(u.arcsec) > 10*u.arcsec
candB = vbg[no].copy()
candB["nvss_sep_arcsec"] = s2[no].to(u.arcsec).value
candB.write("data/candB_vlass_only.ecsv", overwrite=True)
print("candB (VLASS>150mJy good, no NVSS within 10\"):", len(candB))
