import otbApplication as otb

app = otb.Registry.CreateApplication("BandMath")

if app is not None:
    print("OTB installation is working.")
else:
    print("OTB installation is not found.")