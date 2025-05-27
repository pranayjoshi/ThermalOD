from roboflow import Roboflow
rf = Roboflow(api_key="hw1lD98iF2uZNg8ognve")
project = rf.workspace("smart2").project("persondection-61bc2")
version = project.version(5)
dataset = version.download("yolov11")
project = rf.workspace("scifair2324").project("people-lajkn")
version = project.version(1)
dataset = version.download("yolov11")
project = rf.workspace("smart-yjdj0").project("persondection")
version = project.version(9)
dataset = version.download("yolov11")
project = rf.workspace("remotesurveillance-xy8vj").project("remotesurveillancethermal")
version = project.version(7)
dataset = version.download("yolov11")
project = rf.workspace("university-a4j9h").project("pedestrians-detection-vatow")
version = project.version(1)
dataset = version.download("yolov11")
                

                
                