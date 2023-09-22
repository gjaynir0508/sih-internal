# Input Format

The first line consists number of test cases - T
The second line consists of number of commands to be executed - N
The next N lines consists of commands to be executed
The commands are of the form:

- Adding Patients
  - `add-patient` - adds a patient to the default department (General diagnosis)
  - `add-patient dept` - adds a patient to the department dept
  - `add-patient dept doc` - adds a patient to the department dept to the doctor doc

- Doctor Presence and Absence
  - `doctor-in dept doc` - marks the doctor doc in the department dept as present
  - `doctor-out dept doc` - marks the doctor doc in the department dept as absent

- Session ending
  - `session-over dept doc` token - marks the session of the patient with token token in the department dept with the doctor doc as over
  - `session-over dept doc` - marks the session of the patient currently in the cabin in the department dept with the doctor doc as over
  - `session-over dept doc token` - marks the session of the patient with the tokenId token as over

- Estimating time
  - `estimate-time dept doc token` - returns the estimated time of the patient with token token in the department dept with the doctor doc

- Getting state
  - `get-state` - returns the entire state
  - `get-state dept` - returns the state of the department dept
  - `get-state dept doc` - returns the state of the doctor doc in the department dept

- Delays
  - `delay time` - delays execution of next command by time seconds

## Sample Input

```txt
1
9
add-patient
add-patient Cardiology
add-patient Cardiology doc4
get-state
estimate-time Cardiology doc3 token3
estimate-time Cardiology doc4 token6
session-over Cardiology doc3
session-over Cardiology doc4 token6
get-state
```
