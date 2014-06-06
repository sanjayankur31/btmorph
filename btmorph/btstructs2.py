"""
File contains:
    P3D2
    SNode2   
    STree2
    VoxelGrid (Irina Reshodko)
B. Torben-Nielsen (legacy code)
"""
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class P3D2 :
    """
    Basic container to represent and store 3D information
    """
    def __init__(self,xyz,radius,type=7) :
        # """
        # Constructor.

        # Parameters
        # -----------

        # xyz : numpy.array
        #     3D location
        # radius : float
        # type : int
        #     Type asscoiated with the segment according to SWC standards
        # """
        self.xyz = xyz
        self.radius = radius
        self.type = type

    def __str__(self) :
        #return "P3DD " + str(self.xyz) + ", R=",str(self.radius)+ ", T="+str(self.type)
        return "P3D2 [%.2f %.2f %.2f], R=%.2f" % (self.xyz[0],self.xyz[1],self.xyz[2],self.radius)
        #Return "P3D2 ".format, self.xyz)

class SNode2 :
    """
    Simple Node for use with a simple Tree (STree)
    
    By design, the "_content" should be a dictionary. (2013-03-08)
    """
    
    def __init__(self,index) :
        # """
        # Constructor.

        # Parameters
        # -----------
        # index : int
        #    Index, unique name of the SNode2
        # """
        self._parent_node = None
        self._index = index
        self._child_nodes = []
        
    def get_index(self) :
        """
        Return the index of this node

        Returns
        -------
        index : int
        """
        return self._index
        
    def get_parent_node(self) :
        """
        Return the parent node of this one.

        Returns
        -------
        parent : :class:`SNode2`
           In case of the root, None is returned.Otherwise a :class:`SNode2` is returned
        """          
        return self._parent_node
        
    def get_child_nodes(self) :
        """
        Return the child nodes of this one (if any)

        Returns
        -------
        children : list :class:`SNode2`
           In case of a leaf an empty list is returned
        """                  
        return self._child_nodes
        
    def get_content(self) :
        """
        Return the content dict of a :class:`SNode2`

        Returns
        -------
        parent : :class:`SNode2`
           In case of the root, None is returned.Otherwise a :class:`SNode2` is returned
        """                  
        return self._content
    
    def set_index(index) :
        """
        Set the unqiue name of a node

        Parameters
        ----------

        index : int
        """
        self._index = index
    
    def set_parent_node(self,parent_node) :
        """
        Set the parent node of a given other node

        Parameters
        ----------
        node : :class:`SNode2`
        """
        self._parent_node = parent_node
        
    def set_content(self,content) :
        """
        Set the content of a node. The content must be a dict

        Parameters
        ----------
        content : dict
            dict with content. For use in btmorph at least a 'p3d' entry should be present
        """        
        if isinstance(content,dict) :
            self._content = content 
        else :
            raise Exception("SNode2.set_content must receive a dict")    
        
    def add_child(self,child_node) :
        """
        add a child to the children list of a given node

        Parameters
        -----------
        node :  :class:`SNode2`
        """
        self._child_nodes.append(child_node)
            
    def make_empty(self):
        """
        Clear the node. Unclear why I ever implemented this. Probably to cover up some failed garbage collection
        """
        self._parent_node = None
        self._content = None
        self._child_nodes = []
            
    def remove_child(self, child_node) :
        """
        Remove a child node from the list of children of a specific node

        Parameters
        -----------
        node :  :class:`SNode2`
            If the child doesn't exist, you get into problems.
        """
        self._child_nodes.remove(child_node)
        
    def __str__(self) :
        return 'SNode2 (ID: '+str(self._index)+')'

    def __lt__(self,other):
        if self._index < other._index :
            return True
    def __le__(self,other):
        if self._index <= other._index :
            return True
    def __gt__(self,other):
        if self._index > other._index :
            return True
    def __ge__(self,other):
        if self._index >= other._index :
            return True
    
    def __copy__(self) : # customization of copy.copy
        ret = SNode2(self._index)
        for child in self._child_nodes :
            ret.add_child(child)
        ret.content = self._content
        ret.set_parent_node(self._parent_node)
        return ret
        
class STree2 :
    '''
    Simple tree for use with a simple Node (:class:`SNode2`).

    While the class is designed to contain binary trees (for neuronal morphologies) the number of children is not limited.
    As such, this is a generic implementation of a tree structure as a linked list.
    '''
    
    def __init__(self) :
         _root = None
        
    def set_root(self,node) :
        """
        Set the root node of the tree

        Parameters
        -----------
        node : :class:`SNode2`
            to-be-root node
        """
        self._root = node
        self._root.set_parent_node(None)
        
    def get_root(self) :
        """
        Obtain the root node

        Returns
        -------
        root : :class:`SNode2`
        """
        return self._root
        
    def is_root(self,node) :
        """
        Check whether a node is the root node

        Returns
        --------
        is_root : boolean
            True is the queried node is the root, False otherwise
        """
        if node.get_parent_node() != None :
            return False
        else :
            return True
            
    def is_leaf(self,node) :
        """
        Check whether a node is a leaf node, i.e., a node without children

        Returns
        --------
        is_leaf : boolean
            True is the queried node is a leaf, False otherwise
        """
        if len(node.get_child_nodes()) == 0  :
            return True
        else :
            return False
            
    def add_node_with_parent(self,node,parent) :
        """
        Add a node to the tree under a specific parent node

        Parameters
        -----------
        node : :class:`SNode2`
            node to be added
        parent : :class:`SNode2`
            parent node of the newly added node
        """
        node.set_parent_node(parent)
        parent.add_child(node)
        
    def remove_node(self,node) :
        """
        Remove a node from the tree

        Parameters
        -----------
        node : :class:`SNode2`
            node to be removed
        """
        node.get_parent_node().remove_child(node)
        self._deep_remove(node)
        
            
    def _deep_remove(self,node) :
        children = node.get_child_nodes()
        node.make_empty()
        for child in children :
            self._deep_remove(child)        

    def get_nodes(self) :
        """
        Obtain a list of all nodes int the tree

        Returns
        -------
        all_nodes : list of :class:`SNode2`
        """
        n = []
        self._gather_nodes(self._root,n) 
        return n 

    def get_sub_tree(self,fake_root) :
        """
        Obtain the subtree starting from the given node

        Parameters
        -----------
        fake_root : :class:`SNode2`
            Node which becomes the new root of the subtree

        Returns
        -------
        sub_tree :  STree2
            New tree with the node from the first argument as root node
        """
        ret = STree2()
        cp = fake_root.__copy__()
        cp.set_parent_node(None)
        ret.set_root(cp)
        return ret

    def _gather_nodes(self,node,node_list) :
        node_list.append(node)
        for child in node.get_child_nodes() :
            self._gather_nodes(child,node_list)
    
    def get_node_with_index(self, index) :
        """
        Get a node with a specific name. The name is always an integer

        Parameters
        ----------
        index : int
            Name of the node to be found

        Returns
        -------
        node : :class:`SNode2`
            Node with the specific index
        """
        return self._find_node(self._root,index)
        
    def get_node_in_subtree(self,index,fake_root) :
        """
        Get a node with a specific name in a the subtree rooted at fake_root. The name is always an integer

        Parameters
        ----------
        index : int
            Name of the node to be found
        fake_root: :class:`SNode2`
            Root node of the subtree in which the node with a given index is searched for

        Returns
        -------
        node : :class:`SNode2`
            Node with the specific index
        """
        return self._find_node(fake_root,index)
        
    def _find_node(self,node,index) :
        """
        Sweet breadth-first/stack iteration to replace the recursive call. 
        Traverses the tree until it finds the node you are looking for.

        Parameters
        -----------

        
        Returns
        -------
        node : :class:`SNode2`
            when found and None when not found
        """
        stack = []; 
        stack.append(node)
        while(len(stack) != 0) :
            for child in stack :
                if child.get_index() == index  :
                    return child
                else :
                    stack.remove(child)
                    for cchild in child.get_child_nodes() :
                        stack.append(cchild)
        return None # Not found!
        
    def degree_of_node(self,node) :
        """
        Get the degree of a given node. The degree is defined as the number of leaf nodes in the subtree rooted at this node.

        Parameters
        ----------
        node : :class:`SNode2`
            Node of which the degree is to be computed.

        Returns
        -------
        degree : int
        """
        sub_tree = self.get_sub_tree(node)
        st_nodes = sub_tree.get_nodes()
        leafs = 0
        for n in st_nodes :
            if sub_tree.is_leaf(n) :
                leafs = leafs +1
        return leafs
        
    def order_of_node(self,node) :
        """
        Get the order of a given node. The order or centrifugal order is defined as 0 for the root and increased with any bifurcation.
        Hence, a node with 2 branch points on the shortest path between that node and the root has order 2.

        Parameters
        ----------
        node : :class:`SNode2`
            Node of which the order is to be computed.

        Returns
        -------
        order : int
        """
        ptr =self.path_to_root(node)
        order = 0
        for n in ptr :
            if len(n.get_child_nodes()) > 1  :
                order = order +1
        # order is on [0,max_order] thus subtract 1 from this calculation
        return order -1 
                
    def path_to_root(self,node) :
        """
        Find and return the path between a node and the root.

        Parameters
        ----------
        node : :class:`SNode2`
            Node at which the path starts

        Returns
        -------
        path : list of :class:`SNode2`
            list of :class:`SNode2` with the provided node and the root as first and last entry, respectively.
        """
        n = []
        self._go_up_from(node,n)            
        return n
        
    def _go_up_from(self,node,n):
        n.append(node)
        p_node = node.get_parent_node()
        if p_node != None :
            self._go_up_from(p_node,n)

    def path_between_nodes(self,from_node,to_node) :
        """
        Find the path between two nodes. The from_node needs to be of higher \
        order than the to_node. In case there is no path between the nodes, \
        the path from the from_node to the soma is given.

        Parameters
        -----------
        from_node : :class:`SNode2`
        to_node : :class:`SNode2`
        """
        n = []
        self._go_up_from_until(from_node,to_node,n)
        return n

    def _go_up_from_until(self,from_node,to_node,n) :
        n.append(from_node)
        if from_node == to_node :
            return
        p_node = from_node.get_parent_node()
        if p_node != None :
            self._go_up_from_until(p_node,to_node,n)

    def write_SWC_tree_to_file(self,file_n) :
        """
        Non-specific for a tree. Used to write an SWC file from a morphology stored in this tree.

        Parameters
        ----------
        file_n : str
            name of the file to open
        """
        writer = open(file_n,'w')
        nodes = self.get_nodes()
        nodes.sort()

        # 3 point soma representation (See Neuromoprho.org FAQ)
        s1p = nodes[0].get_content()["p3d"]
        s1_xyz = s1p.xyz
        s2p = nodes[1].get_content()["p3d"]
        s2_xyz = s2p.xyz
        s3p = nodes[2].get_content()["p3d"]
        s3_xyz = s3p.xyz
        soma_str = "1 1 " +str(s1_xyz[0]) + " " + str(s1_xyz[1]) + \
          " " + str(s1_xyz[2]) + " " + str(s1p.radius) + " -1\n" + \
          "2 1 " +str(s2_xyz[0]) + " " + str(s2_xyz[1]) + \
          " " + str(s2_xyz[2]) + " " + str(s2p.radius) + " 1\n" + \
          "3 1 " +str(s3_xyz[0]) + " " + str(s3_xyz[1]) + \
          " " + str(s3_xyz[2]) + " " + str(s3p.radius) + " 1\n"
        writer.write(soma_str)
        writer.flush()
        
        # add the soma compartment, then enter the loop
        for node in nodes[3:] :
            p3d = node.get_content()['p3d'] # update 2013-03-08
            xyz = p3d.xyz
            radius = p3d.radius
            tt = p3d.type
            p3d_string = str(node.get_index())+' '+str(tt) + ' ' + \
                str(xyz[0]) + ' ' + str(xyz[1])+ ' ' + str(xyz[2]) + \
                ' ' + str(radius) + ' ' \
                + str(node.get_parent_node().get_index())
            # print 'p3d_string: ', p3d_string
            writer.write( p3d_string + '\n' )
            writer.flush()
        writer.close()          
        #print 'STree::writeSWCTreeToFile -> finished. Tree in >',fileN,'<'
        
    def read_SWC_tree_from_file(self,file_n,types=range(1,10)) :
        """
        Non-specific for a tree.
        Read and load a morphology from an SWC file. and parse it into an STree2 object. 
        On the NeuroMorpho.org website, 5 types of somadescriptions are 
        considered. (http://neuromorpho.org/neuroMorpho/SomaFormat.html)
        
        Parameters
        -----------
        file_n : str
        name of the file to open
        soma_type : int
            [1-5], see specs
        """
        import numpy as np
        file = open(file_n,'r')
        all_nodes = dict()
        for line in file :
            if not line.startswith('#') :
                split= line.split()
                index = int(split[0].rstrip())
                type = int(split[1].rstrip())
                x = float(split[2].rstrip())
                y = float(split[3].rstrip())
                z = float(split[4].rstrip())
                radius = float(split[5].rstrip())
                parent_index = int(split[6].rstrip())

                if type in types:
                    tP3D = P3D2(np.array([x,y,z]),radius,type)
                    t_node = SNode2(index)
                    t_node.set_content({'p3d':tP3D})
                    all_nodes[index] = (t_node,parent_index)
                
        for index, (node,parent_index) in all_nodes.items() :
            if index == 1:
                self.set_root(node)
            elif index == 2 or index==3:
                # the 3-point soma representation (http://neuromorpho.org/neuroMorpho/SomaFormat.html)
                self.add_node_with_parent(node,self._root)
            else:
                parent_node = all_nodes[parent_index][0]
                self.add_node_with_parent(node,parent_node)
            
        return self

    def __str__(self) :
        return "STree2 ("+str(len(self.get_nodes()))+" nodes)"
        
class VoxelGrid :
    """
    Represents voxelized 3D model of an object with given dimensions and resolution
    Dimensions: real dimensions of an object in micrometers
    Resolution: resolution in voxels
    """
    @staticmethod
    def checkKey(dims, key):
        """
        Check key type and range
        """
        if not isinstance(key, tuple) :
            raise TypeError("The key must be a tuple of 3 integers")
        if len(key) < 3:
            raise TypeError("The key must be a tuple of 3 integers")        
        (x,y,z) = key
        if not (isinstance(x, int) and isinstance(y, int) and isinstance(z, int)):
            raise TypeError("The key must be a tuple of 3 integers") 
        if (x < 0 or x > dims[0]):
            raise IndexError("Index is out of range")
        if (y < 0 or y > dims[1]):
            raise IndexError("Index is out of range")
        if (z < 0 or z > dims[2]):
            raise IndexError("Index is out of range")
        return True
        
    def __getitem__(self, key):
        """
        Right [] operator overload
        """
        VoxelGrid.checkKey(self.res, key)
        if not key in self.grid:
            return False
        else:
            return True
            
    def __setitem__(self, key, value):
        """
        Left [] operator overload
        """
        VoxelGrid.checkKey(self.res, key)
        if not isinstance(value, bool):
            raise TypeError("The value must be boolean")
        if key in self.grid and value == False:
            del self.grid[key]
        elif value == True:
            self.grid[key] = value
        
    def __init__(self, dimensions, resolution):
        """
        Generate a voxel grid for given dimensions and resolution
        Note: the dimensions ratio (x:y:z) must be the same as resolution ratio (rx:ry:rz)
        If this is not the case, the dimensions will be expanded to meet this criteria
        
        Parameters
        ----------
        dimensions : numpy.array
        The grid's real dimensions
        resolution : array(int)
        The grid's resolution (number of voxels in each dimension). Must be a power of two
        """
        if not (len(dimensions) == 3 and len(resolution) == 3):
            raise TypeError("Dimensions and resolution must be number iterables of length 3")
        for i in range(0,3):
            if not VoxelGrid.isPowerOfTwo(resolution[i]):
                raise IndexError("Resolution must be power of 2")
        self.dim = VoxelGrid.adjustDimensions(dimensions, resolution)
        self.res = resolution
        self.grid = {}
    
    @staticmethod    
    def adjustDimensions(dimensions, resolution):
        """
        Adjusts the grid dimensions(x,y,z) in such a way so their ratio is the same as resolution (rx,ry,rz) ratio.
        x:y:z = rx:ry:rz
        
        Parameters
        ----------
        dimensions : numpy.array
        The grid's real dimensions
        resolution : array(int)
        The grid's resolution (number of voxels in each dimension). Must be a power of two
        
        Returns
        ----------
        New dimensions :  numpy.array
        An expanded (if neccessary) dimensions
        """
        if not (len(dimensions) == 3 and len(resolution) == 3):
            raise TypeError("Dimension and resolution must be number iterables of length 3")
        for i in range(0,3):
            if not (dimensions[i] >= 0 and resolution[i] >= 0):
                raise IndexError("Dimensions and resolution must be positive")
        # Check if all dimensions match
        # Is more than one dimension and/or resolution is zero?
        if (resolution.count(0) > 1 or (len(dimensions) - numpy.count_nonzero(dimensions)) > 1):
            return None
        # Is there a case where dimension/resolution is zero but not both of them are zero?
        for i in range(0, 3):
            if resolution[i]*dimensions[i] == 0 and resolution[i]+dimensions[i] != 0:
                return None
        [x,y,z] = dimensions
        [x_new,y_new,z_new] = [x,y,z]
        [rx,ry,rz] = resolution
        if x > y * float(rx)/float(ry):
            y_new = x * float(ry)/float(rx)
            if z > x * float(rz)/float(rx):
                x_new = z * float(rx)/float(rz)
                y_new = x_new * float(ry)/float(rx)
            else:
                z_new = x * float(rz)/float(rx)
        else:
            x_new = y * float(rx)/float(ry)
            if z > y * float(rz)/float(ry):
                y_new = z * float(ry)/float(rz)
                x_new = y_new * float(rx)/float(ry)
            else:
                z_new = y * float(rz)/float(ry)  
        return [x_new,y_new,z_new]
    
    @staticmethod
    def isPowerOfTwo(int_num) :
        """
        Checks if the number is a power of two
        
        Parameters
        ----------
        int_num : int
        Input number
        
        Returns
        ----------
        True if N=2^m and False otherwise
        """
        return isinstance(int_num, int) and int_num > 0 and (int_num & (int_num - 1) == 0)
        
    def plot(this):
        """ 
        Plot the grid as a scattered 3d plot
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        keys = this.grid.keys();
        xs = map(lambda (x,y,z): x, keys)
        ys = map(lambda (x,y,z): y, keys)
        zs = map(lambda (x,y,z): z, keys)
        ax.scatter(xs, ys, zs, zdir="z")
    
    def calcEncompassingBox_sphere(self, center, radius):
        """
        Calculate encompassing box for a sphere of the given radius and center
        
        Parameters
        ------------
        center : array or tuple of numbers (real dimensions)
        The center of the sphere
        radius : number (real dimension)
        The sphere's radius
        
        Returns
        ------------
        Array of ranges (mapped to resolution) for x, y and z: [(x1,x2), (y1,y2), (z1,z2)]
        or None if there is no intersection between the sphere and the grid
        """
        if radius < 0:
            return None
        if radius == 0:
            c = (round(center[0]*self.res[0]/self.dim[0]), round(center[1]*self.res[1]/self.dim[1]), round(center[2]*self.res[2]/self.dim[2]))
            return [(int(c[0]), int(c[0])), (int(c[1]), int(c[1])), (int(c[2]), int(c[2]))]
        ranges = [0, 0, 0]
        for i in range(0,3):
            ranges[i] = (round(center[i] - radius)*self.res[i]/self.dim[i], round(center[i] + radius)*self.res[i]/self.dim[i])
            if ranges[i][0] > self.res[i] and ranges[i][1] > self.res[i] or ranges[i][0] < 0 and ranges[i][1] < 0:
                return None
            ranges[i]= (int(max(ranges[i][0], 0)), int(min(ranges[i][1], self.res[i])))
        return ranges
        
    def fallsIntoSphere(self, point, center, radius):
        """
        Check if the point falls into the sphere of given radius and center
        
        Parameters
        ------------
        point : coordinates of the point of interest (voxel coordinates)
        center : array or tuple of numbers (real dimensions)
        The center of the sphere
        radius : number (real dimension)
        The sphere's radius
        
        Returns:
        True or False
        """
        if radius < 0:
            return False
        if radius == 0:
            center_vox = (round(center[0]*self.res[0]/self.dim[0]), round(center[1]*self.res[1]/self.dim[1]), round(center[2]*self.res[2]/self.dim[2]))
            return bool(center_vox == point)
        s = 0
        for i in range(0, 3):
            s += (point[i]*self.dim[i]/self.res[i] - center[i])**2
        return bool(s <= radius**2)
    
    def addSphere(self, center, radius):
        """
        Adds a voxelized filled sphere of the given radius and center to the grid
        Parameters
        ------------
        center : array or tuple of numbers (real dimensions)
        The center of the sphere
        radius : number (real dimension)
        The sphere's radius
        """
        ranges = self.calcEncompassingBox_sphere(center, radius)
        if ranges == None:
            return
        [(x1,x2), (y1,y2), (z1,z2)] = ranges
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                for z in range(z1, z2+1):
                    self[(x,y,z)] = self.fallsIntoSphere((x,y,z), center, radius)
        
        

    