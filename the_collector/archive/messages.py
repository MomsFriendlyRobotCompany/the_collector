# ##############################################
# # The MIT License (MIT)
# # Copyright (c) 2018 Kevin Walchko
# # see LICENSE for full details
# ##############################################
# from collections import namedtuple
# import time
# import msgpack
#
#
# # simple ones, no stamp, wouldn't just send these. They are datatypes that
# # get put into a messages
# Vector2 = namedtuple('Vector2', 'x y')
# Vector = namedtuple('Vector', 'x y z')
# Quaternion = namedtuple('Quaternion', 'w x y z')
#
# # with timestamp
# # CompressedImage = namedtuple('CompressedImage', 'shape data timestamp')
# # Image = namedtuple('Image', 'shape data timestamp')
# # Lidar = namedtuple('Lidar', 'len data timestamp')
# # Path = namedtuple("Path", 'path')
#
#
# class Image(namedtuple('Image', 'shape bytes timestamp')):
#     """
#     OpenCV images
#     -------------------------------
#     d = img.tobytes()
#     s = img.shape
#     msg = Image(s, d)
#
#     img = np.frombytes(msg.d, dtype=np.uint8)
#     img.reshape(msg.shape)
#     """
#     __slots__ = ()
#
#     def __new__(cls, s, b, ts=None):
#         if ts:
#             return cls.__bases__[0].__new__(cls, s, b, ts)
#         else:
#             return cls.__bases__[0].__new__(cls, s, b, time.time())
#
#
# class Pose(namedtuple('Pose', 'position orientation timestamp')):
#     """
#     Pose refers to the positiona and orientation of a robot.
#     """
#     __slots__ = ()
#
#     def __new__(cls, p, o, ts=None):
#         if ts:
#             return cls.__bases__[0].__new__(cls, p, o, ts)
#         else:
#             return cls.__bases__[0].__new__(cls, p, o, time.time())
#
#
# class IMU(namedtuple('IMU', 'linear_accel angular_vel magnetic_field timestamp')):
#     """
#     Inertial measurement unit
#     """
#     __slots__ = ()
#
#     def __new__(cls, a, g, m, ts=None):
#         if ts:
#             return cls.__bases__[0].__new__(cls, a, g, m, ts)
#         else:
#             return cls.__bases__[0].__new__(cls, a, g, m, time.time())
#
#
# # # new messages get added here
# # # if the msgs contain other messages, then they are complex
# # simple_msgs = [Vector2, Vector, Quaternion, Image]
# # complex_msgs = [IMU, Pose]
# # known_msgs = simple_msgs + complex_msgs
# # complex_strs = ['IMU', 'Pose']
# #
# #
# # def process(x):
# #     """
# #     recursively goes through a data structure and builds a packable tuple data
# #     format for it.
# #     """
# #     # print('process', x)
# #     if type(x) in simple_msgs:
# #         return (x.__class__.__name__,) + x
# #     elif type(x) in complex_msgs:
# #         # print(x)
# #         return (x.__class__.__name__,) + tuple(process(m) for m in x)
# #     else:
# #         return (x,)
# #
# #
# # def serialize(x):
# #     # print('serialize', x)
# #     if type(x) in known_msgs:
# #         msg = msgpack.ExtType(1, msgpack.packb(process(x)))
# #         print(msg)
# #         return msg
# #     return x
# #
# #
# # def deserialize(code, data):
# #     print('deserialize', code, data)
# #     if code == 1:
# #         # you call this again to unpack and ext_hook for nested
# #         d = msgpack.unpackb(data, ext_hook=deserialize, raw=False, use_list=False)
# #         print('d', d)
# #
# #         # print d[0]   # holds class name
# #         # print d[1:]  # holds data inorder
# #         # finds constructor in namespace and calls it
# #         if d[0] in complex_strs:
# #             vals = []
# #             for i in d[1:]:
# #                 # print(i)
# #                 if len(i) > 1:
# #                     v = globals()[i[0]](*i[1:])
# #                 else:
# #                     v = i[0]
# #                 # print(v)
# #                 vals.append(v)
# #             return globals()[d[0]](*vals)
# #         else:
# #             return globals()[d[0]](*d[1:])
# #
# #     return msgpack.ExtType(code, data)
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
# #         self.simple_msgs = [Vector2, Vector, Quaternion, Image] + sm
# #         self.complex_msgs = [IMU, Pose] + cm
# #         self.known_msgs = self.simple_msgs + self.complex_msgs
# #         self.complex_strs = ['IMU', 'Pose', 'Image'] + cs
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
# #             if d[0] in self.complex_strs:
# #                 vals = []
# #                 for i in d[1:]:
# #                     # print(i)
# #                     if len(i) > 1:
# #                         v = globals()[i[0]](*i[1:])
# #                     else:
# #                         v = i[0]
# #                     # print(v)
# #                     vals.append(v)
# #                 return globals()[d[0]](*vals)
# #             else:
# #                 return globals()[d[0]](*d[1:])
# #
# #         return msgpack.ExtType(code, data)
# class Messages(object):
#     """
#     Base class to serialize/deserialize messages. You can easily add messages
#     by creating a new class from this class.
#     """
#     def __init__(self, sm=None, cm=None):
#         """
#         input dictionaries are: dict = {'Test': Test, 'Something': Something}
#         sm = dictionary of simple messages, only contains python variable types
#         cm = dictionary of  complex messages, also contains other messages
#         """
#
#         self.complex_dict = {
#             'IMU': IMU,
#             'Pose': Pose
#         }
#         if cm:
#             for k,v in cm.items():
#                 self.complex_dict[k] = v
#
#         self.complex_strs = tuple(self.complex_dict.keys())
#
#         self.complex_msgs = []
#         for k,v in self.complex_dict.items():
#             self.complex_msgs.append(v)
#
#         self.simple_dict = {
#             'Vector2': Vector2,
#             'Vector': Vector,
#             'Quaternion': Quaternion,
#             'Image': Image
#         }
#         if sm:
#             for k,v in sm.items():
#                 self.simple_dict[k] = v
#
#         self.simple_msgs = []
#         for k,v in self.simple_dict.items():
#             self.simple_msgs.append(v)
#
#         self.known_msgs = self.simple_msgs + self.complex_msgs
#
#         # for msg in self.known_msgs:
#         #     print(msg)
#
#     def process(self, x):
#         """
#         recursively goes through a data structure and builds a packable tuple data
#         format for it.
#         """
#         # print('process', x)
#         if type(x) in self.simple_msgs:
#             return (x.__class__.__name__,) + x
#         elif type(x) in self.complex_msgs:
#             # print(x)
#             return (x.__class__.__name__,) + tuple(self.process(m) for m in x)
#         else:
#             return (x,)
#
#     def serialize(self, x):
#         # print('serialize', x)
#         if type(x) in self.known_msgs:
#             msg = msgpack.ExtType(1, msgpack.packb(self.process(x)))
#             # print(msg)
#             return msg
#         return x
#
#     def deserialize(self, code, data):
#         # print('deserialize', code, data)
#         if code == 1:
#             # you call this again to unpack and ext_hook for nested
#             d = msgpack.unpackb(data, ext_hook=self.deserialize, raw=False, use_list=False)
#             # print('d', d)
#
#             # print d[0]   # holds class name
#             # print d[1:]  # holds data inorder
#             # finds constructor in namespace and calls it
#             if d[0] in self.complex_strs:  # is a complex message
#                 vals = []
#                 for i in d[1:]:
#                     # print(i)
#                     if len(i) > 1:
#                         # v = globals()[i[0]](*i[1:])
#                         v = self.simple_dict[i[0]](*i[1:])
#                     else:
#                         v = i[0]
#                     # print(v)
#                     vals.append(v)
#                 # return globals()[d[0]](*vals)
#                 return self.complex_dict[d[0]](*vals)
#             else:  # is a simple message
#                 # print("last d", d)
#                 # return globals()[d[0]](*d[1:])
#                 # raise Exception("Unknown type", d)
#                 return self.simple_dict[d[0]](*d[1:])
#
#         return msgpack.ExtType(code, data)
