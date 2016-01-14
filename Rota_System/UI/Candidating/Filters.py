__author__ = 'Neil Butcher'

from sets import Set
from datetime import timedelta


class PersonFilterNobody(object):
    def __init__(self, appointment):
        pass

    def transmit(self, person):
        return False

    def mask(self, person):
        return True


class PersonFilterQualifiedForAppointment(object):
    def __init__(self, appointment):
        self._appointment = appointment

    def transmit(self, person):
        return person.suitable_for_role(self._appointment.role)

    def mask(self, person):
        return not person.suitable_for_role(self._appointment.role)


class PersonFilterAvailableForAppointment(object):
    def __init__(self, appointment):
        self._appointment = appointment

    def transmit(self, person):
        return person.is_available_on_date(self._appointment.date)

    def mask(self, person):
        return not person.is_available_on_date(self._appointment.date)


class PersonFilterHasClashingAppointmentInEvent(object):
    def __init__(self, appointment):
        self._role = appointment.role
        self._event = appointment.event

    def transmit(self, person):
        for a in self._event.appointments:
            if a.person == person and not a.role.compatible_with(self._role):
                return True
        return False

    def mask(self, person):
        return not self.transmit(person)

    def appointments(self, person):
        return filter(self._event.appointments,
                      key=lambda a: a.person == person and not a.role.compatible_with(self._role))


class PersonFilterHasAppointmentInEvent(object):
    def __init__(self, event):
        self._event = event

    def transmit(self, person):
        for a in self._event.appointments:
            if a.person == person:
                return True
        return False

    def mask(self, person):
        return not self.transmit(person)

    def appointments(self, person):
        return filter(self._event.appointments, key=lambda a: a.person == person)


class PersonFilterOccupiedDuringAppointment(object):
    def __init__(self, appointment, events, timescaleDurationHours=4):
        self._appointment = appointment
        self._events = events
        self._typicalDuration = timedelta(hours=timescaleDurationHours)
        self._allAppointmentsCache = None
        self._coincidentAppointmentsCache = None
        self._incompatibleAppointmentsCache = None

    def _coincident_events(self):
        return filter(self._events, key=lambda e: (e.datetime - self._appointment.datetime) < self._typicalDuration)

    def _appointments(self):
        if self._allAppointmentsCache:
            return self._allAppointmentsCache
        all_appointments_cache = Set()
        for e in self._events:
            all_appointments_cache.update(e.appointments)
        self._allAppointmentsCache = sorted(all_appointments_cache, key=lambda app: app.datetime)
        return self._allAppointmentsCache

    def _coincident_appointments(self):
        if self._coincidentAppointmentsCache:
            return self._coincidentAppointmentsCache
        _coincidentAppointmentsCache = Set()
        for e in self._coincident_events():
            _coincidentAppointmentsCache.update(e.appointments)
        self._coincidentAppointmentsCache = sorted(_coincidentAppointmentsCache, key=lambda app: app.datetime)
        return self._coincidentAppointmentsCache

    def _incompatible_appointments(self):
        if self._incompatibleAppointmentsCache:
            return self._incompatibleAppointmentsCache
        _incompatibleAppointmentsCache = Set()
        for a in self._coincident_appointments():
            if not a.role.compatibleWith(self._appointment.role):
                _incompatibleAppointmentsCache.add(a)
            elif not self._appointment.role.compatibleWith(a.role):
                _incompatibleAppointmentsCache.add(a)
        self._incompatibleAppointmentsCache = sorted(_incompatibleAppointmentsCache, key=lambda app: app.datetime)
        return self._incompatibleAppointmentsCache

    def transmit(self, person):
        for a in self._incompatible_appointments():
            if a.person == person:
                return True
        return False

    def mask(self, person):
        return not self.transmit(person)

    def existingCoincidentAppointmentsOfPerson(self, person):
        return filter(lambda x: x.person == person, self._appointments())

    def existingIncompatibleAppointmentsOfPerson(self, person):
        return filter(lambda x: x.person == person, self._incompatible_appointments())
