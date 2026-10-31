/* Contrôle indépendant de la logique de T05, sans DOM ni Python élève. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {makeScenario,verify,states}=require('../terminale/t05/lab.js');
assert.deepEqual(states,['SPÉCIFIÉE','EN VÉRIFICATION','BLOQUÉE','ATTENTE_HUMAINE','VALIDÉE']);
const EXPECTED=['VALIDÉE','BLOQUÉE','BLOQUÉE','BLOQUÉE','BLOQUÉE','ATTENTE_HUMAINE','BLOQUÉE'];
for(let index=0;index<EXPECTED.length;index++){
 const data=makeScenario(index);
 const before=JSON.stringify(data);
 const verdict=verify(data.mission,data.rapport,data.registre);
 assert.equal(verdict.etat,EXPECTED[index],String(index));
 assert.equal(JSON.stringify(data),before,'La vérification ne doit pas modifier les données.');
}
let scenario=makeScenario(5);
scenario.mission.decision_humaine=true;
assert.equal(verify(scenario.mission,scenario.rapport,scenario.registre).etat,'VALIDÉE');
scenario.mission.decision_humaine=false;
assert.equal(verify(scenario.mission,scenario.rapport,scenario.registre).etat,'BLOQUÉE');
scenario=makeScenario(0);
scenario.rapport.preuves.push('p1');
assert.equal(verify(scenario.mission,scenario.rapport,scenario.registre).etat,'BLOQUÉE');
scenario=makeScenario(0);
scenario.registre.p1.revision='r999';
assert.equal(verify(scenario.mission,scenario.rapport,scenario.registre).etat,'BLOQUÉE');
const source=fs.readFileSync(path.join(__dirname,'../terminale/t05/lab.js'),'utf8');
assert.ok(source.includes("'microduck-east-0.webp'"));
assert.ok(source.includes("'microduck-east-1.webp'"));
assert.ok(source.includes("'microduck-east-2.webp'"));
assert.ok(!source.includes("'microduck-walk-'+"));
assert.ok(source.includes("sprite.className='board-microduck'"));
console.log('T05 : 7 dossiers, rapport mensonger, preuve indépendante et transitions contrôlées : OK');
