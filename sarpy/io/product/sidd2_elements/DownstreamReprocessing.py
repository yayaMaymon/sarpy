"""
The DownstreamReprocessingType definition.
"""

__classification__ = "UNCLASSIFIED"
__author__ = "Thomas McCullough"

import datetime
from typing import Union, List

import numpy

from sarpy.io.xml.base import Serializable, ParametersCollection
from sarpy.io.xml.descriptors import SerializableDescriptor, ParametersDescriptor, \
    StringDescriptor, DateTimeDescriptor, SerializableListDescriptor

from .base import DEFAULT_STRICT
from .blocks import RowColDoubleType, RowColIntType


class GeometricChipType(Serializable):
    """
    Contains information related to downstream chipping of the product. There is only one instance,
    and the instance is updated with respect to the **full image** parameters.

    For example, if an image is chipped out of a smaller chip, the new chip needs to be updated to
    the original full image corners. Since this relationship is linear, bi-linear interpolation is
    sufficient to determine an arbitrary chip coordinate in terms of the original full image coordinates.
    Chipping is typically done using an exploitation tool, and should not be done in the initial
    product creation.
    """

    _fields = (
        'ChipSize', 'OriginalUpperLeftCoordinate', 'OriginalUpperRightCoordinate',
        'OriginalLowerLeftCoordinate', 'OriginalLowerRightCoordinate')
    _required = _fields
    # Descriptor
    ChipSize = SerializableDescriptor(
        'ChipSize', RowColIntType, _required, strict=DEFAULT_STRICT,
        docstring='Size of the chipped product in pixels.')  # type: RowColIntType
    OriginalUpperLeftCoordinate = SerializableDescriptor(
        'OriginalUpperLeftCoordinate', RowColDoubleType, _required, strict=DEFAULT_STRICT,
        docstring='Upper-left corner with respect to the original product.')  # type: RowColDoubleType
    OriginalUpperRightCoordinate = SerializableDescriptor(
        'OriginalUpperRightCoordinate', RowColDoubleType, _required, strict=DEFAULT_STRICT,
        docstring='Upper-right corner with respect to the original product.')  # type: RowColDoubleType
    OriginalLowerLeftCoordinate = SerializableDescriptor(
        'OriginalLowerLeftCoordinate', RowColDoubleType, _required, strict=DEFAULT_STRICT,
        docstring='Lower-left corner with respect to the original product.')  # type: RowColDoubleType
    OriginalLowerRightCoordinate = SerializableDescriptor(
        'OriginalLowerRightCoordinate', RowColDoubleType, _required, strict=DEFAULT_STRICT,
        docstring='Lower-right corner with respect to the original product.')  # type: RowColDoubleType

    def __init__(self, ChipSize=None, OriginalUpperLeftCoordinate=None, OriginalUpperRightCoordinate=None,
                 OriginalLowerLeftCoordinate=None, OriginalLowerRightCoordinate=None, **kwargs):
        """

        Parameters
        ----------
        ChipSize : RowColIntType|numpy.ndarray|list|tuple
        OriginalUpperLeftCoordinate : RowColDoubleType|numpy.ndarray|list|tuple
        OriginalUpperRightCoordinate : RowColDoubleType|numpy.ndarray|list|tuple
        OriginalLowerLeftCoordinate : RowColDoubleType|numpy.ndarray|list|tuple
        OriginalLowerRightCoordinate : RowColDoubleType|numpy.ndarray|list|tuple
        kwargs
        """

        if '_xml_ns' in kwargs:
            self._xml_ns = kwargs['_xml_ns']
        if '_xml_ns_key' in kwargs:
            self._xml_ns_key = kwargs['_xml_ns_key']
        self.ChipSize = ChipSize
        self.OriginalUpperLeftCoordinate = OriginalUpperLeftCoordinate
        self.OriginalUpperRightCoordinate = OriginalUpperRightCoordinate
        self.OriginalLowerLeftCoordinate = OriginalLowerLeftCoordinate
        self.OriginalLowerRightCoordinate = OriginalLowerRightCoordinate
        super(GeometricChipType, self).__init__(**kwargs)


class ProcessingEventType(Serializable):
    """
    Processing event data.
    """

    _fields = ('ApplicationName', 'AppliedDateTime', 'InterpolationMethod', 'Descriptors')
    _required = ('ApplicationName', 'AppliedDateTime')
    _collections_tags = {'Descriptors': {'array': False, 'child_tag': 'Descriptor'}}
    # Descriptor
    ApplicationName = StringDescriptor(
        'ApplicationName', _required, strict=DEFAULT_STRICT,
        docstring='Application which applied a modification.')  # type: str
    AppliedDateTime = DateTimeDescriptor(
        'AppliedDateTime', _required, strict=DEFAULT_STRICT, numpy_datetime_units='us',
        docstring='Date and time defined in Coordinated Universal Time (UTC).')  # type: numpy.datetime64
    InterpolationMethod = StringDescriptor(
        'InterpolationMethod', _required, strict=DEFAULT_STRICT,
        docstring='Type of interpolation applied to the data.')  # type: Union[None, str]
    Descriptors = ParametersDescriptor(
        'Descriptors', _collections_tags, _required, strict=DEFAULT_STRICT,
        docstring='Descriptors for the processing event.')  # type: ParametersCollection

    def __init__(self, ApplicationName=None, AppliedDateTime=None, InterpolationMethod=None,
                 Descriptors=None, **kwargs):
        """

        Parameters
        ----------
        ApplicationName : str
        AppliedDateTime : numpy.datetime64|str
        InterpolationMethod : None|str
        Descriptors : None|ParametersCollection|dict
        kwargs
        """

        if '_xml_ns' in kwargs:
            self._xml_ns = kwargs['_xml_ns']
        if '_xml_ns_key' in kwargs:
            self._xml_ns_key = kwargs['_xml_ns_key']
        # use naive datetime because numpy warns about parsing timezone aware
        now = numpy.datetime64(datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None))
        self.ApplicationName = ApplicationName
        self.AppliedDateTime = now if AppliedDateTime is None else AppliedDateTime
        self.InterpolationMethod = InterpolationMethod
        self.Descriptors = Descriptors
        super(ProcessingEventType, self).__init__(**kwargs)


class DownstreamReprocessingType(Serializable):
    """
    Further processing after initial image creation.
    """

    _fields = ('GeometricChip', 'ProcessingEvents')
    _required = ()
    _collections_tags = {'ProcessingEvents': {'array': False, 'child_tag': 'ProcessingEvent'}}
    # Descriptor
    GeometricChip = SerializableDescriptor(
        'GeometricChip', GeometricChipType, _required, strict=DEFAULT_STRICT,
        docstring='')  # type: Union[None, GeometricChipType]
    ProcessingEvents = SerializableListDescriptor(
        'ProcessingEvents', ProcessingEventType, _collections_tags, _required, strict=DEFAULT_STRICT,
        docstring='')  # type: Union[None, List[ProcessingEventType]]

    def __init__(self, GeometricChip=None, ProcessingEvents=None, **kwargs):
        """

        Parameters
        ----------
        GeometricChip : None|GeometricChipType
        ProcessingEvents : None|List[ProcessingEventType]
        kwargs
        """

        if '_xml_ns' in kwargs:
            self._xml_ns = kwargs['_xml_ns']
        if '_xml_ns_key' in kwargs:
            self._xml_ns_key = kwargs['_xml_ns_key']
        self.GeometricChip = GeometricChip
        self.ProcessingEvents = ProcessingEvents
        super(DownstreamReprocessingType, self).__init__(**kwargs)
