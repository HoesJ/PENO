import ReadObj
import Meshing
import Triangulation
import ShowMesh

# Set ReadObj constants
file_name = "garage.obj"
mtl_name = "garage.mtl"
factor = 1
ReadObj.SetFile(file_name, mtl_name, factor)

# Set Triangulation constants
max_area = 200
min_edge_step = 50
in_face_step = 50
in_face_density = 1000
Triangulation.SetConstants(max_area, min_edge_step, in_face_step, in_face_density, False)

# Set Meshing constant
method = Triangulation.TriangulateRecursive

# Set process constants
export = True
show = False

# Start Process
ReadObj.GetAllInfo()

if not export:
    result = Meshing.MeshAll(ReadObj.GetAllFaces(), ReadObj.GetAbsorb(), method)
    if (show):
        ShowMesh.Show(result[0])
else:
    Meshing.ExportMesh(ReadObj.GetAllFaces(), ReadObj.GetAbsorb(), method)