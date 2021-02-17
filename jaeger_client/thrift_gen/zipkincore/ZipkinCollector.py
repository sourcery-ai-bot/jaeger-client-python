#
# Autogenerated by Thrift Compiler (0.9.3)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style,tornado
#
import six
from six.moves import xrange

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None

from tornado import gen
from tornado import concurrent
from thrift.transport import TTransport

class Iface(object):
  def submitZipkinBatch(self, spans):
    """
    Parameters:
     - spans
    """
    pass


class Client(Iface):
  def __init__(self, transport, iprot_factory, oprot_factory=None):
    self._transport = transport
    self._iprot_factory = iprot_factory
    self._oprot_factory = (oprot_factory if oprot_factory is not None
                           else iprot_factory)
    self._seqid = 0
    self._reqs = {}
    self._transport.io_loop.spawn_callback(self._start_receiving)

  @gen.coroutine
  def _start_receiving(self):
    while True:
      try:
        frame = yield self._transport.readFrame()
      except TTransport.TTransportException as e:
        for future in self._reqs.itervalues():
          future.set_exception(e)
        self._reqs = {}
        return
      tr = TTransport.TMemoryBuffer(frame)
      iprot = self._iprot_factory.getProtocol(tr)
      (fname, mtype, rseqid) = iprot.readMessageBegin()
      future = self._reqs.pop(rseqid, None)
      if not future:
        # future has already been discarded
        continue
      method = getattr(self, 'recv_' + fname)
      try:
        result = method(iprot, mtype, rseqid)
      except Exception as e:
        future.set_exception(e)
      else:
        future.set_result(result)

  def submitZipkinBatch(self, spans):
    """
    Parameters:
     - spans
    """
    self._seqid += 1
    future = self._reqs[self._seqid] = concurrent.Future()
    self.send_submitZipkinBatch(spans)
    return future

  def send_submitZipkinBatch(self, spans):
    oprot = self._oprot_factory.getProtocol(self._transport)
    oprot.writeMessageBegin('submitZipkinBatch', TMessageType.CALL, self._seqid)
    args = submitZipkinBatch_args()
    args.spans = spans
    args.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def recv_submitZipkinBatch(self, iprot, mtype, rseqid):
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = submitZipkinBatch_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "submitZipkinBatch failed: unknown result")


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {"submitZipkinBatch": Processor.process_submitZipkinBatch}

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name in self._processMap:
      return self._processMap[name](self, seqid, iprot, oprot)

    iprot.skip(TType.STRUCT)
    iprot.readMessageEnd()
    x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
    oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
    x.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()
    return

  @gen.coroutine
  def process_submitZipkinBatch(self, seqid, iprot, oprot):
    args = submitZipkinBatch_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = submitZipkinBatch_result()
    result.success = yield gen.maybe_future(self._handler.submitZipkinBatch(args.spans))
    oprot.writeMessageBegin("submitZipkinBatch", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES

class submitZipkinBatch_args(object):
  """
  Attributes:
   - spans
  """

  thrift_spec = (
    None, # 0
    (1, TType.LIST, 'spans', (TType.STRUCT,(Span, Span.thrift_spec)), None, ), # 1
  )

  def __init__(self, spans=None,):
    self.spans = spans

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1 and ftype == TType.LIST:
        self.spans = []
        (_etype17, _size14) = iprot.readListBegin()
        for _i18 in xrange(_size14):
          _elem19 = Span()
          _elem19.read(iprot)
          self.spans.append(_elem19)
        iprot.readListEnd()
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('submitZipkinBatch_args')
    if self.spans is not None:
      oprot.writeFieldBegin('spans', TType.LIST, 1)
      oprot.writeListBegin(TType.STRUCT, len(self.spans))
      for iter20 in self.spans:
        iter20.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.spans)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in six.iteritems(self.__dict__)]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class submitZipkinBatch_result(object):
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.LIST, 'success', (TType.STRUCT,(Response, Response.thrift_spec)), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0 and ftype == TType.LIST:
        self.success = []
        (_etype24, _size21) = iprot.readListBegin()
        for _i25 in xrange(_size21):
          _elem26 = Response()
          _elem26.read(iprot)
          self.success.append(_elem26)
        iprot.readListEnd()
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('submitZipkinBatch_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.LIST, 0)
      oprot.writeListBegin(TType.STRUCT, len(self.success))
      for iter27 in self.success:
        iter27.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.success)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in six.iteritems(self.__dict__)]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
