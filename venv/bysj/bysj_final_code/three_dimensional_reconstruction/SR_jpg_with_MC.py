import vtk
# source->filter(MC算法)->mapper->actor->render->renderwindow->interactor

# 读取jpg数据，对应source
vtk_reader = vtk.vtkJPEGReader()
vtk_reader.SetDataScalarTypeToUnsignedChar()
vtk_reader.SetFileDimensionality(3)
#阈值法的结果
vtk_reader.SetFilePrefix("image_with_geli/")#文件夹路径
#vtk_reader.SetFilePrefix("D:/pyProject/Graduation_project/venv/bysj/bysj_final_code/threadshold/thred_450_image_with_geli/")#文件夹路径
#vtk_reader.SetFilePrefix("D:/ct_2_jpg/")
#三维区域生长法的结果
#vtk_reader.SetFilePrefix("D:/pyProject/Graduation_project/venv/bysj/bysj_final_code/Three_dimensional_region_growing_method/image_without_geli/")#文件夹路径
vtk_reader.SetFilePrefix("D:/pyProject/Graduation_project/venv/bysj/bysj_final_code/Three_dimensional_region_growing_method/thred_200_image/")#文件夹路径

vtk_reader.SetFilePattern("%s%d.jpg")
vtk_reader.SetDataExtent( 0, 200, 0, 400, 41,280)#1,20代表读取序列图片张数
vtk_reader.SetDataSpacing(1,1,1)
vtk_reader.Update()

# 利用封装好的MC算法抽取等值面，对应filter
marchingCubes = vtk.vtkMarchingCubes()
marchingCubes.SetInputConnection(vtk_reader.GetOutputPort())
marchingCubes.SetValue(0, 30)#设置第i个等值面的值为value

# 剔除旧的或废除的数据单元，提高绘制速度，对应filter
Stripper = vtk.vtkStripper()
Stripper.SetInputConnection(marchingCubes.GetOutputPort())

# 建立映射，对应mapper
mapper = vtk.vtkPolyDataMapper()
#mapper.SetInputConnection(marchingCubes.GetOutputPort())
mapper.SetInputConnection(Stripper.GetOutputPort())
mapper.ScalarVisibilityOff()

# 建立角色以及属性的设置，对应actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
# 角色的颜色设置
actor.GetProperty().SetDiffuseColor(1, 0, 0)#设置物体颜色为红色
# 设置高光照明系数
actor.GetProperty().SetSpecular(.1)
# 设置高光能量
actor.GetProperty().SetSpecularPower(100)

# 定义舞台，也就是渲染器，对应render
renderer = vtk.vtkRenderer()

# 定义舞台上的相机，对应render
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, 1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()

# 定义整个剧院(绘制窗口)，对应renderwindow
rewin = vtk.vtkRenderWindow()

# 定义与actor之间的交互，对应interactor
interactor = vtk.vtkRenderWindowInteractor()

# 将相机添加到舞台renderer
renderer.SetActiveCamera(aCamera)
aCamera.Dolly(1.5)

# 设置交互方式
style = vtk.vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# 将舞台添加到剧院中
rewin.AddRenderer(renderer)
interactor.SetRenderWindow(rewin)

# 将角色添加到舞台中
renderer.AddActor(actor)
renderer.SetBackground(1,1,1)#设置背景色为白色

# 将相机的焦点移动至中央，The camera will reposition itself to view the center point of the actors,
# and move along its initial view plane normal
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()





