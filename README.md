# DroidSolver

DroidSolver tries to model the android permissions system and help to find vulnerabilities by a Solver approach, using Clingo.

## Usage

```
$ ./DroidSolver.py
DroidSolver v1.0.1 - by @ghizmo

Hello DroidSolver!
You can choose to use your own script, or find CVEs:
	1) Bruteforce my script!
	2) Let's see the main script.
	3) Let's see the CVE-2021-0307.
	4) Let's see the CVE-2021-0317.
	5) Let's see the CVE-2023-20947.
	6) Exit
```

## Tool

1) Choose the Clingo script
2) (Optional) Debugging
3) (Optional) Save the output in a file

## Files

- `main.lp` : main script that you can modify to perform your tests.
- `CVE-2023-20947.lp`: modelisation to perform the CVE-2023-20947.
- `cve-2021-0307.lp`: modelisation to perform the CVE-2021-0307.
- `cve-2021-0307.lp`: modelisation to perform the CVE-2021-0317.


## CVEs

### CVE-2021-0307

```
%-- keep a perm normal granted if we dont uninstall the app --%
granted(A,P,S+1) :- granted(A,P,S), perm(P,0,1,S+1), not uninstall(A,S), S<=s.

% if not dangerous keep granted to apps
granted(A,P,S+1) :- uninstall(A2,S), defPerm(A2,P,S), granted(A,P,S), not perm(P,_,2,S), A!=A2, S<=s.
```

### CVE-2021-0317

```
granted(A,P,S+1) :- not updateDangerousPerm(P,S), not uninstall(A,S), granted(A,P,S), installed(A,M,S), manifest(M,U,D), use(U,P), defPerm(_,P,S+1), S<=s.
granted(A,P,S+1) :- not updateDangerousPerm(P,S), not uninstall(A,S), granted(A,P,S), installed(A,M,S), manifest(M,U), use(U,P), defPerm(_,P,S+1), S<=s.
```


## Refs

- https://github.com/Ghizmoo/LeveragingAndroidPermissions
