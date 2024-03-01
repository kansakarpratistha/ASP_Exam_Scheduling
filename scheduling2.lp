%get availabilites of different time duration of timeslots with an examiner assigned to each time slot based on the examiner's availability
availability(D,ST,ET,Eid,((ET/100)*60 + ET \ 100) - ((ST/100)*60 + ST \ 100)) :- timeslot(D,ST,ET), examinerschedule(Eid,D,ST1,ET1), 
ST >= ST1, ET1 >= ET.

%0 or 1 examination for checking purpose
0 {examination(D, ST, ET, Examiner, SID, M) : availability(D, ST, ET, Examiner, Dur), course(Course, Examiner)} :- student(SID, S, M), 
module(M, Dur, Course), studentCourses(SID, Course).
:- student(SID, _, _), EC = #count{Examiner: examination(_, _, _, Examiner, SID, _), course(Course, Examiner)}, CC = #count{Course: studentCourses(SID, Course)}, EC > 0, EC != CC.

%constraints to ensure a student doesn't have examinations on different timeslots
:- student(SID, S, M), examination(D1, ST1, ET1, _, SID, M), examination(D2, ST2, ET2, _, SID, M), D1 != D2.
:- student(SID, S, M), examination(D, ST1, ET1, _, SID, M), examination(D, ST2, ET2, _, SID, M), ST1 != ST2.

%constraints to ensure an examiner is not taking examination at the same timeslot for two different students
:- examination(D, ST, ET, Examiner, S1, _), examination(D, ST, ET, Examiner, S2, _), S1 !=S2.

unassigned(SID) :- student(SID, _, _), not examination(_, _, _, _, SID, _).

penalty(N) :- N = #count{SID : unassigned(SID)}.
#minimize{N:penalty(N)}.
