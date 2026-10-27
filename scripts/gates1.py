from astropy.table import Table, vstack
import astropy.units as u
from astropy.coordinates import SkyCoord

A = Table.read("data/candA_nvss_only.ecsv")
B = Table.read("data/candB_vlass_only.ecsv")
nv = Table.read("data/nvss_field.ecsv")
vl = Table.read("data/vlass_all.ecsv")
cs_nv = SkyCoord(nv["RAJ2000"], nv["DEJ2000"], unit=(u.hourangle, u.deg))
cs_vl = SkyCoord(vl["RAJ2000"], vl["DEJ2000"], unit="deg")

# subtile table (VLASS E1 tile metadata) for coverage/flag gate
from astroquery.vizier import Vizier
sub = Vizier(columns=['*'], row_limit=100000).query_region(SkyCoord("165d +65d"), radius=6*u.deg, catalog="J/ApJS/255/30/subtile")[0]
sub.write("data/subtile.ecsv", overwrite=True)
print("subtile cols:", sub.colnames, len(sub))
