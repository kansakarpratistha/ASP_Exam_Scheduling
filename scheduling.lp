%get availabilites of different time duration of timeslots with an examiner assigned to each time slot based on the examiner's availability
availability(D,ST,ET,Eid,((ET/100)*60 + ET \ 100) - ((ST/100)*60 + ST \ 100)) :- timeslot(D,ST,ET), examinerschedule(Eid,D,ST1,ET1), ST >= ST1, ET1 >= ET.

%create examination with examiner assignment according to the module requirement
examination(D, ST, ET, Examiner, SID, M) : availability(D, ST, ET, Examiner, Dur), course(Course, Examiner) :- student(SID, S, M), module(M, Dur, Course), studentCourses(SID, Course).

%constraints to ensure a student doesn't have examinations on different timeslots
:- student(SID, S, M), examination(D1, ST1, ET1, _, SID, M), examination(D2, ST2, ET2, _, SID, M), D1 != D2.
:- student(SID, S, M), examination(D, ST1, ET1, _, SID, M), examination(D, ST2, ET2, _, SID, M), ST1 != ST2.

%constraints to ensure an examiner is not taking examination at the same timeslot for two different students
:- examination(D, ST, ET, Examiner, S1, _), examination(D, ST, ET, Examiner, S2, _), S1 !=S2.

%-----optimizations-----

%try to minimize assigning too many different exam dates for an examiner
assigned(Examiner, D) :- examination(D, _, _, Examiner, _, _).
penalty("DateStability", assigned(Examiner, N), (N-1)*5) :- examiner(Examiner, EName), N = {assigned(Examiner, Date)}, N > 1.
#minimize{P,C,S : penalty(S,C,P)}.

%minimize gaps between exam slots on same day for the examiner
assignedExamSlot(Examiner, D, ST, ET) :- examination(D, ST, ET, Examiner, _, _).
penalty("ExamSlotInterval", interval(Examiner, D, ST1, ET1, ST2 ,ET2), I*5) :- examiner(Examiner, EName), assignedExamSlot(Examiner, D, ST1, ET1), assignedExamSlot(Examiner, D, ST2, ET2), I = ((ST2/100)*60 + ST2 \ 100) - ((ET1/100)*60 + ET1 \ 100), I > 10.

%examiner combination stability
nextSlot(Examiner, D, ST1, ST2) :- examination(D, ST1, ET1, Examiner, _, _), examination(D, ST2, ET2, Examiner, _, _), ST2 > ET1, not existsBetween(Examiner, D, ST1, ST2).
existsBetween(Examiner, D, ST1, ST2) :- examination(D, ST1, ET1, Examiner, _, _), examination(D, ST2, ET2, Examiner, _, _), examination(D, ST, ET, Examiner, _, _), ST > ET1, ST2 > ET.

examinerSwitch(Examiner1, D, ST1, ST2, Examiner2, Examiner3) :- examination(D, ST1, ET2, Examiner1, Student1, _), examination(D, ST1, ET1, Examiner2, Student1, _), examination(D, ST2, ET2, Examiner1, Student2, _), examination(D, ST2, ET2, Examiner3, Student2, _), nextSlot(Examiner1, D, ST1, ST2).

penalty("ExaminerCombinationStability", examinerSwitch(Examiner, D, N), N*15) :- examiner(Examiner, EName), assigned(Examiner, D), N = {examinerSwitch(Examiner, D, ST1, ST2, E1, E2)}, N >= 1.

%minimize cases where examiner has only one examination for the day
sameDaySlots(Examiner, D, ST1, ST2) :- assignedExamSlot(Examiner, D, ST1, ET1), assignedExamSlot(Examiner, D, ST2, ET2), ST1 != ST2.
penalty("SingleSlot", singleslot(Examiner, N), N*10) :- examiner(Examiner, EName), N = {sameDaySlots(Examiner, D, ST1, ST2)}, N == 0.