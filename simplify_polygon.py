# -*- coding: utf-8 -*-
# @Time    : 2018/6/23 下午8:49
# @Author  : Dongyang
# @File    : 练习.py
# @Software: PyCharm
from __future__ import print_function
import cv2
import numpy as np
from osgeo import ogr

img = cv2.imread("/home/dongyang/project/Thailand/sym_ply/class.tif",cv2.IMREAD_UNCHANGED)
shapefile="/home/dongyang/project/Thailand/sym_ply/class.shp"
_, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
th=thresh.astype(np.uint8)
#thresh.convertTo(thresh, cv2.CV_8UC1);
image, contours, hierarchy = cv2.findContours(th,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

driver = ogr.GetDriverByName('Esri Shapefile')
ds = driver.CreateDataSource(shapefile)
layer = ds.CreateLayer('class', None, ogr.wkbPolygon)
# Add one attribute
defn = layer.GetLayerDefn()
print("3")
for i in range(len(contours)):
    cnt = contours[i]
    epsilon = 0.00001 * cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    # Create a new feature (attribute and geometry)
    feat = ogr.Feature(defn)
    # Make a geometry, from Shapely object
    #print(approx)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    #print(ring)

    for j in range(len(approx)):
        # Create test polygon
        # print(np.double(approx[j][0][0]))
        # print(np.double(approx[j][0][1]))
        # print(type(np.double(approx[j][0][1])))
        ring.AddPoint_2D(float(approx[j][0][0]),float(approx[j][0][1]))
    #if(approx[0]!=approx[-1][])
    ring.CloseRings()
    #先建立一个polygon对象
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    wkt=poly.ExportToWkt()
    print(wkt)
    # Make a geometry, from Shapely object
    geom = ogr.CreateGeometryFromWkt(wkt)
    feat.SetGeometry(geom)

    layer.CreateFeature(feat)
    feat = geom = None  # destroy these
    # Save and close everything
ds = layer= None
print("11")
print("done")

