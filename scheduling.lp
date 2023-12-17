%get availabilites of different time duration of timeslots with an examiner assigned to each time slot based on the examiner's availability
availability(D,ST, ET, Examiner, ET-ST) :- timeslot(D, ST, ET), examinerschedule(Examiner, D, ST1, ET1), ST >= ST1, ET1 >= ET.

%create exactly N number of examination, N is the number of examiners reqd for the module
N{examination(D, ST, ET, Examiner, S, M) : availability(D, ST, ET, Examiner, Dur)}N :- student(S, M), module(M, Dur, N).

%constraints to ensure a student doesn't have examinations on different timeslots
:- student(S, M), examination(D1, ST1, ET1, _, S, M), examination(D2, ST2, ET2, _, S, M), ST1 != ST2, ET1 != ET2.

%constraints to ensure an examiner is not taking examination at the same timeslot for two different students
:- examination(D, ST, ET, Examiner, S1, _), examination(D, ST, ET, Examiner, S2, _), S1 != S2.