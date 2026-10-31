/* T04 — décisions de politique et effets du monde, indépendants du navigateur. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {verify,applyWorld,CASES}=require('../terminale/t04/lab.js');
assert.equal(CASES.length,7);
for(const item of CASES) {
 const verdict=verify(item.call,item.rights);
 assert.ok(['AUTORISÉ','ATTENTE_HUMAINE','REFUSÉ'].includes(verdict.statut));
 assert.ok(verdict.motif.trim().length>0);
}
assert.equal(verify(CASES[0].call,CASES[0].rights).statut,'AUTORISÉ');
assert.equal(verify(CASES[1].call,CASES[1].rights).statut,'AUTORISÉ');
assert.equal(verify(CASES[2].call,CASES[2].rights).statut,'REFUSÉ');
assert.equal(verify(CASES[3].call,CASES[3].rights).statut,'ATTENTE_HUMAINE');
assert.equal(verify(CASES[4].call,CASES[4].rights).statut,'REFUSÉ');
assert.equal(verify(CASES[5].call,CASES[5].rights).statut,'REFUSÉ');
assert.equal(verify(CASES[6].call,CASES[6].rights).statut,'AUTORISÉ');
assert.equal(verify({outil:'ouvrir_porte',arguments:{position:[true,1]}},['ouvrir_porte']).statut,'REFUSÉ');
assert.equal(verify({outil:'avancer',arguments:{direction:'NORD'}},['avancer']).statut,'REFUSÉ');
assert.equal(verify({outil:'observer',arguments:{secret:'oui'}},['observer']).statut,'REFUSÉ');
const moved=applyWorld([0,1],[],CASES[1].call);
assert.deepEqual(moved.position,[1,1]);
assert.equal(Math.abs(moved.position[0]-0)+Math.abs(moved.position[1]-1),1);
const blocked=applyWorld([0,1],[[1,1]],CASES[6].call);
assert.deepEqual(blocked.position,[0,1]);
const open=applyWorld([0,1],[[2,1]],CASES[3].call);
assert.deepEqual(open.walls,[]);
assert.deepEqual(open.position,[0,1]);
const source=fs.readFileSync(path.join(__dirname,'../terminale/t04/lab.js'),'utf8');
assert.ok(!source.includes("'microduck-walk-'+"));
assert.ok(source.includes("'microduck-'+previousFace+'-0.webp'"));
assert.ok(source.includes("'microduck-'+previousFace+'-1.webp'"));
assert.ok(source.includes("'microduck-'+previousFace+'-2.webp'"));
console.log('T04 : 7 scénarios, contrat strict, accord humain et déplacement unitaire : OK');
