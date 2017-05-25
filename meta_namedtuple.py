from collections import namedtuple
import itertools
def meta_namedtuple(name, attrs):
	base_attrs = [t if isinstance(t, str) else t[0] for t in attrs]

	base_attr_str = ' '.join(base_attrs)

	class _meta_cls(type):
		def __new__(mcs, name, bases, metadict):
			def _meta_new(_cls, *data):
				meta_datas = []
				for attr, data in itertools.izip(attrs, data):
					
					if isinstance(attr, str):
						meta_data = data
					else:
						meta_data = meta_namedtuple('%s_%s'%(_cls.__name__, attr[1]['type_name']), attr[1]['attrs'])(*data)
					
					meta_datas.append(meta_data)

				return tuple.__new__(_cls, meta_datas)
			metadict['__new__'] = _meta_new
			return type.__new__(mcs, bases[0].__name__, bases, metadict)

	class _metabase(namedtuple(name, base_attr_str)):
		__metaclass__ = _meta_cls

		def toList(self):
			ret = []

			for attr, data in itertools.izip(attrs, iter(self)):

				if isinstance(attr, str):
					add_data = data
				else:
					add_data = data.toList()
				
				ret.append(add_data)
			return ret

	return _metabase
if __name__ == '__main__':
	myType = meta_namedtuple('myType', ['a', 'b', 'c', ('d', {'type_name': 'e', 'attrs': ['t', ('y', {'type_name': 'kk', 'attrs': ['v1','v2']})]})])
	t = myType(*[1,2,3,[3,[4,'a']]])

	print t
	print isinstance(t, tuple)
	print t.a
	print t.d
	print t.d.t
	print t.d.y
	print t.d.y.v1
	print t.toList()