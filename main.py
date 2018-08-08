from netCDF4 import Dataset

dataset = Dataset("C:/Users/LI252/Desktop/SMIPSv0.5.nc")
#print(dataset.file_format)
#print(dataset.dimensions.keys())
#print(dataset.dimensions['lon'])

#print(dataset.variables.keys())
#print(dataset.variables['time'])
#
# for attr in dataset.ncattrs():
#      print(attr, '=', getattr(dataset, attr))
#print(dataset.ncattrs()) ##['description', 'history']

print(dataset.units)

