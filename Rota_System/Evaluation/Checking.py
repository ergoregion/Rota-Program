__author__ = 'Neil Butcher'

import CheckingAlgorithms


def priority(a):
    return a.priority


def CheckDuration(duration, population):
    events = duration.events
    appointments = duration.appointments()

    result = []

    result.extend(CheckingAlgorithms.MissingPersonCheck(appointments, population))
    result.extend(CheckingAlgorithms.UnqualifiedPersonCheck(appointments))
    result.extend(CheckingAlgorithms.BlacklistedDatePersonCheck(appointments))
    result.extend(CheckingAlgorithms.MultitaskingPersonCheck(events, 2))
    result.extend(CheckingAlgorithms.IncompatibleMultitaskingPersonCheck(events))
    result.extend(CheckingAlgorithms.MultipleOneDayAppointmentsPersonCheck(appointments, population))
    result.extend(CheckingAlgorithms.MultipleOneWeekAppointmentsPersonCheck(appointments, population))
    result.extend(CheckingAlgorithms.UnfilledAppointmentCheck(events))
    result.extend(CheckingAlgorithms.OverloadedPersonCheck(appointments, ratioLimit=0.3))
    result.extend(CheckingAlgorithms.OverloadedOneRolePersonCheck(appointments, ratioLimit=0.3))
    result.extend(CheckingAlgorithms.UnderusedPersonCheck(population, appointments))
    result.extend(CheckingAlgorithms.UnderusedOneRolePersonCheck(population, appointments))

    return sorted(result, key=priority, reverse=True)
