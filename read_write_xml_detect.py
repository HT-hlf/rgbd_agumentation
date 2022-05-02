# coding:utf-8
# @Author     : HT
# @Time       : 2022/3/15 22:15
# @File       : readxml.py
# @Software   : PyCharm

from xml.dom.minidom import parse
import xml.dom.minidom
def readXML(path):
	domTree = parse(path)
	# domTree = parse(r"RGBD_m_7\annotation/RGBD_m_7_327.xml")
	# 文档根元素
	rootNode = domTree.documentElement
	# print(rootNode.nodeName)
	object_node=rootNode.getElementsByTagName("object")[0]
	bndbox=object_node.getElementsByTagName("bndbox")[0]
	xmin = bndbox.getElementsByTagName("xmin")[0].childNodes[0].data
	ymin = bndbox.getElementsByTagName("ymin")[0].childNodes[0].data
	xmax = bndbox.getElementsByTagName("xmax")[0].childNodes[0].data
	ymax = bndbox.getElementsByTagName("ymax")[0].childNodes[0].data
	# print(type(xmin))
	return (xmin,ymin,xmax,ymax)
# writeXML('voc.xml','rgb_depth','RGBD_m_7_47.jpg','G:\lab_collect_dataset\recordData_process\RGBD_m_7\rgb_depth\RGBD_m_7_47.jpg','775','532','3','person',4,4,264,264)
def writeXML(save_path,folder,filename,path,width,height,depth,name,xmin,ymin,xmax,ymax):
	# 在内存中创建一个空的文档
	doc = xml.dom.minidom.Document()
	# 创建一个根节点Managers对象
	root = doc.createElement('annotation')
	# 设置根节点的属性
	# root.setAttribute('company', 'xx科技')
	# root.setAttribute('address', '科技软件园')
	# 将根节点添加到文档对象中
	doc.appendChild(root)

	nodefolder = doc.createElement('folder')
	nodefolder.appendChild(doc.createTextNode(folder))
	nodefilename = doc.createElement('filename')
	# 给叶子节点name设置一个文本节点，用于显示文本内容
	nodefilename.appendChild(doc.createTextNode(filename))

	nodepath = doc.createElement('path')
	nodepath.appendChild(doc.createTextNode(path))

	nodesource = doc.createElement("source")
	nodedatabase = doc.createElement("database")
	nodedatabase.appendChild(doc.createTextNode('Unknown'))

	nodesource.appendChild(nodedatabase)


	nodesize = doc.createElement("size")
	nodewidth = doc.createElement("width")
	nodewidth.appendChild(doc.createTextNode(width))
	nodeheight = doc.createElement("height")
	nodeheight.appendChild(doc.createTextNode(height))
	nodedepth = doc.createElement("depth")
	nodedepth.appendChild(doc.createTextNode(depth))

	nodesize.appendChild(nodewidth)
	nodesize.appendChild(nodeheight)
	nodesize.appendChild(nodedepth)

	nodesegmented = doc.createElement("segmented")
	nodesegmented.appendChild(doc.createTextNode('0'))

	nodeobject = doc.createElement("object")
	nodename = doc.createElement("name")
	nodename.appendChild(doc.createTextNode(name))
	nodepose = doc.createElement("pose")
	nodepose.appendChild(doc.createTextNode('Unspecified'))
	nodetruncated = doc.createElement("truncated")
	nodetruncated.appendChild(doc.createTextNode('1'))
	nodedifficult = doc.createElement("difficult")
	nodedifficult.appendChild(doc.createTextNode('0'))

	nodebndbox = doc.createElement("bndbox")

	# nodexmin = doc.createElement("xmin")
	# nodexmin.appendChild(doc.createTextNode('255'))
	# nodeymin = doc.createElement("ymin")
	# nodeymin.appendChild(doc.createTextNode('80'))
	# nodexmax = doc.createElement("xmax")
	# nodexmax.appendChild(doc.createTextNode('557'))
	# nodeymax = doc.createElement("ymax")
	# nodeymax.appendChild(doc.createTextNode('532'))

	nodexmin = doc.createElement("xmin")
	nodexmin.appendChild(doc.createTextNode(xmin))
	nodeymin = doc.createElement("ymin")
	nodeymin.appendChild(doc.createTextNode(ymin))
	nodexmax = doc.createElement("xmax")
	nodexmax.appendChild(doc.createTextNode(xmax))
	nodeymax = doc.createElement("ymax")
	nodeymax.appendChild(doc.createTextNode(ymax))


	nodebndbox.appendChild(nodexmin)
	nodebndbox.appendChild(nodeymin)
	nodebndbox.appendChild(nodexmax)
	nodebndbox.appendChild(nodeymax)

	nodeobject.appendChild(nodename)
	nodeobject.appendChild(nodepose)
	nodeobject.appendChild(nodetruncated)
	nodeobject.appendChild(nodedifficult)
	nodeobject.appendChild(nodebndbox)

	root.appendChild(nodefolder)
	root.appendChild(nodefilename)
	root.appendChild(nodepath)
	root.appendChild(nodesource)
	root.appendChild(nodesize)
	root.appendChild(nodesegmented)
	root.appendChild(nodeobject)


	# 将各叶子节点添加到父节点Manager中，
	# 最后将Manager添加到根节点Managers中
	# nodeManager.appendChild(nodewidth)
	# nodeManager.appendChild(nodeheight)
	# nodeManager.appendChild(nodeorigin)
	# nodeManager.appendChild(nodedata)
	# root.appendChild(nodeManager)
	# 开始写xml文档
	fp = open(save_path, 'w')
	# doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
	doc.writexml(fp, encoding="utf-8")

def append(save_path,name,end,xmin,ymin,xmax,ymax):
	domTree = parse(save_path)
	rootNode = domTree.documentElement

	nodeobject = domTree.createElement("object")
	nodename = domTree.createElement("name")
	nodename.appendChild(domTree.createTextNode(name))
	nodepose = domTree.createElement("pose")
	nodepose.appendChild(domTree.createTextNode('Unspecified'))
	nodetruncated = domTree.createElement("truncated")
	nodetruncated.appendChild(domTree.createTextNode('1'))
	nodedifficult = domTree.createElement("difficult")
	nodedifficult.appendChild(domTree.createTextNode('0'))

	nodebndbox = domTree.createElement("bndbox")


	nodexmin = domTree.createElement("xmin")
	nodexmin.appendChild(domTree.createTextNode(xmin))
	nodeymin = domTree.createElement("ymin")
	nodeymin.appendChild(domTree.createTextNode(ymin))
	nodexmax = domTree.createElement("xmax")
	nodexmax.appendChild(domTree.createTextNode(xmax))
	nodeymax = domTree.createElement("ymax")
	nodeymax.appendChild(domTree.createTextNode(ymax))


	nodebndbox.appendChild(nodexmin)
	nodebndbox.appendChild(nodeymin)
	nodebndbox.appendChild(nodexmax)
	nodebndbox.appendChild(nodeymax)

	nodeobject.appendChild(nodename)
	nodeobject.appendChild(nodepose)
	nodeobject.appendChild(nodetruncated)
	nodeobject.appendChild(nodedifficult)
	nodeobject.appendChild(nodebndbox)

	rootNode.appendChild(nodeobject)


	# 将各叶子节点添加到父节点Manager中，
	# 最后将Manager添加到根节点Managers中
	# nodeManager.appendChild(nodewidth)
	# nodeManager.appendChild(nodeheight)
	# nodeManager.appendChild(nodeorigin)
	# nodeManager.appendChild(nodedata)
	# root.appendChild(nodeManager)
	# 开始写xml文档
	if end:
		with open(save_path, 'w') as f:
			# 缩进 - 换行 - 编码
			domTree.writexml(f, indent='\t', addindent='\t', newl='\n',encoding='utf-8')
	else:
		with open(save_path, 'w') as f:
			# 缩进 - 换行 - 编码
			domTree.writexml(f, encoding='utf-8')

# readXML(r"RGBD_m_7\annotation/RGBD_m_7_327.xml")
# # writeXML('voc.xml',)
# writeXML('RGBD_m_7_47.xml','rgb_depth','RGBD_m_7_47.jpg','G:\lab_collect_dataset\recordData_process\RGBD_m_7\rgb_depth\RGBD_m_7_47.jpg','775','532','3','person',str(4),str(4),str(264),str(264))
# append('RGBD_m_7_47.xml','person',False,str(14),str(14),str(1264),str(1264))
# append('RGBD_m_7_47.xml','person',False,str(14),str(14),str(1264),str(1264))
# append('RGBD_m_7_47.xml','person',False,str(14),str(14),str(1264),str(1264))
# append('RGBD_m_7_47.xml','person',True,str(14),str(14),str(1264),str(1264))