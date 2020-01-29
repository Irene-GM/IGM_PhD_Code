from osgeo import gdal, ogr, osr
import csv
import os

################
# Main program #
################

path_grid = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/1km_clipped/1km_clipped_centroids.shp"
path_bites = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TickBites_Dec16/NL_TickBites_Dec16_RD_New.shp"
path_out = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/txt/TB_reports_risk_per_pixel.csv"

driver = ogr.GetDriverByName("ESRI Shapefile")
grid_ds = driver.Open(path_grid, 0)
grid_layer = grid_ds.GetLayer()

bite_ds = driver.Open(path_bites, 0)
bite_layer = bite_ds.GetLayer()

with open(path_out, "w", newline="") as w:
    writer = csv.writer(w, delimiter=";")
    writer.writerow(["cellid", "biteid"])
    for bite in bite_layer:
        bite_geom = bite.GetGeometryRef()
        j = 0
        rowid = int(bite.GetField(0))
        for cell in grid_layer:
            cell_geom = cell.GetGeometryRef()
            distance = int(bite_geom.Distance(cell_geom.Centroid()))
            if distance <= 1000:
                if bite_geom.Within(cell_geom):
                    newrow = [j, bite.GetField(0)]
                    writer.writerow(newrow)
                    break
                elif bite_geom.Intersects(cell_geom):
                    newrow = [j, bite.GetField(0)]
                    writer.writerow(newrow)
                    break
            w.flush()
            j += 1
        grid_layer.SetNextByIndex(0)

