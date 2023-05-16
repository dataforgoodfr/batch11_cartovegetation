from qgis.core import QgsApplication

QgsApplication.setPrefixPath("/QGIS", True)

qgs = QgsApplication([], False)
qgs.initQgis()

if qgs:
    print("QGIS installation is working.")
else:
    print("QGIS installation is not found.")

qgs.exitQgis()