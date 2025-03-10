import os
import platform

system = platform.system()
username = os.getlogin()

jobs = { "JobResearchAssistant": "research assistant",
        "JobPsychologist": "psychologist",
        "JobChiefEngineer": "ce",
        "JobReporter": "reporter",
        "JobZookeeper": "zookeeper",
        "JobMedicalIntern": "med intern",
        "JobStationAi": "ai",
        "JobWarden": "warden",
        "JobBoxer": "boxer",
        "JobScientist": "sci",
        "JobStationEngineer": "engi",
        "JobSecurityOfficer": "sec off", 
        "JobMusician": "musician",
        "JobChaplain": "chaplain",
        "JobChef": "chef",
        "JobSalvageSpecialist": "savl",
        "JobChemist": "chem",
        "JobMedicalDoctor": "med doctor",
        "JobHeadOfSecurity": "hos",
        "JobTechnicalAssistant": "technical assistant",
        "JobResearchDirector": "rd",
        "JobMime": "mime",
        "JobParamedic": "paramed",
        "JobCaptain": "cap",
        "JobBorg": "cyborg",
        "JobCargoTechnician": "cargo tech",
        "JobHeadOfPersonnel": "hop",
        "JobServiceWorker": "service worker",
        "JobClown": "clown",
        "JobDetective": "det",
        "JobLawyer": "lawyer",
        "JobAtmosphericTechnician": "atmos",
        "JobBartender": "bartender",
        "JobBotanist": "botanist",
        "JobQuartermaster": "qm",
        "JobJanitor": "janitor",
        "JobPassenger": "passenger",
        "JobSecurityCadet": "sec cadet",
        "JobLibrarian": "librarian",
        "JobChiefMedicalOfficer": "cmo" }

overall = 0

account = input("SS14 account name: ")

if system == "Linux":
    path = "/home/" + username + "/.local/share/Space Station 14/data/roles/"
    file = open(path + account, "w")
else:
    path = "C:/Users/" + username + "/AppData/Roaming/Space Station 14/data/roles/"
    file = open(path + account, "w")

i = 0
for id, name in jobs.items():
    while True:
        inp = input("Time for " + name + " (eg. 30 47 for 30h 47m): ")

        inp = inp.split()

        if (len(inp) != 2):
            continue

        if (not inp[0].isdigit):
            continue

        if (not inp[1].isdigit):
            continue

        time = int(inp[0]) * 60
        time += int(inp[1])
        overall += time
        file.write("playtime_addrole " + account + " " + id +  " " + str(time) + "\n")
        i += 1
        break

file.write("playtime_addoverall " + account + " " + str(overall))
file.close()
