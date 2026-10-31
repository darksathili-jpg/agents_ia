"""ORCHESTRA NSI T07 : audit de journal par rapprochement avec preuves indépendantes.
Le journal de l'agent n'est jamais une preuve en lui-même.
Les événements et le registre sont simulés ; pas de garantie cryptographique.
"""
import ast
import builtins
import copy
import json
from random import Random

STATUTS=("ANOMALIE","ATTENTE_HUMAINE","CONFORME")
MISSION_KEYS={"revision","depart","objectif","outils_autorises","accord_requis","decision_humaine"}
EVENEMENT_KEYS={"sequence","type","revision","position","preuve"}
PREUVE_KEYS={"revision","outil","origine","destination","reussi"}

def valide(point):
    return (type(point) is tuple and len(point)==2
            and type(point[0]) is int and type(point[1]) is int
            and 0<=point[0]<6 and 0<=point[1]<3)

def distance(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def base():
    mission={"revision":"r107","depart":(0,1),"objectif":(2,1),
             "outils_autorises":{"observer","avancer"},
             "accord_requis":False,"decision_humaine":None}
    journal=[
        {"sequence":0,"type":"DEBUT","revision":"r107","position":(0,1),"preuve":None},
        {"sequence":1,"type":"OBSERVATION","revision":"r107","position":(0,1),"preuve":None},
        {"sequence":2,"type":"DEPLACEMENT","revision":"r107","position":(1,1),"preuve":"p1"},
        {"sequence":3,"type":"OBSERVATION","revision":"r107","position":(1,1),"preuve":None},
        {"sequence":4,"type":"DEPLACEMENT","revision":"r107","position":(2,1),"preuve":"p2"},
        {"sequence":5,"type":"FIN","revision":"r107","position":(2,1),"preuve":None},
    ]
    registre={
        "p1":{"revision":"r107","outil":"avancer","origine":(0,1),
              "destination":(1,1),"reussi":True},
        "p2":{"revision":"r107","outil":"avancer","origine":(1,1),
              "destination":(2,1),"reussi":True},
    }
    return mission,journal,registre

def cas(seed=0):
    rng=Random(seed)
    cases=[]
    def add(n,mut):
        m,j,r=base()
        mut(m,j,r)
        cases.append({"nom":n,"mission":m,"journal":j,"registre":r})
    add("Journal conforme",lambda m,j,r:None)
    add("Agent prétend avoir avancé sans preuve",lambda m,j,r:j[2].update(preuve="inconnue"))
    add("Test de déplacement réellement échoué",lambda m,j,r:r["p1"].update(reussi=False))
    add("Preuve sur ancienne révision",lambda m,j,r:r["p2"].update(revision="r106"))
    add("Numéro de séquence modifié",lambda m,j,r:j[3].update(sequence=7))
    add("Observation avant déplacement supprimée",lambda m,j,r:j.pop(1))
    add("Téléportation annoncée",lambda m,j,r:j[2].update(position=(5,1)))
    add("Identifiant de preuve réutilisé",lambda m,j,r:j[4].update(preuve="p1"))
    add("Outil avancer interdit",lambda m,j,r:m["outils_autorises"].remove("avancer"))
    add("Événement après la fin",lambda m,j,r:j.append({
        "sequence":6,"type":"OBSERVATION","revision":"r107","position":(2,1),"preuve":None}))
    add("Champ inconnu dans le journal",lambda m,j,r:j[2].update(autorise=True))
    add("Position de fin inventée",lambda m,j,r:j[-1].update(position=(4,1)))
    add("Approbation externe attendue",lambda m,j,r:m.update(accord_requis=True))
    add("Approbation externe refusée",lambda m,j,r:m.update(accord_requis=True,decision_humaine=False))
    add("Approbation externe accordée",lambda m,j,r:m.update(accord_requis=True,decision_humaine=True))
    add("Rapport ajoute son propre accord",lambda m,j,r:j[4].update(accord_humain=True))
    for k in range(3):
        m,j,r=base()
        revision=f"r{rng.randrange(200,900)}"
        x=rng.choice((0,1,2))
        y=rng.choice((0,1,2))
        m.update(revision=revision,depart=(x,y),objectif=(x+2,y))
        for event in j:
            event["revision"]=revision
            event["position"]=(event["position"][0]+x,event["position"][1]-1+y)
        r["p1"].update(revision=revision,origine=(x,y),destination=(x+1,y))
        r["p2"].update(revision=revision,origine=(x+1,y),destination=(x+2,y))
        if k==1:r["p2"]["reussi"]=False
        if k==2:m["accord_requis"]=True
        cases.append({"nom":f"Contrôle variable {k+1}","mission":m,"journal":j,"registre":r})
    return tuple(cases)

def oracle(mission,journal,registre):
    """Vérifie des transitions reconstituées, sans croire les déclarations seules."""
    try:
        if (type(mission) is not dict or set(mission)!=MISSION_KEYS
            or type(journal) is not list or len(journal)<4
            or type(registre) is not dict):
            return "ANOMALIE"
        revision=mission["revision"]
        depart,objectif=mission["depart"],mission["objectif"]
        droits=mission["outils_autorises"]
        if (type(revision) is not str or not revision or
            not valide(depart) or not valide(objectif) or
            type(droits) is not set or
            any(type(x) is not str for x in droits) or
            type(mission["accord_requis"]) is not bool or
            type(mission["decision_humaine"]) not in (type(None),bool) or
            not {"observer","avancer"}.issubset(droits)):
            return "ANOMALIE"
        position=depart
        seen_proofs=set()
        precedent=None
        moved=0
        for index,event in enumerate(journal):
            if type(event) is not dict or set(event)!=EVENEMENT_KEYS:
                return "ANOMALIE"
            t=event["type"]
            p=event["position"]
            proof_id=event["preuve"]
            if (type(event["sequence"]) is not int or event["sequence"]!=index
                or type(t) is not str or
                type(event["revision"]) is not str or event["revision"]!=revision
                or not valide(p)):
                return "ANOMALIE"
            if index==0:
                if t!="DEBUT" or p!=depart or proof_id is not None:
                    return "ANOMALIE"
            elif index==len(journal)-1:
                if t!="FIN" or p!=objectif or p!=position or proof_id is not None or moved==0:
                    return "ANOMALIE"
            elif t=="OBSERVATION":
                if p!=position or proof_id is not None or precedent not in ("DEBUT","DEPLACEMENT"):
                    return "ANOMALIE"
            elif t=="DEPLACEMENT":
                if (precedent!="OBSERVATION" or distance(position,p)!=1 or
                    type(proof_id) is not str or not proof_id or
                    proof_id in seen_proofs):
                    return "ANOMALIE"
                proof=registre.get(proof_id)
                if (type(proof) is not dict or set(proof)!=PREUVE_KEYS or
                    type(proof["revision"]) is not str or proof["revision"]!=revision or
                    type(proof["outil"]) is not str or proof["outil"]!="avancer" or
                    type(proof["reussi"]) is not bool or proof["reussi"] is not True or
                    not valide(proof["origine"]) or not valide(proof["destination"]) or
                    proof["origine"]!=position or proof["destination"]!=p):
                    return "ANOMALIE"
                seen_proofs.add(proof_id)
                position=p
                moved+=1
            else:
                return "ANOMALIE"
            precedent=t
        if mission["accord_requis"]:
            if mission["decision_humaine"] is None:return "ATTENTE_HUMAINE"
            if mission["decision_humaine"] is False:return "ANOMALIE"
        return "CONFORME"
    except (KeyError,TypeError,ValueError):
        return "ANOMALIE"

SAFE=("__build_class__","abs","all","any","bool","dict","enumerate","int",
      "isinstance","len","list","max","min","object","range","set",
      "sorted","str","sum","tuple","type","zip","Exception","ValueError",
      "TypeError","KeyError","NotImplementedError")

def verified_source(code):
    if type(code) is not str or not code.strip() or len(code)>18000:
        raise ValueError("Code absent ou trop long (18 000 caractères).")
    tree=ast.parse(code,filename="t07_eleve.py")
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            raise ValueError("Aucun import nécessaire.")
        if isinstance(node,ast.Attribute) and node.attr.startswith("_"):
            raise ValueError("Accès interne interdit.")
        if isinstance(node,ast.Name) and node.id in (
            "exec","eval","compile","open","__import__","__builtins__",
            "globals","locals","getattr","setattr","vars"):
            raise ValueError("Instruction non autorisée.")
    return tree

def evaluate_source(code,seed=0):
    try:
        if type(seed) is not int or not (0<=seed<2**32):
            raise ValueError("Graine invalide.")
        ns={"__builtins__":{x:getattr(builtins,x) for x in SAFE},
            "__name__":"t07_student"}
        exec(compile(verified_source(code),"t07_eleve.py","exec"),ns)
        fn=ns.get("auditer_journal")
        if not callable(fn):
            raise ValueError("Définis auditer_journal(mission, journal, registre).")
    except BaseException as err:
        return {"success":False,"passed":0,"total":19,"results":[],
                "error":type(err).__name__+" : "+str(err)[:220]}
    results=[]
    for item in cas(seed):
        m,j,r=(copy.deepcopy(item[k]) for k in ("mission","journal","registre"))
        before=copy.deepcopy((m,j,r))
        expected=oracle(m,j,r)
        try:
            response=fn(m,j,r)
            if (type(response) is not dict or set(response)!={"etat","motif"}
                or type(response["etat"]) is not str or response["etat"] not in STATUTS
                or type(response["motif"]) is not str or not response["motif"].strip()):
                raise AssertionError("Renvoyer exactement etat et motif (chaîne non vide).")
            if (m,j,r)!=before:
                raise AssertionError("L'audit ne doit modifier ni le journal ni les preuves.")
            if response["etat"]!=expected:
                raise AssertionError("État incorrect : attendu "+expected+".")
            results.append({"name":item["nom"],"ok":True,
                "message":{"ANOMALIE":"Anomalie correctement détectée ; aucun rejeu autorisé.",
                           "ATTENTE_HUMAINE":"Journal conforme, validation humaine encore nécessaire.",
                           "CONFORME":"Trace reconstituée et preuves externes vérifiées."}[expected],
                "trace":{"etat":response["etat"],"motif":response["motif"],
                         "revision":m["revision"],"depart":list(m["depart"]),
                         "objectif":list(m["objectif"]),
                         "evenements":len(j),"preuves_du_registre":sorted(r.keys()),
                         "decision_humaine_simulee":m["decision_humaine"]}})
        except BaseException as err:
            results.append({"name":item["nom"],"ok":False,
                "message":type(err).__name__+" : "+str(err)[:200],"trace":None})
    passed=sum(row["ok"] for row in results)
    return {"success":passed==len(results),"passed":passed,"total":len(results),
            "results":results,"limits":"Audit pédagogique, pas authentification cryptographique du journal."}

def evaluate_source_json(code,seed=0):
    return json.dumps(evaluate_source(code,seed),ensure_ascii=False)
