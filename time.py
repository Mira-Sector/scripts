import os
import platform

system = platform.system()
username = os.getlogin()

jobs = ["atmos", "bartender", "botanist", "cap", "cargo tech", "chaplain", "chef", "chem", "ce", "cmo", "clown", "borg", "detective", "hop", "hos", "janitor", "lawyer", "librarian", "med doctor", "med intern", "mime", "musician", "paramed", "passenger", "psycologist", "qm", "reporter", "research assistant", "rd", "salvage", "scientist", "sec cadet", "sec off", "service worker", "engi", "technical assistant", "warden", "boxer", "zookeeper"]
jobId = ["JobAtmosphericTechnician", "JobBartender", "JobBorg", "JobBotanist", "JobCaptain", "JobCargoTechnician", "JobChaplain", "JobChef", "JobChemist", "JobChiefEngineer", "JobChiefMedicalOfficer", "JobClown", "JobDetective", "JobHeadOfPersonnel", "JobHeadOfSecurity", "JobJanitor", "JobLawyer", "JobLibrarian", "JobMedicalDoctor", "JobMedicalIntern", "JobMime", "JobMusician", "JobPassenger", "JobParamedic", "JobPsychologist", "JobQuartermaster", "JobReporter", "JobResearchAssistant", "JobResearchDirector", "JobSalvageSpecialist", "JobScientist", "JobSecurityCadet", "JobSecurityOfficer", "JobServiceWorker", "JobStationEngineer", "JobTechnicalAssistant", "JobWarden", "JobBoxer", "JobZookeeper"]

overall = 0

account = input("SS14 account name: ")

if system == "Linux":
    path = "/home/" + username + "/.local/share/Space Station 14/data/roles/"
    file = open(path + account, "w")
else:
    path = "C:/Users/" + username + "/AppData/Roaming/Space Station 14/data/roles/"
    file = open(path + account, "w")

i = 0
for x in jobs:
    inp = input("Time for " + x + " (eg. 30 47 for 30h 47m): ")
    inp = [int(i) for i in inp.split() if i.isdigit()]
    time = inp[0] * 60
    time += inp[1] * 3600
    overall += time
    file.write("playtime_addrole " + account + " " + jobId[i] +  " " + str(time) + "\n")
    i += 1

file.write("playtime_addoverall " + account + " " + str(overall))
file.close()
