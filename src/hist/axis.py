import boost_histogram.axis as bha


class Regular(bha.Regular):
	def __init__(self, bins, start, stop, *, name=None, underflow=True, overflow=True, growth=False, circular=False, transform=None):

		"""

		Make a regular axis with nice keyword arguments for underflow,

		overflow, and growth. The modified axis inherits most of its properties

		from the old Regular axis, but however now has a name property that would

		be used to refer to it instead of using its index.

		

		Parameters
		
		----------

		bins : int

			The number of bins between start and stop

		start : float

			The beginning value for the axis

		stop : float

			The ending value for the axis

		name : Any

			Any Python object used to give as a reference to a
			particular axis
			
		underflow : bool = True

			Enable the underflow bin

		overflow : bool = True

			Enable the overflow bin

		growth : bool = False

			Allow the axis to grow if a value is encountered out of range.

			Be careful, the axis will grow as large as needed.

		circular : bool = False

			Filling wraps around.

		transform : Optional[AxisTransform] = None

			Transform the regular bins (Log, Sqrt, and Pow(v))

		"""
		metadata = dict(name=name)
		super().__init__(bins, start, stop, metadata=metadata, underflow=underflow, overflow=overflow, growth=growth, circular=circular, transform=transform)

	@property
	def name(self):
		""" Returns the name of the axis called on. """
		return self.metadata['name']

	@name.setter
	def name(self, value):
		""" Is used to return the name of the axis called upon on. """
		self.metadata['name'] = value




class Variable(bha.Variable):
	def __init__(self, edges, *, name=None, underflow=True, overflow=True, growth=False):

		"""

		Make an axis with irregularly spaced bins. Provide a list

		or array of bin edges, and len(edges)-1 bins will be made.



		Parameters

		----------

		edges : Array[float]

			The edges for the bins. There will be one less bin than edges.

		name : object

			Any Python object to attach to the axis, like a label.

		underflow : bool = True

			Enable the underflow bin

		overflow : bool = True

			Enable the overflow bin

		circular : bool = False

			Enable wraparound

		growth : bool = False

			Allow the axis to grow if a value is encountered out of range.

			Be careful, the axis will grow as large as needed.

		"""
		metadata = dict(name=name)
		super().__init__(edges, metadata=metadata, underflow=underflow, overflow=overflow, growth=growth)

	@property
	def name(self):
		""" Returns the name of the axis that is udes to refer to the axis """
		return self.metadata['name']

	@name.setter
	def name(self, value):
		""" Sets the name of the axis called upon """
		self.metadata['name'] = value



class Integer(bha.Integer):
	def __init__(self, start, stop, *, name=None, underflow=True, overflow=True, growth=False):

		"""

		Make an integer axis, with a collection of consecutive integers.



		Parameters

		----------

		start : int

			The beginning value for the axis

		stop : int

			The ending value for the axis. (start-stop) bins will be created.

		name : object

			Any Python object to attach to the axis, like a label.

		underflow : bool = True

			Enable the underflow bin

		overflow : bool = True

			Enable the overflow bin

		circular : bool = False

			Enable wraparound

		growth : bool = False

			Allow the axis to grow if a value is encountered out of range.

			Be careful, the axis will grow as large as needed.

		"""
		metadata = dict(name=name)
		super().__init__(start, stop, metadata=metadata, underflow=underflow, overflow=overflow, growth=growth)

	@property
	def name(self):
		""" Returns the name of the axis called upon. """
		return self.metadata['name']
    
	@name.setter
	def name(self, value):
		""" Sets the name of the axis """
		self.metadata['name'] = value



class IntCategory(bha.IntCategory):
	def __init__(self, categories, *, name=None, growth=False):

		"""

		Make a category axis with ints; items will

		be added to a predefined list of bins or a growing (with growth=True)

		list of bins. An empty list is allowed if growth=True.





		Parameters

		----------

		categories : Iteratable[int]

			The bin values, either ints or strings.

		metadata : object

			Any Python object to attach to the axis, like a label.

		growth : bool = False

			Allow the axis to grow if a value is encountered out of range.

			Be careful, the axis will grow as large as needed.

		"""

		metadata = dict(name=name)
		super().__init__(categories, metadata=metadata, growth=growth)

	@property
	def name(self):
		""" Returns the name of the axis called upon. """
		return self.metadata['name']

	@name.setter
	def name(self, value):
		""" Sets the name of the axis called upon. """
		self.metadata['name'] = value



class StrCategory(bha.StrCategory):
	def __init__(self, categories, *, name=None, growth=False):

		"""

		Make a category axis with strings; items will

		be added to a predefined list of bins or a growing (with growth=True)

		list of bins.




		Parameters

		----------

		categories : Iterator[str]

			The bin values in strings. May be empty if growth is enabled.

		metadata : object

			Any Python object to attach to the axis, like a label.

		growth : bool = False

			Allow the axis to grow if a value is encountered out of range.

		Be careful, the axis will grow as large as needed.

		"""
		metadata = dict(name=name)
		super().__init__(categories, metadata=metadata, growth=growth)

	@property
	def name(self):
		""" Returns the name of the axis. """
		return self.metadata['name']

	@name.setter
	def name(self, value):
		""" Sets the name of the axis called upon. """
		self.metadata['name'] = value


class Bool(Integer):
	def __init__(self, name=None):
		""" This is basically the Integer axis with only two bins starting from zero and overflow turned off """
		super().__init__(0, 2, name=name, overflow=False)
