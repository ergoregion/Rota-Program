__author__ = 'Neil Butcher'

from collections import Counter
from Rota_System.StandardTimes import time_string, date_string
from datetime import timedelta


def person(a):
    return a.person


def role(a):
    return a.role


class CheckInformation(object):
    def __init__(self, text):
        self.text = text
        self.color = 'green'
        self.priority = 2


class CheckConcern(object):
    def __init__(self, text):
        self.text = text
        self.color = 'yellow'
        self.priority = 4


class CheckWarning(object):
    def __init__(self, text):
        self.text = text
        self.color = 'orange'
        self.priority = 6


class CheckError(object):
    def __init__(self, text):
        self.text = text
        self.color = 'red'
        self.priority = 8


def MissingPersonCheck(appointments, population):
    l = []
    for a in appointments:
        if a.is_filled():
            if not (a.person in population):
                error = CheckError(
                    'The person, ' + a.person.name + ' is scheduled for ' + a.role.description + ' on ' + str(
                        a.date) + ' but does not exist')
                l.append(error)
    return l


def UnqualifiedPersonCheck(appointments):
    l = []
    for a in appointments:
        if a.is_filled():
            if not a.person.suitable_for_role(a.role):
                error = CheckError(
                    'The person, ' + a.person.name + ' is scheduled for ' + a.role.description + ' on ' + date_string(
                        a.date) + ' but is not qualified as a ' + a.role.description)
                l.append(error)
    return l


def BlacklistedDatePersonCheck(appointments):
    l = []
    for a in appointments:
        if a.is_filled():
            if not a.person.is_available_on_date(a.date):
                error = CheckError(
                    'The person, ' + a.person.name + ' is scheduled for ' + a.role.description + ' on ' + date_string(
                        a.date) + ' but is not available on that date')
                l.append(error)
    return l


def MultitaskingPersonCheck(events, appointmentsWarningLimit):
    l = []
    for e in events:
        c = Counter(map(person, e.appointments))
        for p in c:
            if p and c[p] > appointmentsWarningLimit:
                error = CheckWarning('The person, ' + p.name + ' is scheduled for ' + str(
                        c[p]) + ' appointments during the same event (' + e.name + date_string(e.date) + time_string(
                    e.time) + ')')
                l.append(error)
            elif p and c[p] > 1:
                error = CheckInformation('The person, ' + p.name + ' is scheduled for ' + str(
                        c[p]) + ' appointments during the same event (' + e.name + date_string(e.date) + time_string(
                    e.time) + ')')
                l.append(error)
    return l


def IncompatibleMultitaskingPersonCheck(events):
    l = []
    for e in events:
        a = list(e.appointments)
        b = list(e.appointments)
        for appointment in a:
            b.remove(appointment)
            for otherAppointment in b:
                if appointment.is_filled() and appointment.person == otherAppointment.person and not appointment.role.compatible_with(
                        otherAppointment.role):
                    error = CheckError(
                        'The person, ' + appointment.person.name + ' is scheduled for conflicting appointments during the same event (' + e.name + date_string(
                            e.date) + time_string(e.time) + ')')
                    l.append(error)

    return l


def MultipleProximalAppointmentsPersonCheck(appointments, population, permittedTimedelta):
    l = []
    for p in population:
        pAppointments = filter(lambda a: a.person == person, appointments)
        remainingPAppointments = set(pAppointments)
        for appointment in pAppointments:
            remainingPAppointments.remove(appointment)
            proximalAppointments = filter(lambda a: abs(a.datetime - appointment.datetime) <= permittedTimedelta,
                                          remainingPAppointments)
            for app in proximalAppointments:
                warning = CheckWarning(
                    'The person, ' + p.name + ' has 2 oppointments within a short timescale (one of them is' + appointment.role + date_string(
                        appointment.date) + time_string(appointment.time) + ') the other is (' + app.role + date_string(
                        app.date) + time_string(app.time) + +') within ' + str(permittedTimedelta))
                l.append(warning)

    return l


def MultipleOneDayAppointmentsPersonCheck(appointments, population):
    return MultipleProximalAppointmentsPersonCheck(appointments, population, timedelta(days=1))


def MultipleOneWeekAppointmentsPersonCheck(appointments, population):
    return MultipleProximalAppointmentsPersonCheck(appointments, population, timedelta(days=7))


def UnfilledAppointmentCheck(events):
    l = []
    for e in events:
        a = list(e.appointments)
        for appointment in a:
            if not appointment.is_filled() and not appointment.disabled:
                error = CheckError(
                    'The appointment, ' + appointment.role.description + ' is unfilled during the event (' + e.name + date_string(
                        e.date) + time_string(e.time) + ')')
                l.append(error)

    return l


def OverloadedPersonCheck(appointments, absLimit=1e8, ratioLimit=1.01):
    l = []
    totalNumber = len(appointments)
    c = Counter(map(person, appointments))
    for p, count in c.most_common(100):
        if p and (count > absLimit or (count / totalNumber) > ratioLimit):
            w = CheckWarning(p.name + ' is doing ' + str(count) + ' appointments out of ' + str(totalNumber))
            l.append(w)
    return l


def OverloadedOneRolePersonCheck(appointments, absLimit=1e8, ratioLimit=1.01):
    l = []
    roles = set(map(role, appointments))
    for r in roles:
        rAppointments = filter(lambda a: a.role == r, appointments)
        totalNumber = len(rAppointments)
        c = Counter(map(person, rAppointments))
        for p, count in c.most_common(100):
            if p and (count > absLimit or (count / totalNumber) > ratioLimit):
                w = CheckWarning(
                    p.name + ' is doing ' + r.description + ' ' + str(count) + ' times out of ' + str(totalNumber))
                l.append(w)
    return l


def UnderusedPersonCheck(population, appointments, absLimit=0, ratioLimit=0):
    l = []
    totalNumber = len(appointments)
    c = Counter(map(person, appointments))
    for p in population:
        if c[p] == 0:
            w = CheckWarning(p.name + ' is not taking on any appointments')
            l.append(w)
        elif c[p] < absLimit or (c[p] / totalNumber) < ratioLimit:
            w = CheckWarning(p.name + ' is only doing ' + str(c[p]) + ' appointments')
            l.append(w)
    return l


def UnderusedOneRolePersonCheck(population, appointments, absLimit=0, ratioLimit=0):
    l = []
    c = Counter(map(role, appointments))
    for p in population:
        pAppointments = filter(lambda a: a.person == p, appointments)
        for r in p.roles():
            rAppointments = filter(lambda a: a.role == r, pAppointments)
            if len(rAppointments) == 0:
                w = CheckWarning(p.name + ' is not taking on any ' + r.description + ' appointments')
                l.append(w)
            elif len(rAppointments) < absLimit or (len(rAppointments) / c[r]) < ratioLimit:
                w = CheckWarning(p.name + ' is only doing ' + r.description + ' ' + str(c[p]) + ' times')
                l.append(w)
    return l
