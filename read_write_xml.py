# coding:utf-8
# @Author     : HT
# @Time       : 2022/3/15 22:15
# @File       : readxml.py
# @Software   : PyCharm

from xml.dom.minidom import parse
import xml.dom.minidom
def readXML():
	domTree = parse(r"RGBD_m_7\annotation/RGBD_m_7_327.xml")
	# 文档根元素
	rootNode = domTree.documentElement
	print(rootNode.nodeName)
	object_node=rootNode.getElementsByTagName("object")[0]
	bndbox=object_node.getElementsByTagName("bndbox")[0]
	xmin = bndbox.getElementsByTagName("xmin")[0].childNodes[0].data
	ymin = bndbox.getElementsByTagName("xmin")[0].childNodes[0].data
	xmax = bndbox.getElementsByTagName("xmin")[0].childNodes[0].data
	ymax = bndbox.getElementsByTagName("xmin")[0].childNodes[0].data
	# print(type(xmin))
	return (xmin,ymin,xmax,ymax)

def writeXML():
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
	nodefolder.appendChild(doc.createTextNode('rgb_depth'))
	nodefilename = doc.createElement('filename')
	# 给叶子节点name设置一个文本节点，用于显示文本内容
	nodefilename.appendChild(doc.createTextNode('RGBD_m_7_47.jpg'))

	nodepath = doc.createElement('path')
	nodepath.appendChild(doc.createTextNode('G:\lab_collect_dataset\recordData_process\RGBD_m_7\rgb_depth\RGBD_m_7_47.jpg'))

	nodesource = doc.createElement("source")
	nodedatabase = doc.createElement("database")
	nodedatabase.appendChild(doc.createTextNode('Unknown'))

	nodesource.appendChild(nodedatabase)


	nodesize = doc.createElement("size")
	nodewidth = doc.createElement("width")
	nodewidth.appendChild(doc.createTextNode('775'))
	nodeheight = doc.createElement("height")
	nodeheight.appendChild(doc.createTextNode('532'))
	nodedepth = doc.createElement("depth")
	nodedepth.appendChild(doc.createTextNode('3'))

	nodesize.appendChild(nodewidth)
	nodesize.appendChild(nodeheight)
	nodesize.appendChild(nodedepth)

	nodesegmented = doc.createElement("segmented")
	nodesegmented.appendChild(doc.createTextNode('0'))

	nodeobject = doc.createElement("object")
	nodename = doc.createElement("name")
	nodename.appendChild(doc.createTextNode('person'))
	nodepose = doc.createElement("pose")
	nodepose.appendChild(doc.createTextNode('Unspecified'))
	nodetruncated = doc.createElement("truncated")
	nodetruncated.appendChild(doc.createTextNode('1'))
	nodedifficult = doc.createElement("difficult")
	nodedifficult.appendChild(doc.createTextNode('0'))

	nodebndbox = doc.createElement("bndbox")
	nodexmin = doc.createElement("xmin")
	nodexmin.appendChild(doc.createTextNode('255'))
	nodeymin = doc.createElement("ymin")
	nodeymin.appendChild(doc.createTextNode('80'))
	nodexmax = doc.createElement("xmax")
	nodexmax.appendChild(doc.createTextNode('557'))
	nodeymax = doc.createElement("ymax")
	nodeymax.appendChild(doc.createTextNode('532'))
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
	fp = open('voc.xml', 'w')
	doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")


readXML()
writeXML()