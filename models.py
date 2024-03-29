"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown),
    and whether it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(
        self, designation, name=None, diameter=float('nan'),
            hazardous=False):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments
        supplied to the constructor.
        """
        self.designation = str(designation)
        self.name = str(name) if name else None
        self.diameter = float(diameter) if diameter else float('nan')
        self.hazardous = True if hazardous == 'Y' else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self.designation} {self.name}'

    def __str__(self):
        """Return `str(self)`."""
        return (f"A NearEarthObject {self.fullname} has a diameter of "
                f"{self.diameter:.3f} km and is potentially "
                f"hazardous = {self.hazardous}")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string.

        representation of this object.
        """
        return (f"NearEarthObject(designation={self.designation!r},"
                f"name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """Return a dictionary of all essential keywords of a NEO's object.

        with their corresponding values defined in the class constructor
        __init__.
        This dictionary is later used to write into CSV/JSON
        output file. Essential keyword for a NEO object are :
        name, designation, diameter_km, potentially_hazardous.
        """
        neo_dict = dict()
        if(self.name is None):
            neo_dict['name'] = ''

        else:
            neo_dict['name'] = "{neo_name}".format(neo_name=self.name)
        neo_dict['designation'] = "{des}".format(des=self.designation)
        neo_dict['diameter_km'] = self.diameter
        neo_dict['potentially_hazardous'] = self.hazardous
        return neo_dict


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach,
    the nominal approach distance in astronomical units, and the relative
    approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(
        self, time, distance=float('nan'), velocity=float('nan'),
            neo=None, designation=None):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments
        supplied to the constructor.
        """
        self._designation = str(designation) if designation else ''
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s.

        approach time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation,
        the default representation includes seconds - significant
        figures that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (f"At {self.time_str}, '{self._designation}' "
                f"approaches Earth at a distance of {self.distance:.2f} au"
                f"and a velocity of {self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable.

        string representation of this object.
        """
        return (f"CloseApproach(time={self.time_str!r}, "
                "distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """Return a dictionary of all essential.

        keywords of a NEO's close approach object with their
        corresponding values defined in the class constructor __init__.

        This dictionary is later used to write into CSV/JSON output file.
        Essential keyword for a NEO object are :
        datetime_utc,distance_au,velocity_km_s.
        """
        approach_dict = dict()
        approach_dict['datetime_utc'] = "{date_time}".format(
            date_time=self.time_str)
        approach_dict['distance_au'] = self.distance
        approach_dict['velocity_km_s'] = self.velocity
        return approach_dict
