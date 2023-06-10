#!/usr/bin/python3
import os
import output


def print_menu():
	print("You can choose to use your own script, or find CVEs:")
	for key in menu_options.keys():
		print(menu_options[key])




def ask_output(msg):
	save = 0
	while(True):
		try:
			answer = str(input(msg))
		except:
			print("\nWrong input. Please enter Y (yes) or N (no).")

		if (answer == "Y" or answer == "yes" or answer == "y"):
			save = 1
			break

		elif (answer == "N" or answer == "no" or answer == "n"):
			break

		else:
			print("Invalid input. Please enter Y (yes) or N (no)")

	return save


def ask_satisf(satisf, msg):
	while(True):
		try:
			answer = str(input(msg))
		except:
			print("\nWrong input. Please enter Y (yes) or N (no).")

		if (answer == "Y" or answer == "yes" or answer == "y"):
			satisf = True
			print(exit)
			break

		elif (answer == "N" or answer == "no" or answer == "n"):
			print("")
			satisf = False
			break

		else:
			print("\nInvalid input. Please enter Y (yes) or N (no)")
	return satisf



def runScript(script):
	sat = False

	result = os.popen('clingo '+script).read()

	if not "UNSATISFIABLE" in result:
		sat = True

	return result, sat


def getParamValue(param,script):

	value = 0
	check = "#const "+param+" = "
	check2 = "#const "+param+"= "
	check3 = "#const "+param+"="
	check4 = "#const "+param+" ="
	for i in range(40):
		if ( (check+str(i)) or (check2+str(i)) or (check3+str(i)) or (check4+str(i)) ) in script:
			value = i
			break
	
	return value


def getAllParams(script):
	f = open(script, "r")
	read_script = f.read()

	nb_apps_syst = getParamValue("as", read_script)

	nb_apps = getParamValue("a", read_script)
	nb_perms = getParamValue("p", read_script)
	nb_groups = getParamValue("g", read_script)
	nb_manifests = getParamValue("m", read_script)

	nb_actions = getParamValue("s", read_script)

	f.close()

	return nb_apps_syst, nb_apps, nb_perms, nb_groups, nb_manifests, nb_actions


def run_output(script, satisf):
	result, sat = runScript(script)
	nb_apps_syst, nb_apps, nb_perms, nb_groups, nb_manifests, nb_actions = 0, 0, 0, 0, 0, 0

	if sat:
		nb_apps_syst, nb_apps, nb_perms, nb_groups, nb_manifests, nb_actions = getAllParams(script)

		debug = ask_output("\nDo you want to debug? Enter Y (yes) or N (no): ")
		save = ask_output("\nDo you want to save the output in a file? Enter Y (yes) or N (no): ")

		if debug:
			result_parsed = output.parse_debug(result, nb_apps_syst, nb_apps, nb_perms, nb_groups, nb_manifests, nb_actions)
		
		else:
			result_parsed = output.parse_output(result, nb_apps_syst, nb_apps, nb_perms, nb_groups, nb_manifests, nb_actions)

		if save:
			f = open("output.txt", "w")
			f.write(result_parsed)
			f.close()

		else:
			print("\n" + result_parsed)


	else:
		print("\nModel: UNSATISFIABLE")

	satisf = ask_satisf(satisf, "\nHave you finished? Enter Y (yes) or N (no): ")
	return satisf








def run_bruteforce(script, satisf):

	bruteforce_script = "bruteforce.lp"


	start = "%------------- PARAMETERS -------------%"
	end = "%--------------------------------------%"


	# need to optimize that
	for aps in range(1):
		for a in range(2):
			for p in range(2):
				for m in range(3):
					for s in range(2,8):

						tryParams = "as=" + str(aps+1) + ", a=" + str(a+1) + ", p=" + str(p+1) + ", m=" + str(m+1) + ", s=" + str(s+1)
						print("Trying to solve with the following parameters: " + tryParams )

						appsyst = ("#const as = " + str(aps+1) + ".\n")
						permsyst = ("#const ps = as.\n")
						apps = ("#const a = " + str(a+1) + ".\n")
						perms = ("#const p = " + str(p+1) + ".\n")
						groups = ("#const g = p.\n")
						manifests = ("#const m = " + str(a+m+1) + ".\n")
						actions = ("#const s = " + str(s+1) + ".\n")

						# Read in the file
						with open(script) as infile, open(bruteforce_script,"w") as outfile:
							for line in infile:
								if line.strip() == start:
									outfile.write(line)
									outfile.write(appsyst)
									outfile.write(permsyst)
									outfile.write(apps)
									outfile.write(perms)
									outfile.write(groups)
									outfile.write(manifests)
									outfile.write(actions)
									break
								outfile.write(line)
							for line in infile:
								if line.strip() == end:
									outfile.write(line)
									break
							for line in infile:
								outfile.write(line)


						result, sat = runScript(bruteforce_script)
						if sat:

							print("\nI found a solution! The parameters are: " + tryParams)

							satisf = ask_output("\nDo you want the output? ")
							if not satisf:
								print(exit)
								return not satisf

							satisf = run_output(bruteforce_script,satisf)

							if satisf:
								return satisf
							
						
	return satisf




if __name__ == '__main__':

	menu_options = {
		1: "	1) Bruteforce my script!",
		2: "	2) Let's see the main script.",
		3: "	3) Let's see the CVE-2021-0307.",
		4: "	4) Let's see the CVE-2021-0317.",
		5: "	5) Let's see the CVE-2023-20947.",
		6: "	6) Exit\n",
	}

	satisf = False
	exit = "\nMay the Clingo be with you!"

	print("DroidSolver v1.0.1 - by @ghizmo\n")
	
	print("Hello DroidSolver!")


	while(not satisf):
		script = ""

		try:
			print_menu()
			option = int(input('Enter your choice: '))
		except:
			option = 0

		if option == 1:
			print("")
			try:
				script = str(input('Enter your script: '))
			except:
				script = "main.lp"
			satisf = run_bruteforce(script, satisf)
			
		elif option == 2:
			script = "main.lp"
			satisf = run_output(script, satisf)

		elif option == 3:
			script = "cve-2021-0307.lp"
			satisf = run_output(script, satisf)

		elif option == 4:
			script = "cve-2021-0317.lp"
			satisf = run_output(script, satisf)

		elif option == 5:
			script = "cve-2023-20947.lp"
			satisf = run_output(script, satisf)

		elif option == 6:
			print(exit)
			satisf = True

		else:
			print("\nInvalid option. Please enter a number between 1 and 4.\n")


