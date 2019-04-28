# #!/usr/bin/env python3
#
# from the_collector import BagWriter, BagReader
# # from the_collector.messages import serialize, deserialize
# from the_collector.messages import Messages
# from the_collector.messages import Pose, Vector2, Vector, Quaternion, IMU, Image
# from collections import namedtuple
# from io import BytesIO
# import os
# import msgpack
#
#
# # class Messages(object):
# #     """
# #     Base class to serialize/deserialize messages. You can easily add messages
# #     by creating a new class from this class.
# #     """
# #     def __init__(self, sm=None, cm=None, cs=None):
# #         if sm is None:
# #             sm = []
# #         if cm is None:
# #             cm = []
# #             cs = []
# #
# #         # for deserialization, need to match string to object
# #         self.simple_msgs = {
# #             'Vector2': Vector2,
# #             'Vector': Vector,
# #             'Quaternion': Quaternion,
# #             'Image': Image
# #         }
# #         self.complex_msgs = {
# #             'IMU': IMU,
# #             'Pose': Pose
# #         }
# #
# #         # for serialization, need to match type(obj) to a message
# #         self.known_msgs = []
# #         for key in self.simple_msgs.keys():
# #             self.known_msgs.append(self.simple_msgs[key])
# #         for key in self.complex_msgs.keys():
# #             self.known_msgs.append(self.complex_msgs[key])
# #         # self.complex_strs = ['IMU', 'Pose', 'Image'] + cs
# #
# #         print(self.known_msgs)
# #
# #     def process(self, x):
# #         """
# #         recursively goes through a data structure and builds a packable tuple data
# #         format for it.
# #         """
# #         # print('process', x)
# #         print('process', type(x))
# #         if type(x) in self.simple_msgs:
# #             return (x.__class__.__name__,) + x
# #         elif type(x) in self.complex_msgs:
# #             # print(x)
# #             return (x.__class__.__name__,) + tuple(self.process(m) for m in x)
# #         else:
# #             return (x,)
# #
# #     def serialize(self, x):
# #         # print('serialize', x)
# #         if type(x) in self.known_msgs:
# #             msg = msgpack.ExtType(1, msgpack.packb(self.process(x)))
# #             # print(msg)
# #             return msg
# #         return x
# #
# #     def deserialize(self, code, data):
# #         # print('deserialize', code, data)
# #         if code == 1:
# #             # you call this again to unpack and ext_hook for nested
# #             d = msgpack.unpackb(data, ext_hook=self.deserialize, raw=False, use_list=False)
# #             print('d', d)
# #
# #             # print d[0]   # holds class name
# #             # print d[1:]  # holds data inorder
# #             # finds constructor in namespace and calls it
# #             if d[0] in self.complex_msgs.keys():
# #                 vals = []
# #                 for i in d[1:]:
# #                     # print(i)
# #                     if len(i) > 1:
# #                         # v = globals()[i[0]](*i[1:]) #
# #                         v = self.simple_msgs[i[0]](*i[1:])
# #                     else:
# #                         v = i[0]
# #                     # print(v)
# #                     vals.append(v)
# #                 # return globals()[d[0]](*vals)  #
# #                 return self.complex_msgs[d[0]](*vals)
# #             else:
# #                 # return globals()[d[0]](*d[1:])
# #                 # print('d[0]', d[0])
# #                 return self.simple_msgs[d[0]](*d[1:])
# #
# #         return msgpack.ExtType(code, data)
#
#
# # class Messages(object):
# #     """
# #     Base class to serialize/deserialize messages. You can easily add messages
# #     by creating a new class from this class.
# #     """
# #     def __init__(self, sm=None, cm=None):
# #         # self.simple_msgs = [Vector2, Vector, Quaternion, Image]
# #         # self.complex_msgs = [IMU, Pose]
# #         # self.known_msgs = self.simple_msgs + self.complex_msgs
# #         # self.complex_strs = ['IMU', 'Pose', 'Image']
# #
# #         self.complex_dict = {
# #             'IMU': IMU,
# #             'Pose': Pose
# #         }
# #         if cm:
# #             for k,v in cm.items():
# #                 self.complex_dict[k] = v
# #
# #         self.complex_strs = tuple(self.complex_dict.keys())
# #
# #         self.complex_msgs = []
# #         for k,v in self.complex_dict.items():
# #             self.complex_msgs.append(v)
# #
# #         self.simple_dict = {
# #             'Vector2': Vector2,
# #             'Vector': Vector,
# #             'Quaternion': Quaternion,
# #             'Image': Image
# #         }
# #         if sm:
# #             for k,v in sm.items():
# #                 self.simple_dict[k] = v
# #
# #         self.simple_msgs = []
# #         for k,v in self.simple_dict.items():
# #             self.simple_msgs.append(v)
# #
# #         self.known_msgs = self.simple_msgs + self.complex_msgs
# #
# #         for msg in self.known_msgs:
# #             print(msg)
# #
# #     def process(self, x):
# #         """
# #         recursively goes through a data structure and builds a packable tuple data
# #         format for it.
# #         """
# #         # print('process', x)
# #         if type(x) in self.simple_msgs:
# #             return (x.__class__.__name__,) + x
# #         elif type(x) in self.complex_msgs:
# #             # print(x)
# #             return (x.__class__.__name__,) + tuple(self.process(m) for m in x)
# #         else:
# #             return (x,)
# #
# #     def serialize(self, x):
# #         # print('serialize', x)
# #         if type(x) in self.known_msgs:
# #             msg = msgpack.ExtType(1, msgpack.packb(self.process(x)))
# #             # print(msg)
# #             return msg
# #         return x
# #
# #     def deserialize(self, code, data):
# #         # print('deserialize', code, data)
# #         if code == 1:
# #             # you call this again to unpack and ext_hook for nested
# #             d = msgpack.unpackb(data, ext_hook=self.deserialize, raw=False, use_list=False)
# #             # print('d', d)
# #
# #             # print d[0]   # holds class name
# #             # print d[1:]  # holds data inorder
# #             # finds constructor in namespace and calls it
# #             if d[0] in self.complex_strs:  # is a complex message
# #                 vals = []
# #                 for i in d[1:]:
# #                     # print(i)
# #                     if len(i) > 1:
# #                         # v = globals()[i[0]](*i[1:])
# #                         v = self.simple_dict[i[0]](*i[1:])
# #                     else:
# #                         v = i[0]
# #                     # print(v)
# #                     vals.append(v)
# #                 # return globals()[d[0]](*vals)
# #                 return self.complex_dict[d[0]](*vals)
# #             else:  # is a simple message
# #                 # print("last d", d)
# #                 # return globals()[d[0]](*d[1:])
# #                 # raise Exception("Unknown type", d)
# #                 return self.simple_dict[d[0]](*d[1:])
# #
# #         return msgpack.ExtType(code, data)
#
#
# Test = namedtuple('Test', 'a b c')
#
#
# class myMessages(Messages):
#     """
#     How to add new messages?
#     """
#     def __init__(self):
#         Messages.__init__(self, sm={'Test': Test})
#
# def test_messages():
#     filename = 's.bag'
#     save = {
#         'test': [],
#         'bob': []
#     }
#     msgs = Messages()
#     bag = BagWriter(filename, buffer_size=10, pack=msgs.serialize)
#
#     for i in range(20):
#         d = Pose(Vector(1, 1, 1), Quaternion(1, 1, 1, 1))
#         bag.push('test', d)
#
#         k = IMU(Vector(.1,.1,.1), Vector(.2,.2,.2), Vector(.3,.3,.3))
#         bag.push('bob', k)
#
#         save['test'].append(d)
#         save['bob'].append(k)
#
#     bag.close()
#
#     bag = BagReader(unpack=msgs.deserialize)
#     load = bag.read(filename)
#     # assert save == load
#     print("*"*40)
#     print('\nAre they the same?', save == load, '\n')
#     print("*"*40)
#     # print('save', save['test'][0])
#     # print('load', load['test'][0])
#     # #
#     # print('-'*40)
#     # print(save)
#     # print('-'*40)
#     # print(load)
#
#     # clean up and delete file
#     os.remove(filename)
#
#
# def test_new_messages():
#     filename = 's.bag'
#     save = {
#         'test': [],
#         'bob': []
#     }
#     msgs = myMessages()
#     bag = BagWriter(filename, buffer_size=10, pack=msgs.serialize)
#
#     for i in range(20):
#         d = Test(i, 2*i, 3*i)
#         bag.push('bob', d)
#         bag.push('test', d)
#         save['test'].append(d)
#         save['bob'].append(d)
#
#     bag.close()
#
#     bag = BagReader(unpack=msgs.deserialize)
#     load = bag.read(filename)
#     # assert save == load
#     print("*"*40)
#     print('\nAre they the same?', save == load, '\n')
#     print("*"*40)
#     #
#     # print('-'*40)
#     # print(save)
#     # print('-'*40)
#     # print(load)
#     # clean up and delete file
#     os.remove(filename)
#
# if __name__ == "__main__":
#     test_messages()
#     test_new_messages()
