
import os
import sys

api.load("sgtk")
import sys

import sgtk 
from tank_vendor import shotgun_api3
import getpass

class DDShotgunAPIError(object):
    def __init__(self, msg):
        raise shotgun_api3.shotgun.ShotgunError(msg)


class DDShotgun():
    def __init__(self):
        if os.environ["DD_OS"] == "cent7_64":
            self.sg = shotgun_api3.Shotgun("", "", "") # replace with your details
        else :
            self.sg = shotgun_api3.Shotgun(base_url="", script_name="", api_key="", http_proxy="") # replace with your details

        self.user = getpass.getuser()
        self.seq = None
        self.shot = None
        self.project = None
        self.asset = None
        self.step = None

    def sg_user(self,sg_user = None):
        try:
            if sg_user is None:
                sg_user = self.user
            id_user = self.sg.find_one("HumanUser", [["login", "is", sg_user ]], ["id"])
            id_user = id_user["id"]
        except Exception :
            DDShotgunAPIError("\n WHO ARE U ??")
        return id_user

    def sg_users(self):
        try:
            users = self.sg.find("HumanUser", [["sg_status_list", "is" , "act"]], ["login"])
        except Exception :
            DDShotgunAPIError("\n ISSUE ??")
        return users

    def sg_projects(self):
        id_user = self.sg_user()
        if id_user is not None:
            user = self.sg.find_one("HumanUser",[["id", "is",id_user]],["projects"])
            projects = user["projects"]
            return projects

    def sg_project(self):
        try:
            projects = self.sg.find("Project", [["sg_status", "is", "Active"]], ["name"])
        except Exception :
            DDShotgunAPIError("\n WHO ARE U ?? \n I CANT FIND YOUR Projects")
        return projects


    def sg_assets(self, project):
        try:
            if  project is not None:
                assets = self.sg.find("Asset", [["project.Project.name", "is", project]], ["code"])
        except Exception :
            DDShotgunAPIError("\n I CANT FIND THIS Project")
        return assets

    def sg_sequences(self,project):
        try:
            if  project is not None:
                sequences = self.sg.find("Sequence", [["project.Project.name", "is", project ]], ["code"])
        except Exception :
            DDShotgunAPIError("\n I CANT FIND THIS Project")
        return sequences

    def sg_shots(self,project,sequence):
        try:
            shots = self.sg.find("Shot", [['project.Project.name', 'is', project], ['sg_sequence.Sequence.code', 'is', sequence]], ["code"])
        except Exception as e :
            DDShotgunAPIError(e)
        return shots


    def sg_templates(self,template, fields):
        try:
            template_obj = sgtk.templates[template]
            template_obj.apply_fields(fields)
        except Exception as e :
            DDShotgunAPIError(e)
        return template_obj

    def sg_tasks(self, status=None):
        try:                
            user = self.sg_user()
            if status:
                filters = [["task_assignees", "is", {"type": "HumanUser", "id": user}],["sg_status_list", "is", status]]
            else:
                filters = [["task_assignees", "is", {"type": "HumanUser", "id": user}],{"filter_operator" : "any", "filters" : [["sg_status_list", "is", "ip"],["sg_status_list", "is", "kbk"], ["sg_status_list", "is", "rts"]]}]
            fields = ["sg_status_list","entity", "entity.Shot.sg_sequence" ,  "project","step"]
            task_assigned = self.sg.find("Task", filters, fields)
            task_assigned = task_assigned[::-1]
        except Exception as e :
            DDShotgunAPIError(e)
        return task_assigned

    def sg_task_project(self, idx):
        try:
            project = self.sg_tasks()[idx]["project"]["name"]
        except Exception as e :
            DDShotgunAPIError(e)
        return project    

    def sg_task_sequence(self, idx):
        try:
            if self.sg_tasks()[idx]["entity.Shot.sg_sequence"] is not None:
                self.seq = self.sg_tasks()[idx]["entity.Shot.sg_sequence"]["name"]
        except Exception as e :
            DDShotgunAPIError(e)
        if self.seq:
            return self.seq

    def sg_task_shot(self, idx):
        try:
            if self.sg_tasks()[idx]["entity"]["type"] == "Shot":
                self.shot = self.sg_tasks()[idx]["entity"]["name"]
        except Exception as e :
            DDShotgunAPIError(e)
        if self.shot:
            return self.shot

    def sg_task_asset(self, idx):
        try:
            if self.sg_tasks()[idx]["entity"]["type"]== "Asset":
                self.asset = self.sg_tasks()[idx]["entity"]["name"]
        except Exception as e :
            DDShotgunAPIError(e)
        if self.asset:
            return self.asset
    def sg_task_step(self, idx):
        try:
            if self.sg_tasks()[idx]["step"] is not None:
                step_key = self.sg_tasks()[idx]["step"]["name"]
                dd_steps = {"Roto":"roto","Paint":"paint", "Compositing":"comp", "Integration":"integ", "Modeling":"model", "Texturing":"texture", "Animation":"anim", "Lighting":"light", "Look Dev":"lookdev", "Rigging":"rig", "Effects":"fx", "TD":"td", "Vendor":"vendor"}
                self.step = dd_steps[step_key]
        except Exception as e :
            DDShotgunAPIError(e)
        return self.step

    def sg_task_status(self, idx):
        try:
            status = self.sg_tasks()[idx]["sg_status_list"]
        except Exception as e :
            DDShotgunAPIError(e)
        return status

    def sg_task_details(self, idx, status = None):
        try:
            if status != None:
                task = self.sg_tasks(status)[idx]
            else:
                task = self.sg_tasks()[idx]
            if task["entity"]["type"] == "Asset":
                self.asset = task["entity"]["name"]
                self.project = task["project"]["name"]
                step_key = task["step"]["name"]
                dd_steps = {"Roto":"roto","Paint":"paint", "Compositing":"comp", "Integration":"integ", "Modeling":"model", "Texturing":"texture", "Animation":"anim", "Lighting":"light", "Look Dev":"lookdev", "Rigging":"rig", "Effects":"fx", "TD":"td", "Vendor":"vendor"}
                self.step = dd_steps[step_key]
                print(f"go {self.project} {self.asset} ={self.step}")
            elif task["entity"]["type"]== "Shot":
                self.shot = task["entity"]["name"]
                self.seq = task["entity.Shot.sg_sequence"]["name"]
                self.project = task["project"]["name"]
                step_key = task["step"]["name"]
                dd_steps = {"Roto":"roto","Paint":"paint", "Compositing":"comp", "Integration":"integ", "Modeling":"model", "Texturing":"texture", "Animation":"anim", "Lighting":"light", "Look Dev":"lookdev", "Rigging":"rig", "Effects":"fx", "TD":"td", "Vendor":"vendor"}
                self.step = dd_steps[step_key]
                print(f"go {self.project} {self.seq} {self.shot} ={self.step}")
        except Exception as e :
            DDShotgunAPIError(e)

    def getFiles(self, template, show , user, seq = None, shot =None , step = None ):
        print(os.system("echo $DD_SHOW"))
        path = f""# your main shows DIR
        tk = sgtk.sgtk_from_path(path)
        work_files = tk.templates[template]
        paths_from_template = tk.paths_from_template(work_files, {"Sequence": seq , "Shot" : shot, "step" : step, "User": user})
        return paths_from_template
