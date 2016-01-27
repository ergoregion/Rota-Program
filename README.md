## Rota-Program

A desktop application to record save, review, and optimise the use of manpower across a number of tasks and different events.

It was written to address the difficulty of a church where many people were capable of fulfilling a number of the requirement but not at the same time.
It could equally be applied to other situations where the same people may be expected in a range of tasks with the risk of clashes.

#Key features
-quickly find a candidate for a task from a population given qualification, availability and other committments
-produce reports personalised to individuals and occasions
-option to (attempt to) fill every task automatically given the workers

#Details
Written in Python with a pyqt UI.
Some of the key classes are

-Role:		the nature of a task to be performed (such as "cook" or "waiter")
-Worker:	a person qualified for one or more roles and with some avaialability
-Event:		a time session with a date and start time (such as a work-day, lesson or a meeting)
-Appointment:	a task to do during the whole of an event, classified by its role
-Duration:		a collection of events across a range of dates (such as 1st-quarter or spring-term)
-Institution:	a population of people, and events sorted into durations

