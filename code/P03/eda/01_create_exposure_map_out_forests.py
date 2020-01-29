from mpl_toolkits.basemap import Basemap
import osr, gdal
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

import matplotlib.cm as cm
import matplotlib.colors as mcolors


font = {'family' : 'normal',
        'size'   : 20}

matplotlib.rc('font', **font)


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

    return xx, yy

def save_fig_maximized(fig, path_fig, name_fig):
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    manager.window.showMaximized()
    fig = plt.gcf()
    print(manager)
    plt.show()
    fig.savefig(path_fig.format(name_fig), format="png", dpi=300)


def colorbar_index(ncolors, cmap):
    # cmap = cmap_discretize(cmap, ncolors)
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(range(ncolors))


################
# Main program #
################

# Read the data and metadata
path_tif = r"D:\PycharmProjects\IGM_PhD_Materials\data\P03\in\Exposure_WGS84_classified.tif"
path_mask = r"D:\PycharmProjects\IGM_PhD_Materials\data\P03\in\mask_LGN.csv"

mask = np.loadtxt(path_mask, delimiter=";")

ds = gdal.Open(path_tif, gdal.GA_ReadOnly)
data = ds.ReadAsArray()

canvas = np.empty((352, 311))

for i in range(mask.shape[0]):
    for j in range(mask.shape[1]):
        canvas[i,j] = mask[i,j]

newmask = np.roll(canvas, 6, axis=1)

data_masked = np.ma.masked_array(data, newmask==0)

z = np.ma.masked_array(data, data == 6)

z = data_masked

print(np.unique(z, return_counts=True))

# get the edge coordinates and add half the resolution
# to go to center coordinates
gt = ds.GetGeoTransform()
proj = ds.GetProjection()
xres = gt[1]
yres = gt[5]
xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5

ds = None

# create a grid of xy coordinates in the original projection
xy_source = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

# Create the figure and basemap object
fig = plt.figure()

m = Basemap(projection='merc', lon_0=3.0, lat_0=52.0, resolution='h', llcrnrlon=3.0, llcrnrlat=50.0, urcrnrlon=8.0, urcrnrlat=54.0)
m.drawcountries(zorder=4)
m.drawcoastlines(zorder=5)
m.fillcontinents(color='tan',lake_color='lightblue', zorder=2)
m.drawmapboundary(fill_color='lightblue',zorder=1)

# Create the projection objects for the convertion
inproj = osr.SpatialReference()
inproj.ImportFromWkt(proj)
outproj = osr.SpatialReference()
outproj.ImportFromProj4(m.proj4string)

xx, yy = convertXY(xy_source, inproj, outproj)

colors = ["white", "#448C51", "#F2E127", "#3D3D3D"]


z[z==3] = 33 # Exposure
z[z==4] = 44 # No data
z[z==5] = 55 # Hazard
z[z==6] = 66 # Risk

z[z==33] = 1 # Exposure
z[z==66] = 2 # Risk
z[z==55] = 3 # Hazard
z[z==44] = 4 # No data


plt.title("(b)", size = 24)
im1 = m.pcolormesh(xx, yy, z.T, cmap=matplotlib.colors.ListedColormap(colors), vmin=1, vmax=9, zorder=3)
cbar = m.colorbar(im1, location='bottom', pad="5%", size="5%", ticks=matplotlib.ticker.FixedLocator([1, 2, 3, 4, 5, 6, 7, 8]))
cbar.set_ticklabels(["", "1", "", "2", "", "3", "", "4", ""])
print(cbar.ax.get_xticks())

im2 = m.pcolormesh(xx, yy, z.T, cmap=matplotlib.colors.ListedColormap(colors), vmin=1, vmax=4, zorder=4)

plt.show()