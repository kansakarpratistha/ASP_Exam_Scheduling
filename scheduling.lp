%get availabilites of different time duration of timeslots with an examiner assigned to each time slot based on the examiner's availability
%{availability(D, ST, ET, Eid, ((ET/100)*60 + ET \ 100) - ((ST/100)*60 + ST \ 100)) : examinerschedule(Eid, D, ST1, ET1), examiner(Eid, Name), ST >= ST1, ET1 >= ET} :- timeslot(D, ST, ET).
%{availability(D, ST, ET, Eid, ((ET/100)*60 + ET \ 100) - ((ST/100)*60 + ST \ 100)) : examinerschedule(Eid, D, ST1, ET1), examiner(Eid, Name), ST >= ST1, ET1 >= ET} :- timeslot(D, ST, ET).
availability(D,ST,ET,Eid,((ET/100)*60 + ET \ 100) - ((ST/100)*60 + ST \ 100)) :- timeslot(D,ST,ET), examinerschedule(Eid,D,ST1,ET1), ST >= ST1, ET1 >= ET.

%create examination with examiner assignment according to the module requirement
examination(D, ST, ET, Examiner, SID, M) : availability(D, ST, ET, Examiner, Dur), course(Course, Examiner) :- student(SID, S, M), module(M, Dur, Course), studentCourses(SID, Course).

%constraints to ensure a student doesn't have examinations on different timeslots
:- student(SID, S, M), examination(D1, ST1, ET1, _, SID, M), examination(D2, ST2, ET2, _, SID, M), D1 != D2.
:- student(SID, S, M), examination(D, ST1, ET1, _, SID, M), examination(D, ST2, ET2, _, SID, M), ST1 != ST2.

%constraints to ensure an examiner is not taking examination at the same timeslot for two different students
%:- examination(D, ST, ET, Examiner, S1, _), examination(D, ST, ET, Examiner, S2, _), S1 != S2.
:- examination(D, ST1, ET1, Examiner, S1, _), examination(D, ST2, ET2, Examiner, S2, _), ST1 == ST2, S1 !=S2.

%availability without choice rule, because we donot need to guess 12, 01pm