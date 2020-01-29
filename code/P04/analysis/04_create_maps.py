import os
import itertools
from osgeo import gdal, osr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
import cartopy.feature as cfeature
from cartopy.io import shapereader
import matplotlib
import matplotlib.patheffects as PathEffects
import matplotlib.gridspec as gridspec

# Monkey patching because matplotlib 3 does
# not have an onHold method required by cartopy.
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.io.shapereader as shpreader
from geopy.geocoders import Nominatim
GeoAxes._pcolormesh_patched = Axes.pcolormesh

def convertXY(xy_source, inproj, outproj):
    # function to convert coordinates
    shape = xy_source[0,:,:].shape
    size = xy_source[0,:,:].size

    # the ct object takes and returns pairs of x,y, not 2d grids
    # so the the grid needs to be reshaped (flattened) and back.
    ct = osr.CoordinateTransformation(inproj, outproj)
    xy_target = np.array(ct.TransformPoints(xy_source.reshape(2, size).T))

    xx = xy_target[:,0].reshape(shape)
    yy = xy_target[:,1].reshape(shape)

    return xx.T, yy.T

def get_projections():
    inproj = osr.SpatialReference()
    inproj.ImportFromEPSG(28992)
    outproj = osr.SpatialReference()
    outproj.ImportFromEPSG(3395)
    return inproj, outproj

def framing_tif(ds):
    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()
    xres = gt[1]
    yres = gt[5]
    xmin = gt[0] + xres * 0.5
    xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
    ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
    ymax = gt[3] - yres * 0.5

    ds = None

    return [xmin, xmax, ymin, ymax, xres, yres]

def get_natural_features():
    coast = NaturalEarthFeature(category='physical', name="coastline", scale='10m', facecolor='blue', zorder=1)
    border = NaturalEarthFeature(category='cultural', name='admin_0_countries', scale='10m', edgecolor='black', facecolor="tan", zorder=15)
    ocean = NaturalEarthFeature(category='physical', name="ocean", scale='50m', facecolor=cfeature.COLORS["water"], zorder=2)
    lakes = NaturalEarthFeature(category='physical', name='lakes', scale='10m', edgecolor='face',facecolor=cfeature.COLORS["water"], zorder=17)
    return [coast, border, ocean, lakes]

def get_NL_contour():
    shpfilename = shapereader.natural_earth(resolution='10m', category='cultural', name='admin_0_countries')
    reader = shapereader.Reader(shpfilename)
    countries = reader.records()
    for country in countries:
        if country.attributes['GEOUNIT'] == 'Netherlands':
            return country.geometry

################
# Main program #
################

########
# This program is prepared to make a joint chart
# for the ensemble selected in the paper  (i.e. (20T, 200S))
# Change the following two parameters if you wish to
# plot together the maps of another generated ensemble.
########
ns = 200
nt = 20
########

xoffset = 0.015
yoffset = 0.015

# Extent of the Netherlands
extent = [3, 7.4, 50.6, 53.7]
extent_zoom = [4.0, 7.2, 51.85, 52.7]
projection=ccrs.PlateCarree()

color_marker = "black"
s = 9

rows = range(0, 2)
cols = range(0, 3)

path_in = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/pred_tif/{0}"
lbl_title = ["(a) RF-Poisson", "(b) RF-NB", "(c) RF-ZIP", "(d) RF-ZINB", "(e) RF-Canon"]
names_tmp = ["NL_TB_Risk_Poi_{0}x{1}", "NL_TB_Risk_NB_{0}x{1}", "NL_TB_Risk_ZIP_{0}x{1}", "NL_TB_Risk_ZINB_{0}x{1}", "NL_TB_Risk_RF_{0}x{1}"]
names = [n.format(ns, nt) for n in names_tmp]

inproj, outproj = get_projections()
pairs = list(itertools.product(rows, cols))
coast, border, ocean, lakes = get_natural_features()
nl_contour = get_NL_contour()

########################################
# Create the figure and basemap object #
########################################

gs = gridspec.GridSpec(3, 5, height_ratios=[10, 10, 4])
gs.update(wspace=0.1)
# gs.update(left=0.05, right=0.48, wspace=0.05)

ax1 = plt.subplot(gs[0, 0], projection=ccrs.Mercator())
ax2 = plt.subplot(gs[0, 1], projection=ccrs.Mercator())
ax3 = plt.subplot(gs[0, 2], projection=ccrs.Mercator())
ax4 = plt.subplot(gs[0, 3], projection=ccrs.Mercator())
ax5 = plt.subplot(gs[0, 4], projection=ccrs.Mercator())
ax6 = plt.subplot(gs[1, 0:2], projection=ccrs.Mercator())
ax7 = plt.subplot(gs[1, 3:5], projection=ccrs.Mercator())
ax8 = plt.subplot(gs[2, :],  projection=ccrs.Mercator())

laxes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]

#########################################################
# Add base layers to the map and full-extent prediction #
#########################################################

for k in range(len(names)):
    i, j = pairs[k]
    path_tif = path_in.format(names[k])
    ds = gdal.Open(path_tif)
    xmin, xmax, ymin, ymax, xres, yres = framing_tif(ds)
    xy_source = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
    xx, yy = convertXY(xy_source, inproj, outproj)

    # Add layers to the map
    ban_mod = ds.GetRasterBand(1).ReadAsArray()
    ban_mod[ban_mod<0] = np.nan
    laxes[k].set_title(lbl_title[k], size=24)
    laxes[k].set_extent(extent)
    laxes[k].add_feature(coast, edgecolor='black', linewidth=2)
    laxes[k].add_feature(border, edgecolor="black", linewidth=2)
    laxes[k].add_feature(lakes, edgecolor="black")
    laxes[k].add_feature(ocean, edgecolor="black")
    laxes[k].add_geometries(nl_contour, ccrs.PlateCarree(), facecolor="none", edgecolor="black", zorder=20)

    im = laxes[k].pcolormesh(xx, yy, ban_mod, zorder=16, cmap=plt.cm.RdYlGn_r, vmin=0, vmax=30)

########################
# Add zoomed ZIP model #
########################

path_tif = path_in.format(names[2])
ds = gdal.Open(path_tif)
xmin, xmax, ymin, ymax, xres, yres = framing_tif(ds)
xy_source = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
xx, yy = convertXY(xy_source, inproj, outproj)
# Add layers to the map
ban_mod = ds.GetRasterBand(1).ReadAsArray()
ban_mod[ban_mod<0] = np.nan
laxes[5].set_title("(f) Zoomed RF-ZIP", size=24)
laxes[5].set_extent(extent_zoom)
laxes[5].add_feature(coast, edgecolor='black', linewidth=2)
laxes[5].add_feature(border, edgecolor="black", linewidth=2)
laxes[5].add_feature(lakes, edgecolor="black")
laxes[5].add_feature(ocean, edgecolor="black")

laxes[5].add_geometries(nl_contour, ccrs.Mercator(), facecolor="none", edgecolor="black", zorder=20)
im = laxes[5].pcolormesh(xx, yy, ban_mod, zorder=16, cmap=plt.cm.RdYlGn_r, vmin=0, vmax=30)

#########################
# Add zoomed ZINB model #
#########################

path_tif = path_in.format(names[3])
ds = gdal.Open(path_tif)
xmin, xmax, ymin, ymax, xres, yres = framing_tif(ds)
xy_source = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
xx, yy = convertXY(xy_source, inproj, outproj)
# Add layers to the map
ban_mod = ds.GetRasterBand(1).ReadAsArray()
ban_mod[ban_mod<0] = np.nan
laxes[6].set_title("(g) Zoomed RF-ZINB", size=24)
laxes[6].set_extent(extent_zoom)
laxes[6].add_feature(coast, edgecolor='black', linewidth=2)
laxes[6].add_feature(border, edgecolor="black", linewidth=2)
laxes[6].add_feature(lakes, edgecolor="black")
laxes[6].add_feature(ocean, edgecolor="black")

laxes[6].add_geometries(nl_contour, ccrs.Mercator(), facecolor="none", edgecolor="black", zorder=20)
im = laxes[6].pcolormesh(xx, yy, ban_mod, zorder=16, cmap=plt.cm.RdYlGn_r, vmin=0, vmax=30)

##################################
# Add shared colorbar to the map #
##################################

cax, kw = matplotlib.colorbar.make_axes(laxes[7], location='top', shrink=0.55, pad=0.1)
cbar = plt.colorbar(im, cax=cax, **kw, )
cbar.set_label("Tick bites", size=24, labelpad=-100)
cbar.ax.tick_params(labelsize=20)
cax.set_aspect('auto')
cax.yaxis.set_ticks_position('both')

laxes[7].set_visible(False)

############################################################
# Use geocoder to obtain lat/lon for each selecte location #
############################################################

geolocator = Nominatim()

loc_utr = geolocator.geocode("Utrecht, NL")
loc_ams = geolocator.geocode("Amersfoort, NL")
loc_ape = geolocator.geocode("Apeldoorn, NL")
loc_ams = geolocator.geocode("Amsterdam, NL")
loc_arn = geolocator.geocode("Arnhem, NL")
loc_gou = geolocator.geocode("Gouda, NL")
loc_zwo = geolocator.geocode("Zwolle, NL")
loc_dev = geolocator.geocode("Deventer, NL")
loc_rot = geolocator.geocode("Rotterdam, NL")
loc_ens = geolocator.geocode("Enschede, NL")

pack = [loc_utr, loc_ams, loc_ape, loc_ams, loc_arn, loc_gou, loc_zwo, loc_rot, loc_ens]

lons = [item.longitude for item in pack]
lats = [item.latitude for item in pack]
city = [item.address.split(",")[0] for item in pack]

####################################################
# Add label to the zoomed maps and text decoration #
####################################################

for i in range(len(pack)):
    laxes[5].plot(lons[i], lats[i], color=color_marker, linewidth=2, marker='s', transform=ccrs.Geodetic(), markersize=s, zorder=18)
    if city[i] == "Enschede":
        txt = laxes[5].text(lons[i] - xoffset * 20, lats[i] + yoffset, city[i], color='black', transform=ccrs.Geodetic(), size=18, variant='small-caps', fontname='Sans', zorder=20)
    else:
        txt = laxes[5].text(lons[i] + xoffset, lats[i] + yoffset, city[i], color='black', transform=ccrs.Geodetic(), size=18, variant='small-caps', fontname='Sans', zorder=20)

    txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='white')])


for i in range(len(pack)):
    laxes[6].plot(lons[i], lats[i], color=color_marker, linewidth=2, marker='s', transform=ccrs.Geodetic(), markersize=s, zorder=18)
    if city[i] == "Enschede":
        txt = laxes[6].text(lons[i] - xoffset*20, lats[i] + yoffset, city[i], color='black', transform=ccrs.Geodetic(), size=18, variant='small-caps', fontname='Sans', zorder=20)
    else:
        txt = laxes[6].text(lons[i] + xoffset, lats[i] + yoffset, city[i], color='black', transform=ccrs.Geodetic(), size=18, variant='small-caps', fontname='Sans', zorder=20)

    txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='white')])

################
# Main program #
################

path_fig_out = r"D:/PycharmProjects/IGM_PhD_Materials/figures/P04/Fig_08_SevenMaps.png"
manager = plt.get_current_fig_manager()
manager.window.showMaximized()
plt.pause(10)
plt.gcf().savefig(path_fig_out, format='png', dpi=300)

# plt.show()