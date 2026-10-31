/* T07 : invariants de l'audit indépendant, aucune action sans verdict. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {scenario,audit,STATES}=require('../terminale/t07/lab.js');
assert.deepEqual(STATES,['JOURNAL_REÇU','AUDIT_EN_COURS','ANOMALIE',
 'ATTENTE_HUMAINE','CONFORME','REJEU_TERMINÉ']);
const expectations=['CONFORME','ANOMALIE','ANOMALIE','ANOMALIE',
 'ANOMALIE','ANOMALIE','ATTENTE_HUMAINE','ANOMALIE','ANOMALIE'];
for(let i=0;i<expectations.length;i++){
 const obj=scenario(i),snapshot=JSON.stringify(obj);
 assert.equal(audit(obj.mission,obj.journal,obj.registre).etat,expectations[i],i);
 assert.equal(JSON.stringify(obj),snapshot,'L’audit ne doit pas modifier les entrées');
}
let obj=scenario(6);
obj.mission.decision_humaine=true;
assert.equal(audit(obj.mission,obj.journal,obj.registre).etat,'CONFORME');
obj.mission.decision_humaine=false;
assert.equal(audit(obj.mission,obj.journal,obj.registre).etat,'ANOMALIE');
obj=scenario(0);
obj.journal[4].preuve='p1';
assert.equal(audit(obj.mission,obj.journal,obj.registre).etat,'ANOMALIE');
obj=scenario(0);
obj.registre.p1.destination=[5,1];
assert.equal(audit(obj.mission,obj.journal,obj.registre).etat,'ANOMALIE');
const s=fs.readFileSync(path.join(__dirname,'../terminale/t07/lab.js'),'utf8');
assert.ok(s.includes("if(state!=='CONFORME'||step>=data.journal.length)return"));
assert.ok(s.includes("if(item.type==='DEPLACEMENT')pos=item.position.slice()"));
for(const frame of ['0','1','2'])assert.ok(s.includes("'microduck-east-"+frame+".webp'"));
assert.ok(!s.includes("'microduck-walk-'+"));
assert.ok(s.includes("sprite.className='board-microduck'"));
console.log('T07 : journal trompeur, preuves et rejeu étape par étape : OK');
