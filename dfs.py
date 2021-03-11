import re


def readFile():
	g = Graph()
	with open('sampleGraph3.txt') as fo:  #edo anoigo to grapho gia na diavaso
		start=0
		roagflag=0  #flag to know road tag will start
		predflag=0  #flag to know prediction tag will start
		acttraff=0  #flag to know actual traffic per day tag will start
		day=0  #which day it is
		with open("output.txt", 'w') as opf: #edo anoigo to arxeio exodou
			for x in fo.read().split("\n"): #edo kano split ana grammi kai arxizo diavasma
				if (start==0):
					ww=re.findall(r"<Source>(.*?)</Source>",x,re.DOTALL)
					opf.write("Source -----> " + ww[0] + "\n")
					source=Vertex(ww[0])
					g.add_vertex(source)
				elif (start==1):
					ww=re.findall(r"<Destination>(.*?)</Destination>",x,re.DOTALL)
					opf.write("Destination -----> " + ww[0] + "\n")
					dest=Vertex(ww[0])
					g.add_vertex(dest)
					roadflag=1  #roads will start next round
				elif (start>=3 and roadflag==1):
					ww=x.split("; ")
					if (x=='</Roads>'):
						roadflag=0
						predflag=1  #predictions will start next round
					else:
						counter=0
						for xi in x.split("; "):  #spliting each road line
							if(counter==0):
								opf.write(xi + ' ')
								road=xi
							elif(counter==1):
								node1=xi
								g.add_vertex(Vertex(xi))
							elif(counter==2):
								node2=xi
								g.add_vertex(Vertex(xi))
							else:
								opf.write('with weight: ' + xi + '\n')
								weight=xi
							counter+=1
						
						g.add_edge(node1,node2,weight)
						g.dfs(source,dest)
				elif (predflag==1):
					if (x=="<Predictions>"):
						pass
					elif (x=="</Predictions>"):
						acttraff=1 #actual traffic will start next round
						predflag=0
					elif(x=="<Day>"):
						sday=0  #a new day just started
						day+=1  #a day passed from 80
					elif(sday>=0):
						if(x=="</Day>"): #an teleiose i mera
							sday=-1
						else:
							i=0 # just to know if first or second word in each day line
							for xi in x.split("; "):
								if(i==0):
									opf.write("Road: " + xi)
									i+=1
								else:
									opf.write(' with traffic: ' + xi + '\n')
							sday+=1 #counts for each road in the day
				elif(acttraff==1):
					if (x=="<ActualTrafficPerDay>"):
						pass
					elif (x=="</ActualTrafficPerDay>"):
						acttraff=0
					elif(x=="<Day>"):
						sday=0  #a new day just started
						day+=1  #a day passed from 80
					elif(sday>=0):
						if(x=="</Day>"): #an teleiose i mera
							sday=-1
						else:
							i=0 # just to know if first or second word in each day line
							for xi in x.split("; "):
								if(i==0):
									opf.write("Road: " + xi)
									i+=1
								else:
									opf.write(' with actual traffic: ' + xi + '\n')
							sday+=1 #counts for each road in the day
				start+=1
			opf.close()	
		fo.close()
	return True
	


class Vertex:
	def __init__(self, n):
		self.name = n
		self.neighbors = list()
		
		self.discovery = 0
		self.finish = 0
		self.color = 'black'
	
	def add_neighbor(self, v):
		if v not in self.neighbors:
			self.neighbors.append(v)
			self.neighbors.sort()

class Graph:
	vertices = {}
	time = 0
	done=0
	course=[]
	edges = []
	edge_indices = {}
	
	def add_vertex(self, vertex):
		if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
			self.vertices[vertex.name] = vertex
			for row in self.edges:
				row.append(0)
			self.edges.append([0] * (len(self.edges)+1))
			self.edge_indices[vertex.name] = len(self.edge_indices)
			return True
		else:
			return False
	
	def add_edge(self, u, v,weight):
		if u in self.vertices and v in self.vertices:
			self.edges[self.edge_indices[u]][self.edge_indices[v]] = weight
			self.edges[self.edge_indices[v]][self.edge_indices[u]] = weight
			for key, value in self.vertices.items():
				if key == u:
					value.add_neighbor(v)
				if key == v:
					value.add_neighbor(u)
			return True
		else:
			return False
			
	def print_graph(self):
		for key in sorted(list(self.vertices.keys())):
			print(key + str(self.vertices[key].neighbors) + "  " + str(self.vertices[key].discovery) + "/" + str(self.vertices[key].finish))

	def printCourse(self):
		print (self.course) 
			
	def _dfs(self, vertex,dest):
		global done
		global time
		if (done==1):
			return True
		vertex.color = 'red'
		vertex.discovery = time
		time += 1
		self.course.append(vertex.name)
		print (self.course) 
		for v in vertex.neighbors:
			if(self.vertices[v].name==dest.name):
				done=1
				self.course.append(dest.name)
				#print (self.course) 
			elif self.vertices[v].color == 'black':
				self._dfs(self.vertices[v],dest)
		vertex.color = 'blue'
		vertex.finish = time
		time += 1
		if(done!=1):
			self.course.pop()
		#print (self.course) 
		
	def dfs(self, vertex,dest):
		global time
		global done #if the course was set at last
		done=0
		time = 1
		self._dfs(vertex,dest)

		


g = Graph()
a = Vertex('A')
b = Vertex('H')
g.add_vertex(a)
g.add_vertex(b)
g.add_vertex(Vertex('B'))
for i in range(ord('A'), ord('K')):
	g.add_vertex(Vertex(chr(i)))

edges = ['AB', 'AE', 'BF', 'CG', 'DE', 'DH', 'EH', 'FG', 'FI', 'FJ', 'GJ', 'HI']
for edge in edges:
	g.add_edge(edge[:1], edge[1:],1)
	
g.dfs(a,b)

g.printCourse()

'''		
		

a=readFile()

g = Graph()
g.printCourse()
#g.print_graph()

'''