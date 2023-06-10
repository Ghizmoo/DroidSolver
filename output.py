#!/usr/bin/python3


def parse_debug(result, nb_apps_syst, nb_apps, nb_perms, nb_groups, nb_manifests, nb_actions):

	output = ""





	output += ("-------------------------\n")
	output += ("Model: SATISFIABLE\n\n")

	output += (" ".join(["action("+str(s)+")" for s in range(1, nb_actions+1)]))

	output += ("\n\n----------------\n")





	output += ("Initial system:\n\n")

	for aps in range(1, nb_apps_syst+1):
		output += ("appSyst(" + str(aps) + ") manifSyst(" + str(aps) +") permSyst(" + str(aps) + "," + str(aps) + ",2)" + "\n")
		

		defPerm_string = ""
		installed_string = ""
		for s in range(nb_actions+1):
			defPerm_string += ("defPerm(" + str(aps) + "," + str(aps) + "," + str(s+1) + ") ")
			installed_string += ("installed(" + str(aps) + "," + str(aps) + "," + str(s+1) + ") ")

		output += (installed_string + "\n")
		output += (defPerm_string + "\n")

	output += ("\n----------------\n")








	output += ("System:\n\n")


	# ---------- APPS ---------- #
	appList = []
	for a in range(nb_apps_syst+1, nb_apps+nb_apps_syst+1):
		app = "app(" + str(a) + ")"
		if app in result:
			appList.append(app)

	if appList:
		output += (" ".join(appList)) + "\n"

	# ------------------------- #



	# ---------- Manifests ---------- #
	manifestList = []
	for m in range(nb_apps_syst, nb_apps_syst+ (2*nb_manifests)+1):
		for u in range(1,nb_apps_syst + nb_perms + 1):

			manifestUse = "manifest(" + str(m) + "," + str(u) + ")"

			if manifestUse in result:
				manifestList.append(manifestUse)

			for d in range(nb_apps_syst+1, nb_apps_syst + nb_perms + 1):


				manifestDef = "manifest(" + str(m) + "," + str(u) + "," + str(d) + ")"
				if manifestDef in result:
					manifestList.append(manifestDef)
	
	if manifestList:
		output += (" ".join(manifestList)) + "\n"

	# ------------------------------- #




	# ---------- usrP / use ---------- #
	def_list = []
	use_list = []
	permManifestInitial = []


	for p in range(0, nb_apps_syst+nb_perms+1):
		for u in range(1,nb_apps_syst + nb_perms + 1):

			use = ("use(" + str(u) + "," + str(p) + ")")
			if use in result:
				use_list.append(use)

		for d in range(nb_apps_syst, nb_apps_syst + nb_perms + 1):

			usrP = ("usrP(" + str(d) + "," + str(p) + ")")
			if usrP in result:
				def_list.append(usrP)

		for g in range(0, nb_apps_syst + nb_groups+1):
			for l in range(1,3):
				testPermManifest = ("permManifest("+ str(p) +","+ str(g) +","+ str(l) +",1)")
				if testPermManifest in result:
					permManifestInitial.append(testPermManifest)

	if def_list:
		output += (" ".join(def_list)) + "\n"

	if use_list:
		output += (" ".join(use_list)) + "\n"

	if permManifestInitial:
		output += (" ".join(permManifestInitial)) + "\n"




	# ------------------------------ #

	output += ("\n----------------\n")


	output += ("Actions performed:\n\n")



	action_list = []
	actions = ["install", "uninstall", "run", "stop", "grant", "grantAuto", "grantOneTime", "reboot", "update"]
	for s in range(1, nb_actions+1):

		for a in range(nb_apps_syst, nb_apps+nb_apps_syst+1):

			uninstallAction = (actions[1]+"("+str(a)+","+str(s)+")")
			if uninstallAction in result:
				action_list.append(uninstallAction)

			runAction = (actions[2]+"("+str(a)+","+str(s)+")")
			if runAction in result:
				action_list.append(runAction)

			stopAction = (actions[3]+"("+str(a)+","+str(s)+")")
			if stopAction in result:
				action_list.append(stopAction)

			for m in range(nb_apps_syst, nb_apps_syst+ (2*nb_manifests)+1):
				installAction = (actions[0]+"("+str(a)+","+str(m)+","+str(s)+")")
				if installAction in result:
					action_list.append(installAction)

				updateAction = (actions[8] + "(" + str(a) + "," + str(m) + "," + str(s) + ")")
				if updateAction in result:
					action_list.append(updateAction)

			for p in range(nb_apps_syst, nb_apps_syst+nb_perms+1):
				grantAction = (actions[4]+"("+str(a)+","+str(p)+","+str(s)+")")
				if grantAction in result:
					action_list.append(grantAction)

				grantAutoAction = (actions[5]+"("+str(a)+","+str(p)+","+str(s)+")")
				if grantAutoAction in result:
					action_list.append(grantAutoAction)

				grantOTAction = (actions[6]+"("+str(a)+","+str(p)+","+str(s)+")")
				if grantOTAction in result:
					action_list.append(grantOTAction)

		rebootAction = (actions[7] + "(" + str(s) + ")")
		if rebootAction in result:
			action_list.append(rebootAction)




	for s in range (len(action_list)):
		output += ("\t- " + action_list[s] + ":")

		permManifest_list = []
		perm_list = []
		defPerm_list = []
		installed_list = []
		running_list = []
		granted_list = []
		grantedOT_list = []
		grantAutoOK_list = []
		updateNormalToDangerousPerm_list = []
		updateDangerousPerm_list = []
		revokeGrant_list = []
		newPermManifest_list = []
		tryDefPerm_list = []
		multipleTry_list = []


		for a in range(nb_apps_syst+1, nb_apps+nb_apps_syst+1):
			for m in range(nb_apps_syst+1, nb_apps_syst+ (2*nb_manifests)+1):
				testInstalled = ("installed(" + str(a) + "," + str(m) + "," + str(s+2) + ")")
				if testInstalled in result:
					installed_list.append(testInstalled)

			testAppRunning = ("running(" + str(a) + "," + str(s+2) + ")")
			if testAppRunning in result:
				running_list.append(testAppRunning)

			for p in range(0, nb_apps_syst+nb_perms+1):
				testPermsDefined = ("defPerm(" + str(a) + "," + str(p) + "," + str(s+2) + ")")
				if testPermsDefined in result:
					defPerm_list.append(testPermsDefined)

				testPermsGranted = ("granted(" + str(a) + "," + str(p) + "," + str(s+2) + ")")
				if testPermsGranted in result:
					granted_list.append(testPermsGranted)

				testPermsOTGranted = ("grantedOneTime(" + str(a) + "," + str(p) + "," + str(s+1) + ")")
				if testPermsOTGranted in result:
					grantedOT_list.append(testPermsOTGranted)

				testRevokeGrant = ("revokeGrant(" + str(a) + "," + str(p) + "," + str(s+1) + ")")
				if testRevokeGrant in result:
					revokeGrant_list.append(testRevokeGrant)

				testTryDefPerm = ("tryDefPerm(" + str(a) + "," + str(p) + "," + str(s+2) + ")")
				if testTryDefPerm in result:
					tryDefPerm_list.append(testTryDefPerm)

				testGrantAutoOK = ("grantAutoOK(" + str(a) + "," + str(p) + "," + str(s+2) + ")")
				if testGrantAutoOK in result:
					grantAutoOK_list.append(testGrantAutoOK)


		for p in range(0, nb_apps_syst+nb_perms+1):
			testUpdateNormalToDangerousPerm = ("updateNormalToDangerousPerm(" + str(p) + "," + str(s+1) + ")")
			testUpdateDangerousPerm = ("updateDangerousPerm(" + str(p) + "," + str(s+1) + ")")
			testNewPermManifest = ("newPermManifest(" + str(p) + "," + str(s+2) + ")")
			testMultipleTry = ("multipleTry(" + str(p) + "," + str(s+1) + ")")

			if testUpdateNormalToDangerousPerm in result:
				updateNormalToDangerousPerm_list.append(testUpdateNormalToDangerousPerm)

			if testUpdateDangerousPerm in result:
				updateDangerousPerm_list.append(testUpdateDangerousPerm)

			if testNewPermManifest in result:
				newPermManifest_list.append(testNewPermManifest)

			if testMultipleTry in result:
				multipleTry_list.append(testMultipleTry)

			for g in range(0, nb_apps_syst + nb_groups+1):
				for l in range(1,3):
					testPermManifest = ("permManifest("+ str(p) +","+ str(g) +","+ str(l) +"," + str(s+2) + ")")
					if testPermManifest in result:
						permManifest_list.append(testPermManifest)

					testPerm = ("perm("+ str(p) +","+ str(g) +","+ str(l) +","+ str(s+2) +")")
					if testPerm in result:
						perm_list.append(testPerm)




		def output_add_list(listToAdd):
			outputList = ""
			if listToAdd:
				outputList += "\n\t\t"
				outputList += ("\n\t\t".join(listToAdd))
			return outputList

		output += output_add_list(revokeGrant_list)
		output += output_add_list(updateNormalToDangerousPerm_list)
		output += output_add_list(updateDangerousPerm_list)
		output += output_add_list(installed_list)
		output += output_add_list(newPermManifest_list)
		output += output_add_list(permManifest_list)
		output += output_add_list(perm_list)
		output += output_add_list(defPerm_list)
		output += output_add_list(tryDefPerm_list)
		output += output_add_list(multipleTry_list)
		output += output_add_list(running_list)
		output += output_add_list(granted_list)
		output += output_add_list(grantedOT_list)
		output += output_add_list(grantAutoOK_list)

		output += "\n\n"



	output += ("-------------------------")


	return output








def parse_output(result, nb_apps_syst, nb_apps, nb_perms, nb_groups, nb_manifests, nb_actions):

	output = ""

	output += ("-------------------------\n")
	output += ("Model: SATISFIABLE\n")

	# il faut que je dise à chaque instant S ce qu'il y a, definit par qui etc

	output += ("\nInitial system:")

	for i in range(nb_apps_syst):
		output += ("\tSystem App: "+str(i+1)+"\tDefine dangerous perm "+str(i+1)+", group: "+str(i+1)) + "\n"
	


	output += ("\nNb of Actions: "+ str(nb_actions))


	actions = ["install", "uninstall", "run", "stop", "grant", "grantAuto", "grantOneTime", "update", "reboot"]
	for s in range(1, nb_actions+1):

		output +=("\n\n----------------\n")

		action = ""
		test = ""

		test = (actions[8] + "(" + str(s) + ")")
		if test in result:
			action = test



		for a in range(nb_apps_syst, nb_apps+nb_apps_syst+1):

			test = (actions[1] + "(" + str(a) + "," + str(s) + ")")
			if test in result:
				action = test

			test = (actions[2] + "(" + str(a) + "," + str(s) + ")")
			if test in result:
				action = test

			test = (actions[3] + "(" + str(a) + "," + str(s) + ")")
			if test in result:
				action = test

			for m in range(nb_apps_syst, nb_apps_syst+ (2*nb_manifests)+1):
				test = (actions[0] + "(" + str(a) + "," + str(m) + "," + str(s) + ")")
				if test in result:
					action = test

				test = (actions[7] + "(" + str(a) + "," + str(m) + "," + str(s) + ")")
				if test in result:
					action = test

			for p in range(nb_apps_syst, nb_apps_syst+nb_perms+1):
				test = (actions[4] + "(" + str(a) + "," + str(p) + "," + str(s) + ")")
				if test in result:
					action = test

				test = (actions[5] + "(" + str(a) + "," + str(p) + "," + str(s) + ")")
				if test in result:
					action = test

				test = (actions[6] + "(" + str(a) + "," + str(p) + "," + str(s) + ")")
				if test in result:
					action = test


		if "uninstall" in action:
			output += ("Action " + str(s) + ": " + "uninstall app " + action[10] + "\n")

		elif "install" in action[:7]:
			output += ("Action " + str(s) + ": " + "install app " + action[8] +"\n")

		elif "run" in action:
			output += ("Action " + str(s) + ": " + "run app " + action[4] + "\n")

		elif "stop" in action:
			output += ("Action " + str(s) + ": " + "stop app " + action[5] + "\n")

		elif "grantAuto" in action:
			output += ("Action " + str(s) + ": " + "grant auto perm " + action[12] + " to app " + action[10] + "\n")

		elif "grantOneTime" in action:
			output += ("Action " + str(s) + ": " + "grant one-time perm " + action[15] + " to app " + action[13] + "\n")

		elif "grant" in action:
			output += ("Action " + str(s) + ": " + "grant perm " + action[8] + " to app " + action[6] + "\n")

		elif "update" in action:
			output += ("Action " + str(s) + ": " + "update app " + action[7] + "\n")

		else: #reboot
			output += ("Action " + str(s) + ": " + "reboot phone\n")



		#for a in range(nb_apps_syst, nb_apps+nb_apps_syst+1):

			#installed = "installed("+str(a)+","+str(m)
		

		output += ("\nCurrent environment of the system:")

		

		output += ("\n\t- Manifests:")

		appsInstalled = []

		for a in range(nb_apps_syst+1, nb_apps+nb_apps_syst+1):
			for m in range(nb_apps_syst, nb_apps_syst+ (2*nb_manifests)+1):

				# check if installed(A,M,S) exists
				test = ( "installed(" + str(a) + "," + str(m) + "," + str(s+1) + ")" )

				# if that is the case
				if test in result:

					appsInstalled.append(str(a))

					for u in range(1,nb_apps_syst + nb_perms + 1):

						# check if manifest(M,U) exists
						testManifestUse = ( "manifest(" + str(m) + "," + str(u) + ")")

						# if that is the case
						if testManifestUse in result:

							use_list = []

							for p in range(0, nb_apps_syst+nb_perms+1):

								use = ("use(" + str(u) + "," + str(p) + ")")
								if use in result:
									use_list.append(str(p))


							output += ("\n\t\tApp " + str(a) + ": Manifest use perm " + (", ".join(use_list)))

						

					# check if manifest(M,U,D) exists
					def_list = []
					use_list = []
					for d in range(nb_apps_syst, nb_apps_syst + nb_perms + 1):
						for u in range(1,nb_apps_syst + nb_perms +1):
							testManifestDef = ( "manifest(" + str(m) + "," + str(u) + "," + str(d) + ")")

							# if that is the case
							if testManifestDef in result:

								for p in range(0, nb_apps_syst + nb_perms + 1):
									use = ("use(" + str(u) + "," + str(p) + ")")
									usrP = ("usrP(" + str(d) + "," + str(p) + ")")

									if (use in result) and ( not (str(p) in use_list)) :
										use_list.append(str(p))

									if usrP in result:
										def_list.append(str(p))

					if def_list and use_list:
						output += ("\n\t\tApp " + str(a) + ": Manifest use perm " + (", ".join(use_list)) + " and defines perm " + (", ".join(def_list)))



		output += ("\n\n\t- Perms in the manifest:\n")
		for p in range(nb_apps_syst+1, nb_apps_syst + nb_perms + 1):
			for g in range(0, nb_apps_syst + nb_groups + 1):
				group = "not grouped"
				for l in range(1,3):
					permLevel = ""
					permManifest = ("permManifest(" + str(p) + "," + str(g) + "," + str(l) + "," + str(s+1) + ")")
					if permManifest in result:
						if l == 1:
							permLevel = "normal"
						if l == 2:
							permLevel = "dangerous"
							if g!= 0:
								group = "grouped with group " + str(g)

						output += ("\t\tPerm " + str(p) + ": " + permLevel + " and " + group + "\n")





		output += ("\n\t- Perms defined:")
		for a in range(nb_apps_syst+1, nb_apps+nb_apps_syst+1):
			for p in range(nb_apps_syst+1, nb_apps_syst + nb_perms + 1):
				testPermsDefined = ("defPerm(" + str(a) + "," + str(p) + "," + str(s+1) + ")")
				if testPermsDefined in result:
					output += ("\n\t\tPerm " + str(p) + " defined by app " + str(a))
				

		output += ("\n\n\t- Perms registered:\n")

		
		for p in range(nb_apps_syst, nb_apps_syst+nb_perms+1):
			for a in range(nb_apps_syst+1, nb_apps+nb_apps_syst+1):

				testPermsDefined = ("defPerm(" + str(a) + "," + str(p) + "," + str(s+1) + ")")
				if testPermsDefined in result:

					for g in range(0, nb_apps_syst + nb_groups + 1):

						group = "not grouped"

						for l in range(1,3):

							permLevel = ""

							test = ("perm("+ str(p) +","+ str(g) +","+ str(l) +","+ str(s+1) +")")
							if test in result:
								if l == 1:
									permLevel = "normal"
								if l == 2:
									permLevel = "dangerous"
									if g != 0:
										group = "grouped with group " + str(g)

								output += ("\t\tPerm " + str(p) + ": " + permLevel + " and " + group + "\n")



		output += ("\n\nCurrent state of the system:")

		output += ("\n\t- Apps installed: " + (", ".join(appsInstalled)))


		appRunning = []
		for a in range(nb_apps_syst+1, nb_apps+nb_apps_syst+1):
			testAppRunning = ("running(" + str(a) + "," + str(s+1) + ")")
			if testAppRunning in result:
				appRunning.append(str(a))

		output += ("\n\n\t- Apps running: " + (", ".join(appRunning)))

		output += ("\n\n\t- Perms granted:")
		for a in range(nb_apps_syst+1, nb_apps+nb_apps_syst+1):
			permsGranted = []
			for p in range(0, nb_apps_syst + nb_perms + 1):
				testPermsGranted = ("granted(" + str(a) + "," + str(p) + "," + str(s+1) + ")")
				if testPermsGranted in result:
					permsGranted.append(str(p))

			if permsGranted:
				output += ("\n\t\tApp " + str(a) + ": perm " + (", ".join(permsGranted)) + " granted")


		if "grantOneTime" in result:
			output += ("\n\n\t- Perms granted one-time:")
			for a in range(nb_apps_syst+1, nb_apps+nb_apps_syst+1):
				permsGrantedOneTime = []
				for p in range(0, nb_apps_syst + nb_perms + 1):
					testPermsGrantedOT = ("grantedOneTime(" + str(a) + "," + str(p) + "," + str(s+1) + ")")
					if testPermsGrantedOT in result:
						permsGrantedOneTime.append(str(p))

				if permsGrantedOneTime:
					output += ("\n\t\tApp " + str(a) + ": perm " + (", ".join(permsGrantedOneTime)) + " granted one-time")



	output += ("\n\n-------------------------\n")

	return output
