# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from spencer_tracking_msgs/TrackedPersons2d.msg. Do not edit."""
import codecs
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import spencer_tracking_msgs.msg
import std_msgs.msg

class TrackedPersons2d(genpy.Message):
  _md5sum = "972b7d693ce31c3b18f092f43387621c"
  _type = "spencer_tracking_msgs/TrackedPersons2d"
  _has_header = True  # flag to mark the presence of a Header object
  _full_text = """# Message with all 2d bbox in image of currently tracked persons 
#

Header                header      # Header containing timestamp etc. of this message
TrackedPerson2d[]     boxes       # All persons that are currently being tracked (2d image bbox)

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: spencer_tracking_msgs/TrackedPerson2d
# Message defining a 2d image bbox of a tracked person
#

uint64      track_id        # unique identifier of the target, consistent over time
float32     person_height   # 3d height of person in m
int32       x               # top left corner x of 2d image bbox
int32       y               # top left corner y of 2d image bbox
uint32      w               # width of 2d image bbox
uint32      h               # height of 2d image bbox
float32     depth           # distance from the camera in m
"""
  __slots__ = ['header','boxes']
  _slot_types = ['std_msgs/Header','spencer_tracking_msgs/TrackedPerson2d[]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       header,boxes

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(TrackedPersons2d, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.header is None:
        self.header = std_msgs.msg.Header()
      if self.boxes is None:
        self.boxes = []
    else:
      self.header = std_msgs.msg.Header()
      self.boxes = []

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_3I().pack(_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs))
      _x = self.header.frame_id
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.Struct('<I%ss'%length).pack(length, _x))
      length = len(self.boxes)
      buff.write(_struct_I.pack(length))
      for val1 in self.boxes:
        _x = val1
        buff.write(_get_struct_Qf2i2If().pack(_x.track_id, _x.person_height, _x.x, _x.y, _x.w, _x.h, _x.depth))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    if python3:
      codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      if self.header is None:
        self.header = std_msgs.msg.Header()
      if self.boxes is None:
        self.boxes = None
      end = 0
      _x = self
      start = end
      end += 12
      (_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs,) = _get_struct_3I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.header.frame_id = str[start:end].decode('utf-8', 'rosmsg')
      else:
        self.header.frame_id = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.boxes = []
      for i in range(0, length):
        val1 = spencer_tracking_msgs.msg.TrackedPerson2d()
        _x = val1
        start = end
        end += 32
        (_x.track_id, _x.person_height, _x.x, _x.y, _x.w, _x.h, _x.depth,) = _get_struct_Qf2i2If().unpack(str[start:end])
        self.boxes.append(val1)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_3I().pack(_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs))
      _x = self.header.frame_id
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.Struct('<I%ss'%length).pack(length, _x))
      length = len(self.boxes)
      buff.write(_struct_I.pack(length))
      for val1 in self.boxes:
        _x = val1
        buff.write(_get_struct_Qf2i2If().pack(_x.track_id, _x.person_height, _x.x, _x.y, _x.w, _x.h, _x.depth))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    if python3:
      codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      if self.header is None:
        self.header = std_msgs.msg.Header()
      if self.boxes is None:
        self.boxes = None
      end = 0
      _x = self
      start = end
      end += 12
      (_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs,) = _get_struct_3I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.header.frame_id = str[start:end].decode('utf-8', 'rosmsg')
      else:
        self.header.frame_id = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.boxes = []
      for i in range(0, length):
        val1 = spencer_tracking_msgs.msg.TrackedPerson2d()
        _x = val1
        start = end
        end += 32
        (_x.track_id, _x.person_height, _x.x, _x.y, _x.w, _x.h, _x.depth,) = _get_struct_Qf2i2If().unpack(str[start:end])
        self.boxes.append(val1)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_3I = None
def _get_struct_3I():
    global _struct_3I
    if _struct_3I is None:
        _struct_3I = struct.Struct("<3I")
    return _struct_3I
_struct_Qf2i2If = None
def _get_struct_Qf2i2If():
    global _struct_Qf2i2If
    if _struct_Qf2i2If is None:
        _struct_Qf2i2If = struct.Struct("<Qf2i2If")
    return _struct_Qf2i2If
