/* T06 : test algorithmique JS sans DOM, invariants de reprise contrôlée. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {makeScenario,verifyRecovery,states}=require('../terminale/t06/lab.js');
assert.equal(states[0],'INCIDENT_DÉTECTÉ');
assert.ok(states.includes('EN_REVÉRIFICATION'));
assert.ok(states.includes('REPRISE_EXÉCUTÉE'));
const expected=['REPRISE_AUTORISÉE','BLOQUÉE','BLOQUÉE','BLOQUÉE',
 'BLOQUÉE','BLOQUÉE','ATTENTE_HUMAINE','BLOQUÉE','BLOQUÉE'];
for(let i=0;i<expected.length;i++){
 const data=makeScenario(i),original=JSON.stringify(data);
 const ans=verifyRecovery(data.mission,data.incident,data.correctif,data.registre);
 assert.equal(ans.etat,expected[i],String(i));
 assert.equal(JSON.stringify(data),original,'Aucun contrôle ne modifie les données.');
}
let s=makeScenario(6);
s.mission.decision_humaine=true;
assert.equal(verifyRecovery(s.mission,s.incident,s.correctif,s.registre).etat,'REPRISE_AUTORISÉE');
s.mission.decision_humaine=false;
assert.equal(verifyRecovery(s.mission,s.incident,s.correctif,s.registre).etat,'BLOQUÉE');
s=makeScenario(0);s.correctif.preuves.push('p1');
assert.equal(verifyRecovery(s.mission,s.incident,s.correctif,s.registre).etat,'BLOQUÉE');
s=makeScenario(0);s.incident.position_sure=[true,1];
assert.equal(verifyRecovery(s.mission,s.incident,s.correctif,s.registre).etat,'BLOQUÉE');
const script=fs.readFileSync(path.join(__dirname,'../terminale/t06/lab.js'),'utf8');
for(const frame of ['0','1','2'])assert.ok(script.includes("'microduck-east-"+frame+".webp'"));
assert.ok(!script.includes("'microduck-walk-'+"));
assert.ok(script.includes("if(state!=='REPRISE_AUTORISÉE'||pos[0]!==0"));
assert.ok(script.includes("sprite.className='board-microduck'"));
console.log('T06 : neuf scénarios, preuves fraîches, approbation et reprise distincte : OK');
